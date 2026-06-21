"""Collaborative demo: open a VISIBLE browser to Business Function and keep it live, auto-capturing a
screenshot every ~12s so the USER can click through the table-menu features while Claude reads the captures.
Read-only on Claude's side (only screenshots). py -X utf8 tmp/scripts/demo_browser.py"""
import os, time
from playwright.sync_api import sync_playwright

EC_URL = os.environ.get("EC_URL", "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/")
USER, PWD = os.environ.get("EC_USER", "sysadmin"), os.environ.get("EC_PWD", "sysadmin")
OUT = "tmp/demo_live"
os.makedirs(OUT, exist_ok=True)
LOG = os.path.join(OUT, "status.log")


def esc(i):
    return "#" + i.replace(":", "\\:")


def log(m):
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(m + "\n")
    print(m, flush=True)


with sync_playwright() as p:
    b = p.chromium.launch(headless=False, args=["--ignore-certificate-errors", "--start-maximized"])
    page = b.new_context(ignore_https_errors=True, no_viewport=True).new_page()
    page.goto(EC_URL, wait_until="domcontentloaded", timeout=45000)
    page.fill("#username", USER); page.fill("#password", PWD); page.click("#kc-login")
    page.wait_for_selector(esc("menu:searchForm:searchTxt"), timeout=60000)
    page.wait_for_timeout(1500)
    box = page.locator(esc("menu:searchForm:searchTxt")); box.click(); box.type("Business Function", delay=40)
    page.wait_for_timeout(2500)
    page.locator("xpath=//*[contains(@class,'tv-link') and normalize-space(text())='Business Function']").first.click()
    try:
        page.wait_for_load_state("networkidle", timeout=20000)
    except Exception:
        pass
    page.wait_for_timeout(1500)
    log("READY: Business Function open. Capturing every 12s -> tmp/demo_live/shot_NNN.png")

    for i in range(160):   # ~32 min of capture window
        try:
            page.screenshot(path=os.path.join(OUT, f"shot_{i:03d}.png"), full_page=False)
            pag = page.evaluate("""()=>{const m=document.body.innerText.match(/\\((\\d+)\\s+of\\s+(\\d+)\\)/);return m?m[0]:'';}""")
            log(f"shot_{i:03d}  paginator={pag}")
        except Exception as e:
            log(f"shot_{i:03d} ERR {str(e)[:50]}")
        time.sleep(12)
    b.close()
print("demo session ended.")
