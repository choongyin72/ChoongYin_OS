"""Nomination Cycle (TV) recon: grid cell ids, headers, toolbar insert/delete labels.
Read-only. Mirrors the MIME/Language TV pattern recon."""
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
    box.type("Nomination Cycle", delay=50)
    time.sleep(1.2)
    page.locator('xpath=//*[contains(@class,"tv-link") and normalize-space(text())="Nomination Cycle"]').first.click()
    page.wait_for_load_state("networkidle", timeout=20000)
    time.sleep(2.5)

    info = page.evaluate("""() => {
      const vis = e => e && e.offsetParent !== null;
      const ths = [...document.querySelectorAll('[id="table:form:T_head"] th')]
        .map(th => (th.textContent||'').trim()).filter(t => t);
      const row0 = [...document.querySelectorAll('[id^="table:form:T:0:"]')]
        .map(e => ({id: e.id, v: e.value})).filter(c => /(_in|_dd_input|_cb|_da_input)$/.test(c.id));
      const rows = document.querySelectorAll('[id="table:form:T_data"] tr').length;
      return {headers: ths, row0, rows};
    }""")
    print("headers:", info["headers"])
    print("row0:", info["row0"])
    print("rows:", info["rows"])

    page.locator('xpath=//li[contains(@class,"ui-menu-parent")][.//span[contains(@class,"ui-icon-insert")]]').hover()
    time.sleep(1.2)
    items = page.evaluate("""() => [...document.querySelectorAll('ul.ui-menu-child li a')]
        .filter(e => e.offsetParent).map(e => (e.textContent||'').trim()).filter(t => t)""")
    print("INSERT submenu:", items)
    page.mouse.click(900, 500)
    page.screenshot(path=str(OUT / "nomcycle_grid.png"), full_page=True)
    browser.close()
