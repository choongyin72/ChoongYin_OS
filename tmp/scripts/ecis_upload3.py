"""Upload round 3: FA+Interface -> set file -> inspect widget state + real button ids ->
click the enabled UPLOAD FILE button -> GO -> DB verify."""
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
    page.locator(f'[id="{dd}_panel"] tr[data-item-label="{label}"]').click()
    page.wait_for_load_state("networkidle", timeout=15000)
    time.sleep(1.2)

WIDGET = """
() => {
  const vis = e => e && e.offsetParent !== null;
  const btns = [...document.querySelectorAll('button')].filter(vis)
    .map(b => ({id: b.id, t: (b.textContent||'').trim().slice(0,22),
                disabled: b.disabled || b.className.includes('ui-state-disabled')}));
  const files = [...document.querySelectorAll('input[type="file"]')].map(e => e.id);
  const chosen = [...document.querySelectorAll('.ui-fileupload-files, .ui-fileupload-filename')]
    .map(e => (e.textContent||'').trim()).filter(t => t);
  return {btns: btns.filter(b => b.t || b.id.includes('upload')), files, chosen};
}
"""

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
    pick(page, "StandardNavigator:form:G:2:R:1:C:0:dd", "ECIS Interface Area")
    pick(page, "StandardNavigator:form:G:3:R:1:C:0:dd", "Excel Import")

    print("BEFORE file:", page.evaluate(WIDGET))
    page.set_input_files('[id="upload_file_btn:form:fa_input"]', str(XLSX))
    time.sleep(2.5)
    state = page.evaluate(WIDGET)
    print("AFTER file:", state)
    page.screenshot(path=str(OUT / "upload3_widget.png"), full_page=True)

    # click the real, ENABLED upload button
    target = next((b for b in state["btns"] if "UPLOAD" in b["t"].upper() and not b["disabled"]), None)
    print("upload button to click:", target)
    if target and target["id"]:
        page.click(f'[id="{target["id"]}"]')
    elif target:
        page.locator(f'xpath=//button[normalize-space(.)="{target["t"]}"]').locator("visible=true").first.click()
    page.wait_for_load_state("networkidle", timeout=30000)
    time.sleep(3)
    page.screenshot(path=str(OUT / "upload3_after_upload.png"), full_page=True)
    page.click('[id="buttongo:form:B"]')
    page.wait_for_load_state("networkidle", timeout=20000)
    time.sleep(2.5)
    page.screenshot(path=str(OUT / "upload3_after_go.png"), full_page=True)
    browser.close()

conn = oracledb.connect(user="ECKERNEL_EC", password="energy",
                        dsn=os.environ.get("EC_DB_DSN", "localhost:1521/ORCL"))
cur = conn.cursor()
cur.execute("""SELECT interface_code, file_name, file_no, file_source, uploaded_into_ec_ind, created_date
               FROM imp_source_interface_file ORDER BY created_date DESC FETCH FIRST 5 ROWS ONLY""")
rows = cur.fetchall()
print("\nIMP_SOURCE_INTERFACE_FILE:", rows if rows else "EMPTY")
conn.close()
