"""RC.0050: clean up the leftover well-setup row left by the failed TC03, AND learn the
SAVED-row cell ids (a saved row renders C0 as text C0_in, not calendar C0_da_input).
Nav to UNIT_3 -> find row by perf interval -> dump its cell ids -> select a safe cell ->
Delete 'Well Setup' -> Save -> verify DV_UNIT_WELL_SETUP back to 0. Local sandbox."""
import os
import os, oracledb
from playwright.sync_api import sync_playwright

EC_URL = os.environ.get("EC_URL", "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/")
PERF = "108_WB1-1_PF1"; UA = "Unit Agreement 3"; FORM_DATE = "2011-01-01"
GRID = "well_setup:form:T_data"; PREFIX = "well_setup:form:T"
NAV_DATE = "nav:form:G:0:R:1:C:0:da_input"; NAV_UA = "nav:form:G:1:R:1:C:0:dd"


def db_count():
    c = oracledb.connect(user="ECKERNEL_EC", password="energy", dsn="localhost:1521/ORCL")
    cur = c.cursor(); cur.execute("SELECT COUNT(*) FROM DV_UNIT_WELL_SETUP WHERE PERF_INTERVAL_CODE=:c AND OBJECT_CODE='UNIT_3'", c=PERF)
    n = cur.fetchone()[0]; c.close(); return n


def _css(f): return "#" + f.replace(":", "\\:")

print("DB before cleanup (UNIT_3 x", PERF, "):", db_count())
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

    pg.goto(EC_URL, wait_until="domcontentloaded", timeout=30000)
    pg.fill("#username", os.environ.get("EC_USER", "sysadmin")); pg.fill("#password", os.environ.get("EC_PASS", "sysadmin")); pg.click("#kc-login")
    pg.wait_for_url("**/dashboard**", timeout=60000); ajax()
    si = pg.locator(_css("menu:searchForm:searchTxt")); si.clear(); si.type("Unit - Well Setup", delay=50); ajax(8000)
    pg.locator("xpath=//*[self::label or self::span][contains(@class,'tv-link') and normalize-space(text())='Unit - Well Setup']").first.click(); ajax()
    pg.fill(_css(NAV_DATE), FORM_DATE); pg.keyboard.press("Tab"); pg.wait_for_timeout(700)
    select_dd(NAV_UA, UA); pg.click(_css("button:form:B")); ajax()

    row = find_row(PERF)
    print("found leftover row idx:", row)
    if row >= 0:
        ids = pg.evaluate("(a)=>{const g=a[0],r=a[1];const base=g.replace('_data','')+':'+r+':';"
            "const t=document.getElementById(g);const o=[];"
            "t.querySelectorAll('[id^=\"'+base+'\"]').forEach(e=>{if(e.tagName==='INPUT'&&e.type!=='hidden')o.push(e.id);});return o;}", [GRID, str(row)])
        print("SAVED ROW input ids:", ids)
        # pick a safe non-dropdown cell to select the row: prefer C0_in, else C1_*, else first non-dd
        sel = next((i for i in ids if i.endswith("C0_in")), None) \
            or next((i for i in ids if (":C1" in i)), None) \
            or next((i for i in ids if not i.endswith("dd_input")), ids[0])
        print("selecting cell:", sel)
        pg.click(_css(sel)); pg.wait_for_timeout(800)
        pg.hover("xpath=//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'ui-icon-delete')]]")
        dl = pg.locator("xpath=//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'ui-icon-delete')]]//ul[contains(@class,'ui-menu-child')]//a[normalize-space(.)='Well Setup']")
        dl.first.wait_for(state="visible", timeout=10000); dl.first.click(); ajax()
        pg.click("xpath=//a[@title='Save [Ctrl+s]' and not(contains(@class,'ui-state-disabled'))]"); ajax()
        pg.click("xpath=//a[@title='Refresh [Ctrl+r]']"); ajax()
    else:
        print("no leftover row found in grid")
    b.close()
print("DB after cleanup (UNIT_3 x", PERF, "):", db_count())
