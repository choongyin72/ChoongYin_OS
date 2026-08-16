"""READ-ONLY recon round 2 for Basic Objects: navigate by DIRECT URL (full page
load per screen - no dirty-form state leakage). Keeps complete records from
round 1; re-probes the rest. Adds groupmodel-navigator DOM capture.
Output: tmp/screen_scan/basic_objects_recon.json (merged)."""
import json
import re
from pathlib import Path

import oracledb
from playwright.sync_api import sync_playwright

EC_URL = "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"
SCAN = Path(r"c:/Projects/ChoongYin_OS/tmp/screen_scan/assets_scan.json")
OUT = Path(r"c:/Projects/ChoongYin_OS/tmp/screen_scan/basic_objects_recon.json")
SCREENS = [
    "Production Unit", "Business Unit", "Production Sub Unit", "Country",
    "State", "County", "Area", "Sub Area", "Region", "Object List",
    "Object List Setup", "Functional Area", "Regulatory Permits",
]

scan = json.loads(SCAN.read_text(encoding="utf-8"))
URLMAP = {r["screen"]: r["url"] for r in scan.values()
          if r.get("section") == "Basic Objects" and r.get("url")}

FORM_JS = r"""(formName) => {
    const out = [];
    document.querySelectorAll("[id^='tab:tabPanel:" + formName + ":form:G:']").forEach(el => {
        const id = el.id;
        if (!/(:in|:da_input|:dd_input|:dd_button|:cb)$/.test(id)) return;
        const kind = id.endsWith(':da_input') ? 'date'
                   : id.endsWith(':dd_input') || id.endsWith(':dd_button') ? 'dropdown'
                   : id.endsWith(':cb') ? 'checkbox' : 'text';
        const m = id.match(/G:(\d+):R:(\d+):C:(\d+)/);
        let label = '';
        if (m) {
            const lab = document.getElementById(`tab:tabPanel:${formName}:form:G:${m[1]}:R:${m[2]}:C:0`);
            if (lab) label = (lab.textContent || '').trim();
        }
        const style = window.getComputedStyle(el);
        const mandatory = /rgb\(255,\s*255,\s*(?:153|204)\)/i.test(style.backgroundColor);
        out.push({id, kind, label, mandatory, visible: el.offsetParent !== null});
    });
    return out;
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

NAV_JS = r"""() => {
    // dump the navigator region structure (dropdown buttons, trees, GO button)
    const out = {ddButtons: [], trees: [], goButtons: []};
    document.querySelectorAll("[id$=':dd_button']").forEach(e => {
        if (e.offsetParent !== null) out.ddButtons.push(e.id);
    });
    document.querySelectorAll('.ui-tree').forEach(e => out.trees.push(e.id || '(no id)'));
    document.querySelectorAll("button[id$=':form:B'], a[id$=':form:B']").forEach(e => {
        if (e.offsetParent !== null) out.goButtons.push(e.id);
    });
    return out;
}"""


def complete(rec):
    return bool(rec.get("gridId")) and rec.get("insertFields") and rec.get("updateFields")


def login(page):
    page.goto(EC_URL, wait_until="domcontentloaded", timeout=45000)
    page.fill("#username", "sysadmin")
    page.fill("#password", "sysadmin")
    page.click("#kc-login")
    page.wait_for_url("**/dashboard**", timeout=60000)
    page.wait_for_timeout(1500)


def recon_screen(page, label, url):
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
    rec["navStructure"] = page.evaluate(NAV_JS)

    if rec["firstCodes"]:
        try:
            page.click(f"tbody[id='{rec['gridId']}'] tr >> nth=0")
            page.wait_for_timeout(1800)
            rec["updateFields"] = page.evaluate(FORM_JS, "updateAttributes")
            rec["dateFields"] = page.evaluate(FORM_JS, "objectdates")
        except Exception as e:
            rec["updateFields"], rec["dateFields"] = [], []
            rec["rowSelectError"] = str(e)[:120]
    else:
        rec["updateFields"], rec["dateFields"] = [], []

    try:
        page.hover("xpath=//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'ui-icon-insert')]]")
        item = page.locator("xpath=//ul[contains(@class,'ui-menu-child')]//li//a[normalize-space(.)='New Object']")
        item.wait_for(state="visible", timeout=8000)
        item.click()
        page.wait_for_timeout(2000)
        rec["insertFields"] = page.evaluate(FORM_JS, "objectForm")
    except Exception as e:
        rec["insertFields"] = []
        rec["insertFormError"] = str(e)[:120]
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
                        "AND data_type LIKE '%CHAR%' AND column_id<=5 ORDER BY column_id", v=view)
            for (col,) in cur.fetchall():
                cur.execute(f'SELECT COUNT(*) FROM {view} WHERE "{col}" = :c', c=code)
                if cur.fetchone()[0]:
                    return True
        except Exception:
            pass
        return False

    for rec in records:
        ns = norm(rec["screen"])
        # rank: exact name match first, then contains, shortest first
        cands = sorted([v for v in views if ns in norm(v)],
                       key=lambda v: (norm(v) != "OV" + ns, len(v)))
        # also derive from CLASS_NAME in url
        m = re.search(r"CLASS_NAME/([A-Z_]+)", rec.get("url", ""))
        if m:
            cn = norm(m.group(1))
            cands = sorted(set(cands) | {v for v in views if norm(v) == "OV" + cn},
                           key=lambda v: (norm(v) not in ("OV" + ns, "OV" + cn), len(v)))
        rec["dbView"], rec["dbViewVerified"] = None, False
        code = (rec.get("firstCodes") or [None])[0]
        for v in cands:
            if code and verify(v, code):
                rec["dbView"], rec["dbViewVerified"] = v, True
                break
        if not rec["dbView"] and cands:
            rec["dbView"] = cands[0]
        rec["dbViewCandidates"] = cands[:6]
    cur.close()
    conn.close()


def main():
    old = {r["screen"]: r for r in json.loads(OUT.read_text(encoding="utf-8"))} if OUT.exists() else {}
    records = []
    todo = [s for s in SCREENS if not complete(old.get(s, {}))]
    print(f"keeping {len(SCREENS) - len(todo)} complete, re-probing {len(todo)}: {todo}")
    with sync_playwright() as p:
        b = p.chromium.launch(headless=True, args=["--ignore-certificate-errors"])
        ctx = b.new_context(ignore_https_errors=True, viewport={"width": 1680, "height": 1200})
        page = ctx.new_page()
        page.on("dialog", lambda d: d.accept())
        login(page)
        for label in SCREENS:
            if label not in todo:
                records.append(old[label])
                continue
            url = URLMAP.get(label)
            try:
                rec = recon_screen(page, label, url)
            except Exception as e:
                rec = {"screen": label, "url": url, "error": str(e)[:200]}
            records.append(rec)
            print(f"recon {label}: grid={rec.get('gridId')} codes={len(rec.get('firstCodes') or [])} "
                  f"ins={len(rec.get('insertFields') or [])} upd={len(rec.get('updateFields') or [])} "
                  f"nav={rec.get('navStructure', {}).get('ddButtons')}")
        ctx.close()
        b.close()
    discover_views(records)
    OUT.write_text(json.dumps(records, indent=1), encoding="utf-8")
    print(f"-> {OUT}")
    for r in records:
        print(f"  {r['screen']:22s} grid={str(r.get('gridId'))[:38]:38s} view={r.get('dbView')} verified={r.get('dbViewVerified')}")


if __name__ == "__main__":
    main()
