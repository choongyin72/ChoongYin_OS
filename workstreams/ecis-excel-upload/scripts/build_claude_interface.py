"""Build step 1: insert the CLAUDE_WELL_TEST interface row via Mapping Configuration
(TV insert pattern: Insert > Source Interface -> fill blank row -> Save). DB-verify."""
import os
import time
from pathlib import Path

import oracledb
from playwright.sync_api import sync_playwright

URL = os.environ.get("EC_URL", "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/")
OUT = Path(r"c:/Projects/ChoongYin_OS/tmp/ecis_recon")
GRID = "imp_interface_table:form"

CELLS = {  # col -> (value, kind)
    0: ("CLAUDE_WELL_TEST", "text"),
    1: ("Claude Well Test", "text"),
    2: ("ECIS Interface Area", "dd"),
    3: ("First Insert then Update", "dd"),
    4: ("Row based transactions", "dd"),
    5: ("Excel", "dd"),
    7: ("Provisional", "dd"),
    8: ("Provisional", "dd"),
    9: ("Full", "dd"),
}

def type_cell(page, cell_id, value):
    page.click(f'[id="{cell_id}"]')
    page.fill(f'[id="{cell_id}"]', "")
    page.type(f'[id="{cell_id}"]', value, delay=30)
    page.keyboard.press("Tab")
    page.wait_for_load_state("networkidle", timeout=12000)
    time.sleep(0.6)

def pick_cell_dd(page, dd_prefix, value):
    """Grid dd cell: open panel via _button, click the item by label (proven gesture)."""
    page.click(f'[id="{dd_prefix}_button"]')
    page.wait_for_selector(f'[id="{dd_prefix}_panel"] tr[data-item-label]', timeout=8000)
    item = page.locator(f'[id="{dd_prefix}_panel"] tr[data-item-label="{value}"]')
    if item.count() == 0:
        opts = page.evaluate(f"""() => [...document.querySelectorAll('[id="{dd_prefix}_panel"] tr[data-item-label]')]
            .map(tr => tr.getAttribute('data-item-label')).slice(0, 15)""")
        page.keyboard.press("Escape")
        raise RuntimeError(f"{dd_prefix}: '{value}' not in options {opts}")
    item.first.click()
    page.wait_for_load_state("networkidle", timeout=12000)
    time.sleep(0.6)

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

    page.locator('xpath=//li[contains(@class,"ui-menu-parent")][.//span[contains(@class,"ui-icon-insert")]]').hover()
    item = page.locator('xpath=//ul[contains(@class,"ui-menu-child")]//li//a[normalize-space(.)="Source Interface" and contains(@onclick,"insert")]')
    item.wait_for(state="visible", timeout=10000)
    item.click()
    page.wait_for_load_state("networkidle", timeout=15000)
    time.sleep(1.5)

    blank = page.evaluate(f"""() => {{
        const ins = [...document.querySelectorAll('[id^="{GRID}:T:"][id$=":C0_in"], [id^="{GRID}:T:"][id$="C0_in"]')];
        for (const e of ins) {{ if (!e.value) {{ const m = e.id.match(/T:(\\d+):/); if (m) return +m[1]; }} }}
        return -1; }}""")
    print("blank row index:", blank)
    if blank < 0:
        raise SystemExit("no blank row appeared after insert")

    for col, (val, kind) in CELLS.items():
        if kind == "dd":
            pick_cell_dd(page, f"{GRID}:T:{blank}:C{col}_dd", val)
        else:
            type_cell(page, f"{GRID}:T:{blank}:C{col}_in", val)
        print(f"  filled C{col} = {val}")

    page.locator('xpath=//li[.//span[contains(@class,"ui-icon-save")]][1]').first.click()
    page.wait_for_load_state("networkidle", timeout=20000)
    time.sleep(3)
    page.screenshot(path=str(OUT / "claude_iface_saved.png"), full_page=True)
    banner = page.evaluate("""() => { const t = [...document.querySelectorAll('div,span')]
        .map(e => (e.textContent||'').trim())
        .filter(t => t.includes('Required fields') || /could not|failed|error/i.test(t) && t.length < 250);
        return t.sort((a,b)=>a.length-b.length)[0] || null; }""")
    print("banner:", banner)
    browser.close()

conn = oracledb.connect(user="ECKERNEL_EC", password="energy",
                        dsn=os.environ.get("EC_DB_DSN", "localhost:1521/ORCL"))
cur = conn.cursor()
cur.execute("""SELECT object_code, name, type, transaction_type, source_type, ec_valid_level,
               ec_data_level, overwrite, functional_area_id FROM imp_source_interface
               WHERE object_code = 'CLAUDE_WELL_TEST'""")
print("DB row:", cur.fetchall())
conn.close()
