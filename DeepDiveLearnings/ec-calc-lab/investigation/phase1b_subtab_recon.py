"""Phase 1b recon (READ-ONLY): select an existing variable, study the DEFINITION sub-tab fields +
the READ MAPPINGS sub-grid (columns, cell ids, insert gesture) so I can CLONE it for Var B. No save."""
from playwright.sync_api import sync_playwright
import os, json
EC_URL=os.environ.get('EC_URL','https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/')
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
    # select first variable row (click name cell)
    name0=fr.evaluate("(g)=>{const e=document.getElementById(`${g}:0:C0_in`);return e?e.value:'';}", G)
    print("selecting row 0 variable:", name0)
    fr.locator(cell(f'{G}:0:C0_in')).click(); pg.wait_for_timeout(1200)
    def dump_tab(label):
        # click the sub-tab by its (CSS-uppercased) text, case-insensitive
        tab=fr.locator("xpath=//a[contains(@class,'ui-tabs-anchor') or @role='tab' or contains(@class,'ui-menuitem-link')][contains(translate(.,'abcdefghijklmnopqrstuvwxyz','ABCDEFGHIJKLMNOPQRSTUVWXYZ'),%s)]" % json.dumps(label.upper()))
        if tab.count()>0:
            try: tab.first.click(timeout=5000); pg.wait_for_timeout(1100)
            except Exception as e: print("  tab click note:",str(e)[:60])
        # dump inputs + any sub-grid in the active tab panel
        info=fr.evaluate("""()=>{const out={inputs:[],grids:[]};
            const panels=[...document.querySelectorAll(".ui-tabs-panel,[role='tabpanel']")].filter(p=>getComputedStyle(p).display!=='none');
            const scope=panels.length?panels:[document.body];
            scope.forEach(pl=>{
              pl.querySelectorAll("input:not([type=hidden]),select,a[id$='_button']").forEach(e=>{const r=e.getBoundingClientRect();
                 if(r.width>0)out.inputs.push({id:e.id.slice(-46),type:e.type||e.tagName});});
              pl.querySelectorAll("[id$='T_data']").forEach(t=>out.grids.push({id:t.id,rows:t.querySelectorAll('tr').length,
                 heads:[...t.closest("[id$='_data']").parentElement.querySelectorAll('thead th')].map(h=>h.innerText.trim()).filter(Boolean)}));
            });
            return out;}""")
        print("  inputs:", info['inputs'][:14])
        print("  grids:", info['grids'][:4])
    print("\n--- DEFINITION tab ---"); dump_tab('Definition')
    print("\n--- READ MAPPINGS tab ---"); dump_tab('Read Mappings')
    b.close()
print("DONE phase1b_subtab_recon (no save)")
