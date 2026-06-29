"""SCAN (READ-ONLY): dump the full element structure of the EQUATIONS grid for AUTOTEST_CALC_TEST +
the edit trigger (how the equation-editor popup opens). No save."""
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
    eqtab=pg.locator("xpath=//a[normalize-space(.)='Equations']"); 
    if eqtab.count()>0: eqtab.first.click(); wa(pg)
    # dump EVERY element inside the equations grid tbody
    dump=pg.evaluate("""()=>{
      const tb=document.getElementById('maintab:tabPanel:equations:form:T_data'); if(!tb) return {err:'no tbody'};
      const els=[...tb.querySelectorAll('*')].filter(e=>e.id||e.tagName==='INPUT'||e.tagName==='TEXTAREA'||(e.onclick||e.getAttribute('onclick'))||/_in$|_input$|edit/i.test(e.id||''))
        .map(e=>({tag:e.tagName, id:e.id||'', cls:(e.className&&e.className.toString?e.className.toString():'').slice(0,30), val:(e.value||e.textContent||'').trim().slice(0,40), click:!!(e.onclick||e.getAttribute('onclick'))})).slice(0,25);
      return {rowText: tb.innerText.replace(/\s+/g,' ').trim().slice(0,120), els};
    }""")
    print("equation row text:", dump.get('rowText'))
    print("elements in equations grid:")
    for e in dump.get('els',[]): print("   ",e)
    # also: toolbar edit/+ on equations tab + any equation-editor popup elements present
    extra=pg.evaluate("""()=>({editbtns:[...document.querySelectorAll("[id*='equations'] a[title], [id*='equations'] button[title]")].map(e=>({id:e.id,t:e.getAttribute('title')})).filter(x=>x.t).slice(0,8)})""")
    print("equations-tab action buttons:",extra['editbtns'])
    b.close()
