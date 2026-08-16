"""Diagnose the WR.0001 inline-grid EDIT + SAVE gesture (mostly READ-ONLY; tries one edit but
does NOT save). Why did Save stay disabled? Inspect the C4 cell structure + toolbar controls."""
import time, json
from playwright.sync_api import sync_playwright

URL = "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"
SCREEN = "Daily Production Well Status 1"

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

    CELL='daily_well_status:form:T:0:C4_in'
    # 1) cell structure: tag, readonly, disabled, class, parent td html
    info = fr.evaluate(f"""() => {{
      const e=document.getElementById('{CELL}'); if(!e) return {{err:'no cell'}};
      return {{tag:e.tagName, type:e.type, readOnly:e.readOnly, disabled:e.disabled, cls:e.className,
               val:e.value, onchange: e.getAttribute('onchange')||'', onblur:e.getAttribute('onblur')||'',
               tdcls: e.closest('td')?e.closest('td').className:''}};
    }}""")
    print("C4 cell:", json.dumps(info, indent=1))

    # 2) toolbar / save controls available anywhere (top app toolbar lives in page top doc)
    bars = page.evaluate("""() => {
      const a=[...document.querySelectorAll('a[title], button[title]')].filter(e=>e.offsetParent)
        .map(e=>({id:e.id, title:e.title, cls:e.className.slice(0,40)}));
      return a.filter(x => /save|store|commit|apply|ctrl/i.test(x.title));
    }""")
    print("\nSAVE-ish controls (top doc):", json.dumps(bars, indent=1))
    # also inside the screen frame
    barsf = fr.evaluate("""() => {
      const a=[...document.querySelectorAll('a[title], button[title]')].filter(e=>e.offsetParent)
        .map(e=>({id:e.id, title:e.title, cls:e.className.slice(0,40)}));
      return a.filter(x => /save|store|commit|apply|ctrl|disk/i.test(x.title));
    }""")
    print("SAVE-ish controls (screen frame):", json.dumps(barsf, indent=1))

    # 3) try editing via real keystrokes and watch the cell value + Save state
    try:
        fr.locator(f'[id="{CELL}"]').click(timeout=4000)
        fr.locator(f'[id="{CELL}"]').fill("21")
        fr.locator(f'[id="{CELL}"]').press("Tab")
        page.wait_for_load_state("networkidle", timeout=12000); time.sleep(1.5)
        after = fr.evaluate(f"""() => {{ const e=document.getElementById('{CELL}'); return e?e.value:null; }}""")
        print("\nC4 value after edit+Tab:", after)
        # save state now
        sv = page.evaluate("""() => [...document.querySelectorAll('a[title*="Save"]')].map(e=>({title:e.title, disabled:e.className.includes('ui-state-disabled')}))""")
        svf = fr.evaluate("""() => [...document.querySelectorAll('a[title*="Save"]')].map(e=>({title:e.title, disabled:e.className.includes('ui-state-disabled')}))""")
        print("Save state (top):", sv, " (frame):", svf)
        # NOTE: not clicking save — revert the in-DOM edit by setting back to 24 (no persistence happened)
        fr.locator(f'[id="{CELL}"]').fill("24"); fr.locator(f'[id="{CELL}"]').press("Tab"); time.sleep(0.8)
    except Exception as e:
        print("edit diag err:", str(e)[:120])
    browser.close()
print("DONE")
