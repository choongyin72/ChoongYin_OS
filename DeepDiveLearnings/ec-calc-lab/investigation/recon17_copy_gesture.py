"""Phase-2 copy-gesture probe: select an EQUATIONS stub -> 'create a copy' -> CAPTURE the dialog/row.
Does NOT save (escape/navigate away). Maps the create flow before the real write."""
from playwright.sync_api import sync_playwright
import os
EC_URL=os.environ.get('EC_URL','https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/')
SS=os.path.join(os.path.dirname(__file__),'..','evidence')
def wa(pg,t=20000): pg.wait_for_load_state('networkidle',timeout=t); pg.wait_for_timeout(1200)
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
    d='nav:form:G:0:R:1:C:0:da_input'
    pg.locator(cell(d)).click(); pg.locator(cell(d)).fill('2003-01-01'); pg.keyboard.press('Tab'); pg.wait_for_timeout(800)
    pg.locator(cell('nav:form:G:1:R:1:C:0:dd_button')).click(); pg.wait_for_timeout(1000)
    pg.locator("xpath=//*[@id='nav:form:G:1:R:1:C:0:dd_panel']//tr[normalize-space(@data-item-label)='Production Allocation']").first.click(); wa(pg)
    pg.locator(cell('button:form:B')).click(); wa(pg)
    # select the 01_TEST_CALCULATION row (click its code cell)
    row=pg.locator("xpath=//tbody[@id='calculation:form:T_data']//tr[.//*[contains(text(),'01_TEST_CALCULATION')] or .//input[@value='01_TEST_CALCULATION']]")
    print("row match count:",row.count())
    pg.locator("xpath=//*[@id='calculation:form:T_data']//input[@value='01_TEST_CALCULATION']").first.click(); pg.wait_for_timeout(800)
    pg.screenshot(path=os.path.join(SS,'build_01_selected.png'))
    # click the copy toolbar button by title
    cp=pg.locator("xpath=//a[contains(@title,'Create a new calculation as a copy')] | //button[contains(@title,'Create a new calculation as a copy')]")
    print("copy button count:",cp.count())
    cp.first.click(); pg.wait_for_timeout(2000)
    pg.screenshot(path=os.path.join(SS,'build_02_after_copy_click.png'))
    # capture any dialog / new input
    dlg=pg.evaluate("""()=>{
      const vis=[...document.querySelectorAll("div[role='dialog'], .ui-dialog")].filter(d=>d.offsetParent!==null).map(d=>d.id);
      const inputs=[...document.querySelectorAll("div[role='dialog'] input, .ui-dialog input, [id*='copy' i] input, [id*='Dialog'] input")].filter(e=>e.offsetParent!==null).map(e=>e.id).slice(0,10);
      return {dialogs:vis, inputs};
    }""")
    print("dialogs:",dlg['dialogs'])
    print("dialog inputs:",dlg['inputs'])
    print("DONE (captured; NOT saved).")
    b.close()
