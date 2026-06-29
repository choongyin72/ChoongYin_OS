"""SCAN (HEADED, read-only): select P1_DAY_ALLOC -> dump VISIBLE tab headers -> click visible 'Calculation Job'
tab -> dump job grid + insert(+) + Calculation Job dd. No add/save."""
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
    # dump VISIBLE tab headers (with ids) to find 'Calculation Job'
    tabs=pg.evaluate("""()=>[...document.querySelectorAll("a")].filter(e=>e.offsetParent!==null && /^(Calculation Job|Members List|Dependent Calculation Jobs)$/.test((e.textContent||'').trim())).map(e=>({id:e.id, t:(e.textContent||'').trim(), role:e.getAttribute('role')||''}))""")
    print("visible tab links:",tabs)
    cj=[t for t in tabs if t['t']=='Calculation Job']
    if not cj: print("ABORT: visible 'Calculation Job' tab not found"); 
    else:
        (pg.locator(cell(cj[0]['id'])) if cj[0]['id'] else pg.get_by_role('tab', name='Calculation Job')).first.click(); wa(pg)
        pg.screenshot(path=os.path.join(SS,'buildB_06_jobtab.png'))
        j=pg.evaluate("""()=>{
          const tbs=[...document.querySelectorAll("tbody[id$='_data']")].filter(t=>t.offsetParent!==null && (/calculation test|daily well/i.test(t.innerText)||/job/i.test(t.id))).map(t=>({id:t.id,txt:t.innerText.replace(/\s+/g,' ').slice(0,70)}));
          const dds=[...document.querySelectorAll("[id$='dd_button']")].filter(e=>e.offsetParent!==null && !e.id.startsWith('nav')).map(e=>e.id).slice(0,10);
          return {tbs, dds};
        }""")
        print("job grids:",j['tbs']); print("dd_buttons:",j['dds'])
    if HEADED: pg.wait_for_timeout(4000)
    b.close()
