"""Delete the AUTOTEST_PHASE Simple Object Type via UI (select row -> Delete flyout -> Save),
then DB-verify it is gone. Proves the reversibility gate empirically + is the self-clean path."""
from playwright.sync_api import sync_playwright
import os, re as _re, oracledb
EC_URL=os.environ.get('EC_URL','https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/')
CODE='AUTOTEST_PHASE'
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
    # find row index of AUTOTEST_PHASE
    idx=fr.evaluate("""(g)=>{const trs=document.querySelectorAll(`[id='${g}_data'] tr`);
        for(let i=0;i<trs.length;i++){const e=document.getElementById(`${g}:${i}:C0_in`); if(e && e.value.trim()==='AUTOTEST_PHASE') return i;} return -1;}""", G)
    print("AUTOTEST_PHASE row index:", idx)
    if idx<0: print("row not found in UI"); b.close(); raise SystemExit(1)
    # select the row (click its code cell), then Delete flyout
    fr.locator(cell(f'{G}:{idx}:C0_in')).click(); pg.wait_for_timeout(400)
    a=fr.locator("xpath=//a[.//span[contains(@class,'ui-icon-delete')]]").first
    a.scroll_into_view_if_needed(); a.hover(); pg.wait_for_timeout(1000)
    items=fr.locator("a.ui-menuitem-link").filter(has_text=_re.compile("simple object types", _re.I))
    dc=False
    for k in range(items.count()):
        it=items.nth(k)
        try:
            if it.is_visible(): it.hover(); pg.wait_for_timeout(200); it.click(timeout=4000); dc=True; break
        except Exception: continue
    print("delete flyout clicked:", dc); pg.wait_for_timeout(900)
    # confirm dialog Yes if present
    yes=fr.locator("xpath=//button[normalize-space(.)='Yes' or .//span[normalize-space(.)='Yes']]")
    if yes.count()>0:
        try: yes.first.click(timeout=4000); pg.wait_for_timeout(600)
        except Exception: pass
    save=fr.locator("xpath=//a[@title='Save [Ctrl+s]' and not(contains(@class,'ui-state-disabled'))]")
    print("save enabled:", save.count()>0)
    if save.count()>0: save.first.click(); wa(pg)
    b.close()
c=oracledb.connect(user=os.environ.get('EC_DB_USER','ECKERNEL_EC'),password=os.environ.get('EC_DB_PASS','energy'),dsn=os.environ.get('EC_DB_DSN','localhost:1521/ORCL'))
cur=c.cursor(); cur.execute("select count(*) from calc_object_type where object_type_code=:1",[CODE])
n=cur.fetchone()[0]; print("\nDB VERIFY after delete: rows with %s = %d" % (CODE,n)); print("RESULT:", "PASS (deleted, clean)" if n==0 else "FAIL (still present)")
c.close()
