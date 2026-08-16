"""Why is the Delivery Stream list empty after GO? Dump navigator + all tbodys
before GO, after GO, and after picking the first navigator dropdown option + GO."""
import os
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

URL = os.environ.get("EC_URL", "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/")
OUT = Path(r"c:/Projects/ChoongYin_OS/tmp/dispatching_recon")

DUMP = """
() => {
  const vis = e => e && e.offsetParent !== null;
  const tb = [...document.querySelectorAll('tbody')].filter(e => e.id)
    .map(e => ({id: e.id, rows: e.querySelectorAll('tr').length, vis: vis(e)}))
    .filter(t => t.rows > 0 || /T_data/.test(t.id)).slice(0, 12);
  const nav = [...document.querySelectorAll('[id^="nav:form"]')]
    .filter(e => vis(e) && /(_la|:dd$|da_input)$/.test(e.id))
    .map(e => ({id: e.id, t: (e.textContent||e.value||'').trim().slice(0,30)})).slice(0, 14);
  return {tbodys: tb, nav};
}
"""

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_context(ignore_https_errors=True, viewport={"width": 1920, "height": 1080}).new_page()
    page.goto(URL, wait_until="domcontentloaded", timeout=60000)
    page.fill('[id="username"]', "sysadmin")
    page.fill('[id="password"]', "sysadmin")
    page.click('[id="kc-login"]')
    page.wait_for_selector('[id="menu:searchForm:searchTxt"]', timeout=60000)
    box = page.locator('[id="menu:searchForm:searchTxt"]')
    box.type("Delivery Stream", delay=50)
    time.sleep(1)
    page.locator('xpath=//*[contains(@class,"tv-link") and normalize-space(text())="Delivery Stream"]').first.click()
    page.wait_for_load_state("networkidle", timeout=20000)
    time.sleep(2)
    print("BEFORE GO:", page.evaluate(DUMP))
    page.click('[id="button:form:B"]')
    page.wait_for_load_state("networkidle", timeout=20000)
    time.sleep(2.5)
    print("AFTER GO:", page.evaluate(DUMP))
    page.screenshot(path=str(OUT / "delstrm_after_go.png"), full_page=True)
    # pick first option in the first navigator dd (if any), then GO again
    dd = page.evaluate("""() => { const e=[...document.querySelectorAll('[id^="nav:form"][id$=":dd"]')]
        .filter(x => x.offsetParent); return e.length ? e[0].id : null; }""")
    if dd:
        page.click(f'[id="{dd}_button"]')
        try:
            page.wait_for_selector(f'[id="{dd}_panel"] tr[data-item-label]', timeout=8000)
            first = page.locator(f'[id="{dd}_panel"] tr[data-item-label]').first
            print("nav dd first option:", first.get_attribute("data-item-label"))
            first.click()
            page.wait_for_load_state("networkidle", timeout=15000)
            time.sleep(1)
            page.click('[id="button:form:B"]')
            page.wait_for_load_state("networkidle", timeout=20000)
            time.sleep(2.5)
            print("AFTER NAV-PICK + GO:", page.evaluate(DUMP))
            page.screenshot(path=str(OUT / "delstrm_after_nav_go.png"), full_page=True)
        except Exception as e:
            print("nav dd probe failed:", str(e)[:120])
    browser.close()
