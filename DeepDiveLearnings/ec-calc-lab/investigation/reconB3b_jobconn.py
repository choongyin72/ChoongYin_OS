"""SCAN (READ-ONLY): Calc Group Setup -> Allocation Network Calculation -> GO -> network grid (find P1_DAY_ALLOC)
-> select it -> CALCULATION JOB CONNECTION tab -> dump job-connection grid + + button + Calculation Job dd. No add/save."""
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
    pg.screenshot(path=os.path.join(SS,'buildB_05_calcgroup.png'))
    # dump the network grid (tbodies + which holds P1_DAY_ALLOC)
    g=pg.evaluate("""()=>{
      const tbs=[...document.querySelectorAll("tbody[id$='_data']")].map(t=>({id:t.id, has_p1:/P1_DAY_ALLOC/.test(t.textContent), rows:t.querySelectorAll('tr').length}));
      const tabs=[...document.querySelectorAll("a,span,li")].map(e=>e.textContent.trim()).filter(t=>/calculation job connection|calculation group|list/i.test(t)).slice(0,6);
      return {tbs, tabs:[...new Set(tabs)]};
    }""")
    print("grids:",g['tbs'])
    print("tabs present:",g['tabs'])
    # select the P1_DAY_ALLOC network row
    net=pg.locator("xpath=//tbody[contains(@id,'_data')]//tr[.//*[contains(text(),'P1_DAY_ALLOC')] or .//input[@value='P1_DAY_ALLOC']]")
    print("P1_DAY_ALLOC row count:",net.count())
    if net.count()>0:
        net.first.click(); wa(pg)
    # click CALCULATION JOB CONNECTION tab
    jc=pg.locator("xpath=//a[contains(translate(.,'CALCULATION JOB','calculation job'),'calculation job connection')] | //span[contains(translate(.,'CALCULATION JOB','calculation job'),'calculation job connection')]")
    print("JOB CONNECTION tab count:",jc.count())
    if jc.count()>0: jc.first.click(); wa(pg)
    pg.screenshot(path=os.path.join(SS,'buildB_06_jobconn_tab.png'))
    # dump job-connection grid + Calculation Job dd cells + the + (insert) toolbar
    j=pg.evaluate("""()=>{
      const tbs=[...document.querySelectorAll("tbody[id$='_data']")].map(t=>({id:t.id, txt:t.innerText.replace(/\s+/g,' ').slice(0,60)})).filter(o=>/calculation test|daily well|job/i.test(o.txt)||/job/i.test(o.id));
      const dds=[...document.querySelectorAll("[id$='dd_button']")].filter(e=>e.offsetParent!==null && !e.id.startsWith('nav:form')).map(e=>e.id).slice(0,8);
      const ins=[...document.querySelectorAll("a,span")].filter(e=>/ui-icon-insert/.test((e.querySelector('span')||e).className||'')||/ui-icon-insert/.test(e.className||'')).map(e=>e.id||'(insert-icon)').slice(0,4);
      return {tbs, dds, ins};
    }""")
    print("job-conn grids:",j['tbs'])
    print("dd_buttons (non-nav):",j['dds'])
    b.close()
