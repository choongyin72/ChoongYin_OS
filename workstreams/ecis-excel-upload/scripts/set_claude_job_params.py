"""Set CLAUDE_JOB action-10 params: INTERFACE_CODE=CLAUDE_WELL_TEST, FILE_DROP_SERVICE=DB,
FILE_FILTER=*, CONFIG_VALIDATION=Y (via the ecis_params grid). DB-verified."""
import os
import time
from pathlib import Path

import oracledb
from playwright.sync_api import sync_playwright

URL = os.environ.get("EC_URL", "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/")
OUT = Path(r"c:/Projects/ChoongYin_OS/tmp/ecis_recon")
NAME = "CLAUDE_EXCEL_IMPORT"
WANT = {"INTERFACE_CODE": "CLAUDE_WELL_TEST", "FILE_DROP_SERVICE": "DB",
        "FILE_FILTER": "*", "CONFIG_VALIDATION": "Y"}
EP = "tab:tabPanel:ecis_params:form"

conn = oracledb.connect(user="ECKERNEL_EC", password="energy",
                        dsn=os.environ.get("EC_DB_DSN", "localhost:1521/ORCL"))
cur = conn.cursor()

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
    time.sleep(1.5)
    page.click('[id="button:form:B"]')
    page.wait_for_load_state("networkidle", timeout=20000)
    time.sleep(2.5)
    page.fill('[id="schedule:form:T:sfilter0_ft_filter"]', NAME)
    page.keyboard.press("Enter")
    page.wait_for_load_state("networkidle", timeout=15000)
    time.sleep(2.5)
    page.locator(f'xpath=//tbody[@id="schedule:form:T_data"]//input[@value="{NAME}"]').first.click()
    page.wait_for_load_state("networkidle", timeout=15000)
    time.sleep(1.5)
    page.locator('xpath=//*[self::a or self::span][normalize-space(text())="Business Action"]').locator("visible=true").first.click()
    page.wait_for_load_state("networkidle", timeout=15000)
    time.sleep(2)
    page.locator('xpath=//tbody[@id="tab:tabPanel:busAction:form:T_data"]//input').first.click()
    page.wait_for_load_state("networkidle", timeout=15000)
    time.sleep(1.5)
    # select job action row whose C0 value is 10
    page.locator('xpath=//tbody[@id="tab:tabPanel:ecis_conf_action:form:T_data"]//input[@value="10"]').first.click()
    page.wait_for_load_state("networkidle", timeout=15000)
    time.sleep(2)

    rows = page.evaluate(f"""() => {{
        const out = {{}};
        document.querySelectorAll('[id^="{EP}:T:"][id$=":C1_in"]').forEach(inp => {{
            const r = inp.id.split(':T:')[1].split(':')[0];
            const tr = inp.closest('tr');
            const name = tr ? (tr.querySelector('td') ? tr.querySelector('td').textContent.trim() : '') : '';
            out[r] = {{name, value_id: inp.id, v: inp.value}};
        }});
        return out; }}""")
    print("param rows:", {r: (d["name"], d["v"]) for r, d in sorted(rows.items(), key=lambda x: int(x[0]))})

    for row, d in rows.items():
        if d["name"] not in WANT:
            continue
        val = WANT[d["name"]]
        cell_id = d["value_id"]
        if cell_id.endswith("_dd_input"):
            ddp = cell_id[:-len("_input")]
            page.click(f'[id="{ddp}_button"]')
            page.wait_for_selector(f'[id="{ddp}_panel"] tr[data-item-label]', timeout=8000)
            page.locator(f'[id="{ddp}_panel"] tr[data-item-label="{val}"]').first.click()
        else:
            page.click(f'[id="{cell_id}"]')
            page.fill(f'[id="{cell_id}"]', "")
            page.type(f'[id="{cell_id}"]', val, delay=25)
            page.keyboard.press("Tab")
        page.wait_for_load_state("networkidle", timeout=12000)
        time.sleep(0.6)
        print(f"set {d['name']} = {val}")

    page.locator('xpath=//li[.//span[contains(@class,"ui-icon-save")]][1]').first.click()
    for _ in range(15):
        time.sleep(2)
        cur.execute("""SELECT COUNT(*) FROM action_job_config WHERE job_id='CLAUDE_JOB'
                       AND param_name='INTERFACE_CODE' AND param_value='CLAUDE_WELL_TEST'""")
        if cur.fetchone()[0]:
            print("SAVED + DB-verified")
            break
    page.screenshot(path=str(OUT / "claude_job_params.png"), full_page=True)
    browser.close()

cur.execute("""SELECT param_name, param_value FROM action_job_config
               WHERE job_id='CLAUDE_JOB' AND job_action_no=10 AND param_value IS NOT NULL""")
print("final params:", cur.fetchall())
conn.close()
