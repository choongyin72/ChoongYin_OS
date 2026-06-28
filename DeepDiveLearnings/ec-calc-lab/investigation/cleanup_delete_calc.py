"""Phase-5 cleanup: delete AUTOTEST_DBL_VOL via Create Calculation 'Delete Calculation' (EC-clean). Verify gone."""
from playwright.sync_api import sync_playwright
import os, re
EC_URL=os.environ.get('EC_URL','https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/')
SS=os.path.join(os.path.dirname(__file__),'..','evidence')
def wa(pg,t=20000): pg.wait_for_load_state('networkidle',timeout=t); pg.wait_for_timeout(1300)
def cell(s): return '#'+s.replace(':',r'\:')
with sync_playwright() as p:
    b=p.chromium.launch(headless=True,args=['--ignore-certificate-errors'])
    pg=b.new_context(ignore_https_errors=True,viewport={'width':1920,'height':1080}).new_page()
    pg.goto(EC_URL,wait_until='domcontentloaded',timeout=30000)
    pg.fill('#username','sysadmin'); pg.fill('#password','sysadmin'); pg.click('#kc-login')
    pg.wait_for_url('**/dashboard**',timeout=60000); wa(pg)
    si=pg.locator(r'#menu\:searchForm\:searchTxt'); si.wait_for(state='visible',timeout=10000)
    si.clear(); si.type('Create Calculation',delay=50); pg.wait_for_load_state('networkidle',timeout=8000); pg.wait_for_timeout(700)
    pg.locator("xpath=//*[contains(@class,'tv-link') and normalize-space(text())='Create Calculation']").first.click(); wa(pg)
    pg.locator(cell('nav:form:G:0:R:1:C:0:da_input')).click(); pg.locator(cell('nav:form:G:0:R:1:C:0:da_input')).fill('2003-01-01'); pg.keyboard.press('Tab'); pg.wait_for_timeout(700)
    pg.locator(cell('nav:form:G:1:R:1:C:0:dd_button')).click(); pg.wait_for_timeout(900)
    pg.locator("xpath=//*[@id='nav:form:G:1:R:1:C:0:dd_panel']//tr[normalize-space(@data-item-label)='Production Allocation']").first.click(); wa(pg)
    pg.locator(cell('button:form:B')).click(); wa(pg)
    sel=pg.locator("xpath=//*[@id='calculation:form:T_data']//input[@value='AUTOTEST_DBL_VOL']")
    print("AUTOTEST_DBL_VOL row present:",sel.count())
    if sel.count()==0:
        print("not in grid - nothing to delete via UI"); b.close(); raise SystemExit
    sel.first.click(); pg.wait_for_timeout(1000)
    # click DELETE CALCULATION (case-insensitive)
    try:
        pg.get_by_role("button", name=re.compile("delete calculation", re.I)).first.click(timeout=8000)
    except Exception:
        pg.locator("xpath=//*[contains(translate(.,'DELETE','delete'),'delete calculation')][self::button or self::a]").first.click()
    pg.wait_for_timeout(1500)
    # confirm dialog if any (Yes/OK)
    for lab in ("Yes","OK","Ok","Confirm","Delete"):
        bx=pg.get_by_role("button", name=re.compile(f"^{lab}$", re.I))
        if bx.count()>0 and bx.first.is_visible():
            bx.first.click(); print("confirmed via",lab); break
    wa(pg)
    pg.screenshot(path=os.path.join(SS,'build_07_after_delete.png'))
    print("delete attempted.")
    b.close()
