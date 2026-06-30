"""Diag2: after selecting Var B1 + READ MAPPINGS tab, locate EVERY ui-icon-insert anchor and the
form/panel it belongs to (top variable-grid toolbar vs the readMapping sub-grid's own toolbar).
Then hover the readMapping one and dump its flyout. No save. PRE-REQ: Var B1 exists."""
from playwright.sync_api import sync_playwright
import os, re as _re
EC_URL=os.environ.get('EC_URL','https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/')
VAR='AUTOTEST_rCO2Rate'
def wa(pg,t=20000): pg.wait_for_load_state('networkidle',timeout=t); pg.wait_for_timeout(900)
def cell(s): return '#'+s.replace(':',r'\:')
G='variable_definition_table:form:T'
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
    fr.locator(cell(f'{G}:{idx}:C0_in')).click(); pg.wait_for_timeout(1000)
    fr.locator("xpath=//a[contains(translate(.,'abcdefghijklmnopqrstuvwxyz','ABCDEFGHIJKLMNOPQRSTUVWXYZ'),'READ MAPPINGS')]").first.click(timeout=5000); pg.wait_for_timeout(1200)
    # every insert anchor + its nearest ancestor form id + y
    anchors=fr.evaluate("""()=>[...document.querySelectorAll("a")].filter(a=>a.querySelector("span[class*='ui-icon-insert']")).map(a=>{
        const r=a.getBoundingClientRect(); let f=a.closest("[id]"); let fid='';
        let e=a; while(e){ if(e.id && /form/.test(e.id)){fid=e.id;break;} e=e.parentElement;}
        return {y:Math.round(r.y), x:Math.round(r.x), vis:r.width>0, formId:fid, aid:a.id||''};})""")
    print("INSERT anchors (with form):"); [print("   ",o) for o in anchors]
    # hover the readMapping one (formId contains readMapping) else the lowest y below the tab
    target=None
    for o in anchors:
        if 'readMapping' in o['formId']: target=o; break
    print("readMapping insert target:", target)
    if target:
        loc=fr.locator(f"xpath=//*[@id='{target['formId']}']//a[.//span[contains(@class,'ui-icon-insert')]]").first
        loc.scroll_into_view_if_needed(); loc.hover(); pg.wait_for_timeout(1000)
        fly=fr.evaluate("""()=>[...document.querySelectorAll("a.ui-menuitem-link")].filter(e=>{const r=e.getBoundingClientRect();return r.width>0;}).map(e=>e.innerText.trim()).filter(Boolean).slice(0,10)""")
        print("readMapping insert flyout:", fly)
    b.close()
print("DONE b2_diag2 (no save)")
