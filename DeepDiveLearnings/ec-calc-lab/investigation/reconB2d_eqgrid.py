"""SCAN (READ-ONLY): dump the equations grid (maintab:tabPanel:equations:form:T_data) full id structure +
equations-screenlet toolbar actions. No tab-click, no save."""
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
    pg.locator(cell('nav:form:G:1:R:1:C:0:dd_button')).click(); pg.wait_for_timeout(900)
    pg.locator("xpath=//*[@id='nav:form:G:1:R:1:C:0:dd_panel']//tr[normalize-space(@data-item-label)='Production Allocation']").first.click(); wa(pg)
    pg.locator(cell('nav:form:G:2:R:1:C:0:dd_button')).click(); pg.wait_for_timeout(900)
    pg.locator("xpath=//*[@id='nav:form:G:2:R:1:C:0:dd_panel']//tr[normalize-space(@data-item-label)='AUTOTEST Calc Test']").first.click(); wa(pg)
    pg.locator(cell('button:form:B')).click(); wa(pg)
    pg.screenshot(path=os.path.join(SS,'buildB_02_equations_tab.png'))
    dump=pg.evaluate("""()=>{
      const tb=document.getElementById('maintab:tabPanel:equations:form:T_data');
      if(!tb) return {err:'equations tbody not in DOM (tab not active)'};
      const els=[...tb.querySelectorAll('[id]')].map(e=>({tag:e.tagName,id:e.id,cls:(e.className&&e.className.toString?e.className.toString():'').slice(0,28),val:(e.value||'').slice(0,45),vis:e.offsetParent!==null})).slice(0,30);
      return {rowtext:tb.innerText.replace(/\s+/g,' ').trim().slice(0,140), n:els.length, els};
    }""")
    if dump.get('err'): print(dump['err'])
    else:
        print("equation row text:",dump['rowtext'])
        print(f"ids in equations tbody ({dump['n']}):")
        for e in dump['els']: print("   ",e)
    b.close()
