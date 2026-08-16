"""Select EXCEL_IMPORT interface -> dump SOURCE MAPPING grid headers/cells; select its
WELL mapping -> dump Source Mapping Commands grid; dump TARGET MAPPING grid. Read-only."""
import os
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

URL = os.environ.get("EC_URL", "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/")
OUT = Path(r"c:/Projects/ChoongYin_OS/tmp/ecis_recon")

def dump_grid(page, form):
    return page.evaluate(f"""() => {{
      const ths = [...document.querySelectorAll('[id="{form}:T_head"] th')]
        .map(th => (th.textContent||'').trim()).filter(t => t);
      const rows = [...document.querySelectorAll('[id^="{form}:T:"]')]
        .map(e => e.id).filter(id => /T:0:/.test(id) && /(_in|_dd_input|_cb|_da_input)$/.test(id));
      const n = document.querySelectorAll('[id="{form}:T_data"] tr').length;
      return {{headers: ths, row0: rows, nrows: n}}; }}""")

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

    # select the EXCEL_IMPORT interface row (click its Code cell input)
    page.locator('xpath=//tbody[@id="imp_interface_table:form:T_data"]//input[@value="EXCEL_IMPORT"]').first.click()
    page.wait_for_load_state("networkidle", timeout=15000)
    time.sleep(2)
    sm = dump_grid(page, "imp_source_mapping_table:form")
    print("SOURCE MAPPING headers:", sm["headers"])
    print("SOURCE MAPPING row0:", sm["row0"])
    print("rows:", sm["nrows"])

    # select first source mapping row -> commands grid in the tab
    first_in = page.locator('xpath=//tbody[@id="imp_source_mapping_table:form:T_data"]//input').first
    first_in.click()
    page.wait_for_load_state("networkidle", timeout=15000)
    time.sleep(2)
    cmd = dump_grid(page, "tab:tabPanel:imp_source_path_table:form")
    print("COMMANDS headers:", cmd["headers"])
    print("COMMANDS row0:", cmd["row0"])

    # target mapping grid (bottom)
    tgt_forms = page.evaluate("""() => [...document.querySelectorAll('tbody[id$=":T_data"]')]
        .map(e => e.id)""")
    print("all grids on screen:", tgt_forms)
    for f in tgt_forms:
        if "target" in f.lower():
            t = dump_grid(page, f.replace(":T_data", ""))
            print(f"TARGET grid {f}: headers={t['headers']}")
            print("  row0:", t["row0"])
    page.screenshot(path=str(OUT / "mapcfg_children.png"), full_page=True)
    browser.close()
