"""Diag3: is CLASS READ MAPPING disabled? Try proper row-select (click C0 then Escape to exit edit;
also try clicking the row TD). Dump the readMapping T_data HTML + the menuitem disabled state
before/after clicking. No save. PRE-REQ: Var B1 exists."""
from playwright.sync_api import sync_playwright
import os, re as _re
EC_URL=os.environ.get('EC_URL','https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/')
VAR='AUTOTEST_rCO2Rate'
def wa(pg,t=20000): pg.wait_for_load_state('networkidle',timeout=t); pg.wait_for_timeout(900)
def cell(s): return '#'+s.replace(':',r'\:')
G='variable_definition_table:form:T'; RMD="tab:tabPanel:readMapping:form:T_data"
def grid_html(fr):
    return fr.evaluate("""(g)=>{const t=document.getElementById(g);return t?{trs:t.querySelectorAll('tr').length, html:t.innerHTML.replace(/\\s+/g,' ').slice(0,260)}:null;}""", RMD)
with sync_playwright() as p:
    b=p.chromium.launch(headless=True,args=['--ignore-certificate-errors'])
    pg=b.new_context(ignore_https_errors=True,viewport={'width':1920,'height':1080}).new_page()
    pg.goto(EC_URL,wait_until='domcontentloaded',timeout=30000)
    pg.fill('#username','sysadmin'); pg.fill('#password','sysadmin'); pg.click('#kc-login')
    pg.wait_for_url('**/dashboard**',timeout=60000); wa(pg)
    si=pg.locator(r'#menu\:searchForm\:searchTxt'); si.wait_for(state='visible',timeout=10000)
    si.clear(); si.type('Variable Definitions',delay=40); pg.wait_for_timeout(900)
    pg.locator("xpath=//*[contains(@class,'tv-link') and normalize-space(text())='Variable Definitions']").first.click(); wa(pg)
    fr=[f for f in pg.frames if 'variable_definition' in f.url.lower()][0]
    fr.locator(cell('nav:form:G:0:R:1:C:0:da_input')).fill('2003-01-01'); fr.locator('body').press('Tab'); pg.wait_for_timeout(500)
    fr.locator(cell('nav:form:G:1:R:1:C:0:dd_button')).click(); pg.wait_for_timeout(800)
    fr.locator("xpath=//*[@id='nav:form:G:1:R:1:C:0:dd_panel']//tr[normalize-space(@data-item-label)='Production Allocation']").first.click(timeout=8000); pg.wait_for_timeout(400)
    fr.locator(cell('button:form:B')).click(); wa(pg)
    idx=fr.evaluate("""([g,n])=>{const trs=document.querySelectorAll(`[id='${g}_data'] tr`);
        for(let i=0;i<trs.length;i++){const e=document.getElementById(`${g}:${i}:C0_in`); if(e&&e.value.trim()===n)return i;}return -1;}""", [G, VAR])
    print("var idx:", idx)
    # select: click C0 then Escape to leave edit mode but keep row active
    fr.locator(cell(f'{G}:{idx}:C0_in')).click(); pg.wait_for_timeout(600)
    fr.locator('body').press('Escape'); pg.wait_for_timeout(400)
    # is the row highlighted (selected)?
    selcls=fr.evaluate("""([g,i])=>{const tr=document.querySelectorAll(`[id='${g}_data'] tr`)[i];return tr?tr.className:'';}""", [G, idx])
    print("var row class:", selcls)
    fr.locator("xpath=//a[contains(translate(.,'abcdefghijklmnopqrstuvwxyz','ABCDEFGHIJKLMNOPQRSTUVWXYZ'),'READ MAPPINGS')]").first.click(timeout=5000); pg.wait_for_timeout(1200)
    print("RM grid BEFORE:", grid_html(fr))
    # hover insert, inspect CLASS READ MAPPING menuitem disabled state
    a=fr.locator("xpath=//a[.//span[contains(@class,'ui-icon-insert')]]").first
    a.scroll_into_view_if_needed(); a.hover(); pg.wait_for_timeout(1000)
    mi=fr.evaluate("""()=>{const out=[];document.querySelectorAll("a.ui-menuitem-link").forEach(e=>{const t=e.innerText.trim();
        if(/read mapping/i.test(t)){const li=e.closest('li')||e; out.push({t, disabled:(li.className+e.className).includes('ui-state-disabled'), vis:e.getBoundingClientRect().width>0});}});return out;}""")
    print("read-mapping menuitems:", mi)
    item=fr.locator("a.ui-menuitem-link").filter(has_text=_re.compile(r"^\s*class read mapping",_re.I))
    for k in range(item.count()):
        it=item.nth(k)
        try:
            if it.is_visible(): it.click(timeout=4000); break
        except Exception: continue
    pg.wait_for_timeout(1300)
    print("RM grid AFTER insert click:", grid_html(fr))
    b.close()
print("DONE b2_diag3 (no save)")
