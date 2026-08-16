"""Mapping Configuration: dump toolbar Insert submenu items, interface grid headers,
and one existing row's cell ids (EXCEL_IMPORT) — the template for inserting my own."""
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
    box.type("Mapping Configuration", delay=50)
    time.sleep(1.2)
    page.locator('xpath=//*[contains(@class,"tv-link") and normalize-space(text())="Mapping Configuration"]').first.click()
    page.wait_for_load_state("networkidle", timeout=20000)
    time.sleep(2.5)

    # toolbar insert submenu
    page.locator('xpath=//li[contains(@class,"ui-menu-parent")][.//span[contains(@class,"ui-icon-insert")]]').hover()
    time.sleep(1.2)
    items = page.evaluate("""() => [...document.querySelectorAll('ul.ui-menu-child li a')]
        .filter(e => e.offsetParent).map(e => (e.textContent||'').trim()).filter(t => t)""")
    print("INSERT submenu:", items)
    page.keyboard.press("Escape")

    info = page.evaluate("""() => {
      const vis = e => e && e.offsetParent !== null;
      // headers of the interface grid
      const ths = [...document.querySelectorAll('[id="imp_interface_table:form:T_head"] th')]
        .map(th => (th.textContent||'').trim()).filter(t => t);
      // first row cell ids
      const row0 = [...document.querySelectorAll('[id^="imp_interface_table:form:T:0:"]')]
        .map(e => e.id).filter(id => /(_in|_dd_input|_cb|_da_input)$/.test(id));
      return {headers: ths, row0};
    }""")
    print("HEADERS:", info["headers"])
    print("ROW0 cells:", info["row0"])
    page.screenshot(path=str(OUT / "mapcfg_full.png"), full_page=True)
    browser.close()
