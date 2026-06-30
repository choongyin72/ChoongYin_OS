"""Phase 1a recon v3 (READ-ONLY): label the Simple Object Types columns - dump header text +
2 existing rows' cell values + the C3 dropdown options (likely DATA_TYPE). No insert, no save."""
from playwright.sync_api import sync_playwright
import os
EC_URL=os.environ.get('EC_URL','https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/')
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
    hdr=fr.evaluate("""(g)=>{const t=document.getElementById(g); if(!t)return[];
        const ths=t.querySelectorAll("thead th, .ui-datatable-thead th"); return [...ths].map(e=>e.innerText.trim()).filter(x=>x!=='');}""", G)
    print("HEADERS:", hdr)
    rows=fr.evaluate("""(g)=>{const out=[];const trs=document.querySelectorAll(`[id='${g}_data'] tr`);
        for(let i=0;i<Math.min(3,trs.length);i++){out.push([...trs[i].querySelectorAll('td')].map(td=>td.innerText.trim()).slice(0,6));}
        return out;}""", G)
    print("EXISTING ROWS (first 3):"); [print("   ",r) for r in rows]
    # open C3 dd on an existing row to see the data-type options (read-only)
    ddb=fr.locator(cell(G+':0:C3_dd_button'))
    if ddb.count()>0:
        ddb.click(); pg.wait_for_timeout(700)
        opts=fr.evaluate("""(g)=>[...document.querySelectorAll(`[id='${g}:0:C3_dd_panel'] tr`)].map(t=>t.getAttribute('data-item-label')||t.innerText.trim()).filter(Boolean).slice(0,12)""", G)
        print("C3 dd options:", opts)
    b.close()
print("DONE recon3 (no save)")
