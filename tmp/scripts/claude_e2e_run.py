"""GRAND FINALE: my own interface + my own schedule, end to end.
1) Excel (sheet 'Data': Well|Date|Pressure, rows 2-4) + zip reorder
2) Upload Files: FA + Interface 'Claude Well Test' + GO + file + Upload File
3) Enable CLAUDE_EXCEL_IMPORT + RUN NOW
4) Verify dv_pwel_day_status.AVG_BH_PRESS; disable schedule again."""
import datetime
import os
import shutil
import time
import zipfile
from pathlib import Path

import oracledb
from openpyxl import Workbook
from playwright.sync_api import sync_playwright

URL = os.environ.get("EC_URL", "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/")
OUT = Path(r"c:/Projects/ChoongYin_OS/tmp/ecis_recon")
XLSX = OUT / "claude_own_interface_test.xlsx"
NAME = "CLAUDE_EXCEL_IMPORT"

wb = Workbook()
ws = wb.active
ws.title = "Data"
ws.append(["Well", "Date", "Pressure"])
d = datetime.datetime(2003, 1, 5)
ws.append(["AS1_Well_001", d, 151.5])
ws.append(["AS1_Well_002", d, 152.7])
ws.append(["AS1_Well_003", d, 153.9])
wb.save(XLSX)
tmp = XLSX.with_suffix(".reordered.xlsx")
with zipfile.ZipFile(XLSX) as zin:
    names = zin.namelist()
    order = [n for n in names if n == "[Content_Types].xml"] + [n for n in names if n != "[Content_Types].xml"]
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
        for n in order:
            zout.writestr(n, zin.read(n))
shutil.move(tmp, XLSX)
print("excel ready:", XLSX)

def pick(page, dd, label):
    page.click(f'[id="{dd}_button"]')
    page.wait_for_selector(f'[id="{dd}_panel"] tr[data-item-label]', timeout=8000)
    page.locator(f'[id="{dd}_panel"] tr[data-item-label="{label}"]').click()
    page.wait_for_load_state("networkidle", timeout=15000)
    time.sleep(1.2)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_context(ignore_https_errors=True, viewport={"width": 1920, "height": 1080}).new_page()
    page.goto(URL, wait_until="domcontentloaded", timeout=60000)
    page.fill('[id="username"]', "sysadmin")
    page.fill('[id="password"]', "sysadmin")
    page.click('[id="kc-login"]')
    page.wait_for_selector('[id="menu:searchForm:searchTxt"]', timeout=60000)

    # ---- upload
    box = page.locator('[id="menu:searchForm:searchTxt"]')
    box.type("Upload Files", delay=50)
    time.sleep(1.2)
    page.locator('xpath=//*[contains(@class,"tv-link") and normalize-space(text())="Upload Files"]').first.click()
    page.wait_for_load_state("networkidle", timeout=20000)
    time.sleep(2)
    pick(page, "StandardNavigator:form:G:2:R:1:C:0:dd", "ECIS Interface Area")
    pick(page, "StandardNavigator:form:G:3:R:1:C:0:dd", "Claude Well Test")
    page.click('[id="buttongo:form:B"]')
    page.wait_for_load_state("networkidle", timeout=20000)
    time.sleep(2)
    page.set_input_files('[id="upload_file_btn:form:fa_input"]', str(XLSX))
    time.sleep(2.5)
    page.locator('xpath=//*[self::button or self::span][normalize-space(.)="Upload File"]').locator("visible=true").first.click()
    page.wait_for_load_state("networkidle", timeout=30000)
    time.sleep(3)
    print("uploaded")

    # ---- enable + run now
    page.goto(URL, wait_until="domcontentloaded", timeout=60000)
    page.wait_for_selector('[id="menu:searchForm:searchTxt"]', timeout=30000)
    time.sleep(1)
    box = page.locator('[id="menu:searchForm:searchTxt"]')
    box.fill("")
    box.type("Schedules", delay=50)
    time.sleep(1.2)
    page.locator('xpath=//*[contains(@class,"tv-link") and normalize-space(text())="Schedules"]').first.click()
    page.wait_for_load_state("networkidle", timeout=20000)
    time.sleep(2)
    dd = "nav:form:G:0:R:0:C:1:dd"
    pick(page, dd, "All")
    page.click('[id="button:form:B"]')
    page.wait_for_load_state("networkidle", timeout=20000)
    time.sleep(2.5)
    page.fill('[id="schedule:form:T:sfilter0_ft_filter"]', NAME)
    page.keyboard.press("Enter")
    page.wait_for_load_state("networkidle", timeout=15000)
    time.sleep(2.5)
    page.locator(f'xpath=//tbody[@id="schedule:form:T_data"]//input[@value="{NAME}"]').first.click()
    page.wait_for_load_state("networkidle", timeout=15000)
    time.sleep(1.5)
    page.click('[id="tab:tabPanel:job_details_more:form:G:0:R:0:C:0:cb"]')
    page.locator('xpath=//li[.//span[contains(@class,"ui-icon-save")]][1]').first.click()
    page.wait_for_load_state("networkidle", timeout=20000)
    time.sleep(4)
    page.click('[id="runNowButton:form:B"]')
    page.wait_for_load_state("networkidle", timeout=30000)
    time.sleep(2)
    dlg = page.locator('xpath=//*[self::button or self::span][normalize-space(.)="Yes" or normalize-space(.)="OK"]').locator("visible=true")
    if dlg.count():
        dlg.first.click()
    time.sleep(12)
    page.screenshot(path=str(OUT / "claude_e2e_run.png"), full_page=True)

    # ---- disable again (restore)
    page.click('[id="tab:tabPanel:job_details_more:form:G:0:R:0:C:0:cb"]')
    page.locator('xpath=//li[.//span[contains(@class,"ui-icon-save")]][1]').first.click()
    page.wait_for_load_state("networkidle", timeout=20000)
    time.sleep(3)
    browser.close()

conn = oracledb.connect(user="ECKERNEL_EC", password="energy",
                        dsn=os.environ.get("EC_DB_DSN", "localhost:1521/ORCL"))
cur = conn.cursor()
cur.execute("SELECT file_name, uploaded_into_ec_ind, parsed_date FROM imp_source_interface_file WHERE interface_code='CLAUDE_WELL_TEST'")
print("file:", cur.fetchall())
cur.execute("SELECT code, key_1, key_2, value_number FROM imp_staging WHERE interface_code='CLAUDE_WELL_TEST'")
print("staging:", cur.fetchall())
cur.execute("""SELECT * FROM (SELECT schedule_no, run_status, from_daytime FROM tv_action_instance_history
               ORDER BY from_daytime DESC NULLS LAST) WHERE ROWNUM <= 2""")
print("history:", cur.fetchall())
cur.execute("""SELECT object_code, avg_bh_temp, avg_bh_press FROM dv_pwel_day_status
               WHERE daytime = DATE '2003-01-05' AND object_code IN ('AS1_Well_001','AS1_Well_002','AS1_Well_003')""")
print("FINAL dv_pwel_day_status:", cur.fetchall())
cur.execute("SELECT enabled FROM tv_schedule_list WHERE name=:n", n=NAME)
print("schedule enabled (should be N):", cur.fetchall())
conn.close()
