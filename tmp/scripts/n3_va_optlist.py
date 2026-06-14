"""Read-only: on HA.0001 with From/To = a MONTH range (2024-02-01..2024-02-29), open the G:2 process
dropdown and dump ALL options — does 'P1 Parent1 Forward Status Update' (the monthly V->A approve)
appear here, or are monthly processes on a different screen / under a different label? Resolves the
approve-pick snag without blind retry."""
import time, json
from playwright.sync_api import sync_playwright
URL = "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"; SCREEN = "Daily Data Status Processes"
with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    page = b.new_context(ignore_https_errors=True, viewport={"width": 1680, "height": 1000}).new_page()
    page.goto(URL, wait_until="domcontentloaded", timeout=60000)
    page.fill('[id="username"]', "sysadmin"); page.fill('[id="password"]', "sysadmin"); page.click('[id="kc-login"]')
    page.wait_for_selector('[id="menu:searchForm:searchTxt"]', timeout=60000); time.sleep(1.0)
    sel = f'xpath=//*[contains(@class,"tv-link") and normalize-space(text())="{SCREEN}"]'
    page.locator('[id="menu:searchForm:searchTxt"]').type(SCREEN, delay=30)
    page.wait_for_selector(sel, timeout=12000); page.locator(sel).first.click()
    page.wait_for_load_state("networkidle", timeout=30000); time.sleep(2.0)
    fr = next((f for f in page.frames if "dashboard.jsf" in (f.url or "") and "top=false" in (f.url or "")), None) or page
    for g, v in ((0, "2024-02-01"), (1, "2024-02-29")):
        fr.locator(f'[id="nav:form:G:{g}:R:1:C:0:da_input"]').fill(v); fr.locator(f'[id="nav:form:G:{g}:R:1:C:0:da_input"]').press("Tab"); time.sleep(0.9)
    fr.locator('[id="nav:form:G:2:R:1:C:0:dd_button"]').click(timeout=5000); time.sleep(1.2)
    opts = fr.evaluate("""()=>[...document.querySelectorAll('[id="nav:form:G:2:R:1:C:0:dd_panel"] tr[data-item-label]')].map(e=>(e.getAttribute('data-item-label')||'').trim()).filter(t=>t)""")
    print(f"G:2 options for month range ({len(opts)}):")
    for o in opts:
        print("   ", o)
    # also list any treeview screens with 'Monthly' status processes
    page.fill('[id="menu:searchForm:searchTxt"]', ""); page.locator('[id="menu:searchForm:searchTxt"]').type("Status Process", delay=25); time.sleep(1.2)
    scr = page.evaluate("""()=>[...document.querySelectorAll('.tv-link')].map(e=>e.textContent.trim()).filter(t=>/Status Process|Data Status/i.test(t))""")
    print("\nscreens matching 'Status Process / Data Status':", json.dumps(scr))
    b.close()
print("DONE")
