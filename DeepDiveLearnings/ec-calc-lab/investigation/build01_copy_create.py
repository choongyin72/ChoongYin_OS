"""Phase-2 FIRST WRITE (v3): copy RUN_NO_TEST -> AUTOTEST_DBL_VOL. Case-insensitive confirm-button match."""
from playwright.sync_api import sync_playwright
import os, re
EC_URL=os.environ.get('EC_URL','https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/')
SS=os.path.join(os.path.dirname(__file__),'..','evidence')
def wa(pg,t=20000): pg.wait_for_load_state('networkidle',timeout=t); pg.wait_for_timeout(1200)
def cell(s): return '#'+s.replace(':',r'\:')
DONOR='RUN_NO_TEST'; CODE='AUTOTEST_DBL_VOL'; NAME='AUTOTEST Double Volume'; START='2003-01-01'
with sync_playwright() as p:
    b=p.chromium.launch(headless=True,args=['--ignore-certificate-errors'])
    pg=b.new_context(ignore_https_errors=True,viewport={'width':1920,'height':1080}).new_page()
    pg.goto(EC_URL,wait_until='domcontentloaded',timeout=30000)
    pg.fill('#username','sysadmin'); pg.fill('#password','sysadmin'); pg.click('#kc-login')
    pg.wait_for_url('**/dashboard**',timeout=60000); wa(pg)
    si=pg.locator(r'#menu\:searchForm\:searchTxt'); si.wait_for(state='visible',timeout=10000)
    si.clear(); si.type('Create Calculation',delay=50); pg.wait_for_load_state('networkidle',timeout=8000); pg.wait_for_timeout(700)
    pg.locator("xpath=//*[contains(@class,'tv-link') and normalize-space(text())='Create Calculation']").first.click(); wa(pg)
    pg.locator(cell('nav:form:G:0:R:1:C:0:da_input')).click(); pg.locator(cell('nav:form:G:0:R:1:C:0:da_input')).fill(START); pg.keyboard.press('Tab'); pg.wait_for_timeout(800)
    pg.locator(cell('nav:form:G:1:R:1:C:0:dd_button')).click(); pg.wait_for_timeout(1000)
    pg.locator("xpath=//*[@id='nav:form:G:1:R:1:C:0:dd_panel']//tr[normalize-space(@data-item-label)='Production Allocation']").first.click(); wa(pg)
    pg.locator(cell('button:form:B')).click(); wa(pg)
    pg.locator(f"xpath=//*[@id='calculation:form:T_data']//input[@value='{DONOR}']").first.click(); pg.wait_for_timeout(1000)
    pg.locator("xpath=//a[contains(@title,'Create a new calculation as a copy')] | //button[contains(@title,'Create a new calculation as a copy')]").first.click(); pg.wait_for_timeout(2000)
    pg.locator(cell('copyCalculationForm:form:G:0:R:0:C:1:in')).fill(CODE)
    pg.locator(cell('copyCalculationForm:form:G:0:R:0:C:3:in')).fill(NAME)
    sd=cell('copyCalculationForm:form:G:0:R:0:C:5:da_input')
    pg.locator(sd).click(); pg.locator(sd).fill(START); pg.keyboard.press('Tab'); pg.wait_for_timeout(600)
    cand=pg.evaluate("""()=>[...document.querySelectorAll('button,a,input[type=submit]')].filter(e=>/copy to new/i.test(e.textContent||e.value||'')).map(e=>({tag:e.tagName,id:e.id,txt:((e.textContent||e.value||'').trim()).slice(0,30)}))""")
    print("copy-button candidates:",cand)
    clicked=False
    try:
        pg.get_by_role("button", name=re.compile("copy to new", re.I)).first.click(timeout=8000); clicked=True
    except Exception as e:
        print("role click failed:",str(e)[:60])
        if cand and cand[0]['id']:
            pg.locator(cell(cand[0]['id'])).click(); clicked=True
    print("clicked:",clicked); wa(pg)
    pg.screenshot(path=os.path.join(SS,'build_05_after_copy_to_new.png'))
    err=pg.evaluate("""()=>{const n=document.getElementById('ECNotificationArea')||document.getElementById('ECClientNotificationArea');return n?n.textContent.trim().slice(0,200):'';}""")
    print("notification:",err or '(none)')
    b.close()
