"""READ-ONLY: confirm the Create Calculation grid cell map (C0-C5) by reading a KNOWN row's cell values."""
from playwright.sync_api import sync_playwright
import os
EC_URL=os.environ.get('EC_URL','https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/')
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
    pg.locator(cell('nav:form:G:0:R:1:C:0:da_input')).click(); pg.locator(cell('nav:form:G:0:R:1:C:0:da_input')).fill('2003-01-01'); pg.keyboard.press('Tab'); pg.wait_for_timeout(800)
    pg.locator(cell('nav:form:G:1:R:1:C:0:dd_button')).click(); pg.wait_for_timeout(1000)
    pg.locator("xpath=//*[@id='nav:form:G:1:R:1:C:0:dd_panel']//tr[normalize-space(@data-item-label)='Production Allocation']").first.click(); wa(pg)
    pg.locator(cell('button:form:B')).click(); wa(pg)
    # for each grid row, read C0..C5 values (input value or text)
    rows=pg.evaluate("""()=>{
      const out=[];
      for(let r=0;r<6;r++){
        const v=[];
        for(let cc=0; cc<6; cc++){
          const e=document.getElementById(`calculation:form:T:${r}:C${cc}_in`)||document.getElementById(`calculation:form:T:${r}:C${cc}_da_input`);
          v.push(e? (e.value||e.textContent||'').trim() : '(none)');
        }
        out.push(v);
      }
      return out;
    }""")
    print("ROW : C0 | C1 | C2 | C3 | C4 | C5")
    for i,v in enumerate(rows): print(f"  {i}: "+" | ".join(x[:18] for x in v))
    b.close()
