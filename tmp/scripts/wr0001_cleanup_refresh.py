"""Cleanliness: open WR.0001, render the scope, click Refresh (discard any uncommitted edit),
confirm grid C4 shows the DB value 24 (READ + one Refresh click; no data write)."""
import time
from playwright.sync_api import sync_playwright
URL="https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"; SCREEN="Daily Production Well Status 1"
CELL='daily_well_status:form:T:0:C4_in'
def dd_opts(fr,g):
    fr.locator(f'[id="nav:form:G:{g}:R:1:C:0:dd_button"]').click(timeout=4000); time.sleep(0.7)
    return fr.evaluate(f"""()=>[...document.querySelectorAll('[id="nav:form:G:{g}:R:1:C:0:dd_panel"] tr[data-item-label]')].map(e=>(e.getAttribute('data-item-label')||'').trim()).filter(t=>t)""")
def dd_pick(fr,g,l): fr.locator(f'[id="nav:form:G:{g}:R:1:C:0:dd_panel"] tr[data-item-label="{l}"]').first.click(timeout=4000); time.sleep(1.0)
with sync_playwright() as p:
    b=p.chromium.launch(headless=True); page=b.new_context(ignore_https_errors=True,viewport={"width":1920,"height":1080}).new_page()
    page.goto(URL,wait_until="domcontentloaded",timeout=60000)
    page.fill('[id="username"]',"sysadmin"); page.fill('[id="password"]',"sysadmin"); page.click('[id="kc-login"]')
    page.wait_for_selector('[id="menu:searchForm:searchTxt"]',timeout=60000)
    sel=f'xpath=//*[contains(@class,"tv-link") and normalize-space(text())="{SCREEN}"]'; fr=None
    for _ in range(2):
        page.fill('[id="menu:searchForm:searchTxt"]',""); page.locator('[id="menu:searchForm:searchTxt"]').type(SCREEN,delay=40)
        page.wait_for_selector(sel,timeout=15000); time.sleep(0.6); page.locator(sel).first.click()
        page.wait_for_load_state("networkidle",timeout=30000)
        for _ in range(25):
            fr=next((f for f in page.frames if "daily_well_status" in f.url),None)
            if fr: break
            time.sleep(1.0)
        if fr: break
    if not fr: print("no frame"); b.close(); raise SystemExit
    time.sleep(2.0)
    fr.locator('[id="nav:form:G:0:R:1:C:0:da_input"]').fill("2003-01-01"); fr.locator('[id="nav:form:G:0:R:1:C:0:da_input"]').press("Tab"); time.sleep(1.5)
    dd_opts(fr,1); dd_pick(fr,1,"AS2 EC Exploration Norway"); dd_opts(fr,2); dd_pick(fr,2,"AS2_Onshore Area")
    dd_opts(fr,3); dd_pick(fr,3,"AS2_Production Facility no 1"); dd_opts(fr,4); dd_pick(fr,4,"AS2_Lift Gas Manifold 1")
    fr.locator('[id="button:form:B"]').click(timeout=5000); page.wait_for_load_state("networkidle",timeout=30000); time.sleep(4.0)
    print("C4 before refresh:", fr.locator(f'[id="{CELL}"]').input_value())
    # click Refresh toolbar (reload grid from DB, discards uncommitted view state)
    try:
        page.locator('xpath=//a[@title="Refresh [Ctrl+r]"]').first.click(timeout=8000)
        page.wait_for_load_state("networkidle",timeout=20000); time.sleep(3.0)
    except Exception as e:
        print("refresh click err:", str(e)[:90])
    # re-render scope after refresh (refresh may reset the navigator)
    try:
        print("C4 after refresh:", fr.locator(f'[id="{CELL}"]').input_value())
    except Exception:
        # navigator may have reset; re-GO
        dd_opts(fr,1); dd_pick(fr,1,"AS2 EC Exploration Norway"); dd_opts(fr,2); dd_pick(fr,2,"AS2_Onshore Area")
        dd_opts(fr,3); dd_pick(fr,3,"AS2_Production Facility no 1"); dd_opts(fr,4); dd_pick(fr,4,"AS2_Lift Gas Manifold 1")
        fr.locator('[id="button:form:B"]').click(timeout=5000); page.wait_for_load_state("networkidle",timeout=30000); time.sleep(3.0)
        print("C4 after refresh+re-GO:", fr.locator(f'[id="{CELL}"]').input_value())
    b.close()
print("DONE")
