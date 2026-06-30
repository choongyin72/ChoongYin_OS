"""Phase 1b recon (READ-ONLY): Variable Definitions screen structure - grid id, headers,
new-row cell ids (after insert via the proven hover-flyout), and any read/write mapping sub-region.
No save (unsaved insert discarded)."""
from playwright.sync_api import sync_playwright
import os, re as _re
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
    si.clear(); si.type('Variable Definitions',delay=40); pg.wait_for_timeout(900)
    pg.locator("xpath=//*[contains(@class,'tv-link') and normalize-space(text())='Variable Definitions']").first.click(); wa(pg)
    fr=[f for f in pg.frames if 'variable_definition' in f.url.lower()][0]
    fr.locator(cell('nav:form:G:0:R:1:C:0:da_input')).fill('2003-01-01'); fr.locator('body').press('Tab'); pg.wait_for_timeout(500)
    fr.locator(cell('nav:form:G:1:R:1:C:0:dd_button')).click(); pg.wait_for_timeout(800)
    fr.locator("xpath=//*[@id='nav:form:G:1:R:1:C:0:dd_panel']//tr[normalize-space(@data-item-label)='Production Allocation']").first.click(timeout=8000); pg.wait_for_timeout(400)
    fr.locator(cell('button:form:B')).click(); wa(pg)
    grids=fr.evaluate("""()=>[...document.querySelectorAll("[id$='T_data']")].map(e=>({id:e.id,rows:e.querySelectorAll('tr').length}))""")
    print("GRIDS:", grids)
    G=grids[0]['id'][:-5] if grids else ''
    print("grid base:", G)
    hdr=fr.evaluate("""(g)=>{const t=document.getElementById(g);if(!t)return[];return [...t.querySelectorAll('thead th')].map(e=>e.innerText.trim()).filter(Boolean);}""", G)
    print("HEADERS:", hdr)
    # insert via hover flyout (grid name = 'Variable Definitions')
    a=fr.locator("xpath=//a[.//span[contains(@class,'ui-icon-insert')]]").first
    a.scroll_into_view_if_needed(); a.hover(); pg.wait_for_timeout(1100)
    items=fr.locator("a.ui-menuitem-link").filter(has_text=_re.compile("variable", _re.I))
    for k in range(items.count()):
        it=items.nth(k)
        try:
            if it.is_visible(): it.click(timeout=4000); break
        except Exception: continue
    pg.wait_for_timeout(1100)
    # dump new (empty) row inputs
    cells=fr.evaluate("""(g)=>{const trs=document.querySelectorAll(`[id='${g}_data'] tr`);
        for(let i=0;i<trs.length;i++){const e=document.getElementById(`${g}:${i}:C0_in`);
          if(e && !e.value.trim()){return {idx:i, inputs:[...trs[i].querySelectorAll('input,select,a[id$=\"_button\"]')].map(x=>({id:x.id.replace(`${g}:${i}:`,''),tag:x.tagName,type:x.type||''}))};}}
        return {idx:-1,inputs:[]};}""", G)
    print("NEW ROW idx:", cells['idx']); [print("   ",c) for c in cells['inputs']]
    # any sub-tab / mapping region (tabs lower on screen)
    tabs=fr.evaluate("""()=>[...document.querySelectorAll(".ui-tabs-nav a,.ui-tabmenuitem a,[role='tab']")].map(e=>e.innerText.trim()).filter(Boolean).slice(0,12)""")
    print("SUB-TABS:", tabs)
    b.close()
print("DONE phase1b_var_recon (no save)")
