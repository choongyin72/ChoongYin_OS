"""WR.0001 final scope test (READ-ONLY): date 2003-01-01 -> PU -> Area -> Facility Class 1/Well
Hookup cascade -> GO -> capture grid id + headers + editable cell ids. Tests whether FC1/WH
cascade from Area (vs groupmodel-empty)."""
import os, time, json
from pathlib import Path
from playwright.sync_api import sync_playwright

URL = "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"
SCREEN = "Daily Production Well Status 1"
DATE = os.environ.get("EC_DATE", "2003-01-01")
PU = os.environ.get("EC_PU", "AS2 EC Exploration Norway")
OUT = Path(r"c:/Projects/ChoongYin_OS/tmp/wr0001_recon"); OUT.mkdir(parents=True, exist_ok=True)

def dd_opts(fr, g):
    fr.locator(f'[id="nav:form:G:{g}:R:1:C:0:dd_button"]').click(timeout=4000); time.sleep(0.7)
    o = fr.evaluate(f"""() => [...document.querySelectorAll('[id="nav:form:G:{g}:R:1:C:0:dd_panel"] tr[data-item-label]')]
        .map(e=>(e.getAttribute('data-item-label')||'').trim()).filter(t=>t)""")
    return o

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

    fr.locator('[id="nav:form:G:0:R:1:C:0:da_input"]').fill(DATE)
    fr.locator('[id="nav:form:G:0:R:1:C:0:da_input"]').press("Tab"); time.sleep(1.5)
    print("date set:", DATE)

    pus = dd_opts(fr, 1)
    print("PU options:", len(pus))
    pick_pu = PU if PU in pus else (pus[0] if pus else None)
    dd_pick(fr, 1, pick_pu); print("PU picked:", pick_pu)

    areas = dd_opts(fr, 2)
    print("AREA options:", len(areas), areas[:8])
    if areas:
        dd_pick(fr, 2, areas[0]); print("AREA picked:", areas[0])
        fc = dd_opts(fr, 3); print("FC1 options after Area:", len(fc), fc[:8])
        if fc:
            dd_pick(fr, 3, fc[0]); print("FC1 picked:", fc[0])
        else:
            wh = dd_opts(fr, 4); print("WH options after Area:", len(wh), wh[:8])
            if wh: dd_pick(fr, 4, wh[0]); print("WH picked:", wh[0])

    # also try selecting the Well Hookup (most specific scope) if it now has options
    wh = dd_opts(fr, 4)
    print("WH options (after FC1):", len(wh), wh[:8])
    if wh:
        dd_pick(fr, 4, wh[0]); print("WH picked:", wh[0])

    # GO
    try:
        fr.locator('[id="button:form:B"]').click(timeout=5000)
        page.wait_for_load_state("networkidle", timeout=30000); time.sleep(6.0); print("GO clicked")
    except Exception as e:
        print("GO failed:", str(e)[:100])

    DUMP = """() => {
      const vis=e=>e&&e.offsetParent!==null;
      const tbls=[...document.querySelectorAll('[id$="T_data"], table.ui-datatable-data, tbody[id*=":"]')].filter(vis)
        .map(t=>({id:t.id, tag:t.tagName.toLowerCase(), rows:t.querySelectorAll('tr').length}));
      let headers=[], row0=[];
      const first=[...document.querySelectorAll('[id$="T_data"]')].find(vis);
      if(first){const base=first.id.replace(/_data$/,'');
        headers=[...document.querySelectorAll('[id="'+base+'_head"] th')].map(th=>(th.textContent||'').trim()).filter(t=>t);
        row0=[...document.querySelectorAll('[id^="'+base+':0:"]')].map(e=>({id:e.id,type:e.type||e.tagName.toLowerCase()})).filter(c=>/(_in|:in|_dd_input|_cb|_da_input|:dd)$/.test(c.id));
      }
      const msgs=[...document.querySelectorAll('.ui-messages-error-summary,.ui-growl-message,.ui-message-error-detail')].map(e=>(e.textContent||'').trim()).filter(t=>t);
      const inputs=[...document.querySelectorAll('input[id*=":T:"], input[id*=":data:"]')].filter(vis).slice(0,5).map(e=>e.id);
      return {tbls,headers,row0,msgs,sampleInputs:inputs};
    }"""
    found = []
    for f in page.frames:
        try:
            g = f.evaluate(DUMP)
            g["_url"] = f.url[:110]
            if g["tbls"] or g["headers"] or g["row0"] or g["msgs"] or g["sampleInputs"]:
                found.append(g)
        except Exception as e:
            pass
    (OUT/"grid_final.json").write_text(json.dumps(found, indent=2), encoding="utf-8")
    page.screenshot(path=str(OUT/"grid_final.png"), full_page=True)
    print("\n=== ALL FRAMES after GO ===  (frame count:", len(page.frames), ")")
    for g in found:
        print("FRAME", g["_url"])
        print("  tables:", g["tbls"])
        print("  headers:", g["headers"][:25])
        print("  row0:", json.dumps(g["row0"][:25]))
        print("  sampleInputs:", g["sampleInputs"])
        print("  msgs:", g["msgs"])
    browser.close()
print("DONE")
