"""Final scope recon: AS2 / AS2_Onshore Area / AS2_Production Facility no 1 / AS2_Water Injection
Manifold 1 @ 2026-02-13 -> dump injection-well grid (well names per row) + editable cell ids +
column header labels (to plan the cell<->IWEL column mapping). Read-only."""
import time, json
from playwright.sync_api import sync_playwright
URL="https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"
SCREEN="Daily Water Injection Well Status"; DATE="2026-02-13"
SCOPE=[(1,"AS2 EC Exploration Norway"),(2,"AS2_Onshore Area"),(3,"AS2_Production Facility no 1"),(4,"AS2_Water Injection Manifold 1")]

def opts(fr,g):
    fr.locator(f'[id="nav:form:G:{g}:R:1:C:0:dd_button"]').click(timeout=4000); time.sleep(0.7)
    return fr.evaluate(f"""()=>[...document.querySelectorAll('[id="nav:form:G:{g}:R:1:C:0:dd_panel"] tr[data-item-label]')].map(e=>(e.getAttribute('data-item-label')||'').trim()).filter(t=>t)""")
def pick(fr,g,label):
    fr.locator(f'[id="nav:form:G:{g}:R:1:C:0:dd_panel"] tr[data-item-label="{label}"]').first.click(timeout=4000); time.sleep(1.1)

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
    di=fr.locator('[id="nav:form:G:0:R:1:C:0:da_input"]'); di.fill(DATE); di.press("Tab"); time.sleep(1.0)
    for g,label in SCOPE:
        o=opts(fr,g)
        if label not in o: print(f"G:{g} '{label}' NOT in {o[:6]}");
        pick(fr,g,label); print(f"G:{g} picked {label}")
    fr.locator('[id="button:form:B"]').click(timeout=5000); page.wait_for_load_state("networkidle",timeout=30000); time.sleep(2.5)
    res=fr.evaluate("""()=>{
      const t=document.getElementById('daily_well_status:form:T_data'); if(!t)return {err:'no grid'};
      const rows=[...t.querySelectorAll('tr')].map((tr,i)=>({i, txt:(tr.textContent||'').replace(/\\s+/g,' ').trim().slice(0,60),
         inputs:[...tr.querySelectorAll('input[id*=":C"]')].map(x=>x.id)})).filter(r=>r.txt);
      // column header labels from the screen (th)
      const heads=[...document.querySelectorAll('[id^="daily_well_status:form"] th')].map(h=>(h.textContent||'').trim()).filter(x=>x).slice(0,30);
      return {nrows:rows.length, rows:rows.slice(0,6), heads};
    }""")
    print("\nRESULT:", json.dumps(res, indent=1)[:1800])
    page.screenshot(path="c:/Projects/ChoongYin_OS/tmp/n1_iwel_recon3.png", full_page=True)
    b.close()
print("DONE")
