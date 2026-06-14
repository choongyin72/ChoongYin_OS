"""Get the parent-page selector of the WR.0001 content iframe (for Browser '>>>' piercing)."""
import time
from playwright.sync_api import sync_playwright

URL = "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"
SCREEN = "Daily Production Well Status 1"

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
    # dump ALL iframe elements in the top document with their id/name/src
    frames = page.evaluate("""() => [...document.querySelectorAll('iframe')].map(f => ({
        id: f.id, name: f.name, cls: f.className, src: (f.src||'').slice(0,90)}))""")
    print("iframes in top document:")
    for f in frames:
        print("  ", f)
    # also the frame_element of the content frame
    try:
        fe = fr.frame_element()
        print("\ncontent frame element id:", fe.get_attribute("id"), "name:", fe.get_attribute("name"))
    except Exception as e:
        print("frame_element err:", str(e)[:100])
    browser.close()
print("DONE")
