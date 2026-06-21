"""Build step 2: CLAUDE_WELL_TEST source mappings (WELL/DATE/PRESSURE) + commands +
target mapping (claudePress -> PWEL_DAY_STATUS.AVG_BH_PRESS), all via the screen.
Saves stage-by-stage, polls the DB after each save (the spinner lesson)."""
import os
import time
from pathlib import Path

import oracledb
from playwright.sync_api import sync_playwright

URL = os.environ.get("EC_URL", "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/")
OUT = Path(r"c:/Projects/ChoongYin_OS/tmp/ecis_recon")
conn = oracledb.connect(user="ECKERNEL_EC", password="energy",
                        dsn=os.environ.get("EC_DB_DSN", "localhost:1521/ORCL"))
cur = conn.cursor()

def db_count(sql, **kw):
    cur.execute(sql, **kw)
    return cur.fetchone()[0]

def type_cell(page, cell_id, value):
    page.click(f'[id="{cell_id}"]')
    page.fill(f'[id="{cell_id}"]', "")
    page.type(f'[id="{cell_id}"]', str(value), delay=25)
    page.keyboard.press("Tab")
    page.wait_for_load_state("networkidle", timeout=12000)
    time.sleep(0.5)

def pick_cell_dd(page, dd_prefix, value):
    page.click(f'[id="{dd_prefix}_button"]')
    page.wait_for_selector(f'[id="{dd_prefix}_panel"] tr[data-item-label]', timeout=8000)
    item = page.locator(f'[id="{dd_prefix}_panel"] tr[data-item-label="{value}"]')
    if item.count() == 0:
        opts = page.evaluate(f"""() => [...document.querySelectorAll('[id="{dd_prefix}_panel"] tr[data-item-label]')]
            .map(tr => tr.getAttribute('data-item-label')).slice(0, 20)""")
        page.keyboard.press("Escape")
        raise RuntimeError(f"{dd_prefix}: '{value}' not in {opts}")
    item.first.click()
    page.wait_for_load_state("networkidle", timeout=12000)
    time.sleep(0.5)

def insert_row(page, menu_label, grid_form, blank_col_suffix):
    page.locator('xpath=//li[contains(@class,"ui-menu-parent")][.//span[contains(@class,"ui-icon-insert")]]').hover()
    item = page.locator(f'xpath=//ul[contains(@class,"ui-menu-child")]//li//a[normalize-space(.)="{menu_label}" and contains(@onclick,"insert")]')
    item.wait_for(state="visible", timeout=10000)
    item.click()
    page.wait_for_load_state("networkidle", timeout=15000)
    time.sleep(1.5)
    blank = page.evaluate(f"""() => {{
        const ins = [...document.querySelectorAll('[id^="{grid_form}:T:"][id$="{blank_col_suffix}"]')];
        for (const e of ins) {{ if (!e.value) {{ const m = e.id.match(/T:(\\d+):/); if (m) return +m[1]; }} }}
        return -1; }}""")
    if blank < 0:
        raise RuntimeError(f"no blank row in {grid_form}")
    return blank

def save(page, verify_sql, expect, label, **kw):
    page.locator('xpath=//li[.//span[contains(@class,"ui-icon-save")]][1]').first.click()
    for _ in range(15):
        time.sleep(2)
        if db_count(verify_sql, **kw) >= expect:
            print(f"SAVED + DB-verified: {label}")
            return
    raise RuntimeError(f"save not verified in DB: {label}")

MAPPINGS = [
    # code, sort, type, valuetype, eckey, key1, key2, move_x
    ("WELL", "10", "KEY_LIST", "STRING", None, None, None, 0),
    ("DATE", "20", "KEY_LIST", "DATE", None, None, None, 1),
    ("PRESSURE", "30", "DATA", "NUMBER", "claudePress", "ROWS:WELL", "ROWS:DATE", 2),
]
SM = "imp_source_mapping_table:form"
CMD = "tab:tabPanel:imp_source_path_table:form"
TGT = "imp_target_mapping_table:form"

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

    # --- source mappings (idempotent: skip those already in DB)
    for code, sort, typ, vtype, eckey, k1, k2, _ in MAPPINGS:
        if db_count("""SELECT COUNT(*) FROM imp_source_mapping m JOIN imp_source_interface i
                       ON i.object_id = m.imp_source_interface_id
                       WHERE i.object_code='CLAUDE_WELL_TEST' AND m.code=:c""", c=code):
            print(f"mapping {code} already exists - skip")
            continue
        r = insert_row(page, "Source Mapping", SM, "C1_in")
        type_cell(page, f"{SM}:T:{r}:C0_in", sort)
        type_cell(page, f"{SM}:T:{r}:C1_in", code)
        type_cell(page, f"{SM}:T:{r}:C2_in", code.title())
        type_cell(page, f"{SM}:T:{r}:C3_in", "Data.A1")
        pick_cell_dd(page, f"{SM}:T:{r}:C4_dd", typ)
        pick_cell_dd(page, f"{SM}:T:{r}:C5_dd", vtype)
        if eckey:
            type_cell(page, f"{SM}:T:{r}:C7_in", eckey)
            type_cell(page, f"{SM}:T:{r}:C8_in", k1)
            type_cell(page, f"{SM}:T:{r}:C9_in", k2)
        save(page, """SELECT COUNT(*) FROM imp_source_mapping m JOIN imp_source_interface i
                      ON i.object_id = m.imp_source_interface_id
                      WHERE i.object_code='CLAUDE_WELL_TEST' AND m.code=:c""",
             1, f"mapping {code}", c=code)

    # --- commands per mapping (select mapping row, activate the Commands tab)
    for code, _s, _t, _v, _e, _k1, _k2, mx in MAPPINGS:
        if db_count("""SELECT COUNT(*) FROM imp_source_path p JOIN imp_source_mapping m
                       ON m.object_id = p.imp_source_mapping_id
                       JOIN imp_source_interface i ON i.object_id = m.imp_source_interface_id
                       WHERE i.object_code='CLAUDE_WELL_TEST' AND m.code=:c""", c=code) >= 2:
            print(f"commands {code} already exist - skip")
            continue
        page.locator(f'xpath=//tbody[@id="{SM}:T_data"]//input[@value="{code}"]').first.click()
        page.wait_for_load_state("networkidle", timeout=15000)
        time.sleep(1.5)
        tab = page.locator('xpath=//*[self::a or self::span][normalize-space(text())="Source Mapping Commands"]').locator("visible=true")
        if tab.count():
            tab.first.click()
            page.wait_for_load_state("networkidle", timeout=15000)
            time.sleep(1.5)
        # NEW command rows render Type/Path as dd cells (saved rows show as text)
        r = insert_row(page, "Source Mapping Commands", CMD, "C0_in")
        type_cell(page, f"{CMD}:T:{r}:C0_in", "10")
        pick_cell_dd(page, f"{CMD}:T:{r}:C1_dd", "UPPER_LEFT")
        pick_cell_dd(page, f"{CMD}:T:{r}:C2_dd", "Move(col, row)")
        type_cell(page, f"{CMD}:T:{r}:C3_in", str(mx))
        type_cell(page, f"{CMD}:T:{r}:C4_in", "1")
        r = insert_row(page, "Source Mapping Commands", CMD, "C0_in")
        type_cell(page, f"{CMD}:T:{r}:C0_in", "20")
        pick_cell_dd(page, f"{CMD}:T:{r}:C1_dd", "LOWER_RIGHT")
        pick_cell_dd(page, f"{CMD}:T:{r}:C2_dd", "FindVertical(text)")
        type_cell(page, f"{CMD}:T:{r}:C3_in", '""')
        save(page, """SELECT COUNT(*) FROM imp_source_path p JOIN imp_source_mapping m
                      ON m.object_id = p.imp_source_mapping_id
                      JOIN imp_source_interface i ON i.object_id = m.imp_source_interface_id
                      WHERE i.object_code='CLAUDE_WELL_TEST' AND m.code=:c""",
             2, f"commands {code}", c=code)

    # --- target mapping
    r = insert_row(page, "Target Mapping", TGT, "C2_dd_input")
    pick_cell_dd(page, f"{TGT}:T:{r}:C0_dd", "PWEL_DAY_STATUS")
    pick_cell_dd(page, f"{TGT}:T:{r}:C1_dd", "AVG_BH_PRESS")
    pick_cell_dd(page, f"{TGT}:T:{r}:C2_dd", "claudePress")
    pick_cell_dd(page, f"{TGT}:T:{r}:C3_dd", "Key 1")
    pick_cell_dd(page, f"{TGT}:T:{r}:C4_dd", "Key 2")
    save(page, "SELECT COUNT(*) FROM imp_target_mapping WHERE ec_key='claudePress'",
         1, "target mapping claudePress")

    page.screenshot(path=str(OUT / "claude_children_done.png"), full_page=True)
    browser.close()

print("\n=== FINAL DB STATE ===")
cur.execute("""SELECT m.code, m.sort_order, m.path_origin, m.type, m.value_type, m.ec_key, m.key_1, m.key_2
  FROM imp_source_mapping m JOIN imp_source_interface i ON i.object_id = m.imp_source_interface_id
  WHERE i.object_code='CLAUDE_WELL_TEST' ORDER BY m.sort_order""")
for r in cur.fetchall():
    print("mapping:", r)
cur.execute("""SELECT m.code, p.sort_order, p.type, p.path, p.path_param_1, p.path_param_2
  FROM imp_source_path p JOIN imp_source_mapping m ON m.object_id = p.imp_source_mapping_id
  JOIN imp_source_interface i ON i.object_id = m.imp_source_interface_id
  WHERE i.object_code='CLAUDE_WELL_TEST' ORDER BY m.sort_order, p.sort_order""")
for r in cur.fetchall():
    print("command:", r)
cur.execute("SELECT ec_key, class, attribute, class_key_1, class_key_2 FROM imp_target_mapping WHERE ec_key='claudePress'")
for r in cur.fetchall():
    print("target:", r)
conn.close()
