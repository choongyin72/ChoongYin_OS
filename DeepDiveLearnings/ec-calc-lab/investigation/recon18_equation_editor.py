"""Phase-2 (READ-ONLY): open Maintain Calculation -> AUTOTEST_DBL_VOL -> characterize the equation-edit UI
(graphical builder vs text formula entry?). Screenshot only; no save."""
from playwright.sync_api import sync_playwright
import os
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
    si.clear(); si.type('Maintain Calculation',delay=50); pg.wait_for_load_state('networkidle',timeout=8000); pg.wait_for_timeout(700)
    link=pg.locator("xpath=//*[contains(@class,'tv-link') and normalize-space(text())='Maintain Calculation']")
    print("Maintain Calculation tv-link:",link.count())
    link.first.click(); wa(pg)
    # try same nav: date + context + GO
    try:
        pg.locator(cell('nav:form:G:0:R:1:C:0:da_input')).click(); pg.locator(cell('nav:form:G:0:R:1:C:0:da_input')).fill('2003-01-01'); pg.keyboard.press('Tab'); pg.wait_for_timeout(700)
        pg.locator(cell('nav:form:G:1:R:1:C:0:dd_button')).click(); pg.wait_for_timeout(900)
        pg.locator("xpath=//*[@id='nav:form:G:1:R:1:C:0:dd_panel']//tr[normalize-space(@data-item-label)='Production Allocation']").first.click(); wa(pg)
        pg.locator(cell('button:form:B')).click(); wa(pg)
    except Exception as e: print("nav note:",str(e)[:60])
    # select AUTOTEST_DBL_VOL if present
    sel=pg.locator("xpath=//input[@value='AUTOTEST_DBL_VOL'] | //*[contains(text(),'AUTOTEST_DBL_VOL')]")
    print("AUTOTEST_DBL_VOL on screen:",sel.count())
    if sel.count()>0:
        sel.first.click(); wa(pg)
    pg.screenshot(path=os.path.join(SS,'build_06_maintain_calc.png'), full_page=True)
    # look for a formula/expression text input vs graphical
    txt=pg.evaluate("""()=>{
      const ta=[...document.querySelectorAll('textarea')].filter(e=>e.offsetParent!==null).map(e=>e.id).slice(0,8);
      const formulaish=[...document.querySelectorAll("input,textarea,[contenteditable]")].filter(e=>/equation|formula|expr/i.test(e.id)).map(e=>e.id).slice(0,8);
      const tabs=[...document.querySelectorAll("a,span")].map(e=>e.textContent.trim()).filter(t=>/equation|variable|mapping|formula/i.test(t)).slice(0,10);
      return {textareas:ta, formulaish, tabs:[...new Set(tabs)]};
    }""")
    print("textareas:",txt['textareas'])
    print("formula-ish inputs:",txt['formulaish'])
    print("equation/var/mapping tabs:",txt['tabs'])
    print("DONE (read-only; screenshot build_06).")
    b.close()
