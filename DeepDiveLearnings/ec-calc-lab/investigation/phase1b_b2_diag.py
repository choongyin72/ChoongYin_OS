"""Diagnose Var B2: how to SELECT the variable as master (so READ MAPPINGS loads ITS mappings),
and the readMapping grid state before/after the CLASS READ MAPPING flyout insert. Read-only-ish
(inserts an unsaved mapping row then closes WITHOUT save -> discarded). PRE-REQ: Var B1 exists."""
from playwright.sync_api import sync_playwright
import os, re as _re
EC_URL=os.environ.get('EC_URL','https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/')
VAR='AUTOTEST_rCO2Rate'
def wa(pg,t=20000): pg.wait_for_load_state('networkidle',timeout=t); pg.wait_for_timeout(900)
def cell(s): return '#'+s.replace(':',r'\:')
G='variable_definition_table:form:T'; RM='tab:tabPanel:readMapping:form:T'
def rm_state(fr):
    return fr.evaluate("""(g)=>{const trs=document.querySelectorAll(`[id='${g}_data'] tr`);const out=[];
        for(let i=0;i<trs.length;i++){const c2=document.getElementById(`${g}:${i}:C2_in`);
          out.push({i, c2:(c2?c2.value:'(none)'), c2ro:(c2?c2.readOnly:null),
                    c4:(document.getElementById(`${g}:${i}:C4_dd_input`)||{}).value||''});}
        return out;}""", RM)
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
    print("var row idx:", idx)
    # how is a row selected? dump the row's selectable elements (radio/checkbox/clickable cell)
    sel=fr.evaluate("""([g,i])=>{const tr=document.querySelectorAll(`[id='${g}_data'] tr`)[i]; if(!tr)return[];
        return [...tr.querySelectorAll("div.ui-radiobutton,div.ui-chkbox,span.ui-icon,td")].slice(0,4).map(e=>({tag:e.tagName,cls:(e.className||'').slice(0,30),id:e.id||''}));}""", [G, idx])
    print("row selectable bits:", sel)
    # APPROACH 1: click the row's first TD (selection col), not the C0 input
    fr.locator(f"xpath=//*[@id='{G}_data']/tr[{idx+1}]/td[1]").click(); pg.wait_for_timeout(1200)
    fr.locator("xpath=//a[contains(translate(.,'abcdefghijklmnopqrstuvwxyz','ABCDEFGHIJKLMNOPQRSTUVWXYZ'),'READ MAPPINGS')]").first.click(timeout=5000); pg.wait_for_timeout(1100)
    print("RM state after row-select (before insert):", rm_state(fr))
    # insert CLASS READ MAPPING
    a=fr.locator("xpath=//a[.//span[contains(@class,'ui-icon-insert')]]").first
    a.scroll_into_view_if_needed(); a.hover(); pg.wait_for_timeout(1000)
    items=fr.locator("a.ui-menuitem-link").filter(has_text=_re.compile("class read mapping",_re.I))
    for k in range(items.count()):
        it=items.nth(k)
        try:
            if it.is_visible(): it.click(timeout=4000); break
        except Exception: continue
    pg.wait_for_timeout(1300)
    print("RM state AFTER CLASS READ MAPPING insert:", rm_state(fr))
    b.close()  # no save -> discarded
print("DONE b2_diag (no save)")
