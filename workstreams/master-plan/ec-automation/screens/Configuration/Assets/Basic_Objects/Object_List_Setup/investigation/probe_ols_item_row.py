"""READ-ONLY: Object List Setup - after FIN_ACCOUNT / 'OPEX GL Equipment Rental'
+ GO, count existing item rows, insert a blank 'Object List Item' row (abandoned,
never saved), find it, open its C2 object dropdown and dump the candidate labels.
Also dump DV_OBJECT_LIST_SETUP / RV_OBJECT_LIST_SETUP columns for the DB oracle."""
import os
import json
from pathlib import Path

import oracledb
from playwright.sync_api import sync_playwright

EC_URL = "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"
_scan = json.loads(Path(r"c:/Projects/ChoongYin_OS/tmp/screen_scan/assets_scan.json").read_text(encoding="utf-8"))
URL = next(r["url"] for r in _scan.values()
           if r.get("section") == "Basic Objects" and r["screen"] == "Object List Setup")
GRID = "tab:tabPanel:object_list_table:form:T_data"

print("--- DB columns ---")
conn = oracledb.connect(user="ECKERNEL_EC", password="energy", dsn="localhost:1521/ORCL")
cur = conn.cursor()
for v in ["DV_OBJECT_LIST_SETUP", "RV_OBJECT_LIST_SETUP", "OBJECT_LIST_SETUP"]:
    try:
        cur.execute("SELECT column_name, data_type FROM all_tab_columns WHERE table_name=:v ORDER BY column_id", v=v)
        cols = [f"{r[0]}({r[1][:7]})" for r in cur.fetchall()]
        print(f"  {v}: {cols[:14]}")
    except Exception as e:
        print(f"  {v}: ERR {str(e)[:60]}")
try:
    cur.execute("SELECT COUNT(*) FROM DV_OBJECT_LIST_SETUP WHERE OBJECT_LIST_CODE = 'LST_GL_EQ_RENT'")
    print("  items in LST_GL_EQ_RENT (DV):", cur.fetchone()[0])
except Exception as e:
    print("  DV count probe:", str(e)[:80])
cur.close()
conn.close()

ROWS_JS = r"""(grid) => {
    const t = document.getElementById(grid);
    if (!t) return null;
    const out = [];
    t.querySelectorAll(':scope > tr').forEach((tr, i) => {
        const dd = tr.querySelector("input[id$='C2_dd_input']");
        const c0 = tr.querySelector("input[id$='C0_in']");
        out.push({row: i, c0: c0 ? c0.value : null, ddVal: dd ? dd.value : null,
                  ddId: dd ? dd.id.replace(/_input$/, '') : null});
    });
    return out;
}"""

with sync_playwright() as p:
    b = p.chromium.launch(headless=True, args=["--ignore-certificate-errors"])
    ctx = b.new_context(ignore_https_errors=True, viewport={"width": 1680, "height": 1200})
    page = ctx.new_page()
    page.goto(EC_URL, wait_until="domcontentloaded", timeout=45000)
    page.fill("#username", os.environ.get("EC_USER", "sysadmin"))
    page.fill("#password", os.environ.get("EC_PASS", "sysadmin"))
    page.click("#kc-login")
    page.wait_for_url("**/dashboard**", timeout=60000)
    page.wait_for_timeout(1500)
    page.goto(URL, wait_until="domcontentloaded", timeout=45000)
    page.wait_for_timeout(2000)

    for dd, val in [("nav:form:G:1:R:1:C:0:dd", "FIN_ACCOUNT"),
                    ("nav:form:G:2:R:1:C:0:dd", "OPEX GL Equipment Rental")]:
        page.click(f"[id='{dd}_button']")
        page.wait_for_selector(f"[id='{dd}_panel'] tr[data-item-label]", state="visible", timeout=10000)
        page.click(f"[id='{dd}_panel'] tr[data-item-label='{val}']")
        page.wait_for_timeout(1500)
    page.click("[id='button:form:B']")
    try:
        page.wait_for_load_state("networkidle", timeout=15000)
    except Exception:
        pass
    page.wait_for_timeout(2000)
    rows = page.evaluate(ROWS_JS, GRID)
    print("existing rows:", rows)

    # insert blank row via the INSERT-scoped menu
    page.hover("xpath=//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'ui-icon-insert')]]")
    item = page.locator("xpath=//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'ui-icon-insert')]]//ul//a[normalize-space(.)='Object List Item']")
    item.wait_for(state="visible", timeout=8000)
    item.click()
    page.wait_for_timeout(2500)
    rows2 = page.evaluate(ROWS_JS, GRID)
    print("rows after insert:", rows2)
    blanks = [r for r in (rows2 or []) if not r["ddVal"]]
    print("blank rows:", blanks)
    if blanks:
        ddp = blanks[-1]["ddId"]
        page.click(f"[id='{ddp}_button']")
        page.wait_for_timeout(2500)
        labels = page.evaluate(
            "(pid) => Array.from(document.querySelectorAll('#' + CSS.escape(pid) + ' tr[data-item-label]')).map(r => r.getAttribute('data-item-label')).slice(0, 15)",
            f"{ddp}_panel")
        print("candidate objects:", labels)
    page.screenshot(path=r"c:/Projects/ChoongYin_OS/tmp/screen_scan/shots/probe_ols_item_row.png")
    ctx.close()
    b.close()
print("done (READ-ONLY, blank row abandoned)")
