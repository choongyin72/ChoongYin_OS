"""Schedules screen: set Active Status=All + GO, select AudreyExcelImport, open the
BUSINESS ACTION tab (and SCHEDULE tab) — screenshot + dump so I can replicate the setup."""
import os
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

URL = os.environ.get("EC_URL", "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/")
OUT = Path(r"c:/Projects/ChoongYin_OS/tmp/ecis_recon")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_context(ignore_https_errors=True, viewport={"width": 1920, "height": 1080}).new_page()
    page.goto(URL, wait_until="domcontentloaded", timeout=60000)
    page.fill('[id="username"]', "sysadmin")
    page.fill('[id="password"]', "sysadmin")
    page.click('[id="kc-login"]')
    page.wait_for_selector('[id="menu:searchForm:searchTxt"]', timeout=60000)
    box = page.locator('[id="menu:searchForm:searchTxt"]')
    box.type("Schedules", delay=50)
    time.sleep(1.2)
    page.locator('xpath=//*[contains(@class,"tv-link") and normalize-space(text())="Schedules"]').first.click()
    page.wait_for_load_state("networkidle", timeout=20000)
    time.sleep(2)
    # Active Status -> All: type into the autocomplete input, then click the panel item
    dd = "nav:form:G:0:R:0:C:1:dd"
    inp = page.locator(f'[id="{dd}_input"]')
    inp.click()
    inp.fill("")
    inp.type("All", delay=80)
    time.sleep(1.2)
    item = page.locator(f'xpath=//*[@id="{dd}_panel"]//*[self::tr or self::li][normalize-space(@data-item-label)="All" or normalize-space(.)="All"]')
    if item.count():
        item.first.click()
    else:
        page.keyboard.press("Enter")
    page.wait_for_load_state("networkidle", timeout=15000)
    time.sleep(1)
    val = page.evaluate(f"""() => {{ const e = document.querySelector('[id="{dd}_input"]');
        return e ? (e.value || '').trim() : null; }}""")
    print("Active Status now shows:", val)
    page.screenshot(path=str(OUT / "sched_after_all_pick.png"), full_page=True)
    # click the VISIBLE GO (hidden default-submit trap — find visible candidates first)
    go_ids = page.evaluate("""() => [...document.querySelectorAll('button, a')]
        .filter(e => e.offsetParent && /form:B/.test(e.id)).map(e => e.id)""")
    print("visible GO candidates:", go_ids)
    page.click(f'[id="{go_ids[0]}"]')
    page.wait_for_load_state("networkidle", timeout=20000)
    time.sleep(2)
    # filter the grid by Name to find Audrey regardless of pagination
    filt = page.evaluate("""() => [...document.querySelectorAll('input[id*="filter"]')]
        .filter(e => e.offsetParent && e.id.startsWith('schedule')).map(e => e.id).slice(0, 5)""")
    print("grid filter inputs:", filt)
    if filt:
        page.fill(f'[id="{filt[0]}"]', "Audrey")
        page.keyboard.press("Enter")
        page.wait_for_load_state("networkidle", timeout=15000)
        time.sleep(2)
    row = page.locator('xpath=//tbody[@id="schedule:form:T_data"]//*[normalize-space(text())="AudreyExcelImport"]')
    print("Audrey rows found:", row.count())
    if row.count() == 0:
        names = page.evaluate("""() => [...document.querySelectorAll('[id="schedule:form:T_data"] tr')]
            .map(tr => (tr.textContent||'').trim().slice(0, 40)).slice(0, 15)""")
        print("grid now shows:", names)
    if row.count():
        row.first.click()
        page.wait_for_load_state("networkidle", timeout=15000)
        time.sleep(1.5)
        page.screenshot(path=str(OUT / "audrey_sched_details.png"), full_page=True)
        for tab in ["BUSINESS ACTION", "SCHEDULE"]:
            t = page.locator(f'xpath=//*[self::a or self::span][normalize-space(text())="{tab}"]')
            if t.count():
                t.first.click()
                page.wait_for_load_state("networkidle", timeout=15000)
                time.sleep(2)
                tag = tab.lower().replace(" ", "_")
                page.screenshot(path=str(OUT / f"audrey_sched_{tag}.png"), full_page=True)
                print(f"captured {tab}")
    browser.close()
