"""Capture the nested-iframe chain for WR.0001 (READ-ONLY): walk frame parents and dump each
iframe element's id/name/src so the Browser '>>>' piercing chain is deterministic."""
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
    time.sleep(2.0)

    # walk parent chain of the screen frame
    print("=== frame parent chain (screen -> root) ===")
    cur = fr
    depth = 0
    while cur is not None:
        try:
            fe = cur.frame_element()
            fid = fe.get_attribute("id"); fname = fe.get_attribute("name")
            print(f"  depth {depth}: url={cur.url[:70]}  iframe id={fid!r} name={fname!r}")
        except Exception as e:
            print(f"  depth {depth}: url={cur.url[:70]}  (root/main frame — no element)")
        cur = cur.parent_frame
        depth += 1

    # also: from each frame in the chain, list its child iframes (id/name/src)
    print("\n=== iframes per frame ===")
    for f in page.frames:
        try:
            ifr = f.evaluate("""() => [...document.querySelectorAll('iframe')].map(e => ({id:e.id, name:e.name, src:(e.src||'').slice(0,80)}))""")
            if ifr:
                print(f"  frame {f.url[:60]}:")
                for x in ifr: print("     ", x)
        except Exception:
            pass
    browser.close()
print("DONE")
