"""Crack the '- by Well' nav cascade: open the screen, set date 2024-10-01, dump the initial options
of each nav dd (G1..G5) to learn the cascade order + find what surfaces FRMW Well 1/2. Read-only."""
import time, json, os
from playwright.sync_api import sync_playwright

URL = "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"
SCREEN = "Sub Daily Production Well Status 1 - by Well"


def dd_options(fr, g):
    try:
        fr.locator(f'[id="nav:form:G:{g}:R:1:C:0:dd_button"]').click(timeout=4000)
        time.sleep(0.7)
        opts = fr.evaluate(f"""()=>[...document.querySelectorAll('[id="nav:form:G:{g}:R:1:C:0:dd_panel"] tr[data-item-label]')].map(e=>(e.getAttribute('data-item-label')||'').trim()).filter(t=>t)""")
        # close panel
        fr.locator(f'[id="nav:form:G:{g}:R:1:C:0:dd_button"]').click(timeout=2000)
        time.sleep(0.3)
        return opts
    except Exception as e:
        return [f"ERR {str(e)[:60]}"]


with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    page = b.new_context(ignore_https_errors=True, viewport={"width": 1680, "height": 1000}).new_page()
    page.goto(URL, wait_until="domcontentloaded", timeout=60000)
    page.fill('[id="username"]', "sysadmin"); page.fill('[id="password"]', "sysadmin"); page.click('[id="kc-login"]')
    page.wait_for_selector('[id="menu:searchForm:searchTxt"]', timeout=60000); time.sleep(1.0)
    sel = f'xpath=//*[contains(@class,"tv-link") and normalize-space(text())="{SCREEN}"]'
    page.locator('[id="menu:searchForm:searchTxt"]').type(SCREEN, delay=30)
    page.wait_for_selector(sel, timeout=12000); page.locator(sel).first.click()
    page.wait_for_load_state("networkidle", timeout=30000); time.sleep(2.5)
    fr = next((f for f in page.frames if "dashboard.jsf" in (f.url or "") and "top=false" in (f.url or "")), None) or page
    # set the date first (G0)
    di = fr.locator('[id="nav:form:G:0:R:1:C:0:da_input"]')
    di.fill("2024-10-01"); di.press("Tab"); time.sleep(1.0)
    print("date set 2024-10-01")
    for g in (1, 2, 3, 4, 5):
        opts = dd_options(fr, g)
        print(f"\nG{g} options ({len(opts)}):")
        for o in opts[:25]:
            print("   ", o)
    b.close()
print("DONE")
