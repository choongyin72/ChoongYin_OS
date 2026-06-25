"""Classify why the flowline screen showed no nav: dump ALL frames + where nav:form:G:* and :T_data
grids live (top-level vs which frame), + the main content frame URL. Distinguishes a frame-selection
issue (easy) from a different screen type (deeper recon). Read-only."""
import time, json
from playwright.sync_api import sync_playwright
URL = "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"; SCREEN = "Daily Production Flowline, by Flowline"
with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    page = b.new_context(ignore_https_errors=True, viewport={"width": 1680, "height": 1000}).new_page()
    page.goto(URL, wait_until="domcontentloaded", timeout=60000)
    page.fill('[id="username"]', "sysadmin"); page.fill('[id="password"]', "sysadmin"); page.click('[id="kc-login"]')
    page.wait_for_selector('[id="menu:searchForm:searchTxt"]', timeout=60000); time.sleep(1.0)
    sel = f'xpath=//*[contains(@class,"tv-link") and normalize-space(text())="{SCREEN}"]'
    page.locator('[id="menu:searchForm:searchTxt"]').type(SCREEN, delay=25)
    page.wait_for_selector(sel, timeout=12000); page.locator(sel).first.click()
    page.wait_for_load_state("networkidle", timeout=30000); time.sleep(2.5)
    print("=== frames ===")
    for fr in page.frames:
        u = (fr.url or "")[:90]
        try:
            navs = fr.evaluate("""()=>document.querySelectorAll('[id^="nav:form:G:"]').length""")
            grids = fr.evaluate("""()=>[...document.querySelectorAll('[id$=":T_data"]')].map(t=>t.id).slice(0,6)""")
            dates = fr.evaluate("""()=>[...document.querySelectorAll('[id$=":da_input"]')].map(e=>e.id).slice(0,4)""")
            btns = fr.evaluate("""()=>[...document.querySelectorAll('[id="button:form:B"]')].length""")
            print(f"  frame: {u}")
            print(f"     nav:form:G count={navs} | button:form:B={btns} | dates={dates} | grids={grids}")
        except Exception as e:
            print(f"  frame: {u}  (eval err {str(e)[:40]})")
    b.close()
print("DONE")
