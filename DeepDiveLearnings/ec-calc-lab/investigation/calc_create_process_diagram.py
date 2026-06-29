"""Create PROCESS DIAGRAM calc via + -> PUBLIC CALCULATION (per user). Robust: handle both direct-row and
submenu behaviours. Then fill Code/Name/Start/Period=Day/Type=Process Diagram -> Save -> DB-verify. CDP keeper."""
from playwright.sync_api import sync_playwright
import os, oracledb
def say(m): print(m, flush=True)
def cell(s): return '#'+s.replace(':', r'\:')
def wa(pg, t=20000): pg.wait_for_load_state('networkidle', timeout=t); pg.wait_for_timeout(1000)
def empty_row(pg):
    for r in range(25):
        loc = pg.locator(cell('calculation:form:T:' + str(r) + ':C0_in'))
        if loc.count() == 0: continue
        if not loc.input_value().strip(): return r
    return None
EC = 'https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/'
CODE = 'AUTOTEST_PROC_TEST'; NAME = 'AUTOTEST Proc Test'
with sync_playwright() as p:
    b = p.chromium.launch(headless=False, slow_mo=300, args=['--ignore-certificate-errors', '--start-maximized', '--remote-debugging-port=9222'])
    pg = b.new_context(ignore_https_errors=True, no_viewport=True).new_page()
    pg.goto(EC, wait_until='domcontentloaded', timeout=30000)
    pg.fill('#username', 'sysadmin'); pg.fill('#password', 'sysadmin'); pg.click('#kc-login')
    pg.wait_for_url('**/dashboard**', timeout=60000); wa(pg); say("logged in")
    s = pg.locator(r'#menu\:searchForm\:searchTxt'); s.click(); s.fill(''); s.type('Create Calculation', delay=40); pg.wait_for_timeout(1400)
    pg.locator("xpath=//*[contains(@class,'tv-link') and normalize-space(text())='Create Calculation']").first.click(); wa(pg)
    pg.locator(cell('nav:form:G:0:R:1:C:0:da_input')).fill('2003-01-01'); pg.keyboard.press('Tab'); pg.wait_for_timeout(700)
    pg.locator(cell('nav:form:G:1:R:1:C:0:dd_button')).click(); pg.wait_for_timeout(900)
    pg.locator("xpath=//*[@id='nav:form:G:1:R:1:C:0:dd_panel']//tr[normalize-space(@data-item-label)='Production Allocation']").first.click(); wa(pg)
    pg.locator(cell('button:form:B')).click(); wa(pg); say("context Production Allocation + GO")
    # robust create: + (then PUBLIC CALCULATION submenu if present), until an empty row appears
    er = None
    for att in range(4):
        ins = pg.locator("xpath=//a[.//span[contains(@class,'ui-icon-insert')]]")
        for i in range(ins.count()):
            if ins.nth(i).is_visible(): ins.nth(i).click(); break
        pg.wait_for_timeout(1000)
        # if a submenu item "Public Calculation" is visible, click it
        pc = pg.locator("xpath=//a[contains(@class,'ui-menuitem-link')][.//span[contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'public calculation')]]")
        for i in range(pc.count()):
            if pc.nth(i).is_visible(): pc.nth(i).click(); say("clicked PUBLIC CALCULATION submenu"); break
        pg.wait_for_timeout(1200)
        er = empty_row(pg)
        if er is not None: say("empty row appeared at index %d (attempt %d)" % (er, att + 1)); break
        pg.keyboard.press('Escape'); pg.wait_for_timeout(500)
    if er is None:
        say("could not add a new row"); pg.screenshot(path="C:/tmp/proc_noadd.png", full_page=True); pg.wait_for_timeout(3600000); b.close(); raise SystemExit
    R = 'calculation:form:T:' + str(er)
    pg.locator(cell(R + ':C0_in')).fill(CODE); pg.keyboard.press('Tab'); pg.wait_for_timeout(400)
    pg.locator(cell(R + ':C1_in')).fill(NAME); pg.keyboard.press('Tab'); pg.wait_for_timeout(400)
    pg.locator(cell(R + ':C2_da_input')).fill('2000-01-01'); pg.keyboard.press('Tab'); pg.wait_for_timeout(500)
    pg.locator(cell(R + ':C4_dd_button')).click(); pg.wait_for_timeout(800)
    pg.locator("xpath=//*[@id='" + R + ":C4_dd_panel']//tr[normalize-space(@data-item-label)='Day']").first.click(); pg.wait_for_timeout(600)
    pg.locator(cell(R + ':C5_dd_button')).click(); pg.wait_for_timeout(800)
    pg.locator("xpath=//*[@id='" + R + ":C5_dd_panel']//tr[normalize-space(@data-item-label)='Process Diagram']").first.click(); pg.wait_for_timeout(600)
    pg.screenshot(path="C:/tmp/proc_filled.png", full_page=True); say("SHOT proc_filled")
    pg.locator("xpath=//a[@title='Save [Ctrl+s]' and not(contains(@class,'ui-state-disabled'))]").first.click(); wa(pg); pg.wait_for_timeout(1500)
    c = oracledb.connect(user=os.environ.get('EC_DB_USER', 'ECKERNEL_EC'), password=os.environ.get('EC_DB_PASS', 'energy'), dsn=os.environ.get('EC_DB_DSN', 'localhost:1521/ORCL'))
    cur = c.cursor(); cur.execute("select object_code, calc_type, calc_period from calculation where object_code='AUTOTEST_PROC_TEST'"); say("DB row: " + str(cur.fetchone())); c.close()
    say("CREATE done - browser open (CDP 9222) for FLOWCHART step")
    pg.wait_for_timeout(3600000)
    b.close()
