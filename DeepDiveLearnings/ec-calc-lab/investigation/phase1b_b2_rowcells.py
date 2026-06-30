"""Diag4: after proper select + insert CLASS READ MAPPING, dump the new mapping row's dropdown
cell ids + which dds have buttons, so I can fill Class Name + Value Attribute. No save."""
from playwright.sync_api import sync_playwright
import os, re as _re
EC_URL=os.environ.get('EC_URL','https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/')
VAR='AUTOTEST_rCO2Rate'
def wa(pg,t=20000): pg.wait_for_load_state('networkidle',timeout=t); pg.wait_for_timeout(900)
def cell(s): return '#'+s.replace(':',r'\:')
G='variable_definition_table:form:T'; RM='tab:tabPanel:readMapping:form:T'
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
    fr.locator(cell(f'{G}:{idx}:C0_in')).click(); pg.wait_for_timeout(500); fr.locator('body').press('Escape'); pg.wait_for_timeout(400)
    fr.locator("xpath=//a[contains(translate(.,'abcdefghijklmnopqrstuvwxyz','ABCDEFGHIJKLMNOPQRSTUVWXYZ'),'READ MAPPINGS')]").first.click(timeout=5000); pg.wait_for_timeout(1100)
    a=fr.locator("xpath=//a[.//span[contains(@class,'ui-icon-insert')]]").first
    a.scroll_into_view_if_needed(); a.hover(); pg.wait_for_timeout(1000)
    it=fr.locator("a.ui-menuitem-link").filter(has_text=_re.compile(r"^\s*class read mapping",_re.I))
    for k in range(it.count()):
        x=it.nth(k)
        try:
            if x.is_visible(): x.click(timeout=4000); break
        except Exception: continue
    pg.wait_for_timeout(1300)
    cells=fr.evaluate("""(g)=>{const tr=document.querySelectorAll(`[id='${g}_data'] tr`)[0]; if(!tr)return[];
        return [...tr.querySelectorAll("input,select,button,span[id]")].map(e=>({id:e.id.replace(`${g}:0:`,''),tag:e.tagName,type:e.type||'',val:e.value||''})).filter(o=>o.id);}""", RM)
    print("NEW mapping row cells:"); [print("   ",c) for c in cells]
    b.close()
print("DONE b2_rowcells (no save)")
