"""Phase 1b Var A: author a Variable Definition dimensioned by the Simple Object Type AUTOTEST_PHASE
(no DB mapping = a pure in-calc variable). Proves Variable Definitions authoring + Simple-type-as-dimension.
Discovers the insert flyout label, fills Name (C0) + Dimension 1 (C1 dd = AUTOTEST_PHASE), Save, DB-verify.
PRE-REQ: run phase1a_create_simpletype.py first so AUTOTEST_PHASE exists."""
from playwright.sync_api import sync_playwright
import os, re as _re, oracledb
EC_URL=os.environ.get('EC_URL','https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/')
VAR='AUTOTEST_gvPhaseKey'; DIM='AUTOTEST_PHASE'
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
    n0=fr.evaluate("(g)=>document.querySelectorAll(`[id='${g}_data'] tr`).length", G)
    # INSERT: hover insert, discover + click the flyout item
    a=fr.locator("xpath=//a[.//span[contains(@class,'ui-icon-insert')]]").first
    a.scroll_into_view_if_needed(); a.hover(); pg.wait_for_timeout(1100)
    labels=fr.evaluate("""()=>[...document.querySelectorAll("a.ui-menuitem-link")].filter(e=>{const r=e.getBoundingClientRect();return r.width>0&&r.height>0;}).map(e=>e.innerText.trim()).filter(Boolean).slice(0,12)""")
    print("visible insert flyout labels:", labels)
    items=fr.locator("a.ui-menuitem-link").filter(has_text=_re.compile("variable", _re.I))
    for k in range(items.count()):
        it=items.nth(k)
        try:
            if it.is_visible(): it.click(timeout=4000); break
        except Exception: continue
    pg.wait_for_timeout(1200)
    n1=fr.evaluate("(g)=>document.querySelectorAll(`[id='${g}_data'] tr`).length", G)
    print("rows %d -> %d" % (n0,n1))
    i=fr.evaluate("""(g)=>{const trs=document.querySelectorAll(`[id='${g}_data'] tr`);
        for(let x=0;x<trs.length;x++){const e=document.getElementById(`${g}:${x}:C0_in`); if(e&&!e.value.trim())return x;}return -1;}""", G)
    print("empty row idx:", i)
    if i<0: print("NO EMPTY ROW -> abort"); b.close(); raise SystemExit(1)
    fr.locator(cell(f'{G}:{i}:C0_in')).click(); fr.locator(cell(f'{G}:{i}:C0_in')).fill(VAR); pg.wait_for_timeout(400)
    # Dimension 1 = C1: discover if dd or text
    has_dd=fr.evaluate("(a)=>!!document.getElementById(a+':C1_dd_button')", f'{G}:{i}')
    print("C1 is dropdown:", has_dd)
    if has_dd:
        fr.locator(cell(f'{G}:{i}:C1_dd_button')).click(); pg.wait_for_timeout(700)
        opt=fr.locator(f"xpath=//*[@id='{G}:{i}:C1_dd_panel']//tr[normalize-space(@data-item-label)='{DIM}']")
        print("AUTOTEST_PHASE option present:", opt.count()>0)
        if opt.count()>0: opt.first.click(timeout=6000); pg.wait_for_timeout(300)
    else:
        fr.locator(cell(f'{G}:{i}:C1_in')).click(); fr.locator(cell(f'{G}:{i}:C1_in')).fill(DIM); pg.wait_for_timeout(400)
    save=fr.locator("xpath=//a[@title='Save [Ctrl+s]' and not(contains(@class,'ui-state-disabled'))]")
    print("save enabled:", save.count()>0)
    if save.count()>0: save.first.click(); wa(pg)
    ban=fr.evaluate("""()=>[...document.querySelectorAll(".ui-messages-error-detail,.ui-message-error-detail,.ui-growl-title")].map(e=>e.innerText.trim()).filter(Boolean).slice(0,4)""")
    print("banner:", ban)
    b.close()
c=oracledb.connect(user=os.environ.get('EC_DB_USER','ECKERNEL_EC'),password=os.environ.get('EC_DB_PASS','energy'),dsn=os.environ.get('EC_DB_DSN','localhost:1521/ORCL'))
cur=c.cursor()
cur.execute("select name, calc_var_data_type, dim1_object_type_code from calc_variable where name=:1",[VAR])
rows=cur.fetchall()
print("\nDB VERIFY calc_variable where name=%s:" % VAR)
for r in rows: print("   name=%s data_type=%s dim1=%s" % (r[0], r[1], r[2]))
print("RESULT:", "PASS (variable persisted, dim1=%s)" % (rows[0][2] if rows else '?') if rows else "FAIL (no row)")
c.close()
