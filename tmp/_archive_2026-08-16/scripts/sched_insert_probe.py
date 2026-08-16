"""Schedules screen: dump the toolbar Insert submenu + structure of the Business Action
tab grids (BA grid, PARAMETERS grid, ECIS JOB ACTIONS section) for EXCEL_IMPORT_1."""
import os
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

URL = os.environ.get("EC_URL", "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/")
OUT = Path(r"c:/Projects/ChoongYin_OS/tmp/ecis_recon")

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

    page.locator('xpath=//li[contains(@class,"ui-menu-parent")][.//span[contains(@class,"ui-icon-insert")]]').hover()
    time.sleep(1.2)
    items = page.evaluate("""() => [...document.querySelectorAll('ul.ui-menu-child li a')]
        .filter(e => e.offsetParent).map(e => (e.textContent||'').trim()).filter(t => t)""")
    print("INSERT submenu:", items)
    page.mouse.click(900, 500)
    time.sleep(1)

    # select EXCEL_IMPORT_1 (All + paginate) then Business Action tab
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
    page.locator('xpath=//*[self::a or self::span][normalize-space(text())="Business Action"]').locator("visible=true").first.click()
    page.wait_for_load_state("networkidle", timeout=15000)
    time.sleep(2)
    grids = page.evaluate("""() => [...document.querySelectorAll('tbody[id$=":T_data"]')]
        .map(e => ({id: e.id, rows: e.querySelectorAll('tr').length,
                    vis: e.offsetParent !== null}))""")
    print("grids on BA tab:", [g for g in grids if g["vis"]])
    # scroll the whole page (ECIS JOB ACTIONS may be below)
    page.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
    time.sleep(1)
    page.screenshot(path=str(OUT / "ba_tab_full.png"), full_page=True)
    # also SCHEDULE tab
    page.locator('xpath=//*[self::a or self::span][normalize-space(text())="Schedule"]').locator("visible=true").first.click()
    page.wait_for_load_state("networkidle", timeout=15000)
    time.sleep(2)
    page.screenshot(path=str(OUT / "schedule_tab_full.png"), full_page=True)
    browser.close()
