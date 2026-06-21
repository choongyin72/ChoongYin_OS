"""Land the data: run EXCEL_IMPORT_2 (staging->EC) against the already-populated IMP_STAGING. The Enabled
decision is driven by a DB READ (reliable) - the UI checkbox state is unreadable. Only tick the cb if the DB
says disabled; otherwise leave it and just RUN NOW. Wait, then verify dv_pwel_day_status in-script.
py -X utf8 this.
"""
import os
import time
from pathlib import Path

import oracledb
from playwright.sync_api import sync_playwright

URL = os.environ.get("EC_URL", "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/")
OUT = Path(r"c:/Projects/ChoongYin_OS/tmp/ecis_recon")
SCHED = "EXCEL_IMPORT_2"
CB = "tab:tabPanel:job_details_more:form:G:0:R:0:C:0:cb"


def db():
    return oracledb.connect(user="ECKERNEL_EC", password="energy", dsn=os.environ.get("EC_DB_DSN", "localhost:1521/ORCL"))


c = db().cursor()
c.execute("SELECT enabled FROM tv_schedule_list WHERE name=:n", n=SCHED)
enabled = c.fetchone()[0]
print(f"{SCHED} enabled (DB) = {enabled}")
need_tick = (enabled == 'N')

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_context(ignore_https_errors=True, viewport={"width": 1920, "height": 1080}).new_page()
    page.goto(URL, wait_until="domcontentloaded", timeout=60000)
    page.fill('[id="username"]', "sysadmin"); page.fill('[id="password"]', "sysadmin"); page.click('[id="kc-login"]')
    page.wait_for_selector('[id="menu:searchForm:searchTxt"]', timeout=60000); time.sleep(1)
    box = page.locator('[id="menu:searchForm:searchTxt"]'); box.type("Schedules", delay=50); time.sleep(1.2)
    page.locator('xpath=//*[contains(@class,"tv-link") and normalize-space(text())="Schedules"]').first.click()
    page.wait_for_load_state("networkidle", timeout=20000); time.sleep(2)
    page.click('[id="nav:form:G:0:R:0:C:1:dd_button"]')
    page.wait_for_selector('[id="nav:form:G:0:R:0:C:1:dd_panel"] tr[data-item-label]', timeout=8000)
    page.locator('[id="nav:form:G:0:R:0:C:1:dd_panel"] tr[data-item-label="All"]').click()
    page.wait_for_load_state("networkidle", timeout=15000); time.sleep(1.5)
    page.click('[id="button:form:B"]'); page.wait_for_load_state("networkidle", timeout=20000); time.sleep(2)
    page.fill('[id="schedule:form:T:sfilter0_ft_filter"]', SCHED); page.keyboard.press("Enter")
    page.wait_for_load_state("networkidle", timeout=15000); time.sleep(2)
    for _ in range(6):
        if page.locator(f'xpath=//tbody[@id="schedule:form:T_data"]//input[@value="{SCHED}"]').count():
            break
        nxt = page.locator('css=[id^="schedule"] .ui-paginator-next:not(.ui-state-disabled)')
        if not nxt.count():
            break
        nxt.first.click(); page.wait_for_load_state("networkidle", timeout=15000); time.sleep(1.5)
    page.locator(f'xpath=//tbody[@id="schedule:form:T_data"]//input[@value="{SCHED}"]').first.click()
    page.wait_for_load_state("networkidle", timeout=15000); time.sleep(1.5)
    if need_tick:
        page.locator(f'[id="{CB}"]').first.click()
        page.locator('xpath=//li[.//span[contains(@class,"ui-icon-save")]][1]').first.click()
        page.wait_for_load_state("networkidle", timeout=20000); time.sleep(3)
        print("ticked enable")
    else:
        print("already enabled - not touching cb")
    page.click('[id="runNowButton:form:B"]'); page.wait_for_load_state("networkidle", timeout=30000); time.sleep(2)
    dlg = page.locator('xpath=//*[self::button or self::span][normalize-space(.)="Yes" or normalize-space(.)="OK"]').locator("visible=true")
    if dlg.count():
        dlg.first.click()
    time.sleep(20)
    page.screenshot(path=str(OUT / "run_stage2.png"), full_page=True)
    browser.close()

cur = db().cursor()
cur.execute("""SELECT object_code, avg_bh_temp FROM dv_pwel_day_status WHERE daytime=DATE '2003-01-05'
               AND object_code IN ('AS1_Well_001','AS1_Well_002','AS1_Well_003') ORDER BY object_code""")
print("FINAL AVG_BH_TEMP:", cur.fetchall())
cur.execute("SELECT COUNT(*) FROM imp_staging WHERE interface_code='EXCEL_IMPORT'")
print("staging rows remaining:", cur.fetchone()[0])
cur.execute("""SELECT * FROM (SELECT schedule_no, business_action_name, run_status, from_daytime
               FROM tv_action_instance_history ORDER BY from_daytime DESC NULLS LAST) WHERE ROWNUM<=4""")
print("history:", cur.fetchall())
print("DONE")
