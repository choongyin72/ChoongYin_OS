"""Recon the 'Daily Prod Well Status 1, by Well' navigator so I can open it for AS1_Well_001 + a date and
show AVG_BH_TEMP. Dump nav dds/date/GO + grid. Read-only. py -X utf8 this.
"""
import os
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

URL = os.environ.get("EC_URL", "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/")
OUT = Path(r"c:/Projects/ChoongYin_OS/tmp/ecis_recon"); OUT.mkdir(parents=True, exist_ok=True)
SCREEN = "Daily Prod Well Status 1, by Well"

with sync_playwright() as p:
    b = p.chromium.launch(headless=True, args=["--ignore-certificate-errors"])
    page = b.new_context(ignore_https_errors=True, viewport={"width": 1920, "height": 1080}).new_page()
    page.goto(URL, wait_until="domcontentloaded", timeout=60000)
    page.fill('[id="username"]', "sysadmin"); page.fill('[id="password"]', "sysadmin"); page.click('[id="kc-login"]')
    page.wait_for_selector('[id="menu:searchForm:searchTxt"]', timeout=60000); time.sleep(1)
    bx = page.locator('[id="menu:searchForm:searchTxt"]'); bx.type(SCREEN, delay=40); time.sleep(1.5)
    links = page.locator('xpath=//*[contains(@class,"tv-link")]')
    n = links.count()
    print("tv-link matches:", [links.nth(i).inner_text() for i in range(min(n, 8))])
    page.locator(f'xpath=//*[contains(@class,"tv-link") and normalize-space(text())="{SCREEN}"]').first.click()
    page.wait_for_load_state("networkidle", timeout=25000); time.sleep(2.5)
    # find the content frame
    fr = None
    for f in page.frames:
        try:
            if f.evaluate("()=>!!document.querySelector('[id*=\"nav:form\"], [id*=\"Navigator\"]')"):
                fr = f; break
        except Exception:
            pass
    fr = fr or page.main_frame
    info = fr.evaluate(r"""() => {
      const vis = e => e && e.offsetParent !== null;
      const t = e => (e.textContent||'').trim();
      return {
        dds: [...document.querySelectorAll('[id$=":dd"]')].filter(vis).map(e=>e.id).slice(0,20),
        dates: [...document.querySelectorAll('[id$=":da_input"], input[id*="date" i]')].filter(vis).map(e=>e.id).slice(0,10),
        finders: [...document.querySelectorAll('input[type="text"]')].filter(vis).map(e=>e.id).filter(x=>x).slice(0,20),
        buttons: [...document.querySelectorAll('a,button,span')].filter(vis).filter(e=>/^(go|search|apply)$/i.test(t(e))).map(e=>({id:e.id,t:t(e)})).slice(0,10),
        gobtn: [...document.querySelectorAll('[id*="button" i][id$=":B"], [id$="go:form:B"], [id="button:form:B"]')].map(e=>e.id).slice(0,8),
        labels: [...document.querySelectorAll('[id$="_la"], label')].filter(vis).map(t).filter(x=>x).slice(0,15)
      }; }""")
    import json
    print(json.dumps(info, indent=1)[:2500])
    page.screenshot(path=str(OUT / "pwel_screen_nav.png"), full_page=True)
    b.close()
print("DONE")
