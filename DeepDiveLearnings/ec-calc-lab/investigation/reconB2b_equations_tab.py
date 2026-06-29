"""SCAN (READ-ONLY): drive Maintain Calc to AUTOTEST_CALC_TEST, open EQUATIONS tab, dump the equation grid +
edit mechanism (cell ids + how the equation-editor popup opens). No save."""
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
    si.clear(); si.type('Maintain Calculation',delay=50); pg.wait_for_load_state('networkidle',timeout=8000); pg.wait_for_timeout(700)
    pg.locator("xpath=//*[contains(@class,'tv-link') and normalize-space(text())='Maintain Calculation']").first.click(); wa(pg)
    pg.locator(cell('nav:form:G:0:R:1:C:0:da_input')).click(); pg.locator(cell('nav:form:G:0:R:1:C:0:da_input')).fill('2003-01-01'); pg.keyboard.press('Tab'); pg.wait_for_timeout(700)
    # context dd G:1
    pg.locator(cell('nav:form:G:1:R:1:C:0:dd_button')).click(); pg.wait_for_timeout(900)
    pg.locator("xpath=//*[@id='nav:form:G:1:R:1:C:0:dd_panel']//tr[normalize-space(@data-item-label)='Production Allocation']").first.click(); wa(pg)
    # Calculation dd G:2 - SCAN its options for the exact AUTOTEST label
    pg.locator(cell('nav:form:G:2:R:1:C:0:dd_button')).click(); pg.wait_for_timeout(1000)
    opts=pg.evaluate("""()=>[...document.querySelectorAll("[id='nav:form:G:2:R:1:C:0:dd_panel'] tr")].map(t=>t.getAttribute('data-item-label')).filter(x=>x&&/autotest/i.test(x))""")
    print("Calculation dd AUTOTEST options:",opts)
    if not opts: print("ABORT scan: AUTOTEST_CALC_TEST not in Calculation dd"); b.close(); raise SystemExit
    pg.locator(f"xpath=//*[@id='nav:form:G:2:R:1:C:0:dd_panel']//tr[normalize-space(@data-item-label)='{opts[0]}']").first.click(); wa(pg)
    pg.locator(cell('button:form:B')).click(); wa(pg)
    # find + click EQUATIONS tab
    eqtab=pg.locator("xpath=//a[normalize-space(.)='Equations'] | //span[normalize-space(.)='Equations']/ancestor::a[1] | //li[.//*[normalize-space(.)='Equations']]//a")
    print("Equations tab count:",eqtab.count())
    if eqtab.count()>0: eqtab.first.click(); wa(pg)
    pg.screenshot(path=os.path.join(SS,'buildB_02_equations_tab.png'))
    # dump the equation grid row + cells + any editable equation cell / edit popup trigger
    grid=pg.evaluate("""()=>{
      const tb=[...document.querySelectorAll("tbody[id$='_data']")].filter(t=>/INFO|equation/i.test(t.textContent)).map(t=>t.id);
      const cells=[...document.querySelectorAll("[id*=':T:0:'][id$='_in'],[id*=':T:0:'][id$='_input'],[id*=':T:0:'] textarea,[id*=':T:0:'][id$='dd_button']")].map(e=>({id:e.id,tag:e.tagName,val:(e.value||'').slice(0,40),ro:e.readOnly})).slice(0,12);
      return {grids:tb, cells};
    }""")
    print("equation grid tbodies:",grid['grids'])
    print("row-0 cells:")
    for c in grid['cells']: print("   ",c)
    b.close()
