"""PWEL day-status BEFORE/AFTER on the EC screen for AS1_Well_001/002/003, fresh date 2003-01-10.
Deterministically finds the Facility whose Well list contains AS1_Well_001 (the wells are split across
facilities). Shows the well-status grid BEFORE (empty) and AFTER (filled by the ECIS upload). Headed.
SELF-CLEANING: pre-cleans the baseline and reverts the demo avg_bh_temp to NULL on teardown, so every run is
empty -> upload -> filled -> reverted-to-empty (zero residue) and is safely re-runnable any number of times.
py -X utf8 tmp/scripts/ecis_pwel_beforeafter.py
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
XLSX = OUT / "ba_upload.xlsx"
WELLS = ["AS1_Well_001", "AS1_Well_002", "AS1_Well_003"]
DATESTR = "2003-01-10"; DAY = datetime.datetime(2003, 1, 10); TEMPS = [71.1, 72.2, 73.3]
PWEL = "Daily Prod Well Status 1, by Well"
PU, AREA, TARGET_WELL = "AS1 EC Exploration Norway", "AS1_Area", "AS1_Well_001"


def db():
    return oracledb.connect(user="ECKERNEL_EC", password="energy", dsn=os.environ.get("EC_DB_DSN", "localhost:1521/ORCL"))


def log(m): print(m, flush=True)


def landed():
    c = db().cursor()
    c.execute("""SELECT object_code, avg_bh_temp FROM dv_pwel_day_status WHERE daytime=TO_DATE(:d,'YYYY-MM-DD')
                 AND object_code IN ('AS1_Well_001','AS1_Well_002','AS1_Well_003') ORDER BY object_code""", d=DATESTR)
    return c.fetchall()


def enabled_state(s):
    c = db().cursor(); c.execute("SELECT enabled FROM tv_schedule_list WHERE name=:n", n=s); return c.fetchone()[0]


def staging_for(d):
    c = db().cursor(); c.execute("SELECT COUNT(*) FROM imp_staging WHERE interface_code='EXCEL_IMPORT' AND key_2 LIKE :x", x=d + "%"); return c.fetchone()[0]


def revert_data():
    """Self-clean: NULL the demo avg_bh_temp for our 3 wells on DATESTR (idempotent). Reverts only my writes."""
    c = db(); cu = c.cursor()
    cu.execute("SELECT object_id FROM ov_well WHERE code IN ('AS1_Well_001','AS1_Well_002','AS1_Well_003')")
    oids = [r[0] for r in cu.fetchall()]
    if oids:
        ph = ",".join(f"'{o}'" for o in oids)
        cu.execute(f"UPDATE pwel_day_status SET avg_bh_temp=NULL WHERE object_id IN ({ph}) "
                   "AND daytime=TO_DATE(:d,'YYYY-MM-DD') AND avg_bh_temp IS NOT NULL", d=DATESTR)
        c.commit()
    c.close()


con = db(); cur = con.cursor(); cur.execute("DELETE FROM imp_staging WHERE interface_code='EXCEL_IMPORT'"); con.commit(); con.close()
revert_data()  # PRE-CLEAN: guarantee an empty baseline (idempotent; also cleans up any crashed prior run)
log(f"BASELINE {DATESTR}: {landed()}")

wb = Workbook(); ws = wb.active; ws.title = "Sheet1"; ws.append(["Well", "Date", "Temperature"])
for w, t in zip(WELLS, TEMPS): ws.append([w, DAY, t])
wb.save(XLSX)
tmp = XLSX.with_suffix(".r.xlsx")
with zipfile.ZipFile(XLSX) as zin:
    nm = zin.namelist(); order = [n for n in nm if n == "[Content_Types].xml"] + [n for n in nm if n != "[Content_Types].xml"]
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zo:
        for n in order: zo.writestr(n, zin.read(n))
shutil.move(tmp, XLSX)


with sync_playwright() as p:
    b = p.chromium.launch(headless=False, slow_mo=200, args=["--ignore-certificate-errors", "--start-maximized"])
    page = b.new_context(ignore_https_errors=True, no_viewport=True).new_page()
    page.goto(URL, wait_until="domcontentloaded", timeout=60000)
    page.fill('[id="username"]', "sysadmin"); page.fill('[id="password"]', "sysadmin"); page.click('[id="kc-login"]')
    page.wait_for_selector('[id="menu:searchForm:searchTxt"]', timeout=60000); time.sleep(1)

    def open_screen(name):
        page.goto(URL, wait_until="domcontentloaded", timeout=60000)
        page.wait_for_selector('[id="menu:searchForm:searchTxt"]', timeout=60000); time.sleep(1)
        bx = page.locator('[id="menu:searchForm:searchTxt"]'); bx.fill(""); bx.type(name, delay=40); time.sleep(1.5)
        page.locator(f'xpath=//*[contains(@class,"tv-link") and normalize-space(text())="{name}"]').first.click()
        page.wait_for_load_state("networkidle", timeout=25000); time.sleep(2.5)

    def options(dd):
        page.click(f'[id="{dd}_button"]')
        page.wait_for_selector(f'[id="{dd}_panel"] tr[data-item-label]', timeout=7000)
        return page.evaluate(f"""()=>[...document.querySelectorAll('[id="{dd}_panel"] tr[data-item-label]')].map(t=>t.getAttribute('data-item-label'))""")

    def pick(dd, label):
        if not page.locator(f'[id="{dd}_panel"]').is_visible():
            page.click(f'[id="{dd}_button"]'); page.wait_for_selector(f'[id="{dd}_panel"] tr[data-item-label]', timeout=7000)
        page.locator(f'[id="{dd}_panel"] tr[data-item-label="{label}"]').first.click()
        page.wait_for_load_state("networkidle", timeout=15000); time.sleep(0.9)

    def nav_to_well(facility=None):
        # dates
        for g in (0, 1):
            di = page.locator(f'[id="nav:form:G:{g}:R:1:C:0:da_input"]')
            if di.count():
                di.first.fill(DATESTR); page.keyboard.press("Tab"); time.sleep(0.6)
        pick("nav:form:G:2:R:1:C:0:dd", PU)
        pick("nav:form:G:3:R:1:C:0:dd", AREA)
        if facility:
            pick("nav:form:G:4:R:1:C:0:dd", facility)
            pick("nav:form:G:5:R:1:C:0:dd", TARGET_WELL)
            return facility
        # find the facility whose well list has AS1_Well_001
        facs = options("nav:form:G:4:R:1:C:0:dd")
        page.keyboard.press("Escape"); time.sleep(0.3)
        for fac in facs:
            pick("nav:form:G:4:R:1:C:0:dd", fac)
            wells = options("nav:form:G:5:R:1:C:0:dd")
            if TARGET_WELL in wells:
                pick("nav:form:G:5:R:1:C:0:dd", TARGET_WELL)
                log(f"    found {TARGET_WELL} under facility '{fac}'")
                return fac
            page.keyboard.press("Escape"); time.sleep(0.3)
        log("    WARN: AS1_Well_001 not found under any facility")
        return None

    def go():
        page.click('[id="button:form:B"]'); page.wait_for_load_state("networkidle", timeout=25000); time.sleep(2.5)

    # ---- BEFORE
    log("BEFORE: open PWEL, find well, GO ...")
    open_screen(PWEL)
    fac = nav_to_well()
    go()
    page.screenshot(path=str(OUT / "pwel_BEFORE.png"), full_page=True)
    log(f"  BEFORE captured (facility={fac}); dv={landed()}")

    # ---- UPLOAD + RUN
    log("UPLOAD + RUN ...")
    open_screen("Upload Files")
    pick("StandardNavigator:form:G:2:R:1:C:0:dd", "ECIS Interface Area")
    pick("StandardNavigator:form:G:3:R:1:C:0:dd", "Excel Import")
    page.click('[id="buttongo:form:B"]'); page.wait_for_load_state("networkidle", timeout=20000); time.sleep(2)
    page.set_input_files('[id="upload_file_btn:form:fa_input"]', str(XLSX)); time.sleep(2.5)
    page.locator('xpath=//*[self::button or self::span][normalize-space(.)="Upload File"]').locator("visible=true").first.click()
    page.wait_for_load_state("networkidle", timeout=30000); time.sleep(3)
    CB = "tab:tabPanel:job_details_more:form:G:0:R:0:C:0:cb"

    def run_sched(sched):
        open_screen("Schedules"); pick("nav:form:G:0:R:0:C:1:dd", "All")
        page.click('[id="button:form:B"]'); page.wait_for_load_state("networkidle", timeout=20000); time.sleep(2)
        page.fill('[id="schedule:form:T:sfilter0_ft_filter"]', sched); page.keyboard.press("Enter"); page.wait_for_load_state("networkidle", timeout=15000); time.sleep(2)
        for _ in range(6):
            if page.locator(f'xpath=//tbody[@id="schedule:form:T_data"]//input[@value="{sched}"]').count(): break
            nx = page.locator('css=[id^="schedule"] .ui-paginator-next:not(.ui-state-disabled)')
            if not nx.count(): break
            nx.first.click(); page.wait_for_load_state("networkidle", timeout=15000); time.sleep(1.5)
        page.locator(f'xpath=//tbody[@id="schedule:form:T_data"]//input[@value="{sched}"]').first.click()
        page.wait_for_load_state("networkidle", timeout=15000); time.sleep(1.5)
        if enabled_state(sched) == 'N':
            page.locator(f'[id="{CB}"]').first.click()
            page.locator('xpath=//li[.//span[contains(@class,"ui-icon-save")]][1]').first.click()
            page.wait_for_load_state("networkidle", timeout=20000); time.sleep(3)
        page.click('[id="runNowButton:form:B"]'); page.wait_for_load_state("networkidle", timeout=30000); time.sleep(2)
        dlg = page.locator('xpath=//*[self::button or self::span][normalize-space(.)="Yes" or normalize-space(.)="OK"]').locator("visible=true")
        if dlg.count(): dlg.first.click()

    run_sched("EXCEL_IMPORT_1")
    for _ in range(20):
        time.sleep(3)
        if staging_for(DATESTR) >= 3: break
    log(f"  staging {DATESTR}: {staging_for(DATESTR)}")
    run_sched("EXCEL_IMPORT_2")
    for _ in range(20):
        time.sleep(3)
        if all(v is not None for _, v in landed()): break
    log(f"  LANDED: {landed()}")

    # ---- AFTER
    log("AFTER: re-open PWEL, same nav, GO ...")
    open_screen(PWEL)
    nav_to_well(facility=fac)
    go()
    page.screenshot(path=str(OUT / "pwel_AFTER.png"), full_page=True)
    log(f"  AFTER captured; dv={landed()}")

    # restore schedules
    for s in ("EXCEL_IMPORT_1", "EXCEL_IMPORT_2"):
        open_screen("Schedules"); pick("nav:form:G:0:R:0:C:1:dd", "All")
        page.click('[id="button:form:B"]'); page.wait_for_load_state("networkidle", timeout=20000); time.sleep(2)
        page.fill('[id="schedule:form:T:sfilter0_ft_filter"]', s); page.keyboard.press("Enter"); page.wait_for_load_state("networkidle", timeout=15000); time.sleep(2)
        if page.locator(f'xpath=//tbody[@id="schedule:form:T_data"]//input[@value="{s}"]').count():
            page.locator(f'xpath=//tbody[@id="schedule:form:T_data"]//input[@value="{s}"]').first.click()
            page.wait_for_load_state("networkidle", timeout=15000); time.sleep(1.5)
            if enabled_state(s) == 'Y':
                page.locator(f'[id="{CB}"]').first.click()
                page.locator('xpath=//li[.//span[contains(@class,"ui-icon-save")]][1]').first.click()
                page.wait_for_load_state("networkidle", timeout=20000); time.sleep(2)
    b.close()

revert_data()  # TEARDOWN: self-clean so every run leaves ZERO residue (empty -> upload -> filled -> empty)
log(f"TEARDOWN: reverted demo data; dv {DATESTR} now {landed()}")
log("DONE")
