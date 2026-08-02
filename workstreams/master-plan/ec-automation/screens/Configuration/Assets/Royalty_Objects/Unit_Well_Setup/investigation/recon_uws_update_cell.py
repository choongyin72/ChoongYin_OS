"""RC.0050 UPDATE recon (self-cleaning write probe): map saved-row cells C3_in/C4_in to
DB columns (SORT_ORDER numeric / COMMENTS text) so the UPDATE test edits the right cell.
Insert -> save -> set C3='333',C4='444' on the saved row -> save -> read DV_UNIT_WELL_SETUP
-> delete -> confirm clean. Local sandbox."""
import os
import os, oracledb
from playwright.sync_api import sync_playwright

EC_URL = os.environ.get("EC_URL", "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/")
PERF = "108_WB1-1_PF1"; UA = "Unit Agreement 3"; FORM_DATE = "2011-01-01"
GRID = "well_setup:form:T_data"; PREFIX = "well_setup:form:T"
NAV_DATE = "nav:form:G:0:R:1:C:0:da_input"; NAV_UA = "nav:form:G:1:R:1:C:0:dd"


def db_row():
    c = oracledb.connect(user="ECKERNEL_EC", password="energy", dsn="localhost:1521/ORCL")
    cur = c.cursor()
    cur.execute("SELECT SORT_ORDER, COMMENTS FROM DV_UNIT_WELL_SETUP WHERE OBJECT_CODE='UNIT_3' AND PERF_INTERVAL_CODE=:p", p=PERF)
    r = cur.fetchall(); c.close(); return r


def _css(f): return "#" + f.replace(":", "\\:")

print("DB row(s) before:", db_row())
with sync_playwright() as p:
    b = p.chromium.launch(headless=True, args=["--ignore-certificate-errors"])
    pg = b.new_context(ignore_https_errors=True, viewport={"width": 1680, "height": 1000}).new_page()
    pg.set_default_timeout(30000)

    def ajax(t=15000):
        try: pg.wait_for_load_state("networkidle", timeout=t)
        except Exception: pass
        pg.wait_for_timeout(1200)

    def select_dd(dd, v):
        it = f"xpath=//*[@id='{dd}_panel']//tr[normalize-space(@data-item-label)='{v}']"
        pg.click(_css(dd + "_button")); pg.locator(it).first.wait_for(state="visible", timeout=10000)
        pg.locator(it).first.click(); ajax(12000)

    def find_row(v):
        return pg.evaluate("(a)=>{const[g,x]=a;const t=document.getElementById(g);if(!t)return -1;"
            "for(const e of t.querySelectorAll(\"input[id$='C2_dd_input']\")){if((e.value||'')===x){const m=e.id.match(/:T:(\\d+):/);if(m)return +m[1];}}return -1;}", [GRID, v])

    def type_cell(cid, val):
        pg.click(_css(cid)); pg.fill(_css(cid), ""); pg.type(_css(cid), val, delay=40)
        pg.keyboard.press("Tab"); ajax(12000)

    def save(): pg.click("xpath=//a[@title='Save [Ctrl+s]' and not(contains(@class,'ui-state-disabled'))]"); ajax()
    def refresh(): pg.click("xpath=//a[@title='Refresh [Ctrl+r]']"); ajax()

    pg.goto(EC_URL, wait_until="domcontentloaded", timeout=30000)
    pg.fill("#username", os.environ.get("EC_USER", "sysadmin")); pg.fill("#password", os.environ.get("EC_PASS", "sysadmin")); pg.click("#kc-login")
    pg.wait_for_url("**/dashboard**", timeout=60000); ajax()
    si = pg.locator(_css("menu:searchForm:searchTxt")); si.clear(); si.type("Unit - Well Setup", delay=50); ajax(8000)
    pg.locator("xpath=//*[self::label or self::span][contains(@class,'tv-link') and normalize-space(text())='Unit - Well Setup']").first.click(); ajax()
    pg.fill(_css(NAV_DATE), FORM_DATE); pg.keyboard.press("Tab"); pg.wait_for_timeout(700)
    select_dd(NAV_UA, UA); pg.click(_css("button:form:B")); ajax()

    # INSERT
    pg.hover("xpath=//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'ui-icon-insert')]]")
    il = pg.locator("xpath=//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'ui-icon-insert')]]//ul[contains(@class,'ui-menu-child')]//a[normalize-space(.)='Well Setup']")
    il.first.wait_for(state="visible", timeout=10000); il.first.click(); ajax()
    row = find_row(""); print("blank row idx:", row)
    select_dd(f"{PREFIX}:{row}:C2_dd", PERF); row = find_row(PERF)
    pg.fill(_css(f"{PREFIX}:{row}:C0_da_input"), FORM_DATE); pg.keyboard.press("Tab"); pg.wait_for_timeout(700)
    save(); refresh()
    row = find_row(PERF); print("saved row idx:", row)

    # UPDATE PROBE: set C3=333, C4=444 on the saved row
    for cid, val in ((f"{PREFIX}:{row}:C3_in", "333"), (f"{PREFIX}:{row}:C4_in", "444")):
        try: type_cell(cid, val); print("typed", val, "into", cid)
        except Exception as e: print("  could not type into", cid, "-", str(e)[:60])
    save(); refresh()
    print("DB row(s) after update probe (SORT_ORDER, COMMENTS):", db_row())

    # DELETE (self-clean)
    row = find_row(PERF)
    if row >= 0:
        pg.click(_css(f"{PREFIX}:{row}:C0_in")); pg.wait_for_timeout(800)
        pg.hover("xpath=//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'ui-icon-delete')]]")
        dl = pg.locator("xpath=//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'ui-icon-delete')]]//ul[contains(@class,'ui-menu-child')]//a[normalize-space(.)='Well Setup']")
        dl.first.wait_for(state="visible", timeout=10000); dl.first.click(); ajax()
        save(); refresh()
    b.close()
print("DB row(s) after cleanup:", db_row())
