"""Diagnose the Source Mapping Commands insert: select WELL mapping (row click), activate
tab, attempt insert, dump banner + tab-panel inputs + screenshot."""
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
    page.locator('xpath=//tbody[@id="imp_interface_table:form:T_data"]//input[@value="CLAUDE_WELL_TEST"]').first.click()
    page.wait_for_load_state("networkidle", timeout=15000)
    time.sleep(2)
    # click the WELL row's TD (not the input) to be sure the row-select event fires
    page.locator('xpath=//tbody[@id="imp_source_mapping_table:form:T_data"]//input[@value="WELL"]/ancestor::td[1]').first.click()
    page.wait_for_load_state("networkidle", timeout=15000)
    time.sleep(2)
    page.screenshot(path=str(OUT / "diag_after_select.png"), full_page=True)

    page.locator('xpath=//li[contains(@class,"ui-menu-parent")][.//span[contains(@class,"ui-icon-insert")]]').hover()
    item = page.locator('xpath=//ul[contains(@class,"ui-menu-child")]//li//a[normalize-space(.)="Source Mapping Commands" and contains(@onclick,"insert")]')
    item.wait_for(state="visible", timeout=10000)
    item.click()
    page.wait_for_load_state("networkidle", timeout=15000)
    time.sleep(2.5)
    page.screenshot(path=str(OUT / "diag_after_insert.png"), full_page=True)
    info = page.evaluate("""() => {
      const vis = e => e && e.offsetParent !== null;
      const cells = [...document.querySelectorAll('[id*="imp_source_path_table"]')]
        .map(e => ({id: e.id, val: e.value, vis: vis(e)}))
        .filter(c => /(_in|_dd_input|_cb)$/.test(c.id));
      const banner = [...document.querySelectorAll('div,span')]
        .map(e => (e.textContent||'').trim())
        .filter(t => t && t.length < 250 && /select|required|missing|insert/i.test(t)).slice(0, 4);
      const tabs = [...document.querySelectorAll('[role="tab"], .ui-tabs-header')]
        .filter(vis).map(e => ({t: (e.textContent||'').trim(), active: e.className.includes('ui-state-active')}));
      return {cells: cells.slice(0, 14), banner, tabs};
    }""")
    print("cells:", info["cells"])
    print("banner:", info["banner"])
    print("tabs:", info["tabs"])
    browser.close()
