"""READ-ONLY full scan of the Daily Allocation run panel: dump the exact DOM subtree around the 'Simulate'
label so we identify the real checkbox element. No clicks on Run/Simulate."""
from playwright.sync_api import sync_playwright
import os, json
EC_URL=os.environ.get('EC_URL','https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/')
def wa(pg,t=22000): pg.wait_for_load_state('networkidle',timeout=t); pg.wait_for_timeout(1300)
def cell(s): return '#'+s.replace(':',r'\:')
def pick(pg,pfx,label):
    pg.locator(cell(pfx+'_button')).click(); pg.wait_for_timeout(900)
    pg.locator(f"xpath=//*[@id='{pfx}_panel']//tr[normalize-space(@data-item-label)='{label}']").first.click(); wa(pg)
with sync_playwright() as p:
    b=p.chromium.launch(headless=True,args=['--ignore-certificate-errors'])
    pg=b.new_context(ignore_https_errors=True,viewport={'width':1920,'height':1080}).new_page()
    pg.goto(EC_URL,wait_until='domcontentloaded',timeout=30000)
    pg.fill('#username','sysadmin'); pg.fill('#password','sysadmin'); pg.click('#kc-login')
    pg.wait_for_url('**/dashboard**',timeout=60000); wa(pg)
    si=pg.locator(r'#menu\:searchForm\:searchTxt'); si.wait_for(state='visible',timeout=10000)
    si.clear(); si.type('Daily Allocation',delay=50); pg.wait_for_load_state('networkidle',timeout=8000); pg.wait_for_timeout(700)
    pg.locator("xpath=//*[contains(@class,'tv-link') and normalize-space(text())='Daily Allocation']").first.click(); wa(pg)
    pg.locator(cell('nav:form:G:1:R:1:C:0:da_input')).click(); pg.locator(cell('nav:form:G:1:R:1:C:0:da_input')).fill('2026-06-27'); pg.keyboard.press('Tab'); pg.wait_for_timeout(700)
    pick(pg,'nav:form:G:2:R:1:C:0:dd','P1 Day Allocation'); pick(pg,'nav:form:G:4:R:1:C:0:dd','Calculation Test')
    pg.locator(cell('button:form:B')).click(); wa(pg)
    dump=pg.evaluate("""()=>{
      const lab=[...document.querySelectorAll('*')].find(e=>e.children.length===0 && e.textContent.trim()==='Simulate');
      if(!lab) return {err:'no Simulate label found'};
      // walk up to a container that also contains 'Run Calculation' (the run-control row)
      let cont=lab;
      for(let i=0;i<6;i++){ cont=cont.parentElement; if(cont && /run calculation/i.test(cont.textContent||'')) break; }
      const desc=[...cont.querySelectorAll('*')].map(e=>{
        const r=e.getBoundingClientRect();
        return {tag:e.tagName, id:e.id||'', cls:(e.className&&e.className.toString?e.className.toString():'').slice(0,45),
                type:e.getAttribute('type')||'', onclick: e.hasAttribute('onclick')||!!e.onclick,
                role:e.getAttribute('role')||'', vis:e.offsetParent!==null, x:Math.round(r.x), y:Math.round(r.y), w:Math.round(r.width), h:Math.round(r.height)};
      }).filter(o=> (o.vis && o.w>0 && o.w<60 && o.h>0 && o.h<60) || /chk|check|cb|bool|sim/i.test(o.id+o.cls+o.type));
      return {labelTag:lab.tagName, labelId:lab.id, container:cont.id||cont.tagName, candidates:desc.slice(0,30)};
    }""")
    print(json.dumps(dump, indent=1)[:3500])
    b.close()
