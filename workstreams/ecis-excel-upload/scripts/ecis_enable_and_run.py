"""Enable EXCEL_IMPORT_1 (DETAILS tab checkbox + Save), RUN NOW, verify staging at DB.
Restores nothing yet — disable again later after the whole pipeline works."""
import os
import sys
import time
from pathlib import Path

import oracledb
from playwright.sync_api import sync_playwright

URL = os.environ.get("EC_URL", "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/")
OUT = Path(r"c:/Projects/ChoongYin_OS/tmp/ecis_recon")
SCHEDULE = sys.argv[1] if len(sys.argv) > 1 else "EXCEL_IMPORT_1"

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
    for pg in range(1, 7):
        if page.locator(f'xpath=//tbody[@id="schedule:form:T_data"]//input[@value="{SCHEDULE}"]').count():
            break
        page.locator('css=[id^="schedule"] .ui-paginator-next:not(.ui-state-disabled)').first.click()
        page.wait_for_load_state("networkidle", timeout=15000)
        time.sleep(1.5)
    page.locator(f'xpath=//tbody[@id="schedule:form:T_data"]//input[@value="{SCHEDULE}"]').first.click()
    page.wait_for_load_state("networkidle", timeout=15000)
    time.sleep(1.5)

    # DETAILS tab Enabled checkbox (probed id)
    page.click('[id="tab:tabPanel:job_details_more:form:G:0:R:0:C:0:cb"]')
    # toolbar Save
    page.locator('xpath=//li[.//span[contains(@class,"ui-icon-save")]][1]').first.click()
    page.wait_for_load_state("networkidle", timeout=20000)
    time.sleep(2.5)
    page.screenshot(path=str(OUT / f"enable_{SCHEDULE}.png"), full_page=True)

    page.click('[id="runNowButton:form:B"]')
    page.wait_for_load_state("networkidle", timeout=30000)
    time.sleep(2)
    dlg = page.locator('xpath=//*[self::button or self::span][normalize-space(.)="Yes" or normalize-space(.)="OK"]').locator("visible=true")
    if dlg.count():
        dlg.first.click()
        time.sleep(2)
    page.wait_for_load_state("networkidle", timeout=30000)
    time.sleep(10)
    page.screenshot(path=str(OUT / f"runnow_{SCHEDULE}.png"), full_page=True)
    browser.close()

conn = oracledb.connect(user="ECKERNEL_EC", password="energy",
                        dsn=os.environ.get("EC_DB_DSN", "localhost:1521/ORCL"))
cur = conn.cursor()
cur.execute("SELECT enabled, status FROM tv_schedule_list WHERE name=:n", n=SCHEDULE)
print("schedule state:", cur.fetchall())
cur.execute("""SELECT * FROM (SELECT schedule_no, business_action_name, run_status, from_daytime
  FROM tv_action_instance_history ORDER BY from_daytime DESC NULLS LAST) WHERE ROWNUM <= 3""")
print("latest history:", cur.fetchall())
cur.execute("SELECT code, ec_key, key_1, key_2, value_number, value_date, value_string FROM imp_staging WHERE interface_code='EXCEL_IMPORT' AND ROWNUM<=12")
rows = cur.fetchall()
print(f"IMP_STAGING ({len(rows)} rows):")
for r in rows:
    print(" ", r)
cur.execute("SELECT file_name, uploaded_into_ec_ind, parsed_date FROM imp_source_interface_file WHERE interface_code='EXCEL_IMPORT'")
print("file state:", cur.fetchall())
conn.close()
