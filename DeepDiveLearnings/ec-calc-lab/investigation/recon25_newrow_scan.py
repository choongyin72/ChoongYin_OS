"""SCAN-FIRST: click the + (a > span.ui-icon-insert), then scan the NEW blank row's editable cells +
how Period/Type are chosen. Unsaved -> safe."""
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
    si.clear(); si.type('Create Calculation',delay=50); pg.wait_for_load_state('networkidle',timeout=8000); pg.wait_for_timeout(700)
    pg.locator("xpath=//*[contains(@class,'tv-link') and normalize-space(text())='Create Calculation']").first.click(); wa(pg)
    pg.locator(cell('nav:form:G:0:R:1:C:0:da_input')).click(); pg.locator(cell('nav:form:G:0:R:1:C:0:da_input')).fill('2003-01-01'); pg.keyboard.press('Tab'); pg.wait_for_timeout(700)
    pg.locator(cell('nav:form:G:1:R:1:C:0:dd_button')).click(); pg.wait_for_timeout(900)
    pg.locator("xpath=//*[@id='nav:form:G:1:R:1:C:0:dd_panel']//tr[normalize-space(@data-item-label)='Production Allocation']").first.click(); wa(pg)
    pg.locator(cell('button:form:B')).click(); wa(pg)
    # click the + insert (icon class)
    ins=pg.locator("xpath=//a[.//span[contains(@class,'ui-icon-insert')]]")
    print("insert button count:",ins.count())
    ins.first.click(); pg.wait_for_timeout(1800)
    pg.screenshot(path=os.path.join(SS,'build_15_newrow.png'))
    # find the blank row (empty C0) + dump its cells incl readOnly + any dd_button/select in C4/C5
    res=pg.evaluate("""()=>{
      const rows=[];
      for(let r=0;r<3;r++){
        const c0=document.getElementById(`calculation:form:T:${r}:C0_in`);
        const cells=[];
        for(let c=0;c<6;c++){
          const e=document.getElementById(`calculation:form:T:${r}:C${c}_in`)||document.getElementById(`calculation:form:T:${r}:C${c}_da_input`);
          // is there a dropdown button/select for this cell?
          const dd=document.getElementById(`calculation:form:T:${r}:C${c}:dd_button`)||document.querySelector(`[id^='calculation:form:T:${r}:C${c}'][id$='dd_button']`);
          cells.push({c, val:e?(e.value||''):'(none)', ro:e?e.readOnly:null, dd: !!dd, ddid: dd?dd.id:''});
        }
        rows.push({r, c0val:c0?c0.value:'(none)', cells});
      }
      return rows;
    }""")
    for row in res:
        print(f"ROW {row['r']} (C0='{row['c0val']}'):")
        for c in row['cells']: print("    ",c)
    b.close()
