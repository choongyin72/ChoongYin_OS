"""Targeted recon: land 'Daily Water Injection Well Status' on data. Try PU=AS5_Injection then AS2,
cascade first-option through Area/FC1/WellHookup, GO, dump grid rows + editable cell ids + resolve
which well (row) maps to a cell. Read-only."""
import time, json
from playwright.sync_api import sync_playwright
URL="https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"
SCREEN="Daily Water Injection Well Status"; DATE="2026-02-13"

def opts(fr,g):
    fr.locator(f'[id="nav:form:G:{g}:R:1:C:0:dd_button"]').click(timeout=4000); time.sleep(0.7)
    return fr.evaluate(f"""()=>[...document.querySelectorAll('[id="nav:form:G:{g}:R:1:C:0:dd_panel"] tr[data-item-label]')].map(e=>(e.getAttribute('data-item-label')||'').trim()).filter(t=>t)""")
def pick(fr,g,label):
    fr.locator(f'[id="nav:form:G:{g}:R:1:C:0:dd_panel"] tr[data-item-label="{label}"]').first.click(timeout=4000); time.sleep(1.1)
def grid_state(fr):
    return fr.evaluate("""()=>{const t=document.getElementById('daily_well_status:form:T_data'); if(!t)return {rows:0,sample:[],cells:[]};
      const trs=[...t.querySelectorAll('tr')]; const tr=trs.find(r=>r.querySelector('td'));
      const sample=tr?[...tr.querySelectorAll('td')].map(td=>(td.textContent||'').trim()).slice(0,8):[];
      const cells=[...t.querySelectorAll('input[id*=":C"]')].map(i=>i.id).slice(0,16);
      const names=trs.map(r=>(r.textContent||'').replace(/\\s+/g,' ').trim().slice(0,40)).filter(x=>x).slice(0,8);
      return {rows:trs.length, sample, cells, names};}""")

with sync_playwright() as p:
    b=p.chromium.launch(headless=True); page=b.new_context(ignore_https_errors=True,viewport={"width":1680,"height":1000}).new_page()
    page.goto(URL,wait_until="domcontentloaded",timeout=60000)
    page.fill('[id="username"]',"sysadmin"); page.fill('[id="password"]',"sysadmin"); page.click('[id="kc-login"]')
    page.wait_for_selector('[id="menu:searchForm:searchTxt"]',timeout=60000); time.sleep(1.0)
    sel=f'xpath=//*[contains(@class,"tv-link") and normalize-space(text())="{SCREEN}"]'
    page.fill('[id="menu:searchForm:searchTxt"]',""); page.locator('[id="menu:searchForm:searchTxt"]').type(SCREEN,delay=35)
    page.wait_for_selector(sel,timeout=12000); page.locator(sel).first.click()
    page.wait_for_load_state("networkidle",timeout=30000); time.sleep(2.0)
    fr=next((f for f in page.frames if "dashboard.jsf" in (f.url or "") and "top=false" in (f.url or "")),None) or page

    for puwant in ["AS5_Injection Production Unit","AS2 EC Exploration Norway"]:
        print(f"\n##### TRY PU = {puwant} #####")
        try:
            di=fr.locator('[id="nav:form:G:0:R:1:C:0:da_input"]'); di.fill(DATE); di.press("Tab"); time.sleep(1.0)
            g1=opts(fr,1); pu=next((o for o in g1 if puwant.lower() in o.lower()), None)
            if not pu: print("  PU not found"); continue
            pick(fr,1,pu); print("  PU:",pu)
            for g in (2,3,4):
                o=opts(fr,g); print(f"  G:{g} opts:", json.dumps(o[:8]))
                if o: pick(fr,g,o[0]); print(f"  G:{g} picked:",o[0])
                else: print(f"  G:{g} EMPTY");
            fr.locator('[id="button:form:B"]').click(timeout=5000); page.wait_for_load_state("networkidle",timeout=30000); time.sleep=getattr(time,'sleep'); time.sleep(2.5)
            gs=grid_state(fr)
            print("  GRID rows=",gs["rows"]," names=",json.dumps(gs["names"]))
            print("  sample=",json.dumps(gs["sample"]))
            print("  cells=",json.dumps(gs["cells"]))
            if gs["rows"]>1 and gs["cells"]:
                print("  >>> DATA LOADED for",puwant); break
        except Exception as e: print("  ERR",str(e)[:90])
    page.screenshot(path="c:/Projects/ChoongYin_OS/tmp/n1_iwel_recon2.png", full_page=True)
    b.close()
print("DONE")
