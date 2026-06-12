"""Build CLAUDE_EXCEL_IMPORT schedule via Schedules screen, stage by stage (idempotent):
1 schedule row -> 2 ECISAction BA (seq 10) -> 3 jobid param=CLAUDE_JOB ->
4 ECIS job actions (Advanced/StagingTarget/TargetMapping) -> 5 action params.
Each stage saves + DB-verifies before moving on."""
import os
import time
from pathlib import Path

import oracledb
from playwright.sync_api import sync_playwright

URL = os.environ.get("EC_URL", "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/")
OUT = Path(r"c:/Projects/ChoongYin_OS/tmp/ecis_recon")
NAME = "CLAUDE_EXCEL_IMPORT"
JOB = "CLAUDE_JOB"
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
            .map(tr => tr.getAttribute('data-item-label')).slice(0, 25)""")
        page.keyboard.press("Escape")
        raise RuntimeError(f"{dd_prefix}: '{value}' not in {opts}")
    item.first.click()
    page.wait_for_load_state("networkidle", timeout=12000)
    time.sleep(0.5)

def insert_row(page, menu_label, grid_form, blank_suffix):
    page.locator('xpath=//li[contains(@class,"ui-menu-parent")][.//span[contains(@class,"ui-icon-insert")]]').hover()
    item = page.locator(f'xpath=//ul[contains(@class,"ui-menu-child")]//li//a[normalize-space(.)="{menu_label}" and contains(@onclick,"insert")]')
    item.wait_for(state="visible", timeout=10000)
    item.click()
    page.wait_for_load_state("networkidle", timeout=15000)
    time.sleep(1.5)
    blank = page.evaluate(f"""() => {{
        const ins = [...document.querySelectorAll('[id^="{grid_form}:T:"][id$="{blank_suffix}"]')];
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
    raise RuntimeError(f"save not verified: {label}")

def dump_grid(page, form):
    return page.evaluate(f"""() => {{
      const ths = [...document.querySelectorAll('[id="{form}:T_head"] th')]
        .map(th => (th.textContent||'').trim()).filter(t => t);
      const cells = [...document.querySelectorAll('[id^="{form}:T:"]')]
        .map(e => ({{id: e.id, v: e.value}})).filter(c => /(_in|_dd_input|_cb|_da_input)$/.test(c.id)).slice(0, 30);
      return {{headers: ths, cells}}; }}""")

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

    # ---- stage 1: schedule row
    if db_count("SELECT COUNT(*) FROM tv_schedule_list WHERE name=:n", n=NAME) == 0:
        r = insert_row(page, "Schedule", "schedule:form", "C0_in")
        type_cell(page, f"schedule:form:T:{r}:C0_in", NAME)
        type_cell(page, f"schedule:form:T:{r}:C1_in", "Claude learning - Excel import")
        # FA cell: try dd, else text
        fa_dd = page.evaluate(f"""() => !!document.querySelector('[id="schedule:form:T:{r}:C2_dd_button"]')""")
        if fa_dd:
            pick_cell_dd(page, f"schedule:form:T:{r}:C2_dd", "ECIS Interface Area")
        else:
            type_cell(page, f"schedule:form:T:{r}:C2_in", "ECIS Interface Area")
        save(page, "SELECT COUNT(*) FROM tv_schedule_list WHERE name=:n", 1, "schedule row", n=NAME)
    else:
        print("schedule row exists - skip")
        # navigate to it: All + GO + paginate
        dd = "nav:form:G:0:R:0:C:1:dd"
        page.click(f'[id="{dd}_button"]')
        page.wait_for_selector(f'[id="{dd}_panel"] tr[data-item-label]', timeout=8000)
        page.locator(f'[id="{dd}_panel"] tr[data-item-label="All"]').click()
        time.sleep(1.5)
        page.click('[id="button:form:B"]')
        page.wait_for_load_state("networkidle", timeout=20000)
        time.sleep(2.5)

    # select the schedule row via the Name column filter (default listing hides it)
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

    # ---- stage 2: business action ECISAction seq 10
    if db_count("SELECT COUNT(*) FROM tv_action_instance WHERE schedule_name=:n", n=NAME) == 0:
        r = insert_row(page, "Business Action", "tab:tabPanel:busAction:form", "C0_dd_input")
        pick_cell_dd(page, f"tab:tabPanel:busAction:form:T:{r}:C0_dd", "ECISAction")
        type_cell(page, f"tab:tabPanel:busAction:form:T:{r}:C2_in", "10")
        save(page, "SELECT COUNT(*) FROM tv_action_instance WHERE schedule_name=:n", 1, "business action", n=NAME)
    else:
        print("business action exists - skip")

    # ---- stage 3: jobid param (params grid row should exist after BA; fill value)
    if db_count("SELECT COUNT(*) FROM tv_action_instance_param WHERE schedule_name=:n AND parameter_value=:v", n=NAME, v=JOB) == 0:
        pr = dump_grid(page, "tab:tabPanel:params:form")
        print("params grid:", pr)
        # find the row whose name cell shows 'jobid' (C0), fill C1 with JOB
        target = None
        for c in pr["cells"]:
            if c["id"].endswith("C0_in") and (c["v"] or "").lower() == "jobid":
                target = c["id"].replace("C0_in", "C1_in")
        if target is None:
            # maybe the param row needs insert? try filling first row C1 anyway after printing
            raise RuntimeError(f"jobid param row not found; grid={pr}")
        type_cell(page, target, JOB)
        save(page, "SELECT COUNT(*) FROM tv_action_instance_param WHERE schedule_name=:n AND parameter_value=:v",
             1, "jobid param", n=NAME, v=JOB)
    else:
        print("jobid param exists - skip")

    # ---- stage 4: ECIS job actions (need busAction row selected)
    page.locator('xpath=//tbody[@id="tab:tabPanel:busAction:form:T_data"]//input').first.click()
    page.wait_for_load_state("networkidle", timeout=15000)
    time.sleep(1.5)
    ECA = "tab:tabPanel:ecis_conf_action:form"
    print("ecis_conf_action structure:", dump_grid(page, ECA))
    CLASSES = [
        ("10", "com.ec.ecdm.is.advancedexcel.sourcemapping.jobaction.AdvancedExcelJobAction"),
        ("20", "com.ec.ecdm.is.advancedexcel.staging.jobaction.StagingJobActionTarget"),
        ("30", "com.ec.ecdm.is.advancedexcel.targetmapping.jobaction.TargetMappingJobAction"),
    ]
    for no, cls in CLASSES:
        if db_count("SELECT COUNT(*) FROM action_job_config WHERE job_id=:j AND job_action_class=:c", j=JOB, c=cls):
            print(f"job action {no} exists - skip")
            continue
        r = insert_row(page, "ECIS Job Actions", ECA, "C0_in")
        struct = dump_grid(page, ECA)
        print(f"after insert row {r}:", [c for c in struct["cells"] if f":T:{r}:" in c["id"]])
        type_cell(page, f"{ECA}:T:{r}:C0_in", no)
        # class cell: dd or text? try dd then text
        has_dd = page.evaluate(f"""() => !!document.querySelector('[id="{ECA}:T:{r}:C1_dd_button"]')""")
        if has_dd:
            pick_cell_dd(page, f"{ECA}:T:{r}:C1_dd", cls)
        else:
            type_cell(page, f"{ECA}:T:{r}:C1_in", cls)
        save(page, "SELECT COUNT(*) FROM action_job_config WHERE job_id=:j AND job_action_class=:c",
             1, f"job action {no}", j=JOB, c=cls)

    page.screenshot(path=str(OUT / "claude_sched_built.png"), full_page=True)
    browser.close()

print("\n=== DB STATE ===")
cur.execute("SELECT name, enabled, status FROM tv_schedule_list WHERE name=:n", n=NAME)
print("schedule:", cur.fetchall())
cur.execute("SELECT business_action_name, exec_order FROM tv_action_instance WHERE schedule_name=:n", n=NAME)
print("BA:", cur.fetchall())
cur.execute("SELECT name, parameter_value FROM tv_action_instance_param WHERE schedule_name=:n", n=NAME)
print("params:", cur.fetchall())
cur.execute("SELECT job_action_no, job_action_class, param_name, param_value FROM action_job_config WHERE job_id=:j ORDER BY job_action_no, param_name", j=JOB)
for r in cur.fetchall():
    print("jobcfg:", r)
conn.close()
