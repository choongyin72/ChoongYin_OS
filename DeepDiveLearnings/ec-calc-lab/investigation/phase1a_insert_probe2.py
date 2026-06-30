"""Probe2: hover the insert toolbar anchor and capture the flyout submenu labels (the insert
sub-items). Dump every visible anchor/menuitem with text in the toolbar band. No save."""
from playwright.sync_api import sync_playwright
import os
EC_URL=os.environ.get('EC_URL','https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/')
def wa(pg,t=20000): pg.wait_for_load_state('networkidle',timeout=t); pg.wait_for_timeout(900)
def cell(s): return '#'+s.replace(':',r'\:')
G='tab:tabPanel:spObjectType:form:T'
with sync_playwright() as p:
    b=p.chromium.launch(headless=True,args=['--ignore-certificate-errors'])
    pg=b.new_context(ignore_https_errors=True,viewport={'width':1920,'height':1080}).new_page()
    pg.goto(EC_URL,wait_until='domcontentloaded',timeout=30000)
    pg.fill('#username','sysadmin'); pg.fill('#password','sysadmin'); pg.click('#kc-login')
    pg.wait_for_url('**/dashboard**',timeout=60000); wa(pg)
    si=pg.locator(r'#menu\:searchForm\:searchTxt'); si.wait_for(state='visible',timeout=10000)
    si.clear(); si.type('Simple Object Types',delay=40); pg.wait_for_timeout(900)
    pg.locator("xpath=//*[contains(@class,'tv-link') and normalize-space(text())='Simple Object Types']").first.click(); wa(pg)
    fr=[f for f in pg.frames if 'simple_predefined' in f.url.lower()][0]
    fr.locator(cell('nav:form:G:0:R:1:C:0:da_input')).fill('2003-01-01'); fr.locator('body').press('Tab'); pg.wait_for_timeout(500)
    fr.locator(cell('nav:form:G:1:R:1:C:0:dd_button')).click(); pg.wait_for_timeout(800)
    fr.locator("xpath=//*[@id='nav:form:G:1:R:1:C:0:dd_panel']//tr[normalize-space(@data-item-label)='Production Allocation']").first.click(timeout=8000); pg.wait_for_timeout(400)
    fr.locator(cell('button:form:B')).click(); wa(pg)
    # dump the whole toolbar band (y 40-70): all anchors with their icon + id + onclick
    band=fr.evaluate("""()=>[...document.querySelectorAll("a,button")].map(e=>{const r=e.getBoundingClientRect();
        const ic=e.querySelector("span[class*='ui-icon-']"); const cl=ic?[...ic.classList].find(c=>c.startsWith('ui-icon-')):'';
        return {x:Math.round(r.x),y:Math.round(r.y),icon:cl||'',id:e.id||'',title:(e.getAttribute('title')||'').slice(0,20),txt:(e.innerText||'').trim().slice(0,18)};})
        .filter(o=>o.y>=40&&o.y<=72&&(o.icon||o.title||o.txt))""")
    print("TOOLBAR BAND:"); [print("   ",o) for o in band]
    a=fr.locator("xpath=//a[.//span[contains(@class,'ui-icon-insert')]]").first
    a.scroll_into_view_if_needed(); a.hover(); pg.wait_for_timeout(1200)
    # after hover, dump any newly visible menuitem flyout anywhere in doc
    fly=fr.evaluate("""()=>{const out=[];document.querySelectorAll("a.ui-menuitem-link,li.ui-menuitem").forEach(it=>{
        const r=it.getBoundingClientRect(); const st=getComputedStyle(it);
        if(r.width>0&&r.height>0&&st.visibility!=='hidden'){out.push({t:it.innerText.trim().slice(0,30),id:it.id||'',y:Math.round(r.y)});}});
        return out.filter(o=>o.t).slice(0,20);}""")
    print("FLYOUT after hover:", fly)
    b.close()
print("DONE probe2")
