"""B-Step2: edit AUTOTEST_CALC_TEST's equation to INFO='AUTOTEST simple calc'. Open C5_b editor, SCAN the
popup, and only act on a clearly-identified editable + OK (else ABORT, no guessing). Headed."""
from playwright.sync_api import sync_playwright
import os, re
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
    # open the Equation (C5) editor
    pg.locator(cell('maintab:tabPanel:equations:form:T:0:C5_b')).click(); pg.wait_for_timeout(1800)
    pg.screenshot(path=os.path.join(SS,'buildB_03_eq_editor.png'))
    # SCAN the popup: visible textarea / contenteditable / text input + OK button
    sc=pg.evaluate("""()=>{
      const editable=[...document.querySelectorAll("textarea, [contenteditable='true'], input[type='text']")].filter(e=>e.offsetParent!==null).map(e=>({tag:e.tagName,id:e.id,cls:(e.className||'').slice(0,25),val:(e.value||e.textContent||'').slice(0,50)}));
      const oks=[...document.querySelectorAll("button,a")].filter(e=>e.offsetParent!==null && /^ok$/i.test((e.textContent||'').trim())).map(e=>e.id||e.textContent.trim());
      return {editable, oks};
    }""")
    print("popup editable candidates:",sc['editable'])
    print("popup OK buttons:",sc['oks'])
    # act only if there is a clearly editable target (a textarea or contenteditable) + an OK
    cand=[e for e in sc['editable'] if e['tag'] in ('TEXTAREA',) or "edit" in e['cls'].lower() or e['val'].strip().upper().startswith('INFO')]
    if len(cand)>=1 and sc['oks']:
        tgt=cand[0]
        loc=pg.locator(cell(tgt['id'])) if tgt['id'] else pg.locator("textarea:visible").first
        loc.click(); pg.keyboard.press('Control+a'); pg.keyboard.press('Delete'); loc.type(EQ, delay=20); pg.wait_for_timeout(400)
        pg.get_by_role("button", name=re.compile(r"^ok$", re.I)).first.click(); wa(pg)
        # Save the screen
        sv=pg.locator("xpath=//a[@title='Save [Ctrl+s]' and not(contains(@class,'ui-state-disabled'))]")
        if sv.count()>0: sv.first.click()
        else: pg.keyboard.press('Control+s')
        wa(pg); pg.screenshot(path=os.path.join(SS,'buildB_04_eq_saved.png'))
        print("RESULT: equation set + saved")
    else:
        print("ABORT: equation-editor editable/OK not unambiguously identified -> not typing (no guessing).")
        pg.screenshot(path=os.path.join(SS,'buildB_03b_eq_editor_unclear.png'))
    if HEADED: pg.wait_for_timeout(2500)
    b.close()
