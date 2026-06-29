"""SCAN (READ-ONLY): select P1_DAY_ALLOC -> open the 'Calculation Job' tab -> dump the job grid + insert(+) +
the Calculation Job dd cell structure. No add/save."""
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
    si.clear(); si.type('Calculation Group Setup',delay=50); pg.wait_for_load_state('networkidle',timeout=8000); pg.wait_for_timeout(700)
    pg.locator("xpath=//*[contains(@class,'tv-link') and normalize-space(text())='Calculation Group Setup']").first.click(); wa(pg)
    pg.locator(cell('nav:form:G:0:R:1:C:0:da_input')).click(); pg.locator(cell('nav:form:G:0:R:1:C:0:da_input')).fill('2026-06-29'); pg.keyboard.press('Tab'); pg.wait_for_timeout(700)
    pg.locator(cell('nav:form:G:0:R:1:C:1:dd_button')).click(); pg.wait_for_timeout(900)
    pg.locator("xpath=//*[@id='nav:form:G:0:R:1:C:1:dd_panel']//tr[normalize-space(@data-item-label)='Allocation Network Calculation']").first.click(); wa(pg)
    pg.locator(cell('button:form:B')).click(); wa(pg)
    pg.locator("xpath=//tbody[@id='nav_model:form:T_data']//tr[.//input[@value='P1_DAY_ALLOC'] or .//*[contains(text(),'P1_DAY_ALLOC')]]").first.click(); wa(pg)
    # open the 'Calculation Job' tab (exact visible text)
    jt=pg.locator("xpath=//a[normalize-space(.)='Calculation Job'] | //span[normalize-space(.)='Calculation Job']/ancestor::a[1]")
    print("'Calculation Job' tab count:",jt.count())
    if jt.count()==0:
        print("ABORT: 'Calculation Job' tab not found"); 
        print("  visible tab-ish:", pg.evaluate("()=>[...document.querySelectorAll('a[role=tab],li.ui-tabs-header a,.ui-tabs-nav a')].map(e=>e.textContent.trim()).slice(0,10)"))
        b.close(); raise SystemExit
    jt.first.click(); wa(pg)
    pg.screenshot(path=os.path.join(SS,'buildB_06_jobtab.png'))
    # dump the job grid + its insert + Calculation Job dd
    j=pg.evaluate("""()=>{
      const tbs=[...document.querySelectorAll("tbody[id$='_data']")].filter(t=>t.offsetParent!==null).map(t=>({id:t.id, txt:t.innerText.replace(/\s+/g,' ').slice(0,70)}));
      const ins=[...document.querySelectorAll("a")].filter(e=>e.offsetParent!==null && /ui-icon-insert/.test((e.querySelector("span[class*='ui-icon']")||{}).className||'')).map(e=>e.id||'(insert-icon-a)').slice(0,4);
      const dds=[...document.querySelectorAll("[id$='dd_button']")].filter(e=>e.offsetParent!==null && /job|calc/i.test(e.id) && !e.id.startsWith('nav')).map(e=>e.id).slice(0,8);
      return {tbs, ins, dds};
    }""")
    print("visible grids:",j['tbs'])
    print("insert-icon links:",j['ins'])
    print("job/calc dd_buttons:",j['dds'])
    b.close()
