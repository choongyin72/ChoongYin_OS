"""SCAN (READ-ONLY): Calculation Group Setup - nav (Group Context dd options) + after GO the network grid +
CALCULATION JOB CONNECTION tab + its add(+)/grid/Calculation-Job dd. No save."""
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
    # nav fields + group-context dd options
    nav=pg.evaluate("""()=>{
      const f=[...document.querySelectorAll("[id^='nav:form'] input,[id^='nav:form'][id$='dd_button']")].map(e=>({id:e.id,type:e.type||e.tagName}));
      return f;
    }""")
    print("nav fields:",nav)
    # open the group-context dd (find which G is the dd)
    ddbtn=[f['id'] for f in nav if f['id'].endswith('dd_button')]
    if ddbtn:
        pg.locator(cell(ddbtn[0])).click(); pg.wait_for_timeout(900)
        pfx=ddbtn[0].replace('_button','')
        opts=pg.evaluate(f"""()=>[...document.querySelectorAll("[id='{pfx}_panel'] tr")].map(t=>t.getAttribute('data-item-label')).filter(Boolean).slice(0,12)""")
        print("group-context dd options:",opts)
    b.close()
