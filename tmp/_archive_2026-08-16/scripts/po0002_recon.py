"""Recon PO.0002 Daily Gas Stream Status (READ-ONLY): URL/CLASS_NAME, nav cascade, then drive the
known-good AS2 scope (Date->PU->Area->Facility Class 1) + GO and dump the grid id + row0 cells +
stream name. Confirms the N1 pattern generalizes to a STREAM screen."""
import time, json
from playwright.sync_api import sync_playwright
URL="https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"; TERM="Daily Gas Stream Status"
def dd_opts(fr,g):
    fr.locator(f'[id="nav:form:G:{g}:R:1:C:0:dd_button"]').click(timeout=5000); time.sleep(0.8)
    return fr.evaluate(f"""()=>[...document.querySelectorAll('[id="nav:form:G:{g}:R:1:C:0:dd_panel"] tr[data-item-label]')].map(e=>(e.getAttribute('data-item-label')||'').trim()).filter(t=>t)""")
def dd_pick(fr,g,l):
    fr.locator(f'[id="nav:form:G:{g}:R:1:C:0:dd_panel"] tr[data-item-label="{l}"]').first.click(timeout=5000); time.sleep(1.2)
with sync_playwright() as p:
    b=p.chromium.launch(headless=True); page=b.new_context(ignore_https_errors=True,viewport={"width":1680,"height":1000}).new_page()
    page.goto(URL,wait_until="domcontentloaded",timeout=60000)
    page.fill('[id="username"]',"sysadmin"); page.fill('[id="password"]',"sysadmin"); page.click('[id="kc-login"]')
    page.wait_for_selector('[id="menu:searchForm:searchTxt"]',timeout=60000)
    sel='xpath=//*[contains(@class,"tv-link") and normalize-space(text())="Daily Gas Stream Status"]'; fr=None
    for attempt in range(3):
        page.fill('[id="menu:searchForm:searchTxt"]',""); page.locator('[id="menu:searchForm:searchTxt"]').type(TERM, delay=40)
        page.wait_for_selector(sel, timeout=15000); time.sleep(0.6); page.locator(sel).first.click()
        page.wait_for_load_state("networkidle",timeout=30000)
        for _ in range(25):
            fr=next((f for f in page.frames if ".screens/" in f.url and "dashboard" not in f.url),None)
            if fr: break
            time.sleep(1.0)
        if fr: break
    if not fr: print("NOT LOADED"); b.close(); raise SystemExit
    time.sleep(2.0)
    print("SCREEN URL:", fr.url)
    # drive known-good AS2 scope
    fr.locator('[id="nav:form:G:0:R:1:C:0:da_input"]').fill("2003-01-01"); fr.locator('[id="nav:form:G:0:R:1:C:0:da_input"]').press("Tab"); time.sleep(1.5)
    o1=dd_opts(fr,1); print("PU opts(5):",o1[:5]); dd_pick(fr,1,"AS2 EC Exploration Norway")
    o2=dd_opts(fr,2); print("AREA opts:",o2[:5])
    if o2: dd_pick(fr,2,"AS2_Onshore Area" if "AS2_Onshore Area" in o2 else o2[0])
    o3=dd_opts(fr,3); print("FC1 opts:",o3[:5])
    if o3: dd_pick(fr,3,"AS2_Production Facility no 1" if "AS2_Production Facility no 1" in o3 else o3[0])
    fr.locator('[id="button:form:B"]').click(timeout=6000); page.wait_for_load_state("networkidle",timeout=30000); time.sleep(3.5)
    grid=fr.evaluate("""()=>{
      const vis=e=>e&&e.offsetParent!==null;
      const tbls=[...document.querySelectorAll('[id$="T_data"]')].filter(vis).map(t=>({id:t.id,rows:t.querySelectorAll('tr').length}));
      const first=[...document.querySelectorAll('[id$="T_data"]')].find(vis); let row0=[], name='';
      if(first){const tr=first.querySelector('tr'); if(tr){name=(tr.textContent||'').trim().slice(0,40);
        tr.querySelectorAll('td').forEach((td,i)=>{const inp=td.querySelector('input'); if(inp&&inp.value)row0.push({c:i,id:inp.id.split(':').pop(),v:inp.value});});}}
      const msgs=[...document.querySelectorAll('.ui-messages-error-summary,.ui-growl-message')].map(e=>(e.textContent||'').trim()).filter(t=>t);
      return {tbls,name,row0,msgs};
    }""")
    print("GRID:", json.dumps(grid, indent=1)[:1500])
    b.close()
print("DONE")
