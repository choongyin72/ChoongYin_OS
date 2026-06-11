"""READ-ONLY recon of the Financial Objects OV screens (Bank already done).
Direct-URL navigation (no dirty-form leakage), per screen: grid id + first
codes, insert-form field plan (labels via :C:0:la, mandatory markers, kinds),
update/date plans via first-row select where rows exist, and OV_* view
discovery verified against a real grid code.
Output: tmp/screen_scan/financial_objects_recon.json"""
import json
import re
from pathlib import Path

import oracledb
from playwright.sync_api import sync_playwright

EC_URL = "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"
SCAN = Path(r"c:/Projects/ChoongYin_OS/tmp/screen_scan/assets_scan.json")
OUT = Path(r"c:/Projects/ChoongYin_OS/tmp/screen_scan/financial_objects_recon.json")

SCREENS = ["Account", "Bank Account", "Cost Centre", "Cost Object Mapping",
           "Currency", "DOA Credit Limit", "Exchange Rate Source", "Payment Scheme",
           "Product Description", "Revenue Order", "Sales Order", "VAT Code", "WBS",
           "Account Mapping"]

scan = json.loads(SCAN.read_text(encoding="utf-8"))
URLMAP = {r["screen"]: r["url"] for r in scan.values()
          if r.get("section") == "Financial Objects" and r.get("url")}

PLAN_JS = r"""(formName) => {
    const rows = {};
    document.querySelectorAll("[id^='tab:tabPanel:" + formName + ":form:G:']").forEach(el => {
        const m = el.id.match(/G:(\d+):R:(\d+):C:(\d+):(la|in|da_input|dd_button|cb)$/);
        if (!m) return;
        const key = `${m[1]}:${m[2]}`;
        rows[key] = rows[key] || {g: +m[1], r: +m[2]};
        const row = rows[key];
        if (m[4] === 'la') row.label = (el.textContent || '').trim();
        else {
            const mand = ((el.className || '') + (el.title || '')).includes('mandatory:true');
            row.kind = m[4] === 'in' ? 'text' : m[4] === 'da_input' ? 'date'
                     : m[4] === 'dd_button' ? 'dropdown' : 'checkbox';
            row.mandatory = row.mandatory || mand;
            row.id = el.id;
            row.visible = el.offsetParent !== null;
        }
    });
    return Object.values(rows).sort((a, b) => a.g - b.g || a.r - b.r);
}"""

GRID_JS = r"""() => {
    const t = document.querySelector("tbody[id$=':form:T_data']");
    if (!t) return {gridId: null, firstCodes: []};
    const codes = [];
    t.querySelectorAll('tr').forEach(tr => {
        const td = tr.querySelector('td');
        if (td) { const v = (td.textContent || '').trim(); if (v && v !== 'No records found') codes.push(v); }
    });
    return {gridId: t.id, firstCodes: codes.slice(0, 3)};
}"""


def recon(page, label, url):
    rec = {"screen": label, "url": url}
    page.goto(url, wait_until="domcontentloaded", timeout=45000)
    try:
        page.wait_for_load_state("networkidle", timeout=20000)
    except Exception:
        pass
    try:
        page.wait_for_selector("tbody[id$=':form:T_data']", state="attached", timeout=10000)
    except Exception:
        pass
    page.wait_for_timeout(1200)
    rec.update(page.evaluate(GRID_JS))

    if rec["firstCodes"]:
        try:
            page.click(f"tbody[id='{rec['gridId']}'] tr >> nth=0")
            page.wait_for_timeout(1800)
            rec["updatePlan"] = page.evaluate(PLAN_JS, "updateAttributes")
            rec["datePlan"] = page.evaluate(PLAN_JS, "objectdates")
        except Exception as e:
            rec["rowSelectError"] = str(e)[:120]
    try:
        page.hover("xpath=//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'ui-icon-insert')]]")
        item = page.locator("xpath=//li[contains(@class,'ui-menu-parent')]"
                            "[.//span[contains(@class,'ui-icon-insert')]]//ul//a[normalize-space(.)='New Object']")
        item.wait_for(state="visible", timeout=8000)
        item.click()
        page.wait_for_timeout(2000)
        rec["insertPlan"] = page.evaluate(PLAN_JS, "objectForm")
    except Exception as e:
        rec["insertFormError"] = str(e)[:150]
    return rec


def discover_views(records):
    conn = oracledb.connect(user="ECKERNEL_EC", password="energy",
                            dsn="localhost:1521/ORCL", tcp_connect_timeout=15)
    cur = conn.cursor()
    cur.execute("SELECT view_name FROM all_views WHERE owner='ECKERNEL_EC' AND view_name LIKE 'OV%'")
    views = [r[0] for r in cur.fetchall()]
    norm = lambda s: re.sub(r"[^A-Z0-9]", "", s.upper())

    def verify(view, code):
        try:
            cur.execute("SELECT column_name FROM all_tab_columns WHERE table_name=:v "
                        "AND data_type LIKE '%CHAR%' AND column_id<=6 ORDER BY column_id", v=view)
            for (col,) in cur.fetchall():
                cur.execute(f'SELECT COUNT(*) FROM {view} WHERE "{col}" = :c', c=code)
                if cur.fetchone()[0]:
                    return True
        except Exception:
            pass
        return False

    for rec in records:
        ns = norm(rec["screen"])
        m = re.search(r"CLASS_NAME/([A-Z_0-9]+)", rec.get("url", ""))
        cn = norm(m.group(1)) if m else ""
        cands = sorted({v for v in views if ns in norm(v) or (cn and norm(v) == "OV" + cn)},
                       key=lambda v: (norm(v) not in ("OV" + ns, "OV" + cn), len(v)))
        rec["dbView"], rec["dbViewVerified"] = None, False
        code = (rec.get("firstCodes") or [None])[0]
        for v in cands:
            if code and verify(v, code):
                rec["dbView"], rec["dbViewVerified"] = v, True
                break
        if not rec["dbView"] and cands:
            rec["dbView"] = cands[0]
        rec["dbViewCandidates"] = cands[:5]
    cur.close()
    conn.close()


records = []
with sync_playwright() as p:
    b = p.chromium.launch(headless=True, args=["--ignore-certificate-errors"])
    ctx = b.new_context(ignore_https_errors=True, viewport={"width": 1680, "height": 1200})
    page = ctx.new_page()
    page.on("dialog", lambda d: d.accept())
    page.goto(EC_URL, wait_until="domcontentloaded", timeout=45000)
    page.fill("#username", "sysadmin")
    page.fill("#password", "sysadmin")
    page.click("#kc-login")
    page.wait_for_url("**/dashboard**", timeout=60000)
    page.wait_for_timeout(1500)
    for label in SCREENS:
        url = URLMAP.get(label)
        if not url:
            records.append({"screen": label, "error": "no url in scan"})
            continue
        try:
            rec = recon(page, label, url)
        except Exception as e:
            rec = {"screen": label, "url": url, "error": str(e)[:200]}
        records.append(rec)
        mand = [f.get("label") for f in rec.get("insertPlan", []) if f.get("mandatory") and f.get("visible")]
        print(f"{label:24s} grid={str(rec.get('gridId'))[:36]:36s} codes={len(rec.get('firstCodes') or [])} "
              f"ins={len(rec.get('insertPlan') or [])} mand={mand}")
    ctx.close()
    b.close()

discover_views(records)
OUT.write_text(json.dumps(records, indent=1), encoding="utf-8")
print(f"-> {OUT}")
for r in records:
    print(f"  {r['screen']:24s} view={r.get('dbView')} verified={r.get('dbViewVerified')}")
