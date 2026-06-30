"""Phase 1b Var B1: author AUTOTEST_rCO2Rate dimensioned by [ALLOC_NODE (DB type), DAY (predefined)] -
clones exemplar CO2_InitialNStdVol's dimensions. Proves a variable using a Database object type +
predefined type as dimensions. (Read mapping = separate slice B2.) Save + DB-verify."""
from playwright.sync_api import sync_playwright
import os, re as _re, oracledb
EC_URL=os.environ.get('EC_URL','https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/')
VAR='AUTOTEST_rCO2Rate'; DIMS=['Allocation Node','Day']  # data-item-labels in the dimension dd
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
    a=fr.locator("xpath=//a[.//span[contains(@class,'ui-icon-insert')]]").first
    a.scroll_into_view_if_needed(); a.hover(); pg.wait_for_timeout(1100)
    items=fr.locator("a.ui-menuitem-link").filter(has_text=_re.compile("variable definition", _re.I))
    for k in range(items.count()):
        it=items.nth(k)
        try:
            if it.is_visible(): it.click(timeout=4000); break
        except Exception: continue
    pg.wait_for_timeout(1200)
    i=fr.evaluate("""(g)=>{const trs=document.querySelectorAll(`[id='${g}_data'] tr`);
        for(let x=0;x<trs.length;x++){const e=document.getElementById(`${g}:${x}:C0_in`); if(e&&!e.value.trim())return x;}return -1;}""", G)
    print("empty row idx:", i)
    if i<0: print("NO EMPTY ROW -> abort"); b.close(); raise SystemExit(1)
    fr.locator(cell(f'{G}:{i}:C0_in')).click(); fr.locator(cell(f'{G}:{i}:C0_in')).fill(VAR); pg.wait_for_timeout(400)
    # dims C1, C2
    for cidx,label in enumerate(DIMS, start=1):
        ddb=fr.locator(cell(f'{G}:{i}:C{cidx}_dd_button'))
        if ddb.count()==0: print("no dd at C%d"%cidx); continue
        ddb.click(); pg.wait_for_timeout(700)
        opt=fr.locator(f"xpath=//*[@id='{G}:{i}:C{cidx}_dd_panel']//tr[normalize-space(@data-item-label)='{label}']")
        print("dim C%d '%s' present:"%(cidx,label), opt.count()>0)
        if opt.count()>0: opt.first.click(timeout=6000); pg.wait_for_timeout(300)
    save=fr.locator("xpath=//a[@title='Save [Ctrl+s]' and not(contains(@class,'ui-state-disabled'))]")
    print("save enabled:", save.count()>0)
    if save.count()>0: save.first.click(); wa(pg)
    print("banner:", fr.evaluate("""()=>[...document.querySelectorAll(".ui-messages-error-detail,.ui-message-error-detail")].map(e=>e.innerText.trim()).filter(Boolean).slice(0,3)"""))
    b.close()
c=oracledb.connect(user=os.environ.get('EC_DB_USER','ECKERNEL_EC'),password=os.environ.get('EC_DB_PASS','energy'),dsn=os.environ.get('EC_DB_DSN','localhost:1521/ORCL'))
cur=c.cursor()
cur.execute("select name, dim1_object_type_code, dim2_object_type_code from calc_variable where name=:1",[VAR])
rows=cur.fetchall()
print("\nDB VERIFY:", rows)
print("RESULT:", "PASS dims=[%s,%s]"%(rows[0][1],rows[0][2]) if rows else "FAIL")
c.close()
