"""SCAN-FIRST (READ-ONLY + one safe +click): Create Calculation toolbar + button + new-row cell structure
(incl. how Period/Type are edited). Unsaved row is discarded -> safe."""
from playwright.sync_api import sync_playwright
import os, json
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
    pg.locator(cell('nav:form:G:0:R:1:C:0:da_input')).click(); pg.locator(cell('nav:form:G:0:R:1:C:0:da_input')).fill('2003-01-01'); pg.keyboard.press('Tab'); pg.wait_for_timeout(700)
    pg.locator(cell('nav:form:G:1:R:1:C:0:dd_button')).click(); pg.wait_for_timeout(900)
    pg.locator("xpath=//*[@id='nav:form:G:1:R:1:C:0:dd_panel']//tr[normalize-space(@data-item-label)='Production Allocation']").first.click(); wa(pg)
    pg.locator(cell('button:form:B')).click(); wa(pg)
    # 1) SCAN toolbar (find the + / Insert) - dump every clickable toolbar element near top
    tb=pg.evaluate("""()=>[...document.querySelectorAll("div[id*='Toolbar'] a, div[id*='toolbar'] a, .ui-toolbar a, a.ui-commandlink, a[id], button[id]")].map(e=>{
        const ic=e.querySelector("span[class*='ui-icon']"); const r=e.getBoundingClientRect();
        return {id:e.id, title:e.getAttribute('title')||'', icon: ic?ic.className.replace('ui-icon ',''):'', y:Math.round(r.y)};
      }).filter(o=>o.y<110 && o.y>40 && (o.title||o.icon||o.id)).slice(0,16)""")
    print("TOOLBAR (top row):"); [print("   ",t) for t in tb]
    # find insert-ish (title or icon contains plus/insert/add/new)
    ins=[t for t in tb if re.search('insert|plus|add|new',(t['title']+' '+t['icon']).lower())] if (re:=__import__('re')) else []
    print("INSERT candidate:",ins[:3])
    if ins:
        pg.locator(cell(ins[0]['id'])).click() if ins[0]['id'] else None
    pg.wait_for_timeout(1500)
    # 2) SCAN new row: top row cells + whether Period/Type are dropdown-editable
    row=pg.evaluate("""()=>{
       const out=[];
       for(let c=0;c<6;c++){
         const e=document.getElementById(`calculation:form:T:0:C${c}_in`)||document.getElementById(`calculation:form:T:0:C${c}_da_input`);
         out.push({c, id:e?e.id:'(none)', val:e?(e.value||''):'', ro:e?e.readOnly:null, tag:e?e.tagName:''});
       }
       return out;
    }""")
    print("NEW ROW 0 cells:"); [print("   ",r) for r in row]
    b.close()
