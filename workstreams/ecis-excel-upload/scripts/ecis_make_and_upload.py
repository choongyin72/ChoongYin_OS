"""1) Create the test Excel matching the EXCEL_IMPORT mapping (Sheet1: A=Well, B=Date,
C=Temperature, headers row 1, data rows 2-4). 2) Upload it via the Upload Files screen
(recon structure on the way). Read-only except the upload itself."""
import datetime
import os
import time
from pathlib import Path

from openpyxl import Workbook
from playwright.sync_api import sync_playwright

URL = os.environ.get("EC_URL", "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/")
OUT = Path(r"c:/Projects/ChoongYin_OS/tmp/ecis_recon")
XLSX = OUT / "claude_excel_import_test.xlsx"

wb = Workbook()
ws = wb.active
ws.title = "Sheet1"
ws.append(["Well", "Date", "Temperature"])
d = datetime.datetime(2003, 1, 5)
ws.append(["AS1_Well_001", d, 41.5])
ws.append(["AS1_Well_002", d, 42.7])
ws.append(["AS1_Well_003", d, 43.9])
wb.save(XLSX)
print(f"excel written: {XLSX}")

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
    # dump structure: dds, file inputs, buttons
    info = page.evaluate("""() => {
        const vis = e => e && e.offsetParent !== null;
        const txt = e => (e.textContent||'').trim();
        return {
          dds: [...document.querySelectorAll('[id$=":dd"], select')].filter(vis).map(e => e.id),
          files: [...document.querySelectorAll('input[type="file"]')].map(e => ({id: e.id, vis: vis(e)})),
          buttons: [...document.querySelectorAll('button, a.ui-button, span.ui-button')]
            .filter(vis).map(e => ({id: e.id, t: txt(e).slice(0,25)})).filter(b => b.t).slice(0, 12),
          labels: [...document.querySelectorAll('label, [id$="_la"]')].filter(vis).map(txt).filter(t => t).slice(0, 12)
        }; }""")
    print("UPLOAD FILES structure:", info)
    page.screenshot(path=str(OUT / "upload_files_screen.png"), full_page=True)

    # pick interface in the visible dd (expect FA + Interface dds)
    dds = [d for d in info["dds"] if d and d.endswith(":dd")]
    picked = False
    for dd in dds:
        try:
            page.click(f'[id="{dd}_button"]', timeout=4000)
            page.wait_for_selector(f'[id="{dd}_panel"] tr[data-item-label]', timeout=5000)
            opts = page.evaluate(f"""() => [...document.querySelectorAll('[id="{dd}_panel"] tr[data-item-label]')]
                .map(tr => tr.getAttribute('data-item-label')).slice(0, 30)""")
            print(f"dd {dd} options: {opts[:12]}")
            tgt = next((o for o in opts if o in ("EXCEL_IMPORT", "Excel Import")), None)
            if tgt:
                page.locator(f'[id="{dd}_panel"] tr[data-item-label="{tgt}"]').click()
                page.wait_for_load_state("networkidle", timeout=15000)
                time.sleep(1)
                picked = True
                print(f"picked {tgt} in {dd}")
            else:
                page.keyboard.press("Escape")
                time.sleep(0.4)
        except Exception as e:
            print(f"dd {dd}: {str(e)[:80]}")
    print("interface picked:", picked)

    fi = page.locator('input[type="file"]')
    if fi.count():
        fi.first.set_input_files(str(XLSX))
        time.sleep(2)
        page.screenshot(path=str(OUT / "upload_files_chosen.png"), full_page=True)
        upl = page.locator('xpath=//*[self::button or self::span or self::a][contains(translate(normalize-space(.),"upload","UPLOAD"),"UPLOAD")]').locator("visible=true")
        print("upload buttons:", upl.count())
        if upl.count():
            upl.first.click()
            page.wait_for_load_state("networkidle", timeout=30000)
            time.sleep(3)
        page.screenshot(path=str(OUT / "upload_files_after.png"), full_page=True)
        msgs = page.evaluate("""() => [...document.querySelectorAll('div,span')]
            .map(e => (e.textContent||'').trim())
            .filter(t => t && t.length < 200 && /upload|success|error|saved/i.test(t)).slice(0, 6)""")
        print("messages:", msgs)
    else:
        print("NO file input found")
    browser.close()
