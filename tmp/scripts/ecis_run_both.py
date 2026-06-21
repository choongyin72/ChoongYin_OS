"""Run EXCEL_IMPORT_1 then _2 cleanly (file already uploaded). Robust: DETECT the Enabled checkbox state and
only tick it if currently OFF (the prior bug toggled an already-enabled schedule OFF). RUN NOW each, confirm a
FRESH history row, then verify staging + dv_pwel_day_status. Restore: leave both disabled at the end.
py -X utf8 this.
"""
import os
import time
from pathlib import Path

import oracledb
from playwright.sync_api import sync_playwright

URL = os.environ.get("EC_URL", "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/")
OUT = Path(r"c:/Projects/ChoongYin_OS/tmp/ecis_recon")
CB = "tab:tabPanel:job_details_more:form:G:0:R:0:C:0:cb"


def open_screen(page, name):
    page.goto(URL, wait_until="domcontentloaded", timeout=60000)
    page.wait_for_selector('[id="menu:searchForm:searchTxt"]', timeout=60000); time.sleep(1)
    box = page.locator('[id="menu:searchForm:searchTxt"]'); box.fill(""); box.type(name, delay=50); time.sleep(1.2)
    page.locator(f'xpath=//*[contains(@class,"tv-link") and normalize-space(text())="{name}"]').first.click()
    page.wait_for_load_state("networkidle", timeout=20000); time.sleep(2)


def cb_state(page):
    return page.evaluate(
        "() => { const el=document.getElementById('%s'); if(!el) return 'noel'; "
        "const b=el.classList.contains('ui-chkbox-box')?el:(el.querySelector('.ui-chkbox-box')||el); "
        "return b.classList.contains('ui-state-active')?'on':'off'; }" % CB)


def set_enabled(page, want_on):
    st = cb_state(page)
    if (st == 'off' and want_on) or (st == 'on' and not want_on):
        page.locator(f'[id="{CB}"]').first.click()
        page.locator('xpath=//li[.//span[contains(@class,"ui-icon-save")]][1]').first.click()
        page.wait_for_load_state("networkidle", timeout=20000); time.sleep(3)
    return cb_state(page)


def select_schedule(page, sched):
    open_screen(page, "Schedules")
    page.click('[id="nav:form:G:0:R:0:C:1:dd_button"]')
    page.wait_for_selector('[id="nav:form:G:0:R:0:C:1:dd_panel"] tr[data-item-label]', timeout=8000)
    page.locator('[id="nav:form:G:0:R:0:C:1:dd_panel"] tr[data-item-label="All"]').click()
    page.wait_for_load_state("networkidle", timeout=15000); time.sleep(1.5)
    page.click('[id="button:form:B"]'); page.wait_for_load_state("networkidle", timeout=20000); time.sleep(2)
    page.fill('[id="schedule:form:T:sfilter0_ft_filter"]', sched); page.keyboard.press("Enter")
    page.wait_for_load_state("networkidle", timeout=15000); time.sleep(2)
    for _ in range(6):
        if page.locator(f'xpath=//tbody[@id="schedule:form:T_data"]//input[@value="{sched}"]').count():
            break
        nxt = page.locator('css=[id^="schedule"] .ui-paginator-next:not(.ui-state-disabled)')
        if not nxt.count():
            break
        nxt.first.click(); page.wait_for_load_state("networkidle", timeout=15000); time.sleep(1.5)
    page.locator(f'xpath=//tbody[@id="schedule:form:T_data"]//input[@value="{sched}"]').first.click()
    page.wait_for_load_state("networkidle", timeout=15000); time.sleep(1.5)


def run_now(page, sched):
    select_schedule(page, sched)
    print(f"  {sched}: cb before =", set_enabled(page, True))
    page.click('[id="runNowButton:form:B"]'); page.wait_for_load_state("networkidle", timeout=30000); time.sleep(2)
    dlg = page.locator('xpath=//*[self::button or self::span][normalize-space(.)="Yes" or normalize-space(.)="OK"]').locator("visible=true")
    if dlg.count():
        dlg.first.click()
    time.sleep(12)
    page.screenshot(path=str(OUT / f"run2_{sched}.png"), full_page=True)


with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_context(ignore_https_errors=True, viewport={"width": 1920, "height": 1080}).new_page()
    page.goto(URL, wait_until="domcontentloaded", timeout=60000)
    page.fill('[id="username"]', "sysadmin"); page.fill('[id="password"]', "sysadmin"); page.click('[id="kc-login"]')
    page.wait_for_selector('[id="menu:searchForm:searchTxt"]', timeout=60000)
    run_now(page, "EXCEL_IMPORT_1")
    run_now(page, "EXCEL_IMPORT_2")
    # restore: disable both
    select_schedule(page, "EXCEL_IMPORT_1"); print("  restore _1:", set_enabled(page, False))
    select_schedule(page, "EXCEL_IMPORT_2"); print("  restore _2:", set_enabled(page, False))
    browser.close()

conn = oracledb.connect(user="ECKERNEL_EC", password="energy", dsn=os.environ.get("EC_DB_DSN", "localhost:1521/ORCL"))
cur = conn.cursor()
cur.execute("SELECT code, key_1, key_2, value_number FROM imp_staging WHERE interface_code='EXCEL_IMPORT' AND ROWNUM<=12")
print("staging:", cur.fetchall())
cur.execute("""SELECT object_code, avg_bh_temp FROM dv_pwel_day_status WHERE daytime=DATE '2003-01-05'
               AND object_code IN ('AS1_Well_001','AS1_Well_002','AS1_Well_003') ORDER BY object_code""")
print("FINAL AVG_BH_TEMP:", cur.fetchall())
cur.execute("""SELECT * FROM (SELECT schedule_no, business_action_name, run_status, from_daytime
               FROM tv_action_instance_history ORDER BY from_daytime DESC NULLS LAST) WHERE ROWNUM<=4""")
print("history:", cur.fetchall())
conn.close()
print("DONE")
