"""READ-ONLY: select exemplar CO2_InitialNStdVol, open READ MAPPINGS, dump the exact cell VALUES of
the readMapping row + attrMapping (class-key) rows, so Var B can clone them faithfully. No save."""
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
    idx=fr.evaluate("""(g)=>{const trs=document.querySelectorAll(`[id='${g}_data'] tr`);
        for(let i=0;i<trs.length;i++){const e=document.getElementById(`${g}:${i}:C0_in`); if(e&&e.value.trim()==='CO2_InitialNStdVol')return i;}return -1;}""", G)
    print("exemplar row idx:", idx)
    if idx<0: print("not on first page"); b.close(); raise SystemExit(1)
    fr.locator(cell(f'{G}:{idx}:C0_in')).click(); pg.wait_for_timeout(1200)
    rm=fr.locator("xpath=//a[contains(translate(.,'abcdefghijklmnopqrstuvwxyz','ABCDEFGHIJKLMNOPQRSTUVWXYZ'),'READ MAPPINGS')]")
    if rm.count()>0: rm.first.click(timeout=5000); pg.wait_for_timeout(1100)
    def grid_vals(gid):
        return fr.evaluate("""(g)=>{const out=[];const trs=document.querySelectorAll(`[id='${g}_data'] tr`);
            for(let i=0;i<trs.length;i++){const row={};
              trs[i].querySelectorAll("input,select").forEach(e=>{const m=e.id.match(/:(C\\d+)(_dd)?(_input|_in|_hinput)?$/);
                if(m && e.type!=='hidden' && e.value!=='')row[m[1]]=e.value;});
              if(Object.keys(row).length)out.push(row);}
            return out;}""", gid)
    print("readMapping rows:", grid_vals('tab:tabPanel:readMapping:form:T'))
    print("attrMapping(classkey) rows:", grid_vals('tab:tabPanel:attrMapping:form:T'))
    b.close()
print("DONE mapping_values_recon (no save)")
