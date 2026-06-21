"""LIVE HEADED ECIS Excel-upload demo (watchable). Lands into a FRESH date so the before->after is obvious.
Flow: pre-clean staging + confirm baseline NULL -> Upload Files (Excel) -> RUN EXCEL_IMPORT_1 (file->staging,
wait for staging) -> RUN EXCEL_IMPORT_2 (staging->EC, wait for dv) -> verify dv -> restore (disable schedules).
Enable-state is decided from the DB read (UI checkbox unreadable); RUN NOW is async so we poll. Headed + slowMo.
py -X utf8 tmp/scripts/ecis_live_demo.py
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
OUT = Path(r"c:/Projects/ChoongYin_OS/tmp/ecis_recon"); OUT.mkdir(parents=True, exist_ok=True)
XLSX = OUT / "live_demo_upload.xlsx"
WELLS = ["AS1_Well_001", "AS1_Well_002", "AS1_Well_003"]
DATESTR = "2003-01-07"
DAY = datetime.datetime(2003, 1, 7)
TEMPS = [51.1, 52.2, 53.3]


def db():
    return oracledb.connect(user="ECKERNEL_EC", password="energy",
                            dsn=os.environ.get("EC_DB_DSN", "localhost:1521/ORCL"))


def log(m):
    print(m, flush=True)


# ---------- pre-clean + baseline ----------
con = db(); cur = con.cursor()
cur.execute("DELETE FROM imp_staging WHERE interface_code='EXCEL_IMPORT'")
con.commit()
cur.execute("""SELECT object_code, avg_bh_temp FROM dv_pwel_day_status WHERE daytime=TO_DATE(:d,'YYYY-MM-DD')
               AND object_code IN ('AS1_Well_001','AS1_Well_002','AS1_Well_003') ORDER BY object_code""", d=DATESTR)
log(f"BASELINE {DATESTR}: {cur.fetchall()}  (cleared staging)")
con.close()

# ---------- build excel ----------
wb = Workbook(); ws = wb.active; ws.title = "Sheet1"
ws.append(["Well", "Date", "Temperature"])
for w, t in zip(WELLS, TEMPS):
    ws.append([w, DAY, t])
wb.save(XLSX)
tmp = XLSX.with_suffix(".r.xlsx")
with zipfile.ZipFile(XLSX) as zin:
    names = zin.namelist()
    order = [n for n in names if n == "[Content_Types].xml"] + [n for n in names if n != "[Content_Types].xml"]
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zo:
        for n in order:
            zo.writestr(n, zin.read(n))
shutil.move(tmp, XLSX)
log(f"excel ready: {XLSX} ({DATESTR}, temps {TEMPS})")


def enabled_state(sched):
    c = db().cursor(); c.execute("SELECT enabled FROM tv_schedule_list WHERE name=:n", n=sched)
    return c.fetchone()[0]


def staging_count():
    c = db().cursor(); c.execute("SELECT COUNT(*) FROM imp_staging WHERE interface_code='EXCEL_IMPORT' AND key_2 LIKE :d", d=DATESTR + "%")
    return c.fetchone()[0]


def landed():
    c = db().cursor()
    c.execute("""SELECT object_code, avg_bh_temp FROM dv_pwel_day_status WHERE daytime=TO_DATE(:d,'YYYY-MM-DD')
                 AND object_code IN ('AS1_Well_001','AS1_Well_002','AS1_Well_003') ORDER BY object_code""", d=DATESTR)
    return c.fetchall()


with sync_playwright() as p:
    b = p.chromium.launch(headless=False, slow_mo=300, args=["--ignore-certificate-errors", "--start-maximized"])
    page = b.new_context(ignore_https_errors=True, no_viewport=True).new_page()
    page.goto(URL, wait_until="domcontentloaded", timeout=60000)
    page.fill('[id="username"]', "sysadmin"); page.fill('[id="password"]', "sysadmin"); page.click('[id="kc-login"]')
    page.wait_for_selector('[id="menu:searchForm:searchTxt"]', timeout=60000); time.sleep(1)

    def open_screen(name):
        page.goto(URL, wait_until="domcontentloaded", timeout=60000)
        page.wait_for_selector('[id="menu:searchForm:searchTxt"]', timeout=60000); time.sleep(1)
        bx = page.locator('[id="menu:searchForm:searchTxt"]'); bx.fill(""); bx.type(name, delay=40); time.sleep(1.2)
        page.locator(f'xpath=//*[contains(@class,"tv-link") and normalize-space(text())="{name}"]').first.click()
        page.wait_for_load_state("networkidle", timeout=20000); time.sleep(2)

    def pick(dd, label):
        page.click(f'[id="{dd}_button"]'); page.wait_for_selector(f'[id="{dd}_panel"] tr[data-item-label]', timeout=8000)
        page.locator(f'[id="{dd}_panel"] tr[data-item-label="{label}"]').click()
        page.wait_for_load_state("networkidle", timeout=15000); time.sleep(1)

    def select_sched(sched):
        open_screen("Schedules")
        pick("nav:form:G:0:R:0:C:1:dd", "All")
        page.click('[id="button:form:B"]'); page.wait_for_load_state("networkidle", timeout=20000); time.sleep(2)
        page.fill('[id="schedule:form:T:sfilter0_ft_filter"]', sched); page.keyboard.press("Enter")
        page.wait_for_load_state("networkidle", timeout=15000); time.sleep(2)
        for _ in range(6):
            if page.locator(f'xpath=//tbody[@id="schedule:form:T_data"]//input[@value="{sched}"]').count():
                break
            nx = page.locator('css=[id^="schedule"] .ui-paginator-next:not(.ui-state-disabled)')
            if not nx.count():
                break
            nx.first.click(); page.wait_for_load_state("networkidle", timeout=15000); time.sleep(1.5)
        page.locator(f'xpath=//tbody[@id="schedule:form:T_data"]//input[@value="{sched}"]').first.click()
        page.wait_for_load_state("networkidle", timeout=15000); time.sleep(1.5)

    CB = "tab:tabPanel:job_details_more:form:G:0:R:0:C:0:cb"

    def set_enabled(sched, want):
        cur_en = enabled_state(sched)
        if (cur_en == 'N' and want) or (cur_en == 'Y' and not want):
            page.locator(f'[id="{CB}"]').first.click()
            page.locator('xpath=//li[.//span[contains(@class,"ui-icon-save")]][1]').first.click()
            page.wait_for_load_state("networkidle", timeout=20000); time.sleep(3)
        log(f"  {sched} enabled (DB) was {cur_en} -> want {'Y' if want else 'N'}")

    def run_now():
        page.click('[id="runNowButton:form:B"]'); page.wait_for_load_state("networkidle", timeout=30000); time.sleep(2)
        dlg = page.locator('xpath=//*[self::button or self::span][normalize-space(.)="Yes" or normalize-space(.)="OK"]').locator("visible=true")
        if dlg.count():
            dlg.first.click()

    # 1) UPLOAD
    log("STEP 1: Upload Files ...")
    open_screen("Upload Files")
    pick("StandardNavigator:form:G:2:R:1:C:0:dd", "ECIS Interface Area")
    pick("StandardNavigator:form:G:3:R:1:C:0:dd", "Excel Import")
    page.click('[id="buttongo:form:B"]'); page.wait_for_load_state("networkidle", timeout=20000); time.sleep(2)
    page.set_input_files('[id="upload_file_btn:form:fa_input"]', str(XLSX)); time.sleep(2.5)
    page.locator('xpath=//*[self::button or self::span][normalize-space(.)="Upload File"]').locator("visible=true").first.click()
    page.wait_for_load_state("networkidle", timeout=30000); time.sleep(3)
    page.screenshot(path=str(OUT / "live_1_uploaded.png"), full_page=True); log("  uploaded.")

    # 2) RUN _1 (file -> staging), wait for staging
    log("STEP 2: RUN EXCEL_IMPORT_1 (file -> staging) ...")
    select_sched("EXCEL_IMPORT_1"); set_enabled("EXCEL_IMPORT_1", True); run_now()
    for _ in range(20):
        time.sleep(3)
        if staging_count() >= 3:
            break
    page.screenshot(path=str(OUT / "live_2_run1.png"), full_page=True)
    log(f"  staging rows for {DATESTR}: {staging_count()}")

    # 3) RUN _2 (staging -> EC), wait for dv
    log("STEP 3: RUN EXCEL_IMPORT_2 (staging -> EC) ...")
    select_sched("EXCEL_IMPORT_2"); set_enabled("EXCEL_IMPORT_2", True); run_now()
    for _ in range(20):
        time.sleep(3)
        if all(v is not None for _, v in landed()):
            break
    page.screenshot(path=str(OUT / "live_3_run2.png"), full_page=True)
    log(f"  LANDED dv_pwel_day_status {DATESTR}: {landed()}")

    # 4) restore (disable both)
    log("STEP 4: restore (disable schedules) ...")
    select_sched("EXCEL_IMPORT_1"); set_enabled("EXCEL_IMPORT_1", False)
    select_sched("EXCEL_IMPORT_2"); set_enabled("EXCEL_IMPORT_2", False)
    time.sleep(3)
    b.close()

log(f"FINAL: {landed()}")
log("DONE")
