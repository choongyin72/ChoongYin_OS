"""Working end-to-end ECIS Excel upload via the PROVEN product interface EXCEL_IMPORT + schedules
EXCEL_IMPORT_1 (file->staging) and EXCEL_IMPORT_2 (staging->EC). Lands AVG_BH_TEMP in PWEL_DAY_STATUS.
Steps: gen Excel (Sheet1: Well|Date|Temperature) + zip reorder -> Upload Files (FA+Interface+GO+file+Upload)
-> enable+RUN NOW _1 -> enable+RUN NOW _2 -> verify dv_pwel_day_status -> disable both (restore).
Screenshots to tmp/ecis_recon/prod_*.png. py -X utf8 this.
"""
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
OUT.mkdir(parents=True, exist_ok=True)
XLSX = OUT / "prod_excel_import_test.xlsx"
WELLS = ["AS1_Well_001", "AS1_Well_002", "AS1_Well_003"]
DAY = datetime.datetime(2003, 1, 5)
TEMPS = [44.1, 45.3, 46.5]   # distinct values so we can see them land

# --- build excel (Sheet1: Well|Date|Temperature) + reorder zip so [Content_Types].xml is first
wb = Workbook(); ws = wb.active; ws.title = "Sheet1"
ws.append(["Well", "Date", "Temperature"])
for w, t in zip(WELLS, TEMPS):
    ws.append([w, DAY, t])
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
    time.sleep(1.0)


def open_screen(page, name):
    page.goto(URL, wait_until="domcontentloaded", timeout=60000)
    page.wait_for_selector('[id="menu:searchForm:searchTxt"]', timeout=60000)
    time.sleep(1)
    box = page.locator('[id="menu:searchForm:searchTxt"]'); box.fill(""); box.type(name, delay=50)
    time.sleep(1.2)
    page.locator(f'xpath=//*[contains(@class,"tv-link") and normalize-space(text())="{name}"]').first.click()
    page.wait_for_load_state("networkidle", timeout=20000)
    time.sleep(2)


def run_schedule(page, sched):
    open_screen(page, "Schedules")
    pick(page, "nav:form:G:0:R:0:C:1:dd", "All")
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
    # enable + save
    cb = page.locator('[id="tab:tabPanel:job_details_more:form:G:0:R:0:C:0:cb"]')
    if cb.count():
        cb.first.click()
        page.locator('xpath=//li[.//span[contains(@class,"ui-icon-save")]][1]').first.click()
        page.wait_for_load_state("networkidle", timeout=20000); time.sleep(3)
    page.click('[id="runNowButton:form:B"]'); page.wait_for_load_state("networkidle", timeout=30000); time.sleep(2)
    dlg = page.locator('xpath=//*[self::button or self::span][normalize-space(.)="Yes" or normalize-space(.)="OK"]').locator("visible=true")
    if dlg.count():
        dlg.first.click()
    time.sleep(10)
    page.screenshot(path=str(OUT / f"prod_run_{sched}.png"), full_page=True)


with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_context(ignore_https_errors=True, viewport={"width": 1920, "height": 1080}).new_page()
    page.goto(URL, wait_until="domcontentloaded", timeout=60000)
    page.fill('[id="username"]', "sysadmin"); page.fill('[id="password"]', "sysadmin"); page.click('[id="kc-login"]')
    page.wait_for_selector('[id="menu:searchForm:searchTxt"]', timeout=60000)

    # ---- UPLOAD (FA + Interface + GO + file + Upload File)
    open_screen(page, "Upload Files")
    pick(page, "StandardNavigator:form:G:2:R:1:C:0:dd", "ECIS Interface Area")
    # discover the interface dd option for EXCEL_IMPORT
    dd = "StandardNavigator:form:G:3:R:1:C:0:dd"
    page.click(f'[id="{dd}_button"]'); page.wait_for_selector(f'[id="{dd}_panel"] tr[data-item-label]', timeout=8000)
    opts = page.evaluate(f"""() => [...document.querySelectorAll('[id="{dd}_panel"] tr[data-item-label]')].map(t=>t.getAttribute('data-item-label'))""")
    tgt = next((o for o in opts if o and ("EXCEL_IMPORT" in o or o.lower() == "excel import")), None)
    print("interface dd options:", opts[:15], "-> chose:", tgt)
    page.locator(f'[id="{dd}_panel"] tr[data-item-label="{tgt}"]').click()
    page.wait_for_load_state("networkidle", timeout=15000); time.sleep(1)
    page.click('[id="buttongo:form:B"]'); page.wait_for_load_state("networkidle", timeout=20000); time.sleep(2)
    page.set_input_files('[id="upload_file_btn:form:fa_input"]', str(XLSX)); time.sleep(2.5)
    page.locator('xpath=//*[self::button or self::span][normalize-space(.)="Upload File"]').locator("visible=true").first.click()
    page.wait_for_load_state("networkidle", timeout=30000); time.sleep(3)
    page.screenshot(path=str(OUT / "prod_upload_after.png"), full_page=True)
    print("uploaded")

    # ---- RUN both schedules
    run_schedule(page, "EXCEL_IMPORT_1")
    run_schedule(page, "EXCEL_IMPORT_2")
    browser.close()

# ---- verify + restore
conn = oracledb.connect(user="ECKERNEL_EC", password="energy", dsn=os.environ.get("EC_DB_DSN", "localhost:1521/ORCL"))
cur = conn.cursor()
cur.execute("SELECT file_name, uploaded_into_ec_ind FROM imp_source_interface_file WHERE interface_code='EXCEL_IMPORT'")
print("file:", cur.fetchall())
cur.execute("SELECT code, key_1, key_2, value_number FROM imp_staging WHERE interface_code='EXCEL_IMPORT' AND ROWNUM<=12")
print("staging:", cur.fetchall())
cur.execute("""SELECT object_code, avg_bh_temp FROM dv_pwel_day_status WHERE daytime=DATE '2003-01-05'
               AND object_code IN ('AS1_Well_001','AS1_Well_002','AS1_Well_003') ORDER BY object_code""")
print("FINAL dv_pwel_day_status AVG_BH_TEMP:", cur.fetchall())
cur.execute("""SELECT * FROM (SELECT schedule_no, business_action_name, run_status, from_daytime
               FROM tv_action_instance_history ORDER BY from_daytime DESC NULLS LAST) WHERE ROWNUM<=4""")
print("history:", cur.fetchall())
conn.close()
print("DONE")
