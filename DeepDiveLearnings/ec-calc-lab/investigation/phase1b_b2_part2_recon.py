"""B2 recon (READ-ONLY, no save): after select + insert CLASS READ MAPPING + set class,
(1) dump Value Attribute dd options matching THEOR -> find the EXACT 'THEOR_CO2_RATE' label;
(2) insert CLASS KEY READ MAPPING and dump the new attrMapping row cell ids + their dd options.
PRE-REQ: Var B1 (AUTOTEST_rCO2Rate) exists."""
from playwright.sync_api import sync_playwright
import os, re as _re
EC_URL=os.environ.get('EC_URL','https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/')
VAR='AUTOTEST_rCO2Rate'
def wa(pg,t=20000): pg.wait_for_load_state('networkidle',timeout=t); pg.wait_for_timeout(900)
def cell(s): return '#'+s.replace(':',r'\:')
G='variable_definition_table:form:T'; RM='tab:tabPanel:readMapping:form:T'; AM='tab:tabPanel:attrMapping:form:T'
def _opts(fr,base):
    return fr.evaluate("""(b)=>{const pan=document.getElementById(b+'_dd_panel'); if(!pan)return [];
        return [...pan.querySelectorAll('tr')].map(r=>r.getAttribute('data-item-label')||r.innerText.trim()).filter(Boolean);}""", base)
def type_pick(fr,pg,base,needle,exact=None):
    inp=fr.locator(cell(base+'_dd_input')); inp.click(); inp.fill(''); inp.type(needle, delay=60); pg.wait_for_timeout(1300)
    opts=_opts(fr,base)
    if exact: lab=next((o for o in opts if o.strip()==exact), None)
    else: lab=next((o for o in opts if needle.lower() in o.lower()), None)
    if lab is None: print("   NO match for %s (exact=%s); opts=%s"%(needle,exact,opts[:8])); return False
    fr.locator(f"xpath=//*[@id='{base}_dd_panel']//tr[normalize-space(@data-item-label)={chr(39)+lab+chr(39)}]").first.click(timeout=6000); pg.wait_for_timeout(500)
    print("   %s <- %s"%(base[-10:],lab)); return True
def flyout(fr,pg,rx):
    a=fr.locator("xpath=//a[.//span[contains(@class,'ui-icon-insert')]]").first
    a.scroll_into_view_if_needed(); a.hover(); pg.wait_for_timeout(1000)
    it=fr.locator("a.ui-menuitem-link").filter(has_text=_re.compile(rx,_re.I))
    for k in range(it.count()):
        x=it.nth(k)
        try:
            if x.is_visible(): x.click(timeout=4000); return True
        except Exception: continue
    return False
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
    flyout(fr,pg,r"^\s*class read mapping"); pg.wait_for_timeout(1100)
    type_pick(fr,pg,f'{RM}:0:C1','Data')
    type_pick(fr,pg,f'{RM}:0:C2','PWEL_DAY_DATA'); pg.wait_for_timeout(800)
    # complete Part 1: set Value Attribute EXACT THEOR_CO2_RATE
    type_pick(fr,pg,f'{RM}:0:C4','THEOR_CO2',exact='THEOR_CO2_RATE'); pg.wait_for_timeout(600)
    # re-select the class-mapping row (so CLASS KEY action targets it)
    fr.locator(f"xpath=//*[@id='{RM}_data']/tr[1]/td[1]").click(); pg.wait_for_timeout(500)
    # is CLASS KEY READ MAPPING now enabled?
    a=fr.locator("xpath=//a[.//span[contains(@class,'ui-icon-insert')]]").first
    a.scroll_into_view_if_needed(); a.hover(); pg.wait_for_timeout(900)
    print("CLASS KEY menuitem state:", fr.evaluate("""()=>{const out=[];document.querySelectorAll("a.ui-menuitem-link").forEach(e=>{const t=e.innerText.trim();
        if(/class key read mapping/i.test(t)){const li=e.closest('li')||e;out.push({t,disabled:(li.className+e.className).includes('ui-state-disabled'),vis:e.getBoundingClientRect().width>0});}});return out;}"""))
    print("insert CLASS KEY READ MAPPING:", flyout(fr,pg,r"^\s*class key read mapping")); pg.wait_for_timeout(1100)
    cells=fr.evaluate("""(g)=>{const tr=document.querySelectorAll(`[id='${g}_data'] tr`)[0]; if(!tr)return[];
        return [...tr.querySelectorAll("input,select,button,span[id]")].map(e=>({id:e.id.replace(`${g}:0:`,''),tag:e.tagName,type:e.type||'',val:e.value||''})).filter(o=>o.id);}""", AM)
    print("attrMapping NEW row cells:"); [print("   ",c) for c in cells]
    b.close()
print("DONE b2_part2_recon (no save)")
