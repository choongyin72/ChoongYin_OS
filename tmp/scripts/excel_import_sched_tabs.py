"""Clean retry: Schedules -> Active Status=All (button gesture + label verify) -> GO ->
scan grid rows (with pagination) for EXCEL_IMPORT_1 -> open BUSINESS ACTION + SCHEDULE tabs."""
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

    dd = "nav:form:G:0:R:0:C:1:dd"
    page.click(f'[id="{dd}_button"]')
    page.wait_for_selector(f'[id="{dd}_panel"] tr[data-item-label]', timeout=8000)
    page.locator(f'[id="{dd}_panel"] tr[data-item-label="All"]').click()
    page.wait_for_load_state("networkidle", timeout=15000)
    time.sleep(1.5)
    state = page.evaluate(f"""() => {{
        const inp = document.querySelector('[id="{dd}_input"]');
        const hin = document.querySelector('[id="{dd}_hinput"]');
        return {{input: inp ? inp.value : null, hidden: hin ? hin.value : null}}; }}""")
    print("dd state after All click:", state)
    page.click('[id="button:form:B"]')
    page.wait_for_load_state("networkidle", timeout=20000)
    time.sleep(2.5)

    found = False
    for pg in range(1, 6):
        names = page.evaluate("""() => [...document.querySelectorAll('[id="schedule:form:T_data"] tr')]
            .map(tr => {const inp = tr.querySelector('td input'); if (inp && inp.value) return inp.value.trim();
                        const td = tr.querySelector('td'); return td ? (td.textContent||'').trim() : '';})""")
        print(f"page {pg}: {len(names)} rows :: {names[:14]}")
        if "EXCEL_IMPORT_1" in names:
            found = True
            break
        nxt = page.locator('css=[id^="schedule"] .ui-paginator-next:not(.ui-state-disabled)')
        if nxt.count() == 0:
            break
        nxt.first.click()
        page.wait_for_load_state("networkidle", timeout=15000)
        time.sleep(1.5)

    print("Audrey found:", found)
    if found:
        page.locator('xpath=//tbody[@id="schedule:form:T_data"]//input[@value="EXCEL_IMPORT_1"]').first.click()
        page.wait_for_load_state("networkidle", timeout=15000)
        time.sleep(1.5)
        page.screenshot(path=str(OUT / "excel_import_sched_details.png"), full_page=True)
        for tab in ["Business Action", "Schedule"]:
            t = page.locator(f'xpath=//*[self::a or self::span][normalize-space(text())="{tab}"]').locator('visible=true')
            if t.count():
                t.first.click()
                page.wait_for_load_state("networkidle", timeout=15000)
                time.sleep(2)
                page.screenshot(path=str(OUT / f"excel_import_sched_{tab.lower().replace(' ', '_')}.png"), full_page=True)
                print("captured", tab)
    browser.close()
