"""SCAN (READ-ONLY): dump the math-equation editor dialog (mathEqEditor:mathEqDialog) internals -
the editable element + its OK/CANCEL buttons. No save."""
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
    pg.locator(cell('maintab:tabPanel:equations:form:T:0:C5_b')).click(); pg.wait_for_timeout(2000)
    dump=pg.evaluate("""()=>{
      const d=document.getElementById('mathEqEditor:mathEqDialog'); if(!d) return {err:'mathEqDialog not found'};
      const inner=[...d.querySelectorAll('[id]')].map(e=>({tag:e.tagName,id:e.id,cls:(e.className&&e.className.toString?e.className.toString():'').slice(0,26),txt:(e.value||e.textContent||'').trim().slice(0,40),vis:e.offsetParent!==null,ce:e.getAttribute('contenteditable')}))
        .filter(o=>o.tag in {INPUT:1,TEXTAREA:1,BUTTON:1,A:1,DIV:1} && (o.vis|| o.tag==='INPUT'))
        .filter(o=>o.tag!=='DIV' || /edit|input|content|field/i.test(o.cls) || o.ce==='true').slice(0,25);
      const btns=[...d.querySelectorAll('button,a')].filter(e=>e.offsetParent!==null && (e.textContent||'').trim()).map(e=>({id:e.id,t:(e.textContent||'').trim().slice(0,15)})).slice(0,10);
      return {inner, btns};
    }""")
    if dump.get('err'): print(dump['err'])
    else:
        print("mathEqDialog editable/field elements:")
        for e in dump['inner']: print("   ",e)
        print("mathEqDialog buttons:",dump['btns'])
    pg.screenshot(path=os.path.join(SS,'buildB_03_eq_editor.png'))
    b.close()
