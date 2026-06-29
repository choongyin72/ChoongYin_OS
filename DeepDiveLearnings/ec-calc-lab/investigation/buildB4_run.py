"""B-Step4 (HEADED): Simulate-run AUTOTEST_CALC_TEST via Daily Allocation. Proven ids. Also verifies Step 3
(if 'AUTOTEST Calc Test' is NOT in the Calculation Job dd -> Step 3 didn't persist). Simulate guard kept."""
from playwright.sync_api import sync_playwright
import os, re
EC_URL=os.environ.get('EC_URL','https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/')
SS=os.path.join(os.path.dirname(__file__),'..','evidence'); HEADED=os.environ.get('EC_HEADED','1')=='1'
def wa(pg,t=25000): pg.wait_for_load_state('networkidle',timeout=t); pg.wait_for_timeout(1400)
def cell(s): return '#'+s.replace(':',r'\:')
SIM='dateStartJob:form:G:0:R:1:C:2:cb'; LOG='dateStartJob:form:G:0:R:1:C:1:dd'
with sync_playwright() as p:
    b=p.chromium.launch(headless=not HEADED, slow_mo=250 if HEADED else 0, args=['--ignore-certificate-errors','--start-maximized'])
    pg=b.new_context(ignore_https_errors=True, no_viewport=HEADED, viewport=None if HEADED else {'width':1920,'height':1080}).new_page()
    pg.goto(EC_URL,wait_until='domcontentloaded',timeout=30000)
    pg.fill('#username','sysadmin'); pg.fill('#password','sysadmin'); pg.click('#kc-login')
    pg.wait_for_url('**/dashboard**',timeout=60000); wa(pg)
    si=pg.locator(r'#menu\:searchForm\:searchTxt'); si.wait_for(state='visible',timeout=10000)
    si.clear(); si.type('Daily Allocation',delay=50); pg.wait_for_load_state('networkidle',timeout=8000); pg.wait_for_timeout(700)
    pg.locator("xpath=//*[contains(@class,'tv-link') and normalize-space(text())='Daily Allocation']").first.click(); wa(pg)
    pg.locator(cell('nav:form:G:1:R:1:C:0:da_input')).click(); pg.locator(cell('nav:form:G:1:R:1:C:0:da_input')).fill('2026-06-27'); pg.keyboard.press('Tab'); pg.wait_for_timeout(700)
    pg.locator(cell('nav:form:G:2:R:1:C:0:dd_button')).click(); pg.wait_for_timeout(900)
    pg.locator("xpath=//*[@id='nav:form:G:2:R:1:C:0:dd_panel']//tr[normalize-space(@data-item-label)='P1 Day Allocation']").first.click(); wa(pg)
    # Calculation Job dd (G:4): scan options for AUTOTEST (verifies Step 3) then pick
    pg.locator(cell('nav:form:G:4:R:1:C:0:dd_button')).click(); pg.wait_for_timeout(1000)
    jobopts=pg.evaluate("""()=>[...document.querySelectorAll("[id='nav:form:G:4:R:1:C:0:dd_panel'] tr")].map(t=>t.getAttribute('data-item-label')).filter(x=>x&&/autotest/i.test(x))""")
    print("Calc Job dd AUTOTEST options (Step-3 proof):", jobopts)
    if not jobopts:
        print("=> STEP 3 NOT PERSISTED: 'AUTOTEST Calc Test' is NOT a connected job on P1_DAY_ALLOC. Stopping.")
        if HEADED: pg.wait_for_timeout(3000)
        b.close(); raise SystemExit
    pg.locator(f"xpath=//*[@id='nav:form:G:4:R:1:C:0:dd_panel']//tr[normalize-space(@data-item-label)='{jobopts[0]}']").first.click(); wa(pg)
    pg.locator(cell('button:form:B')).click(); wa(pg)
    # Log Level Full + Simulate (proven ids)
    try:
        pg.locator(cell(LOG+'_button')).click(); pg.wait_for_timeout(800)
        pg.locator(f"xpath=//*[@id='{LOG}_panel']//tr[normalize-space(@data-item-label)='Full']").first.click(); wa(pg)
    except Exception as e: print("loglevel note",str(e)[:40])
    pg.locator(cell(SIM)).check()
    pg.evaluate("(id)=>{const e=document.getElementById(id);if(e){e.dispatchEvent(new Event('change',{bubbles:true}));}}", SIM); pg.wait_for_timeout(600)
    ticked=pg.evaluate("(id)=>{const e=document.getElementById(id);return e?e.checked:null;}", SIM)
    print("Simulate ticked:",ticked)
    if not ticked: print("ABORT: Simulate not ticked -> not running."); b.close(); raise SystemExit
    pg.get_by_role("button", name=re.compile("run calc", re.I)).first.click(); pg.wait_for_timeout(2500)
    ok=pg.get_by_role("button", name=re.compile(r"^ok$", re.I))
    if ok.count()>0 and ok.first.is_visible(): ok.first.click(); print("OK clicked"); wa(pg)
    pg.wait_for_timeout(8000); pg.locator(cell('button:form:B')).click(); wa(pg); pg.wait_for_timeout(2000)
    pg.screenshot(path=os.path.join(SS,'buildB_10_run.png'))
    body=pg.evaluate("()=>document.body.innerText")
    print("LOG 'Simulate Success':", 'simulate success' in body.lower())
    print("LOG shows calc output ('Test:' from my eqn):", 'test:' in body.lower())
    if HEADED: pg.wait_for_timeout(4000)
    b.close()
