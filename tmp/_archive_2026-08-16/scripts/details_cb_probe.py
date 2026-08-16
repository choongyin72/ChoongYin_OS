"""Dump the DETAILS tab checkbox structure for a selected schedule (EXCEL_IMPORT_1)."""
import os
import time

from playwright.sync_api import sync_playwright

URL = os.environ.get("EC_URL", "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_context(ignore_https_errors=True, viewport={"width": 1920, "height": 1080}).new_page()
    page.goto(URL, wait_until="domcontentloaded", timeout=60000)
    page.fill('[id="username"]', "sysadmin")
    page.fill('[id="password"]', "sysadmin")
    page.click('[id="kc-login"]')
    page.wait_for_selector('[id="menu:searchForm:searchTxt"]', timeout=60000)
    box = page.locator('[id="menu:searchForm:searchTxt"]')
    box.type("Schedules", delay=50)
    time.sleep(1.2)
    page.locator('xpath=//*[contains(@class,"tv-link") and normalize-space(text())="Schedules"]').first.click()
    page.wait_for_load_state("networkidle", timeout=20000)
    time.sleep(2)
    dd = "nav:form:G:0:R:0:C:1:dd"
    page.click(f'[id="{dd}_button"]')
    page.wait_for_selector(f'[id="{dd}_panel"] tr[data-item-label]', timeout=8000)
    page.locator(f'[id="{dd}_panel"] tr[data-item-label="All"]').click()
    time.sleep(1.5)
    page.click('[id="button:form:B"]')
    page.wait_for_load_state("networkidle", timeout=20000)
    time.sleep(2.5)
    for pg in range(1, 7):
        if page.locator('xpath=//tbody[@id="schedule:form:T_data"]//input[@value="EXCEL_IMPORT_1"]').count():
            break
        page.locator('css=[id^="schedule"] .ui-paginator-next:not(.ui-state-disabled)').first.click()
        page.wait_for_load_state("networkidle", timeout=15000)
        time.sleep(1.5)
    page.locator('xpath=//tbody[@id="schedule:form:T_data"]//input[@value="EXCEL_IMPORT_1"]').first.click()
    page.wait_for_load_state("networkidle", timeout=15000)
    time.sleep(1.5)
    info = page.evaluate("""() => {
      const vis = e => { let n = e; while (n) { if (getComputedStyle(n).display === 'none') return false; n = n.parentElement; } return true; };
      const cbs = [...document.querySelectorAll('input[type="checkbox"], .ui-chkbox')]
        .map(e => ({id: e.id, cls: (e.className||'').toString().slice(0,40),
                    vis: vis(e), checked: e.checked}));
      const labels = [...document.querySelectorAll('label')].filter(vis)
        .map(l => ({for: l.htmlFor, t: (l.textContent||'').trim()})).filter(l => l.t).slice(0, 20);
      return {cbs: cbs.filter(c => c.vis || /enable/i.test(c.id)), labels};
    }""")
    for c in info["cbs"]:
        print("cb:", c)
    for l in info["labels"]:
        print("label:", l)
    browser.close()
