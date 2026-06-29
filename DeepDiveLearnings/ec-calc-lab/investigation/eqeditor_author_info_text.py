from playwright.sync_api import sync_playwright
def say(m): print(m, flush=True)
with sync_playwright() as p:
    b=p.chromium.connect_over_cdp("http://localhost:9222")
    pg=b.contexts[0].pages[0]
    pg.mouse.click(957, 483); pg.wait_for_timeout(400)        # New Value field
    pg.keyboard.type("AUTOTEST equation log", delay=40)
    pg.wait_for_timeout(400)
    pg.mouse.click(888, 519); pg.wait_for_timeout(1000)       # OK on Insert Text popup
    pg.screenshot(path="C:/tmp/author_filled.png", full_page=True); say("entered text + OK - SHOT author_filled")
