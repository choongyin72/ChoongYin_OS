"""Phase 1a recon v2 (READ-ONLY): resolve the G:1 navigator dropdown options + the real grid id +
the insert submenu + new-row cell ids on Simple Object Types. No save."""
from playwright.sync_api import sync_playwright
import os
EC_URL=os.environ.get('EC_URL','https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/')
def wa(pg,t=20000): pg.wait_for_load_state('networkidle',timeout=t); pg.wait_for_timeout(900)
def cell(s): return '#'+s.replace(':',r'\:')
with sync_playwright() as p:
    b=p.chromium.launch(headless=True,args=['--ignore-certificate-errors'])
    pg=b.new_context(ignore_https_errors=True,viewport={'width':1920,'height':1080}).new_page()
    pg.goto(EC_URL,wait_until='domcontentloaded',timeout=30000)
    pg.fill('#username','sysadmin'); pg.fill('#password','sysadmin'); pg.click('#kc-login')
    pg.wait_for_url('**/dashboard**',timeout=60000); wa(pg)
    si=pg.locator(r'#menu\:searchForm\:searchTxt'); si.wait_for(state='visible',timeout=10000)
    si.clear(); si.type('Simple Object Types',delay=40); pg.wait_for_timeout(900)
    pg.locator("xpath=//*[contains(@class,'tv-link') and normalize-space(text())='Simple Object Types']").first.click(); wa(pg)
    fr=[f for f in pg.frames if 'simple_predefined' in f.url.lower()]
    fr=fr[0] if fr else [f for f in pg.frames if f.evaluate("()=>!!document.querySelector(\"[id^='nav:form']\")")][0]
    # label of G:1 dd (read the nav cell label text more broadly)
    lbl=fr.evaluate("""()=>{const b=document.getElementById('nav:form:G:1:R:1:C:0:dd_button');
        if(!b)return''; let n=b.closest('td')||b.parentElement; for(let i=0;i<4&&n;i++){n=n.previousElementSibling||n.parentElement; if(n&&n.innerText&&n.innerText.trim())return n.innerText.trim().slice(0,40);} return'';}""")
    print("G:1 dd label-ish:", lbl)
    # set date FIRST (so it doesn't collapse the dd panel later)
    d=fr.locator(cell('nav:form:G:0:R:1:C:0:da_input'))
    if d.count()>0: d.click(); d.fill('2003-01-01'); fr.locator('body').press('Tab'); pg.wait_for_timeout(500)
    # open G:1 dd, pick Production Allocation
    fr.locator(cell('nav:form:G:1:R:1:C:0:dd_button')).click(); pg.wait_for_timeout(900)
    fr.locator("xpath=//*[@id='nav:form:G:1:R:1:C:0:dd_panel']//tr[normalize-space(@data-item-label)='Production Allocation']").first.click(timeout=8000); pg.wait_for_timeout(500)
    fr.locator(cell('button:form:B')).click(); wa(pg)
    # find ANY datatable + its id + row count
    grids=fr.evaluate("""()=>[...document.querySelectorAll("table[id], div.ui-datatable[id], [id$='T_data']")].map(e=>({id:e.id, rows:e.querySelectorAll('tr').length})).filter(o=>o.id && o.rows>=0).slice(0,12)""")
    print("GRIDS:", grids)
    # insert
    ins=fr.locator("xpath=//a[.//span[contains(@class,'ui-icon-insert')]]")
    print("insert anchors:", ins.count())
    if ins.count()>0:
        ins.first.click(); pg.wait_for_timeout(900)
        menu=fr.evaluate("""()=>[...document.querySelectorAll(".ui-menu:not([style*='display: none']) .ui-menuitem-text")].map(e=>e.innerText.trim()).filter(Boolean).slice(0,10)""")
        print("insert submenu:", menu)
        if menu:
            try:
                fr.locator("xpath=//span[contains(@class,'ui-menuitem-text') and normalize-space(text())='%s']" % menu[0]).first.click(); pg.wait_for_timeout(900)
            except Exception as e: print("submenu click note:", str(e)[:70])
        cells=fr.evaluate("""()=>{const tr=document.querySelectorAll("[id$='T_data'] tr")[0]; if(!tr)return[];
            return [...tr.querySelectorAll("input,select,a[id$='_button']")].map(e=>({id:e.id,tag:e.tagName,type:e.type||''}));}""")
        print("NEW ROW inputs:"); [print("   ",c) for c in cells]
    b.close()
print("DONE recon2 (no save)")
