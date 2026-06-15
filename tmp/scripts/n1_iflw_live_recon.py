"""READ-ONLY live recon of 'Daily Water Injection Flowline, by Flowline' (N1 build, sibling of PFLW).
Captures: (1) the TREEVIEW MENU PATH (ancestor nodes) for folder placement; (2) nav cascade dd ids +
options; (3) after walking PU/Area/Facility/Flowline to a P1 flowline + GO, the grid id + column headers
+ the ON_STREAM_HRS cell id. NO writes, NO save."""
import time, json
from playwright.sync_api import sync_playwright

URL = "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"
SCREEN = "Daily Water Injection Flowline, by Flowline"
SHOT = "C:/Projects/ChoongYin_OS/tmp/"


def opts(fr, dd):
    try:
        fr.click(f'[id="{dd}_button"]', timeout=4000)
        time.sleep(0.6)
        o = fr.evaluate("""(pid)=>{const p=document.getElementById(pid);if(!p)return null;
          return [...p.querySelectorAll('li,tr')].map(r=>r.getAttribute('data-item-label')).filter(Boolean).slice(0,40);}""", dd+"_panel")
        return o
    except Exception as e:
        return {"err": str(e)[:60]}


def pick(fr, dd, label):
    fr.click(f'[id="{dd}_button"]', timeout=5000); time.sleep(0.6)
    fr.click(f'xpath=//*[@id="{dd}_panel"]//*[normalize-space(@data-item-label)="{label}"]', timeout=5000)
    time.sleep(1.0)


def pick_contains(fr, dd, needle):
    """pick the first option whose label contains needle (case-insensitive)."""
    o = opts(fr, dd)
    if not isinstance(o, list):
        return None
    cand = next((x for x in o if needle.lower() in x.lower()), None)
    if cand:
        fr.click(f'xpath=//*[@id="{dd}_panel"]//*[normalize-space(@data-item-label)="{cand}"]', timeout=5000)
        time.sleep(1.0)
    else:
        # close panel
        try: fr.click(f'[id="{dd}_button"]', timeout=2000)
        except Exception: pass
    return cand


with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    page = b.new_context(ignore_https_errors=True, viewport={"width": 1680, "height": 1000}).new_page()
    page.goto(URL, wait_until="domcontentloaded", timeout=60000)
    page.fill('[id="username"]', "sysadmin"); page.fill('[id="password"]', "sysadmin"); page.click('[id="kc-login"]')
    page.wait_for_selector('[id="menu:searchForm:searchTxt"]', timeout=60000); time.sleep(1.0)
    page.locator('[id="menu:searchForm:searchTxt"]').type(SCREEN, delay=20); time.sleep(1.3)
    # menu path: the tv node + its ancestor labels (best-effort from the tree DOM)
    menu = page.evaluate(r"""(scr)=>{
      const link=[...document.querySelectorAll('.tv-link')].find(e=>e.textContent.trim()===scr);
      if(!link) return {found:false};
      const path=[]; let n=link.closest('li');
      while(n){ const lab=n.querySelector(':scope > .tv-link, :scope > a, :scope > span'); if(lab&&lab.textContent.trim()) path.unshift(lab.textContent.trim()); n=n.parentElement?n.parentElement.closest('li'):null; }
      return {found:true, path};
    }""", SCREEN)
    print("MENU PATH:", json.dumps(menu))
    page.locator(f'xpath=//*[contains(@class,"tv-link") and normalize-space(text())="{SCREEN}"]').first.click()
    page.wait_for_load_state("networkidle", timeout=30000); time.sleep(2.5)
    fr = next((f for f in page.frames if "dashboard.jsf" in (f.url or "") and "top=false" in (f.url or "")), None) or page

    nav = fr.evaluate(r"""()=>{
      const all=[...document.querySelectorAll('[id*="nav:form"]')];
      return {labels: all.filter(e=>/:la$/.test(e.id)).map(e=>({id:e.id,t:(e.textContent||'').trim().slice(0,18)})),
              dates: all.filter(e=>/da_input$/.test(e.id)).map(e=>e.id),
              dds: all.filter(e=>/:dd$/.test(e.id)).map(e=>e.id)};
    }""")
    print("NAV labels:", json.dumps(nav["labels"]))
    print("NAV dates:", json.dumps(nav["dates"]))
    print("NAV dds:", json.dumps(nav["dds"]))

    # set From/To = 2019-12-20 (G:0/G:1 like PFLW), then walk cascade picking P1 at each level
    try:
        fr.fill('[id="nav:form:G:0:R:1:C:0:da_input"]', "2019-12-20")
        fr.fill('[id="nav:form:G:1:R:1:C:0:da_input"]', "2019-12-20")
        time.sleep(0.4)
    except Exception as e: print("date err:", str(e)[:60])
    chosen = {}
    for g, needle in [("2", "P1"), ("3", "P1"), ("4", "P1"), ("5", "P1 F003")]:
        dd = f"nav:form:G:{g}:R:1:C:0:dd"
        if dd in nav["dds"]:
            print(f"G:{g} options:", json.dumps(opts(fr, dd)))
            chosen[g] = pick_contains(fr, dd, needle)
            print(f"  G:{g} picked:", chosen[g])
    # GO
    fr.click('[id="button:form:B"]', timeout=8000)
    page.wait_for_load_state("networkidle", timeout=30000); time.sleep(2.5)
    page.screenshot(path=SHOT+"iflw_after_go.png", full_page=True)
    grid = fr.evaluate(r"""()=>{
      const grids=[...document.querySelectorAll('[id$=":T_data"]')].map(e=>e.id);
      const headers=[...document.querySelectorAll('th .ui-column-title, th span')].map(e=>(e.textContent||'').trim()).filter(Boolean).slice(0,40);
      const cells=[...document.querySelectorAll('[id*=":T:0:"] input, [id*=":T:0:"] textarea')].map(e=>e.id).slice(0,40);
      return {grids, headers, cells};
    }""")
    print("\nGRIDS:", json.dumps(grid["grids"]))
    print("HEADERS:", json.dumps(grid["headers"]))
    print("ROW0 CELL IDS:", json.dumps(grid["cells"]))
    b.close()
print("DONE")
