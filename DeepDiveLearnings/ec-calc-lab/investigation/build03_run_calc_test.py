"""Prove RUN: Simulate-run 'Calculation Test' via Daily Allocation. Uses EXACT scanned ids:
Log Level dd = dateStartJob:form:G:0:R:1:C:1:dd ; Simulate cb = dateStartJob:form:G:0:R:1:C:2:cb.
SAFETY GUARD: only Run if Simulate cb verified checked. Headed."""
from playwright.sync_api import sync_playwright
import os, re
EC_URL=os.environ.get('EC_URL','https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/')
SS=os.path.join(os.path.dirname(__file__),'..','evidence')
HEADED=os.environ.get('EC_HEADED','1')=='1'
def wa(pg,t=25000): pg.wait_for_load_state('networkidle',timeout=t); pg.wait_for_timeout(1400)
def cell(s): return '#'+s.replace(':',r'\:')
def pick(pg,pfx,label):
    pg.locator(cell(pfx+'_button')).click(); pg.wait_for_timeout(900)
    pg.locator(f"xpath=//*[@id='{pfx}_panel']//tr[normalize-space(@data-item-label)='{label}']").first.click(); wa(pg)
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
    pick(pg,'nav:form:G:2:R:1:C:0:dd','P1 Day Allocation'); pick(pg,'nav:form:G:4:R:1:C:0:dd','Calculation Test')
    pg.locator(cell('button:form:B')).click(); wa(pg)
    # Log Level = Full (exact dd)
    try: pick(pg, LOG, 'Full')
    except Exception as ex: print("loglevel note",str(ex)[:50])
    # Tick Simulate (exact cb input) + dispatch change for EC cell
    cb=pg.locator(cell(SIM))
    print("Simulate cb count:",cb.count())
    cb.check()
    pg.evaluate("""(id)=>{const e=document.getElementById(id); if(e){e.dispatchEvent(new Event('change',{bubbles:true})); e.dispatchEvent(new Event('click',{bubbles:true}));}}""", SIM)
    pg.wait_for_timeout(800)
    ticked = pg.evaluate("(id)=>{const e=document.getElementById(id); return e?e.checked:null;}", SIM)
    print("Simulate checked:", ticked)
    pg.screenshot(path=os.path.join(SS,'build_12_simulate.png'))
    if not ticked:
        print("ABORT: Simulate not confirmed ticked -> NOT running (safe).")
        if HEADED: pg.wait_for_timeout(3000)
        b.close(); raise SystemExit
    print("Simulate CONFIRMED ticked -> safe to Run.")
    run=pg.get_by_role("button", name=re.compile("run calc", re.I)); print("RUN count:",run.count())
    run.first.click(); pg.wait_for_timeout(2500)
    ok=pg.get_by_role("button", name=re.compile(r"^ok$", re.I))
    if ok.count()>0 and ok.first.is_visible(): ok.first.click(); print("OK clicked"); wa(pg)
    pg.wait_for_timeout(8000); pg.locator(cell('button:form:B')).click(); wa(pg); pg.wait_for_timeout(2000)
    pg.screenshot(path=os.path.join(SS,'build_13_myrun_log.png'))
    body=pg.evaluate("()=>document.body.innerText")
    for kw in ['Simulate Success','This is Simple Equation']: print("LOG CONTAINS",kw+":", kw.lower() in body.lower())
    if HEADED: pg.wait_for_timeout(4000)
    b.close()
