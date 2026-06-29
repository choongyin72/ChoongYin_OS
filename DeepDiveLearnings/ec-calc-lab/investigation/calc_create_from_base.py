"""Create a calculation FROM BASE (the proper method) - toolbar + -> new blank row -> fill all mandatory
fields (Code/Name/Start/Period/Type) -> Save -> DB-verify. (Copy-To-New discarded per owner.)
Headed: EC_HEADED=1 py -u -X utf8 calc_create_from_base.py"""
from playwright.sync_api import sync_playwright
import os, oracledb
EC = os.environ.get('EC_URL', 'https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/')
CODE = 'AUTOTEST_BASE_TEST'; NAME = 'AUTOTEST Base Test'; START = '2000-01-01'; PERIOD = 'Day'; CTYPE = 'Equations'
HEADED = os.environ.get('EC_HEADED', '1') == '1'
def say(m): print(m, flush=True)
def cell(s): return '#' + s.replace(':', r'\:')
def wa(pg, t=20000): pg.wait_for_load_state('networkidle', timeout=t); pg.wait_for_timeout(1000)
with sync_playwright() as p:
    b = p.chromium.launch(headless=not HEADED, slow_mo=300 if HEADED else 0, args=['--ignore-certificate-errors', '--start-maximized'])
    pg = b.new_context(ignore_https_errors=True, no_viewport=HEADED, viewport=None if HEADED else {'width': 1920, 'height': 1080}).new_page()
    pg.goto(EC, wait_until='domcontentloaded', timeout=30000)
    pg.fill('#username', 'sysadmin'); pg.fill('#password', 'sysadmin'); pg.click('#kc-login')
    pg.wait_for_url('**/dashboard**', timeout=60000); wa(pg)
    s = pg.locator(r'#menu\:searchForm\:searchTxt'); s.click(); s.fill(''); s.type('Create Calculation', delay=40); pg.wait_for_timeout(1400)
    pg.locator("xpath=//*[contains(@class,'tv-link') and normalize-space(text())='Create Calculation']").first.click(); wa(pg)
    pg.locator(cell('nav:form:G:0:R:1:C:0:da_input')).fill('2003-01-01'); pg.keyboard.press('Tab'); pg.wait_for_timeout(700)
    pg.locator(cell('nav:form:G:1:R:1:C:0:dd_button')).click(); pg.wait_for_timeout(900)
    pg.locator("xpath=//*[@id='nav:form:G:1:R:1:C:0:dd_panel']//tr[normalize-space(@data-item-label)='Production Allocation']").first.click(); wa(pg)
    pg.locator(cell('button:form:B')).click(); wa(pg)
    # CREATE FROM BASE: click + -> new blank row
    ins = pg.locator("xpath=//a[.//span[contains(@class,'ui-icon-insert')]]")
    for i in range(ins.count()):
        if ins.nth(i).is_visible(): ins.nth(i).click(); break
    pg.wait_for_timeout(1300)
    # find the empty row (blank Code)
    empty = None
    for r in range(25):
        loc = pg.locator(cell('calculation:form:T:' + str(r) + ':C0_in'))
        if loc.count() == 0: continue
        if not loc.input_value().strip(): empty = r; break
    say("new blank row index = %s" % empty)
    R = 'calculation:form:T:' + str(empty)
    pg.locator(cell(R + ':C0_in')).fill(CODE); pg.keyboard.press('Tab'); pg.wait_for_timeout(400)
    pg.locator(cell(R + ':C1_in')).fill(NAME); pg.keyboard.press('Tab'); pg.wait_for_timeout(400)
    pg.locator(cell(R + ':C2_da_input')).fill(START); pg.keyboard.press('Tab'); pg.wait_for_timeout(500)
    pg.locator(cell(R + ':C4_dd_button')).click(); pg.wait_for_timeout(800)
    pg.locator("xpath=//*[@id='" + R + ":C4_dd_panel']//tr[normalize-space(@data-item-label)='" + PERIOD + "']").first.click(); pg.wait_for_timeout(600)
    pg.locator(cell(R + ':C5_dd_button')).click(); pg.wait_for_timeout(800)
    pg.locator("xpath=//*[@id='" + R + ":C5_dd_panel']//tr[normalize-space(@data-item-label)='" + CTYPE + "']").first.click(); pg.wait_for_timeout(600)
    pg.locator("xpath=//a[@title='Save [Ctrl+s]' and not(contains(@class,'ui-state-disabled'))]").first.click(); wa(pg); pg.wait_for_timeout(1500)
    if HEADED: pg.wait_for_timeout(2000)
    b.close()
c = oracledb.connect(user=os.environ.get('EC_DB_USER', 'ECKERNEL_EC'), password=os.environ.get('EC_DB_PASS', 'energy'), dsn=os.environ.get('EC_DB_DSN', 'localhost:1521/ORCL'))
cur = c.cursor(); cur.execute("select object_code, calc_type, calc_scope, ecdp_objects.GetObjCode(calc_context_id), calc_period, to_char(start_date,'YYYY-MM-DD') from calculation where object_code='AUTOTEST_BASE_TEST'")
say("DB row: " + str(cur.fetchone())); c.close()
