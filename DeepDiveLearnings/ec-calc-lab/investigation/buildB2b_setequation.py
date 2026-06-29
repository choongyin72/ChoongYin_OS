"""B-Step2 (act): set AUTOTEST_CALC_TEST equation to INFO='AUTOTEST simple calc'. Editable = the contenteditable
inside mathEqEditor:mathEqDialog_content; OK = exact id mathEqEditor:form:ok. Guard: abort if editable not found."""
from playwright.sync_api import sync_playwright
import os
EC_URL=os.environ.get('EC_URL','https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/')
SS=os.path.join(os.path.dirname(__file__),'..','evidence'); HEADED=os.environ.get('EC_HEADED','1')=='1'
def wa(pg,t=20000): pg.wait_for_load_state('networkidle',timeout=t); pg.wait_for_timeout(1200)
def cell(s): return '#'+s.replace(':',r'\:')
EQ="INFO = 'AUTOTEST simple calc'"
with sync_playwright() as p:
    b=p.chromium.launch(headless=not HEADED, slow_mo=250 if HEADED else 0, args=['--ignore-certificate-errors','--start-maximized'])
    pg=b.new_context(ignore_https_errors=True, no_viewport=HEADED, viewport=None if HEADED else {'width':1920,'height':1080}).new_page()
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
    pg.locator(cell('maintab:tabPanel:equations:form:T:0:C5_b')).click(); pg.wait_for_timeout(2000)
    # find the editable surface in the dialog content
    ed=pg.evaluate("""()=>{
      const d=document.getElementById('mathEqEditor:mathEqDialog_content'); if(!d) return {err:'no dialog content'};
      const ce=[...d.querySelectorAll("[contenteditable='true'], textarea, input[type='text']")].filter(e=>e.offsetParent!==null);
      return {found: ce.map(e=>({tag:e.tagName,id:e.id||'',cls:(e.className||'').slice(0,25)}))};
    }""")
    print("editable in dialog:",ed)
    cand=ed.get('found',[])
    if not cand:
        print("ABORT: no editable surface found in math dialog -> not typing (no guessing).")
        pg.screenshot(path=os.path.join(SS,'buildB_03b_unclear.png'))
        if HEADED: pg.wait_for_timeout(2500)
        b.close(); raise SystemExit
    # click the editable (first), select-all, delete, type
    loc = pg.locator(cell(cand[0]['id'])) if cand[0]['id'] else pg.locator("#mathEqEditor\:mathEqDialog_content [contenteditable='true']").first
    loc.click(); pg.wait_for_timeout(300)
    pg.keyboard.press('Control+a'); pg.keyboard.press('Delete'); pg.wait_for_timeout(200)
    pg.keyboard.type(EQ, delay=25); pg.wait_for_timeout(400)
    pg.screenshot(path=os.path.join(SS,'buildB_03c_typed.png'))
    pg.locator(cell('mathEqEditor:form:ok')).click(); wa(pg)   # exact OK inside the dialog
    sv=pg.locator("xpath=//a[@title='Save [Ctrl+s]' and not(contains(@class,'ui-state-disabled'))]")
    if sv.count()>0: sv.first.click()
    else: pg.keyboard.press('Control+s')
    wa(pg); pg.screenshot(path=os.path.join(SS,'buildB_04_eq_saved.png'))
    print("RESULT: equation typed + OK + saved")
    if HEADED: pg.wait_for_timeout(2500)
    b.close()
