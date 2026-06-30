"""Phase 1b Var B2: add a READ MAPPING to AUTOTEST_rCO2Rate, cloning exemplar:
CLASS READ MAPPING -> Class Name=PWEL_DAY_DATA, Value Attribute=THEOR_CO2_RATE.
Then check if CLASS KEY rows auto-populate; if not, add them. Save + DB-verify CALC_VAR_READ_MAPPING.
Verbose prints so a single run shows how far it got (>=2-try discipline on the hard sub-grid)."""
from playwright.sync_api import sync_playwright
import os, re as _re, oracledb
EC_URL=os.environ.get('EC_URL','https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/')
VAR='AUTOTEST_rCO2Rate'; CLS='PWEL_DAY_DATA'; ATTR='THEOR_CO2_RATE'
def wa(pg,t=20000): pg.wait_for_load_state('networkidle',timeout=t); pg.wait_for_timeout(900)
def cell(s): return '#'+s.replace(':',r'\:')
G='variable_definition_table:form:T'; RM='tab:tabPanel:readMapping:form:T'
def click_flyout(fr,pg,icon_cls,label_re):
    a=fr.locator(f"xpath=//a[.//span[contains(@class,'{icon_cls}')]]").first
    a.scroll_into_view_if_needed(); a.hover(); pg.wait_for_timeout(1000)
    items=fr.locator("a.ui-menuitem-link").filter(has_text=_re.compile(label_re,_re.I))
    for k in range(items.count()):
        it=items.nth(k)
        try:
            if it.is_visible(): it.click(timeout=4000); return True
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
    # select AUTOTEST_rCO2Rate
    idx=fr.evaluate("""(g)=>{const trs=document.querySelectorAll(`[id='${g}_data'] tr`);
        for(let i=0;i<trs.length;i++){const e=document.getElementById(`${g}:${i}:C0_in`); if(e&&e.value.trim()==='AUTOTEST_rCO2Rate')return i;}return -1;}""", G)
    print("var row idx:", idx)
    if idx<0: print("var not on first page -> abort"); b.close(); raise SystemExit(1)
    fr.locator(cell(f'{G}:{idx}:C0_in')).click(); pg.wait_for_timeout(1200)
    # READ MAPPINGS tab
    fr.locator("xpath=//a[contains(translate(.,'abcdefghijklmnopqrstuvwxyz','ABCDEFGHIJKLMNOPQRSTUVWXYZ'),'READ MAPPINGS')]").first.click(timeout=5000); pg.wait_for_timeout(1100)
    rm_before=fr.evaluate("()=>document.querySelectorAll(\"[id='tab:tabPanel:readMapping:form:T_data'] tr\").length")
    print("readMapping rows before:", rm_before)
    ok=click_flyout(fr,pg,'ui-icon-insert','class read mapping'); print("CLASS READ MAPPING inserted:",ok); pg.wait_for_timeout(1200)
    # find empty readMapping row (C2 class name empty)
    j=fr.evaluate("""(g)=>{const trs=document.querySelectorAll(`[id='${g}_data'] tr`);
        for(let x=0;x<trs.length;x++){const e=document.getElementById(`${g}:${x}:C2_in`); if(e&&!e.value.trim())return x;}return -1;}""", RM)
    print("empty mapping row idx:", j)
    if j>=0:
        # Class Type C1 = Data (dd or text)
        if fr.evaluate("(a)=>!!document.getElementById(a+':C1_dd_button')", f'{RM}:{j}'):
            fr.locator(cell(f'{RM}:{j}:C1_dd_button')).click(); pg.wait_for_timeout(600)
            o=fr.locator(f"xpath=//*[@id='{RM}:{j}:C1_dd_panel']//tr[normalize-space(@data-item-label)='Data']")
            if o.count()>0: o.first.click(); pg.wait_for_timeout(300)
        # Class Name C2 (type + Tab to resolve)
        fr.locator(cell(f'{RM}:{j}:C2_in')).click(); fr.locator(cell(f'{RM}:{j}:C2_in')).fill(CLS); pg.keyboard.press('Tab'); pg.wait_for_timeout(1200)
        print("C3 class label after resolve:", fr.evaluate("(a)=>(document.getElementById(a+':C3_in')||{}).value", f'{RM}:{j}'))
        # Value Attribute C4 dd
        if fr.evaluate("(a)=>!!document.getElementById(a+':C4_dd_button')", f'{RM}:{j}'):
            fr.locator(cell(f'{RM}:{j}:C4_dd_button')).click(); pg.wait_for_timeout(800)
            o=fr.locator(f"xpath=//*[@id='{RM}:{j}:C4_dd_panel']//tr[normalize-space(@data-item-label)='{ATTR}']")
            print("value attr '%s' present:"%ATTR, o.count()>0)
            if o.count()>0: o.first.click(timeout=6000); pg.wait_for_timeout(300)
        # check class-key auto-populate
        ak=fr.evaluate("()=>document.querySelectorAll(\"[id='tab:tabPanel:attrMapping:form:T_data'] tr\").length")
        print("attrMapping (class-key) rows now:", ak)
    save=fr.locator("xpath=//a[@title='Save [Ctrl+s]' and not(contains(@class,'ui-state-disabled'))]")
    print("save enabled:", save.count()>0)
    if save.count()>0: save.first.click(); wa(pg)
    print("banner:", fr.evaluate("""()=>[...document.querySelectorAll(".ui-messages-error-detail,.ui-message-error-detail")].map(e=>e.innerText.trim()).filter(Boolean).slice(0,4)"""))
    b.close()
c=oracledb.connect(user=os.environ.get('EC_DB_USER','ECKERNEL_EC'),password=os.environ.get('EC_DB_PASS','energy'),dsn=os.environ.get('EC_DB_DSN','localhost:1521/ORCL'))
cur=c.cursor()
cur.execute("""select m.cls_name, m.sql_syntax from calc_var_read_mapping m
               join calc_variable v on v.calc_var_signature=m.calc_var_signature where v.name=:1""",[VAR])
rows=cur.fetchall()
print("\nDB VERIFY read mapping for %s:"%VAR, [(r[0], (r[1].read() if hasattr(r[1],'read') else r[1])) for r in rows])
print("RESULT:", "PASS (read mapping persisted)" if rows else "FAIL (no mapping row)")
c.close()
