"""Delivery Stream: pick BU=ECP Norway + GO, dump grid rows + the 2nd cascading dd's
options; find why AUTOTEST_DS row (BU=ECP_NO in DB) is not listed."""
import os
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

URL = os.environ.get("EC_URL", "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/")
OUT = Path(r"c:/Projects/ChoongYin_OS/tmp/dispatching_recon")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_context(ignore_https_errors=True, viewport={"width": 1920, "height": 1080}).new_page()
    page.goto(URL, wait_until="domcontentloaded", timeout=60000)
    page.fill('[id="username"]', "sysadmin")
    page.fill('[id="password"]', "sysadmin")
    page.click('[id="kc-login"]')
    page.wait_for_selector('[id="menu:searchForm:searchTxt"]', timeout=60000)
    box = page.locator('[id="menu:searchForm:searchTxt"]')
    box.type("Delivery Stream", delay=50)
    time.sleep(1)
    page.locator('xpath=//*[contains(@class,"tv-link") and normalize-space(text())="Delivery Stream"]').first.click()
    page.wait_for_load_state("networkidle", timeout=20000)
    time.sleep(2)
    dd = "nav:form:G:0:R:1:C:1:dd"
    page.click(f'[id="{dd}_button"]')
    page.wait_for_selector(f'[id="{dd}_panel"] tr[data-item-label]', timeout=8000)
    page.locator(f'[id="{dd}_panel"] tr[data-item-label="ECP Norway"]').click()
    page.wait_for_load_state("networkidle", timeout=15000)
    time.sleep(1)
    # 2nd dd options after BU pick (cascading)
    dd2 = "nav:form:G:0:R:1:C:2:dd"
    opts2 = []
    try:
        page.click(f'[id="{dd2}_button"]', timeout=5000)
        page.wait_for_selector(f'[id="{dd2}_panel"] tr[data-item-label]', timeout=6000)
        opts2 = page.evaluate(f"""() => [...document.querySelectorAll('[id="{dd2}_panel"] tr[data-item-label]')]
            .map(tr => tr.getAttribute('data-item-label')).slice(0, 10)""")
        page.keyboard.press("Escape")
    except Exception as e:
        opts2 = [f"none/failed: {str(e)[:60]}"]
    print("2nd dd options after BU=ECP Norway:", opts2)
    page.click('[id="button:form:B"]')
    page.wait_for_load_state("networkidle", timeout=20000)
    time.sleep(2.5)
    rows = page.evaluate("""() => {
        const tb = document.querySelector('[id="manageObject:form:T_data"]');
        if (!tb) return 'NO TBODY';
        return [...tb.querySelectorAll('tr')].map(tr => (tr.textContent||'').trim().slice(0,60)); }""")
    print(f"grid rows under ECP Norway ({len(rows) if isinstance(rows,list) else rows}):")
    if isinstance(rows, list):
        for r in rows[:30]:
            print("  ", r)
    pag = page.evaluate("""() => { const p=document.querySelector('.ui-paginator-current');
        return p ? p.textContent.trim() : null; }""")
    print("paginator:", pag)
    page.screenshot(path=str(OUT / "delstrm_ecpno_grid.png"), full_page=True)
    browser.close()
