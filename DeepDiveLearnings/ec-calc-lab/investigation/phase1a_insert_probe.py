"""Probe the INSERT gesture on Simple Object Types: after clicking the insert anchor, dump the
VISIBLE menu items (text+id) so I can click the correct one. Then click it and re-count rows. No save."""
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
    # all ui-icon-insert anchors with detail
    ins=fr.evaluate("""()=>[...document.querySelectorAll("a")].filter(a=>a.querySelector("span[class*='ui-icon-insert']")).map(a=>{
        const r=a.getBoundingClientRect(); return {id:a.id, title:a.getAttribute('title')||'', vis:r.width>0&&r.height>0, y:Math.round(r.y), onclick:(a.getAttribute('onclick')||'').slice(0,40)};})""")
    print("INSERT anchors:", ins)
    a=fr.locator("xpath=//a[.//span[contains(@class,'ui-icon-insert')]]").first
    a.scroll_into_view_if_needed(); a.hover(); pg.wait_for_timeout(500); a.click(); pg.wait_for_timeout(1000)
    vis=fr.evaluate("""()=>{const out=[];document.querySelectorAll("ul.ui-menu,div.ui-menu,.ui-menu-list,.ui-overlaypanel").forEach(m=>{
        const st=getComputedStyle(m); if(st.display==='none'||st.visibility==='hidden')return;
        m.querySelectorAll("a.ui-menuitem-link,.ui-menuitem-text").forEach(it=>{const r=it.getBoundingClientRect(); if(r.width>0)out.push({t:it.innerText.trim(),id:it.id||(it.closest('a')?it.closest('a').id:'')});});});
        return out.slice(0,15);}""")
    print("VISIBLE menu items after insert click:", vis)
    n=fr.evaluate("(g)=>document.querySelectorAll(`[id='${g}_data'] tr`).length", G)
    print("rows now:", n)
    b.close()
print("DONE insert probe")
