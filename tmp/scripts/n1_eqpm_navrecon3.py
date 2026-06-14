"""Targeted: 'Daily Equipment Status' @2024-02-06, PU='P1 Production Unit', Area='P1 Area', then dump
G3 (FacilityClass1) options, pick the P1 facility, GO, dump grid (equipment names per row + editable
cell ids). Read-only."""
import time, json
from playwright.sync_api import sync_playwright
URL="https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"; SCREEN="Daily Equipment Status"; DATE="2024-02-06"
def opts(fr,g):
    fr.locator(f'[id="nav:form:G:{g}:R:1:C:0:dd_button"]').click(timeout=4000); time.sleep(0.7)
    return fr.evaluate(f"""()=>[...document.querySelectorAll('[id="nav:form:G:{g}:R:1:C:0:dd_panel"] tr[data-item-label]')].map(e=>(e.getAttribute('data-item-label')||'').trim()).filter(t=>t)""")
def pick(fr,g,l): fr.locator(f'[id="nav:form:G:{g}:R:1:C:0:dd_panel"] tr[data-item-label="{l}"]').first.click(timeout=4000); time.sleep(1.1)
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
    g1=opts(fr,1); pu=next((o for o in g1 if o.strip()=="P1 Production Unit"), None) or next((o for o in g1 if "P1" in o), None)
    print("PU pick:", pu); pick(fr,1,pu)
    g2=opts(fr,2); print("G2 areas:", json.dumps(g2[:8])); area=next((o for o in g2 if "P1" in o), g2[0] if g2 else None); pick(fr,2,area); print("Area pick:", area)
    g3=opts(fr,3); print("G3 facilities:", json.dumps(g3[:10])); fac=next((o for o in g3 if o.strip()=="P1 Facility 1"), g3[0] if g3 else None)
    if fac: pick(fr,3,fac); print("Facility pick:", fac)
    fr.locator('[id="button:form:B"]').click(timeout=5000); page.wait_for_load_state("networkidle",timeout=30000); time.sleep(2.5)
    res=fr.evaluate("""()=>{const ts=[...document.querySelectorAll('[id$=":T_data"]')];let best=null,bn=0;ts.forEach(t=>{const n=t.querySelectorAll('tr').length;if(n>bn){bn=n;best=t;}});
      if(!best)return {gid:'',rows:0};
      const trs=[...best.querySelectorAll('tr')].filter(r=>r.querySelector('td'));
      return {gid:best.id, rows:trs.length,
        sample: trs.slice(0,5).map(r=>({txt:(r.textContent||'').replace(/\\s+/g,' ').trim().slice(0,45), inputs:[...r.querySelectorAll('input[id*=\":C\"]')].map(x=>x.id)}))};}""")
    print("GRID:", json.dumps(res, indent=1)[:1600])
    page.screenshot(path="c:/Projects/ChoongYin_OS/tmp/n1_eqpm_nav2.png", full_page=True)
    b.close()
print("DONE")
