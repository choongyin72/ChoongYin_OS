"""Decisive test: is the WR.0001 screen reachable at TOP LEVEL (no frame piercing)?
Compares top-document locator vs frame locator for a known nav element."""
import time
from playwright.sync_api import sync_playwright

URL = "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"
SCREEN = "Daily Production Well Status 1"
ELID = "nav:form:G:0:R:1:C:0:da_input"

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

    # is the screen frame the MAIN frame?
    print("main_frame url:", page.main_frame.url[:80])
    print("screen frame is main_frame?:", fr == page.main_frame)
    print("total frames:", [f.url[:55] for f in page.frames])

    # TOP-LEVEL locator (no frame) — does it see the nav element?
    top_count = page.locator(f'[id="{ELID}"]').count()
    print(f"\nTOP-LEVEL page.locator count for {ELID}: {top_count}")
    # frame locator
    fr_count = fr.locator(f'[id="{ELID}"]').count()
    print(f"FRAME fr.locator count: {fr_count}")
    # left search panel element (app shell) — top level?
    shell = page.locator('[id="menu:searchForm:searchTxt"]').count()
    print(f"app-shell search box at top level: {shell}")
    browser.close()
print("DONE")
