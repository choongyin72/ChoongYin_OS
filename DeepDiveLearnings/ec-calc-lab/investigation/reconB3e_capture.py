"""HEADED capture: select P1_DAY_ALLOC, screenshot the tab/menu area so we locate 'Calculation Job'. Holds open."""
from playwright.sync_api import sync_playwright
import os
EC_URL=os.environ.get('EC_URL','https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/')
SS=os.path.join(os.path.dirname(__file__),'..','evidence'); HEADED=os.environ.get('EC_HEADED','1')=='1'
def wa(pg,t=20000): pg.wait_for_load_state('networkidle',timeout=t); pg.wait_for_timeout(1200)
def cell(s): return '#'+s.replace(':',r'\:')
with sync_playwright() as p:
    b=p.chromium.launch(headless=not HEADED, slow_mo=300 if HEADED else 0, args=['--ignore-certificate-errors','--start-maximized'])
    pg=b.new_context(ignore_https_errors=True, no_viewport=HEADED, viewport=None if HEADED else {'width':1920,'height':1080}).new_page()
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
    pg.screenshot(path=os.path.join(SS,'buildB_07_after_select.png'), full_page=True)
    # also dump ALL elements whose text contains 'Calculation Job' (any tag) + visible
    cj=pg.evaluate("""()=>[...document.querySelectorAll('*')].filter(e=>e.children.length<=1 && /^Calculation Job$/.test((e.textContent||'').trim())).map(e=>({tag:e.tagName,id:e.id||'',role:e.getAttribute('role')||'',vis:e.offsetParent!==null,cls:(e.className&&e.className.toString?e.className.toString():'').slice(0,30)}))""")
    print("'Calculation Job' text elements:",cj)
    if HEADED: pg.wait_for_timeout(7000)
    b.close()
