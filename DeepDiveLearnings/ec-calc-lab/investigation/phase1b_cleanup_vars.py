"""Self-clean: delete the AUTOTEST variables via UI (select row -> delete flyout VARIABLE DEFINITION
-> save), then DB-verify gone. Run phase1a_delete_simpletype.py afterwards for AUTOTEST_PHASE."""
from playwright.sync_api import sync_playwright
import os, re as _re, oracledb
EC_URL=os.environ.get('EC_URL','https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/')
TARGETS=['AUTOTEST_rCO2Rate','AUTOTEST_gvPhaseKey']
def wa(pg,t=20000): pg.wait_for_load_state('networkidle',timeout=t); pg.wait_for_timeout(900)
def cell(s): return '#'+s.replace(':',r'\:')
G='variable_definition_table:form:T'
with sync_playwright() as p:
    b=p.chromium.launch(headless=True,args=['--ignore-certificate-errors'])
    pg=b.new_context(ignore_https_errors=True,viewport={'width':1920,'height':1080}).new_page()
    pg.goto(EC_URL,wait_until='domcontentloaded',timeout=30000)
    pg.fill('#username','sysadmin'); pg.fill('#password','sysadmin'); pg.click('#kc-login')
    pg.wait_for_url('**/dashboard**',timeout=60000); wa(pg)
    for VAR in TARGETS:
        si=pg.locator(r'#menu\:searchForm\:searchTxt'); si.wait_for(state='visible',timeout=10000)
        si.clear(); si.type('Variable Definitions',delay=40); pg.wait_for_timeout(800)
        pg.locator("xpath=//*[contains(@class,'tv-link') and normalize-space(text())='Variable Definitions']").first.click(); wa(pg)
        fr=[f for f in pg.frames if 'variable_definition' in f.url.lower()][0]
        fr.locator(cell('nav:form:G:0:R:1:C:0:da_input')).fill('2003-01-01'); fr.locator('body').press('Tab'); pg.wait_for_timeout(400)
        fr.locator(cell('nav:form:G:1:R:1:C:0:dd_button')).click(); pg.wait_for_timeout(700)
        fr.locator("xpath=//*[@id='nav:form:G:1:R:1:C:0:dd_panel']//tr[normalize-space(@data-item-label)='Production Allocation']").first.click(timeout=8000); pg.wait_for_timeout(400)
        fr.locator(cell('button:form:B')).click(); wa(pg)
        idx=fr.evaluate("""([g,n])=>{const trs=document.querySelectorAll(`[id='${g}_data'] tr`);
            for(let i=0;i<trs.length;i++){const e=document.getElementById(`${g}:${i}:C0_in`); if(e&&e.value.trim()===n)return i;}return -1;}""", [G, VAR])
        print("%s row idx: %d" % (VAR, idx))
        if idx<0: continue
        fr.locator(cell(f'{G}:{idx}:C0_in')).click(); pg.wait_for_timeout(500)
        a=fr.locator("xpath=//a[.//span[contains(@class,'ui-icon-delete')]]").first
        a.scroll_into_view_if_needed(); a.hover(); pg.wait_for_timeout(900)
        items=fr.locator("a.ui-menuitem-link").filter(has_text=_re.compile("variable definition",_re.I))
        for k in range(items.count()):
            it=items.nth(k)
            try:
                if it.is_visible(): it.click(timeout=4000); break
            except Exception: continue
        pg.wait_for_timeout(800)
        yes=fr.locator("xpath=//button[normalize-space(.)='Yes' or .//span[normalize-space(.)='Yes']]")
        if yes.count()>0:
            try: yes.first.click(timeout=4000); pg.wait_for_timeout(500)
            except Exception: pass
        save=fr.locator("xpath=//a[@title='Save [Ctrl+s]' and not(contains(@class,'ui-state-disabled'))]")
        if save.count()>0: save.first.click(); wa(pg)
        print("  deleted+saved", VAR)
    b.close()
c=oracledb.connect(user=os.environ.get('EC_DB_USER','ECKERNEL_EC'),password=os.environ.get('EC_DB_PASS','energy'),dsn=os.environ.get('EC_DB_DSN','localhost:1521/ORCL'))
cur=c.cursor(); cur.execute("select count(*) from calc_variable where upper(name) like 'AUTOTEST%'")
print("\nAUTOTEST variables remaining:", cur.fetchone()[0]); c.close()
