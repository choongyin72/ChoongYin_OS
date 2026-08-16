"""Land 'Daily Equipment Status' on data. Date 2024-02-06; try each PU (G1), cascade G2/G3 first-opt,
GO, check grid for equipment rows + editable cells. Find the scope that loads. Read-only."""
import time, json
from playwright.sync_api import sync_playwright
URL="https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"; SCREEN="Daily Equipment Status"; DATE="2024-02-06"
def opts(fr,g):
    try:
        fr.locator(f'[id="nav:form:G:{g}:R:1:C:0:dd_button"]').click(timeout=4000); time.sleep(0.7)
        return fr.evaluate(f"""()=>[...document.querySelectorAll('[id="nav:form:G:{g}:R:1:C:0:dd_panel"] tr[data-item-label]')].map(e=>(e.getAttribute('data-item-label')||'').trim()).filter(t=>t)""")
    except Exception: return []
def pick(fr,g,l):
    try: fr.locator(f'[id="nav:form:G:{g}:R:1:C:0:dd_panel"] tr[data-item-label="{l}"]').first.click(timeout=4000); time.sleep(1.0); return True
    except Exception: return False
def grid(fr):
    return fr.evaluate("""()=>{const ts=[...document.querySelectorAll('[id$=":T_data"]')];
      let best=null,bn=0; ts.forEach(t=>{const n=t.querySelectorAll('tr').length; if(n>bn){bn=n;best=t;}});
      if(!best)return {gid:'',rows:0,names:[],cells:[]};
      const trs=[...best.querySelectorAll('tr')];
      const names=trs.map(r=>(r.textContent||'').replace(/\\s+/g,' ').trim().slice(0,38)).filter(x=>x).slice(0,6);
      const cells=[...best.querySelectorAll('input[id*=":T:"][id*=":C"]')].map(i=>i.id).slice(0,14);
      return {gid:best.id, rows:trs.length, names, cells};}""")
with sync_playwright() as p:
    b=p.chromium.launch(headless=True); page=b.new_context(ignore_https_errors=True,viewport={"width":1680,"height":1000}).new_page()
    page.goto(URL,wait_until="domcontentloaded",timeout=60000)
    page.fill('[id="username"]',"sysadmin"); page.fill('[id="password"]',"sysadmin"); page.click('[id="kc-login"]')
    page.wait_for_selector('[id="menu:searchForm:searchTxt"]',timeout=60000); time.sleep(1.0)
    sel=f'xpath=//*[contains(@class,"tv-link") and normalize-space(text())="{SCREEN}"]'
    page.fill('[id="menu:searchForm:searchTxt"]',""); page.locator('[id="menu:searchForm:searchTxt"]').type(SCREEN,delay=35)
    page.wait_for_selector(sel,timeout=12000); page.locator(sel).first.click(); page.wait_for_load_state("networkidle",timeout=30000); time.sleep(2.0)
    fr=next((f for f in page.frames if "dashboard.jsf" in (f.url or "") and "top=false" in (f.url or "")),None) or page
    fr.locator('[id="nav:form:G:0:R:1:C:0:da_input"]').fill(DATE); fr.locator('[id="nav:form:G:0:R:1:C:0:da_input"]').press("Tab"); time.sleep(1.0)
    pus=opts(fr,1); print("PUs:", json.dumps(pus))
    found=False
    for pu in pus:
        if not any(k in pu for k in ("AS3","Offshore","Onshore","AS2","P1","Production Unit")):
            pass
        # reset date+PU
        pick(fr,1,pu)
        g2=opts(fr,2)
        if not g2: continue
        pick(fr,2,g2[0])
        g3=opts(fr,3)
        if not g3: continue
        pick(fr,3,g3[0])
        try: fr.locator('[id="button:form:B"]').click(timeout=5000); page.wait_for_load_state("networkidle",timeout=25000); time.sleep(2.0)
        except Exception: pass
        gs=grid(fr)
        if gs["rows"]>1 and gs["cells"]:
            print(f">>> LOADED: PU={pu} / {g2[0]} / {g3[0]}")
            print("   grid:", gs["gid"], "rows", gs["rows"]); print("   names:", json.dumps(gs["names"])); print("   cells:", json.dumps(gs["cells"]))
            found=True; break
        else:
            print(f"  {pu} / {g2[0]} / {g3[0]} -> rows {gs['rows']} (no data)")
    if not found: print("no scope loaded equipment rows")
    page.screenshot(path="c:/Projects/ChoongYin_OS/tmp/n1_eqpm_nav.png", full_page=True)
    b.close()
print("DONE")
