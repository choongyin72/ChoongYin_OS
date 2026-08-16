"""Round-2 reject probe for the 5 stubborn Financial Objects screens: replicate
the suite fill EXACTLY (code/name/date + extras + first-option dropdowns),
Save, then capture banner + grid presence + DB presence. Cleans up after itself
if the save succeeded."""
import json
import time
from pathlib import Path

import oracledb
from playwright.sync_api import sync_playwright

EC_URL = "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"
RECON = Path(r"c:/Projects/ChoongYin_OS/tmp/screen_scan/financial_objects_recon.json")
records = {r["screen"]: r for r in json.loads(RECON.read_text(encoding="utf-8"))}

SUSPECTS = ["Account", "Account Mapping", "Bank Account", "Cost Object Mapping", "DOA Credit Limit"]
EXTRA_VALUES = {"GL Account": "999999", "Sort Code": "000000", "Credit Limit": "1000"}
REQUIRED_DDS = {
    "Bank Account": ["Bank", "Currency"],
    "Cost Object Mapping": ["Object Type", "Cost Object", "Company", "Distribution Object Type"],
    "DOA Credit Limit": ["DOA Type", "Role Name"],
}
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

    for label in SUSPECTS:
        rec = records[label]
        print(f"===== {label} =====")
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
            code = f"AUTOTEST_P2_{time.strftime('%H%M%S')}"
            for fid, val in [(code_f["id"], code), (name_f["id"], "Probe " + code)]:
                page.fill(f"[id='{fid}']", val)
                page.evaluate("(id)=>{const e=document.getElementById(id); if(e){e.dispatchEvent(new Event('change',{bubbles:true}));e.dispatchEvent(new Event('blur',{bubbles:true}));}}", fid)
                page.wait_for_timeout(300)
            page.fill(f"[id='{date_f['id']}']", "2000-01-01")
            page.keyboard.press("Tab")
            page.wait_for_timeout(700)
            for f in extras:
                if f["kind"] == "checkbox":
                    page.check(f"[id='{f['id']}']")
                else:
                    page.fill(f"[id='{f['id']}']", EXTRA_VALUES.get(f.get("label"), "AUTOTEST"))
                    page.evaluate("(id)=>{const e=document.getElementById(id); if(e){e.dispatchEvent(new Event('change',{bubbles:true}));}}", f["id"])
                page.wait_for_timeout(300)
            dds = {(f.get("label") or "").strip(): f for f in rec["insertPlan"]
                   if f.get("kind") == "dropdown" and f.get("visible")}
            for dlab in REQUIRED_DDS.get(label, []):
                f = dds.get(dlab)
                if not f:
                    print(f"  dd '{dlab}' NOT FOUND in plan")
                    continue
                dd = f["id"].rsplit("_", 1)[0] if f["id"].endswith("_button") else f["id"]
                page.click(f"[id='{dd}_button']")
                page.wait_for_timeout(2500)
                opts = page.evaluate(
                    "(pid)=>Array.from(document.querySelectorAll('#'+CSS.escape(pid)+' tr[data-item-label]')).map(r=>r.getAttribute('data-item-label')).slice(0,5)",
                    dd + "_panel")
                print(f"  dd '{dlab}': options={opts}")
                if opts:
                    page.click(f"[id='{dd}_panel'] tr[data-item-label]")
                    page.wait_for_timeout(1500)
                else:
                    page.keyboard.press("Escape")
            page.click("xpath=//a[@title='Save [Ctrl+s]' and not(contains(@class,'ui-state-disabled'))]")
            try:
                page.wait_for_load_state("networkidle", timeout=15000)
            except Exception:
                pass
            page.wait_for_timeout(1800)
            print("  banner:", page.evaluate(MSG_JS))
            present = db_has(rec["dbView"], code)
            print(f"  DB present: {present}")
            page.screenshot(path=rf"c:/Projects/ChoongYin_OS/tmp/screen_scan/shots/finp2_{label.replace(' ', '_')}.png")
            if present:
                # clean up: select row (refresh first), End=Start
                go = page.locator(_css("button:form:B"))
                if go.count() and go.first.is_visible():
                    go.first.click()
                else:
                    page.click("xpath=//a[@title='Refresh [Ctrl+r]']")
                page.wait_for_timeout(2000)
                row = page.locator(f"xpath=//tbody[@id='{rec['gridId']}']//span[normalize-space(text())='{code}']")
                print(f"  row visible in grid after refresh: {row.count() > 0}")
                if row.count():
                    row.first.click()
                    page.wait_for_timeout(1800)
                    el = page.locator(_css(END_ID))
                    el.click()
                    el.fill("2000-01-01")
                    page.keyboard.press("Tab")
                    page.wait_for_timeout(600)
                    page.evaluate("(id)=>{const e=document.getElementById(id); if(e){e.dispatchEvent(new Event('change',{bubbles:true}));e.dispatchEvent(new Event('blur',{bubbles:true}));}}", END_ID)
                    page.wait_for_timeout(800)
                    sv = page.locator("xpath=//a[@title='Save [Ctrl+s]' and not(contains(@class,'ui-state-disabled'))]")
                    if sv.count():
                        sv.first.click()
                        page.wait_for_timeout(2000)
                    print(f"  cleaned: db_now={db_has(rec['dbView'], code)}")
        except Exception as e:
            print(f"  PROBE ERR: {str(e)[:150]}")
    ctx.close()
    b.close()
cur.close()
conn.close()
print("probe2 done")
