"""Diagnostic (READ-ONLY): identify the actual Simulate checkbox element on Daily Allocation. No run."""
from playwright.sync_api import sync_playwright
import os
EC_URL=os.environ.get('EC_URL','https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/')
SS=os.path.join(os.path.dirname(__file__),'..','evidence')
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
    info=pg.evaluate("""()=>{
      const out={};
      // 'Simulate' label rect
      const lab=[...document.querySelectorAll('*')].find(e=>e.children.length===0 && e.textContent.trim()==='Simulate');
      out.label = lab? {x:Math.round(lab.getBoundingClientRect().x), y:Math.round(lab.getBoundingClientRect().y)} : null;
      // ALL input[type=checkbox]
      out.checkboxes=[...document.querySelectorAll("input[type='checkbox']")].map(e=>{const r=e.getBoundingClientRect();return {id:e.id, cls:(e.className||'').slice(0,30), vis:e.offsetParent!==null, checked:e.checked, x:Math.round(r.x),y:Math.round(r.y)};}).slice(0,15);
      // anything with chkbox/checkbox in class, near label y
      out.chk=[...document.querySelectorAll("[class*='chkbox'],[class*='checkbox']")].map(e=>{const r=e.getBoundingClientRect();return {tag:e.tagName,id:e.id,cls:(e.className||'').slice(0,40),vis:e.offsetParent!==null,x:Math.round(r.x),y:Math.round(r.y)};}).filter(o=>out.label && Math.abs(o.y-out.label.y)<60).slice(0,12);
      return out;
    }""")
    print("Simulate label at:",info['label'])
    print("input[type=checkbox] (all):")
    for c in info['checkboxes']: print("   ",c)
    print("chkbox/checkbox-class elems near label:")
    for c in info['chk']: print("   ",c)
    pg.screenshot(path=os.path.join(SS,'build_14_simulate_region.png'))
    b.close()
