"""Phase 1a CREATE (writes one AUTOTEST_ Simple Object Type, then DB-verifies).
Cols: C0=Object Type code, C1=Label Override, C2=Object Type Label, C3=Data Type dd.
EC inserts the blank row mid-grid -> fill the row whose C0 is actually empty. Then Save + DB-verify."""
from playwright.sync_api import sync_playwright
import os, oracledb
EC_URL=os.environ.get('EC_URL','https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/')
CODE='AUTOTEST_PHASE'; LABEL='AUTOTEST Phase'; DTYPE='String'
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
    n_before=fr.evaluate("(g)=>document.querySelectorAll(`[id='${g}_data'] tr`).length", G)
    print("rows before insert:", n_before)
    # INSERT = hover the insert toolbar anchor -> flyout submenu item "Simple Object Types"
    # (CSS-uppercased in render; match case-insensitively; click the VISIBLE flyout item)
    import re as _re
    a=fr.locator("xpath=//a[.//span[contains(@class,'ui-icon-insert')]]").first
    a.scroll_into_view_if_needed(); a.hover(); pg.wait_for_timeout(1100)
    items=fr.locator("a.ui-menuitem-link").filter(has_text=_re.compile("simple object types", _re.I))
    clicked=False
    for k in range(items.count()):
        it=items.nth(k)
        try:
            if it.is_visible():
                it.hover(); pg.wait_for_timeout(200); it.click(timeout=4000); clicked=True; break
        except Exception: continue
    print("insert flyout item clicked:", clicked); pg.wait_for_timeout(1100)
    n_after=fr.evaluate("(g)=>document.querySelectorAll(`[id='${g}_data'] tr`).length", G)
    print("rows after insert:", n_after)
    # find the row whose C0 input is empty
    empty_idx=fr.evaluate("""(g)=>{const trs=document.querySelectorAll(`[id='${g}_data'] tr`);
        for(let i=0;i<trs.length;i++){const e=document.getElementById(`${g}:${i}:C0_in`); if(e && !e.value.trim()) return i;} return -1;}""", G)
    print("empty new-row index:", empty_idx)
    if empty_idx<0: print("NO EMPTY ROW -> abort, no save"); b.close(); raise SystemExit(1)
    i=empty_idx
    # Only the code (C0) is mandatory; Label Override/Object Type Label are optional/derived (readonly).
    c0=fr.locator(cell(f'{G}:{i}:C0_in')); c0.click(); c0.fill(CODE); pg.wait_for_timeout(400)
    # Data Type dd
    fr.locator(cell(f'{G}:{i}:C3_dd_button')).click(); pg.wait_for_timeout(700)
    dt=fr.locator(f"xpath=//*[@id='{G}:{i}:C3_dd_panel']//tr[normalize-space(@data-item-label)='{DTYPE}']")
    if dt.count()>0: dt.first.click(timeout=6000); pg.wait_for_timeout(300)
    print("staged C0:", fr.evaluate("(a)=>(document.getElementById(a+':C0_in')||{}).value", f'{G}:{i}'))
    # Save
    save=fr.locator("xpath=//a[@title='Save [Ctrl+s]' and not(contains(@class,'ui-state-disabled'))]")
    print("save enabled:", save.count()>0)
    if save.count()>0: save.first.click(); wa(pg)
    # capture any banner
    ban=fr.evaluate("""()=>[...document.querySelectorAll(".ui-messages-error-summary,.ui-messages-info-summary,.ui-growl-title,.ui-message-error-detail")].map(e=>e.innerText.trim()).filter(Boolean).slice(0,4)""")
    print("banner:", ban)
    b.close()
# DB verify
c=oracledb.connect(user=os.environ.get('EC_DB_USER','ECKERNEL_EC'),password=os.environ.get('EC_DB_PASS','energy'),dsn=os.environ.get('EC_DB_DSN','localhost:1521/ORCL'))
cur=c.cursor()
cur.execute("select object_type_code, calc_obj_type_category, data_type, object_id from calc_object_type where object_type_code=:1",[CODE])
rows=cur.fetchall()
print("\nDB VERIFY calc_object_type where code=%s:" % CODE)
for r in rows: print("   code=%s category=%s data_type=%s id=%s" % (r[0], r[1], (r[2].read() if hasattr(r[2],'read') else r[2]), r[3]))
print("RESULT:", "PASS (row persisted)" if rows else "FAIL (no row)")
c.close()
