"""Commercial Objects round-1 diagnosis:
A) banner probes for Customer / Vendor / Company Contact / Sub Field (replicate
   suite fill incl. extras, Save, capture banner + DB presence; cleanup if saved)
B) Commercial Entity: select first row, dump updateAttributes field ids/values
C) leftover sweep (Commercial Entity TC04 failed after a successful insert)"""
import os
import json
import time
from pathlib import Path

import oracledb
from playwright.sync_api import sync_playwright

EC_URL = "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"
RECON = Path(r"c:/Projects/ChoongYin_OS/tmp/screen_scan/commercial_objects_recon.json")
records = {r["screen"]: r for r in json.loads(RECON.read_text(encoding="utf-8"))}
EXTRA_VALUES = {"ERP Customer Code": "ERP999", "ERP Vendor Code": "ERP999",
                "Official Name": "AUTOTEST Official"}
END_ID = "tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input"


def _css(fid):
    return "#" + fid.replace(":", "\\:")


def pick_rows(plan):
    vis = [f for f in plan if f.get("visible")]
    texts = [f for f in vis if f.get("kind") == "text"]
    code = next(f for f in texts if f.get("mandatory") and "code" in (f.get("label") or "").lower())
    name = next(f for f in texts if f.get("mandatory") and (f.get("label") or "").strip().lower()
                in ("name", code["label"].lower().replace("code", "name").strip()))
    date = next(f for f in vis if f.get("kind") == "date")
    extras = [f for f in vis if f.get("mandatory") and f["r"] not in (code["r"], name["r"])
              and f.get("kind") in ("text", "checkbox")]
    return code, name, date, extras


MSG_JS = r"""() => {
    const out = [];
    document.querySelectorAll('#ECNotificationArea, #ECClientNotificationArea, .ui-messages, .ui-growl-message').forEach(e => {
        const t = (e.textContent || '').trim();
        if (t) out.push(t.replace(/EC.jsMessage.clear\(\);?/g, '').trim().substring(0, 300));
    });
    return out.filter(Boolean).slice(0, 4);
}"""

conn = oracledb.connect(user="ECKERNEL_EC", password="energy", dsn="localhost:1521/ORCL")
cur = conn.cursor()


def db_has(view, code):
    cur.execute("SELECT column_name FROM all_tab_columns WHERE table_name=:v "
                "AND data_type LIKE '%CHAR%' AND column_id<=6 ORDER BY column_id", v=view)
    for (col,) in cur.fetchall():
        cur.execute(f"SELECT COUNT(*) FROM {view} WHERE {col} = :c", c=code)
        if cur.fetchone()[0]:
            return True
    return False


print("=== C) leftover sweep ===")
for label, r in records.items():
    v = r.get("dbView")
    if not v:
        continue
    try:
        cur.execute("SELECT column_name FROM all_tab_columns WHERE table_name=:v "
                    "AND data_type LIKE '%CHAR%' AND column_id<=6 ORDER BY column_id", v=v)
        cols = [c[0] for c in cur.fetchall()]
        for col in cols:
            cur.execute(f"SELECT {col} FROM {v} WHERE {col} LIKE 'AUTOTEST%'")
            found = [x[0] for x in cur.fetchall()]
            if found:
                print(f"  {label} ({v}): {found}")
            break
    except Exception:
        pass

with sync_playwright() as p:
    b = p.chromium.launch(headless=True, args=["--ignore-certificate-errors"])
    ctx = b.new_context(ignore_https_errors=True, viewport={"width": 1680, "height": 1200})
    page = ctx.new_page()
    page.on("dialog", lambda d: d.accept())
    page.goto(EC_URL, wait_until="domcontentloaded", timeout=45000)
    page.fill("#username", os.environ.get("EC_USER", "sysadmin"))
    page.fill("#password", os.environ.get("EC_PASS", "sysadmin"))
    page.click("#kc-login")
    page.wait_for_url("**/dashboard**", timeout=60000)
    page.wait_for_timeout(1500)

    print("\n=== A) banner probes ===")
    for label in ["Customer", "Vendor", "Company Contact", "Sub Field"]:
        rec = records[label]
        try:
            page.goto(rec["url"], wait_until="domcontentloaded", timeout=45000)
            try:
                page.wait_for_load_state("networkidle", timeout=20000)
            except Exception:
                pass
            page.wait_for_timeout(1500)
            page.hover("xpath=//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'ui-icon-insert')]]")
            item = page.locator("xpath=//li[contains(@class,'ui-menu-parent')]"
                                "[.//span[contains(@class,'ui-icon-insert')]]//ul//a[normalize-space(.)='New Object']")
            item.wait_for(state="visible", timeout=8000)
            item.click()
            page.wait_for_timeout(2000)
            code_f, name_f, date_f, extras = pick_rows(rec["insertPlan"])
            code = f"AUTOTEST_CP_{time.strftime('%H%M%S')}"
            for fid, val in [(code_f["id"], code), (name_f["id"], "Probe " + code)]:
                page.fill(f"[id='{fid}']", val)
                page.evaluate("(id)=>{const e=document.getElementById(id); if(e){e.dispatchEvent(new Event('change',{bubbles:true}));e.dispatchEvent(new Event('blur',{bubbles:true}));}}", fid)
                page.wait_for_timeout(300)
            page.fill(f"[id='{date_f['id']}']", "2003-01-01")
            page.keyboard.press("Tab")
            page.wait_for_timeout(700)
            for f in extras:
                if f["kind"] == "checkbox":
                    page.check(f"[id='{f['id']}']")
                else:
                    page.fill(f"[id='{f['id']}']", EXTRA_VALUES.get(f.get("label"), "AUTOTEST"))
                    page.evaluate("(id)=>{const e=document.getElementById(id); if(e){e.dispatchEvent(new Event('change',{bubbles:true}));}}", f["id"])
                page.wait_for_timeout(300)
            page.click("xpath=//a[@title='Save [Ctrl+s]' and not(contains(@class,'ui-state-disabled'))]")
            try:
                page.wait_for_load_state("networkidle", timeout=15000)
            except Exception:
                pass
            page.wait_for_timeout(1800)
            present = db_has(rec["dbView"], code)
            print(f"  {label:18s} banner={page.evaluate(MSG_JS)} db={present}")
            if present:
                # cleanup
                go = page.locator(_css("button:form:B"))
                if go.count() and go.first.is_visible():
                    go.first.click()
                else:
                    page.click("xpath=//a[@title='Refresh [Ctrl+r]']")
                page.wait_for_timeout(2000)
                row = page.locator(f"xpath=//tbody[@id='{rec['gridId'] or 'manageObject:form:T_data'}']//span[normalize-space(text())='{code}']")
                if row.count():
                    row.first.click()
                    page.wait_for_timeout(1800)
                    el = page.locator(_css(END_ID))
                    el.click()
                    el.fill("2003-01-01")
                    page.keyboard.press("Tab")
                    page.wait_for_timeout(600)
                    page.evaluate("(id)=>{const e=document.getElementById(id); if(e){e.dispatchEvent(new Event('change',{bubbles:true}));e.dispatchEvent(new Event('blur',{bubbles:true}));}}", END_ID)
                    page.wait_for_timeout(800)
                    sv = page.locator("xpath=//a[@title='Save [Ctrl+s]' and not(contains(@class,'ui-state-disabled'))]")
                    if sv.count():
                        sv.first.click()
                        page.wait_for_timeout(2000)
                    print(f"     cleanup: db_now={db_has(rec['dbView'], code)}")
                else:
                    print(f"     !! saved but NOT visible in grid (PSU symptom?) - leftover {code}")
        except Exception as e:
            print(f"  {label:18s} PROBE ERR {str(e)[:120]}")

    print("\n=== B) Commercial Entity update form ===")
    rec = records["Commercial Entity"]
    page.goto(rec["url"], wait_until="domcontentloaded", timeout=45000)
    page.wait_for_timeout(2500)
    page.click(f"tbody[id='{rec['gridId']}'] tr >> nth=0")
    page.wait_for_timeout(2000)
    fields = page.evaluate("""() => {
        const out = [];
        document.querySelectorAll("[id*='updateAttributes'] input, [id*='update'] input").forEach(e => {
            if (e.offsetParent !== null && out.length < 8) out.push({id: e.id, val: (e.value || '').substring(0, 24)});
        });
        return out;
    }""")
    print("  visible update inputs:", json.dumps(fields, indent=1)[:800])
    ctx.close()
    b.close()
cur.close()
conn.close()
print("probe done")
