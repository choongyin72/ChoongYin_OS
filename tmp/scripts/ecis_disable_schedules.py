"""Restore: untick Enabled + Save for EXCEL_IMPORT_1 and EXCEL_IMPORT_2 (back to as-found)."""
import os
import time

import oracledb
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
    page.wait_for_load_state("networkidle", timeout=15000)
    time.sleep(1.5)
    page.click('[id="button:form:B"]')
    page.wait_for_load_state("networkidle", timeout=20000)
    time.sleep(2.5)
    for sched in ("EXCEL_IMPORT_1", "EXCEL_IMPORT_2"):
        for pg in range(1, 7):
            if page.locator(f'xpath=//tbody[@id="schedule:form:T_data"]//input[@value="{sched}"]').count():
                break
            page.locator('css=[id^="schedule"] .ui-paginator-next:not(.ui-state-disabled)').first.click()
            page.wait_for_load_state("networkidle", timeout=15000)
            time.sleep(1.5)
        page.locator(f'xpath=//tbody[@id="schedule:form:T_data"]//input[@value="{sched}"]').first.click()
        page.wait_for_load_state("networkidle", timeout=15000)
        time.sleep(1.5)
        page.click('[id="tab:tabPanel:job_details_more:form:G:0:R:0:C:0:cb"]')
        page.locator('xpath=//li[.//span[contains(@class,"ui-icon-save")]][1]').first.click()
        page.wait_for_load_state("networkidle", timeout=20000)
        time.sleep(2.5)
        print(f"disabled {sched}")
    browser.close()

conn = oracledb.connect(user="ECKERNEL_EC", password="energy",
                        dsn=os.environ.get("EC_DB_DSN", "localhost:1521/ORCL"))
cur = conn.cursor()
cur.execute("SELECT name, enabled, status FROM tv_schedule_list WHERE name IN ('EXCEL_IMPORT_1','EXCEL_IMPORT_2')")
print("final state:", cur.fetchall())
conn.close()
