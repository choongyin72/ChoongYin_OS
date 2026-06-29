"""B-Step1: create AUTOTEST_CALC_TEST via the PROVEN copy-create (donor RUN_NO_TEST, Equations type).
Uses ONLY ids already verified working (copyCalculationForm + copybutton:form:B). Headed."""
from playwright.sync_api import sync_playwright
import os, re
EC_URL=os.environ.get('EC_URL','https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/')
SS=os.path.join(os.path.dirname(__file__),'..','evidence'); HEADED=os.environ.get('EC_HEADED','1')=='1'
def wa(pg,t=20000): pg.wait_for_load_state('networkidle',timeout=t); pg.wait_for_timeout(1300)
def cell(s): return '#'+s.replace(':',r'\:')
DONOR='RUN_NO_TEST'; CODE='AUTOTEST_CALC_TEST'; NAME='AUTOTEST Calc Test'; START='2000-01-01'
with sync_playwright() as p:
    b=p.chromium.launch(headless=not HEADED, slow_mo=250 if HEADED else 0, args=['--ignore-certificate-errors','--start-maximized'])
    pg=b.new_context(ignore_https_errors=True, no_viewport=HEADED, viewport=None if HEADED else {'width':1920,'height':1080}).new_page()
    pg.goto(EC_URL,wait_until='domcontentloaded',timeout=30000)
    pg.fill('#username','sysadmin'); pg.fill('#password','sysadmin'); pg.click('#kc-login')
    pg.wait_for_url('**/dashboard**',timeout=60000); wa(pg)
    si=pg.locator(r'#menu\:searchForm\:searchTxt'); si.wait_for(state='visible',timeout=10000)
    si.clear(); si.type('Create Calculation',delay=50); pg.wait_for_load_state('networkidle',timeout=8000); pg.wait_for_timeout(700)
    pg.locator("xpath=//*[contains(@class,'tv-link') and normalize-space(text())='Create Calculation']").first.click(); wa(pg)
    pg.locator(cell('nav:form:G:0:R:1:C:0:da_input')).click(); pg.locator(cell('nav:form:G:0:R:1:C:0:da_input')).fill('2003-01-01'); pg.keyboard.press('Tab'); pg.wait_for_timeout(800)
    pg.locator(cell('nav:form:G:1:R:1:C:0:dd_button')).click(); pg.wait_for_timeout(1000)
    pg.locator("xpath=//*[@id='nav:form:G:1:R:1:C:0:dd_panel']//tr[normalize-space(@data-item-label)='Production Allocation']").first.click(); wa(pg)
    pg.locator(cell('button:form:B')).click(); wa(pg)
    pg.locator(f"xpath=//*[@id='calculation:form:T_data']//input[@value='{DONOR}']").first.click(); pg.wait_for_timeout(1000)
    pg.locator("xpath=//a[contains(@title,'Create a new calculation as a copy')] | //button[contains(@title,'Create a new calculation as a copy')]").first.click(); pg.wait_for_timeout(2000)
    pg.locator(cell('copyCalculationForm:form:G:0:R:0:C:1:in')).fill(CODE)
    pg.locator(cell('copyCalculationForm:form:G:0:R:0:C:3:in')).fill(NAME)
    sd=cell('copyCalculationForm:form:G:0:R:0:C:5:da_input'); pg.locator(sd).click(); pg.locator(sd).fill(START); pg.keyboard.press('Tab'); pg.wait_for_timeout(600)
    pg.get_by_role("button", name=re.compile("copy to new", re.I)).first.click(); wa(pg)
    pg.screenshot(path=os.path.join(SS,'buildB_01_created.png'))
    err=pg.evaluate("""()=>{const n=document.getElementById('ECNotificationArea')||document.getElementById('ECClientNotificationArea');return n?n.textContent.trim().slice(0,150):'';}""")
    print("notification:",err or '(none)')
    if HEADED: pg.wait_for_timeout(2500)
    b.close()
