"""Phase 1a recon (READ-ONLY, unsaved row discarded): Simple Object Types screen.
Dump the navigator fields+labels, click GO, find the grid + insert toolbar, click insert,
dump the new blank-row cell ids (so I know what to fill), then CLOSE without Save (safe)."""
from playwright.sync_api import sync_playwright
import os, json
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
    fr=None
    for f in pg.frames:
        if 'simple' in f.url.lower() or f.url.endswith('dashboard.jsf?top=false'):
            if f.evaluate("()=>!!document.querySelector(\"[id^='nav:form']\")"): fr=f; break
    if not fr:
        for f in pg.frames:
            if f.evaluate("()=>!!document.querySelector(\"[id^='nav:form']\")"): fr=f; break
    print("content frame:", fr.url[-40:] if fr else None)
    # dump navigator fields + their label text
    navf=fr.evaluate("""()=>[...document.querySelectorAll("[id^='nav:form'] input, [id^='nav:form'] select, [id^='nav:form'] [id$='_button']")].map(e=>{
        const r=e.getBoundingClientRect(); let lab='';
        const cellEl=e.closest("td,div"); if(cellEl){const prev=cellEl.previousElementSibling; if(prev) lab=prev.innerText.trim();}
        return {id:e.id, tag:e.tagName, type:e.type||'', label:lab.slice(0,30)};
      }).filter(o=>o.id)""")
    print("NAV fields:"); [print("   ",n) for n in navf]
    # fill date if present, choose first context option if a dd exists, GO
    d=fr.locator(cell('nav:form:G:0:R:1:C:0:da_input'))
    if d.count()>0:
        d.click(); d.fill('2003-01-01'); fr.locator('body').press('Tab'); pg.wait_for_timeout(400)
    go=fr.locator(cell('button:form:B'))
    if go.count()>0: go.click(); wa(pg)
    g=fr.evaluate("""()=>{const e=document.querySelector("[id$='T_data']");return e?e.id:''}""")
    print("grid id after GO:", g, " rows:", fr.evaluate("()=>document.querySelectorAll(\"[id$='T_data'] tr\").length"))
    # find + click the insert toolbar (a wrapping span.ui-icon-insert), then dump new-row inputs
    ins=fr.locator("xpath=//a[.//span[contains(@class,'ui-icon-insert')]]")
    print("insert anchors:", ins.count())
    if ins.count()>0:
        try:
            ins.first.click(); pg.wait_for_timeout(800)
            # a submenu may appear listing the grid name; capture it
            menu=fr.evaluate("""()=>[...document.querySelectorAll(".ui-menuitem-text,.ui-menuitem-link")].map(e=>e.innerText.trim()).filter(Boolean).slice(0,8)""")
            if menu: print("insert submenu:", menu)
        except Exception as e: print("insert click note:", str(e)[:80])
        pg.wait_for_timeout(600)
        cells=fr.evaluate("""()=>{const out=[];const rows=document.querySelectorAll("[id$='T_data'] tr");
            const tr=rows[0]; if(!tr) return out;
            tr.querySelectorAll("input,select,a[id$='_button']").forEach(e=>out.push({id:e.id,tag:e.tagName,type:e.type||'',cls:(e.className||'').slice(0,18)}));
            return out;}""")
        print("NEW ROW 0 inputs:"); [print("   ",c) for c in cells]
        # column headers for context
        hdr=fr.evaluate("""()=>[...document.querySelectorAll("[id$='T'] th, .ui-datatable-thead th, [id$='_head'] th")].map(e=>e.innerText.trim()).filter(Boolean).slice(0,10)""")
        print("HEADERS:", hdr)
    # do NOT save -> unsaved row discarded
    b.close()
print("DONE phase1_simpletype_recon (no save)")
