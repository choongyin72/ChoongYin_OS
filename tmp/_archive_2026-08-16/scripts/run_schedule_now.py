"""Run an ALREADY-ENABLED schedule via RUN NOW (no enable toggling).
Usage: py run_schedule_now.py <ScheduleName>"""
import os
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

URL = os.environ.get("EC_URL", "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/")
OUT = Path(r"c:/Projects/ChoongYin_OS/tmp/biz_domains")
SCHEDULE = sys.argv[1]

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
    page.fill('[id="schedule:form:T:sfilter0_ft_filter"]', SCHEDULE)
    page.keyboard.press("Enter")
    page.wait_for_load_state("networkidle", timeout=15000)
    time.sleep(2.5)
    page.locator(f'xpath=//tbody[@id="schedule:form:T_data"]//input[@value="{SCHEDULE}"]').first.click()
    page.wait_for_load_state("networkidle", timeout=15000)
    time.sleep(1.5)
    page.click('[id="runNowButton:form:B"]')
    page.wait_for_load_state("networkidle", timeout=30000)
    time.sleep(2)
    dlg = page.locator('xpath=//*[self::button or self::span][normalize-space(.)="Yes" or normalize-space(.)="OK"]').locator("visible=true")
    if dlg.count():
        dlg.first.click()
    time.sleep(15)
    page.screenshot(path=str(OUT / f"run_{SCHEDULE}.png"), full_page=True)
    msg = page.evaluate("""() => { const t = [...document.querySelectorAll('div,span')]
        .map(e => (e.textContent||'').trim())
        .filter(t => t && t.length < 200 && /not enabled|running|started|fail/i.test(t));
        return t.sort((a,b)=>a.length-b.length)[0] || 'no banner'; }""")
    print(f"{SCHEDULE}: RUN NOW clicked; banner: {msg}")
    browser.close()
