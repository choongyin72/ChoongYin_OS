"""Render the WR.0001 grid (full scope) and read row-0/1 well names + cell values (READ-ONLY).
Prep for pinning ROW0_WELL_NAME + the cell<->DB-column mapping. No writes."""
import time, json
from pathlib import Path
from playwright.sync_api import sync_playwright

URL = "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"
SCREEN = "Daily Production Well Status 1"
OUT = Path(r"c:/Projects/ChoongYin_OS/tmp/wr0001_recon")

def dd_opts(fr, g):
    fr.locator(f'[id="nav:form:G:{g}:R:1:C:0:dd_button"]').click(timeout=4000); time.sleep(0.7)
    return fr.evaluate(f"""() => [...document.querySelectorAll('[id="nav:form:G:{g}:R:1:C:0:dd_panel"] tr[data-item-label]')].map(e=>(e.getAttribute('data-item-label')||'').trim()).filter(t=>t)""")
def dd_pick(fr, g, label):
    fr.locator(f'[id="nav:form:G:{g}:R:1:C:0:dd_panel"] tr[data-item-label="{label}"]').first.click(timeout=4000); time.sleep(1.0)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_context(ignore_https_errors=True, viewport={"width":1920,"height":1080}).new_page()
    page.goto(URL, wait_until="domcontentloaded", timeout=60000)
    page.fill('[id="username"]',"sysadmin"); page.fill('[id="password"]',"sysadmin"); page.click('[id="kc-login"]')
    page.wait_for_selector('[id="menu:searchForm:searchTxt"]', timeout=60000)
    sel=f'xpath=//*[contains(@class,"tv-link") and normalize-space(text())="{SCREEN}"]'
    fr=None
    for _ in range(2):
        page.fill('[id="menu:searchForm:searchTxt"]',""); page.locator('[id="menu:searchForm:searchTxt"]').type(SCREEN, delay=40)
        page.wait_for_selector(sel, timeout=15000); time.sleep(0.6); page.locator(sel).first.click()
        page.wait_for_load_state("networkidle", timeout=30000)
        for _ in range(25):
            fr=next((f for f in page.frames if "daily_well_status" in f.url), None)
            if fr: break
            time.sleep(1.0)
        if fr: break
    if not fr: print("no frame"); browser.close(); raise SystemExit
    time.sleep(2.0)
    fr.locator('[id="nav:form:G:0:R:1:C:0:da_input"]').fill("2003-01-01"); fr.locator('[id="nav:form:G:0:R:1:C:0:da_input"]').press("Tab"); time.sleep(1.5)
    dd_opts(fr,1); dd_pick(fr,1,"AS2 EC Exploration Norway")
    dd_opts(fr,2); dd_pick(fr,2,"AS2_Onshore Area")
    dd_opts(fr,3); dd_pick(fr,3,"AS2_Production Facility no 1")
    dd_opts(fr,4); dd_pick(fr,4,"AS2_Lift Gas Manifold 1")
    fr.locator('[id="button:form:B"]').click(timeout=5000); page.wait_for_load_state("networkidle", timeout=30000); time.sleep(4.0)

    # read each grid row: the text of every cell + the value of every input cell
    grid = fr.evaluate("""() => {
      const tb=document.getElementById('daily_well_status:form:T_data'); if(!tb) return {err:'no grid'};
      const out=[];
      tb.querySelectorAll('tr').forEach((tr,ri)=>{
        const cells=[];
        tr.querySelectorAll('td').forEach(td=>{
          const inp=td.querySelector('input,select');
          cells.push({txt:(td.textContent||'').trim().slice(0,20), inId: inp?inp.id:null, inVal: inp?inp.value:null});
        });
        out.push({ri, cells});
      });
      return {rows: out.length, data: out};
    }""")
    (OUT/"grid_rows.json").write_text(json.dumps(grid, indent=2), encoding="utf-8")
    print("rows:", grid.get("rows"))
    for r in grid.get("data", [])[:2]:
        print(f"\n--- ROW {r['ri']} ---")
        for ci,c in enumerate(r["cells"]):
            if c["txt"] or c["inId"]:
                print(f"  c{ci}: txt={c['txt']!r} inId={c['inId']} val={c['inVal']!r}")
    browser.close()
print("DONE")
