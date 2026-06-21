"""Upload Files, proper sequence: FA='ECIS Interface Area' -> Interface (cascaded) ->
set file -> detect upload control -> GO -> DB-verify IMP_SOURCE_INTERFACE_FILE."""
import os
import time
from pathlib import Path

import oracledb
from playwright.sync_api import sync_playwright

URL = os.environ.get("EC_URL", "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/")
OUT = Path(r"c:/Projects/ChoongYin_OS/tmp/ecis_recon")
XLSX = OUT / "claude_excel_import_test.xlsx"

def pick(page, dd, label):
    page.click(f'[id="{dd}_button"]')
    page.wait_for_selector(f'[id="{dd}_panel"] tr[data-item-label]', timeout=8000)
    opts = page.evaluate(f"""() => [...document.querySelectorAll('[id="{dd}_panel"] tr[data-item-label]')]
        .map(tr => tr.getAttribute('data-item-label'))""")
    tgt = label if label in opts else next((o for o in opts if o and label.lower() in o.lower()), None)
    if not tgt:
        page.keyboard.press("Escape")
        return opts
    page.locator(f'[id="{dd}_panel"] tr[data-item-label="{tgt}"]').click()
    page.wait_for_load_state("networkidle", timeout=15000)
    time.sleep(1.2)
    return tgt

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_context(ignore_https_errors=True, viewport={"width": 1920, "height": 1080}).new_page()
    page.goto(URL, wait_until="domcontentloaded", timeout=60000)
    page.fill('[id="username"]', "sysadmin")
    page.fill('[id="password"]', "sysadmin")
    page.click('[id="kc-login"]')
    page.wait_for_selector('[id="menu:searchForm:searchTxt"]', timeout=60000)
    box = page.locator('[id="menu:searchForm:searchTxt"]')
    box.type("Upload Files", delay=50)
    time.sleep(1.2)
    page.locator('xpath=//*[contains(@class,"tv-link") and normalize-space(text())="Upload Files"]').first.click()
    page.wait_for_load_state("networkidle", timeout=20000)
    time.sleep(2)

    print("FA pick:", pick(page, "StandardNavigator:form:G:2:R:1:C:0:dd", "ECIS Interface Area"))
    print("Interface pick:", pick(page, "StandardNavigator:form:G:3:R:1:C:0:dd", "Excel Import"))

    page.set_input_files('[id="upload_file_btn:form:fa_input"]', str(XLSX))
    time.sleep(3)
    page.wait_for_load_state("networkidle", timeout=30000)
    page.screenshot(path=str(OUT / "upload2_after_file.png"), full_page=True)
    # if an explicit upload/confirm button appeared near the fileupload widget, click it
    btns = page.evaluate("""() => [...document.querySelectorAll('button, span.ui-button, a.ui-button')]
        .filter(e => e.offsetParent).map(e => ({id: e.id, t: (e.textContent||'').trim().slice(0,30)}))
        .filter(b => /upload|save|ok/i.test(b.t) && !/Upload Files/.test(b.t)).slice(0, 6)""")
    print("candidate confirm buttons:", btns)
    upl = page.locator('xpath=//*[self::button or self::span][normalize-space(.)="Upload File"]').locator("visible=true")
    if upl.count():
        upl.first.click()
        page.wait_for_load_state("networkidle", timeout=30000)
        time.sleep(3)
        print("clicked Upload File")
    page.click('[id="buttongo:form:B"]')
    page.wait_for_load_state("networkidle", timeout=20000)
    time.sleep(2.5)
    page.screenshot(path=str(OUT / "upload2_after_go.png"), full_page=True)
    browser.close()

conn = oracledb.connect(user="ECKERNEL_EC", password="energy",
                        dsn=os.environ.get("EC_DB_DSN", "localhost:1521/ORCL"))
cur = conn.cursor()
cur.execute("""SELECT interface_code, file_name, file_no, file_source, uploaded_into_ec_ind, created_date
               FROM imp_source_interface_file ORDER BY created_date DESC FETCH FIRST 5 ROWS ONLY""")
print("\nlatest IMP_SOURCE_INTERFACE_FILE rows:")
for r in cur.fetchall():
    print(" ", r)
conn.close()
