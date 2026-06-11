"""READ-ONLY build probe for phase-B implementation facts:
A) Area: PU='Production Unit' + GO -> grid id + row codes.
B) Sub Area: PU='Production Unit' + Area='Offshore area' + GO -> grid id + rows.
C) OLS: FIN_ACCOUNT + 'OPEX GL Equipment Rental' + GO -> existing item values;
   then Insert > Object List Item (scoped to the INSERT menu) -> new-row inputs.
D) DB: tables/views named like OBJECT_LIST (verify target for OLS items).
Nothing is saved anywhere."""
import json
from pathlib import Path

import oracledb
from playwright.sync_api import sync_playwright

EC_URL = "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"
SCAN = Path(r"c:/Projects/ChoongYin_OS/tmp/screen_scan/assets_scan.json")
SHOTS = Path(r"c:/Projects/ChoongYin_OS/tmp/screen_scan/shots")
scan = json.loads(SCAN.read_text(encoding="utf-8"))
URL = {r["screen"]: r["url"] for r in scan.values()
       if r.get("section") == "Basic Objects" and r.get("url")}

GRID_JS = r"""() => {
    const out = [];
    document.querySelectorAll("tbody[id$=':form:T_data']").forEach(t => {
        if (t.id.includes('statusarea')) return;
        const rows = [];
        t.querySelectorAll('tr').forEach(tr => {
            const cells = [];
            tr.querySelectorAll('td').forEach(td => {
                let v = (td.textContent || '').trim();
                const inp = td.querySelector('input');
                if (!v && inp) v = '[in]' + (inp.value || '');
                cells.push(v);
            });
            if (cells.some(c => c)) rows.push(cells.slice(0, 6));
        });
        out.push({id: t.id, nRows: rows.length, rows: rows.slice(0, 10)});
    });
    return out;
}"""

ROW_WIDGETS_JS = r"""(gridId) => {
    const t = document.getElementById(gridId);
    if (!t) return [];
    const out = [];
    t.querySelectorAll('input, button, select').forEach(e => {
        if (e.offsetParent !== null)
            out.push({tag: e.tagName, id: e.id, val: (e.value || '').substring(0, 30)});
    });
    return out.slice(0, 25);
}"""


def pick(page, dd, value):
    page.click(f"[id='{dd}_button']")
    page.wait_for_selector(f"[id='{dd}_panel']", state="visible", timeout=10000)
    page.wait_for_timeout(1200)
    page.click(f"[id='{dd}_panel'] >> text=\"{value}\"")
    page.wait_for_timeout(1500)


def go(page):
    page.click("[id='button:form:B']")
    try:
        page.wait_for_load_state("networkidle", timeout=15000)
    except Exception:
        pass
    page.wait_for_timeout(2000)


print("--- D) DB: OBJECT_LIST-ish tables/views ---")
conn = oracledb.connect(user="ECKERNEL_EC", password="energy",
                        dsn="localhost:1521/ORCL", tcp_connect_timeout=15)
cur = conn.cursor()
cur.execute("SELECT table_name FROM all_tables WHERE owner='ECKERNEL_EC' AND table_name LIKE '%OBJECT_LIST%'")
print("  tables:", [r[0] for r in cur.fetchall()])
cur.execute("SELECT view_name FROM all_views WHERE owner='ECKERNEL_EC' AND view_name LIKE '%OBJECT_LIST%'")
print("  views :", [r[0] for r in cur.fetchall()])
cur.close()
conn.close()

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

    print("--- A) Area after PU + GO ---")
    page.goto(URL["Area"], wait_until="domcontentloaded", timeout=45000)
    page.wait_for_timeout(2000)
    try:
        pick(page, "nav:form:G:0:R:1:C:1:dd", "Production Unit")
        go(page)
        print("  grids:", json.dumps(page.evaluate(GRID_JS))[:600])
        page.screenshot(path=str(SHOTS / "phaseb_Area_after_go.png"))
    except Exception as e:
        print("  ERR:", str(e)[:150])

    print("--- B) Sub Area after PU+Area + GO ---")
    page.goto(URL["Sub Area"], wait_until="domcontentloaded", timeout=45000)
    page.wait_for_timeout(2000)
    try:
        pick(page, "nav:form:G:0:R:1:C:1:dd", "Production Unit")
        pick(page, "nav:form:G:0:R:1:C:2:dd", "Offshore area")
        go(page)
        print("  grids:", json.dumps(page.evaluate(GRID_JS))[:600])
        page.screenshot(path=str(SHOTS / "phaseb_SubArea_after_go.png"))
    except Exception as e:
        print("  ERR:", str(e)[:150])

    print("--- C) OLS items + insert row ---")
    page.goto(URL["Object List Setup"], wait_until="domcontentloaded", timeout=45000)
    page.wait_for_timeout(2000)
    try:
        pick(page, "nav:form:G:1:R:1:C:0:dd", "FIN_ACCOUNT")
        pick(page, "nav:form:G:2:R:1:C:0:dd", "OPEX GL Equipment Rental")
        go(page)
        grid = "tab:tabPanel:object_list_table:form:T_data"
        print("  existing widgets:", json.dumps(page.evaluate(ROW_WIDGETS_JS, grid))[:900])
        page.hover("xpath=//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'ui-icon-insert')]]")
        item = page.locator("xpath=//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'ui-icon-insert')]]//ul[contains(@class,'ui-menu-child')]//a[normalize-space(.)='Object List Item']")
        item.wait_for(state="visible", timeout=8000)
        item.click()
        page.wait_for_timeout(2500)
        print("  after insert widgets:", json.dumps(page.evaluate(ROW_WIDGETS_JS, grid))[:900])
        page.screenshot(path=str(SHOTS / "phaseb_OLS_insert_row.png"))
    except Exception as e:
        print("  ERR:", str(e)[:200])
    ctx.close()
    b.close()
print("build probe done (READ-ONLY)")
