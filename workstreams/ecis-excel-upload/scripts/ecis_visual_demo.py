"""Visual demo addressing both gaps: (1) show the ECIS CONFIG screen (Mapping Configuration: CLAUDE_WELL_TEST
interface + mappings); (2) show the PWEL day-status EC screen BEFORE (empty) and AFTER (filled) for a fresh
date 2003-01-09. Headed. Navigator cascade is driven by scanning each dd's options for the 'AS1' path.
py -X utf8 tmp/scripts/ecis_visual_demo.py
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
XLSX = OUT / "visual_demo_upload.xlsx"
WELLS = ["AS1_Well_001", "AS1_Well_002", "AS1_Well_003"]
DATESTR = "2003-01-09"; DAY = datetime.datetime(2003, 1, 9); TEMPS = [61.1, 62.2, 63.3]
PWEL = "Daily Prod Well Status 1, by Well"


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


def staging_for(datestr):
    c = db().cursor(); c.execute("SELECT COUNT(*) FROM imp_staging WHERE interface_code='EXCEL_IMPORT' AND key_2 LIKE :d", d=datestr + "%"); return c.fetchone()[0]


# clean baseline
con = db(); cur = con.cursor(); cur.execute("DELETE FROM imp_staging WHERE interface_code='EXCEL_IMPORT'"); con.commit(); con.close()
log(f"BASELINE {DATESTR}: {landed()}")

# excel
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
    b = p.chromium.launch(headless=False, slow_mo=250, args=["--ignore-certificate-errors", "--start-maximized"])
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

    def pick(dd, label):
        page.click(f'[id="{dd}_button"]'); page.wait_for_selector(f'[id="{dd}_panel"] tr[data-item-label]', timeout=8000)
        page.locator(f'[id="{dd}_panel"] tr[data-item-label="{label}"]').click()
        page.wait_for_load_state("networkidle", timeout=15000); time.sleep(1)

    # ---------- PART 1: CONFIG screen ----------
    log("PART 1: Mapping Configuration (ECIS config) ...")
    open_screen("Mapping Configuration")
    # filter the SOURCE INTERFACE grid to CLAUDE_WELL_TEST if a filter exists, else just screenshot
    try:
        page.evaluate("""()=>{const e=document.getElementById('imp_interface_table:form:T:tfo'); if(e) e.click();}""")
        time.sleep(1)
        fi = page.locator('[id="imp_interface_table:form:T:sfilter0_ft_filter"]')
        if fi.count():
            fi.first.fill("CLAUDE_WELL_TEST"); page.keyboard.press("Enter"); page.wait_for_load_state("networkidle", timeout=15000); time.sleep(1.5)
    except Exception as e:
        log("  (filter skip) " + str(e)[:60])
    # click the CLAUDE row to load its mappings below
    try:
        page.locator('xpath=//tbody[@id="imp_interface_table:form:T_data"]//input[@value="CLAUDE_WELL_TEST"]').first.click()
        page.wait_for_load_state("networkidle", timeout=15000); time.sleep(2)
    except Exception as e:
        log("  (row select skip) " + str(e)[:60])
    page.screenshot(path=str(OUT / "config_mapping_configuration.png"), full_page=True)
    log("  captured config_mapping_configuration.png")

    # ---------- PART 2: PWEL BEFORE ----------
    def open_pwel_and_go():
        open_screen(PWEL)
        for g in (0, 1):
            di = page.locator(f'[id="nav:form:G:{g}:R:1:C:0:da_input"]')
            if di.count():
                di.first.fill(DATESTR); page.keyboard.press("Tab"); time.sleep(0.6)
        # cascade: for each nav dd G:2..G:6, open + pick an option containing 'AS1' (walks PU->Area->Fac->Well)
        for g in range(2, 7):
            dd = f"nav:form:G:{g}:R:1:C:0:dd"
            if not page.locator(f'[id="{dd}_button"]').count():
                continue
            try:
                page.click(f'[id="{dd}_button"]'); page.wait_for_selector(f'[id="{dd}_panel"] tr[data-item-label]', timeout=6000)
                opts = page.evaluate(f"""()=>[...document.querySelectorAll('[id="{dd}_panel"] tr[data-item-label]')].map(t=>t.getAttribute('data-item-label'))""")
                tgt = next((o for o in opts if o and 'AS1' in o.upper()), None) or (opts[0] if opts else None)
                if tgt:
                    page.locator(f'[id="{dd}_panel"] tr[data-item-label="{tgt}"]').first.click()
                    page.wait_for_load_state("networkidle", timeout=12000); time.sleep(0.8)
                    log(f"    {dd}: picked '{tgt}' (of {opts[:6]})")
                else:
                    page.keyboard.press("Escape")
            except Exception as e:
                log(f"    {dd}: {str(e)[:50]}")
        page.click('[id="button:form:B"]'); page.wait_for_load_state("networkidle", timeout=25000); time.sleep(2.5)

    log("PART 2: PWEL screen BEFORE ...")
    open_pwel_and_go()
    page.screenshot(path=str(OUT / "pwel_BEFORE.png"), full_page=True)

    # ---------- PART 3: upload + run ----------
    log("PART 3: upload + run pipeline ...")
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
        page.fill('[id="schedule:form:T:sfilter0_ft_filter"]', sched); page.keyboard.press("Enter")
        page.wait_for_load_state("networkidle", timeout=15000); time.sleep(2)
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

    # ---------- PART 4: PWEL AFTER ----------
    log("PART 4: PWEL screen AFTER ...")
    open_pwel_and_go()
    page.screenshot(path=str(OUT / "pwel_AFTER.png"), full_page=True)

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

log(f"FINAL dv {DATESTR}: {landed()}")
log("DONE")
