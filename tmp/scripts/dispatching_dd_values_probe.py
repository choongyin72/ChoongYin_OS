"""1) Clean up the orphan Delivery Stream probe row (End Date = Start Date true delete).
2) For each Dispatching screen's MANDATORY dropdown(s): open New Object, set Start Date
   2003-01-01 first (version filter), open the dd panel, dump its option labels.
No saves besides the cleanup delete."""
import json
import os
import time
from pathlib import Path

import oracledb
from playwright.sync_api import sync_playwright

URL = os.environ.get("EC_URL", "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/")
USER = os.environ.get("EC_USER", "sysadmin")
PASS = os.environ.get("EC_PASS", "sysadmin")
OUT = Path(r"c:/Projects/ChoongYin_OS/tmp/dispatching_recon")
ORPHAN = "AUTOTEST_PRB_184844"

# screen -> (date_row, [(label, dd_row)])
PROBES = {
    "Delivery Point":   (3, [("Business Unit Name", 11)]),
    "Meter":            (2, [("Meter Type", 4), ("Delivery Point Name", 5)]),
    "Nomination Point": (3, [("Contract Name", 5)]),
    "Pipeline Segment": (2, [("Pipeline Name", 6)]),
    "Transport System": (2, [("Business Unit Name", 6)]),
    "Transport Zone":   (3, [("Transport System Name", 5)]),
}

def goto_screen(page, name):
    page.goto(URL, wait_until="domcontentloaded", timeout=60000)
    page.wait_for_selector('[id="menu:searchForm:searchTxt"]', timeout=30000)
    time.sleep(0.8)
    box = page.locator('[id="menu:searchForm:searchTxt"]')
    box.fill("")
    box.type(name, delay=50)
    time.sleep(1)
    page.locator(f'xpath=//*[contains(@class,"tv-link") and normalize-space(text())="{name}"]').first.click()
    page.wait_for_load_state("networkidle", timeout=20000)
    time.sleep(2)

results = {}
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_context(ignore_https_errors=True, viewport={"width": 1920, "height": 1080}).new_page()
    page.goto(URL, wait_until="domcontentloaded", timeout=60000)
    page.fill('[id="username"]', USER)
    page.fill('[id="password"]', PASS)
    page.click('[id="kc-login"]')
    page.wait_for_selector('[id="menu:searchForm:searchTxt"]', timeout=60000)

    # --- 1) cleanup orphan Delivery Stream row
    try:
        goto_screen(page, "Delivery Stream")
        page.locator(f'xpath=//tbody[@id="manage_object_nav_nav:form:T_data"]//span[normalize-space(text())="{ORPHAN}"]').click()
        page.wait_for_load_state("networkidle", timeout=15000)
        time.sleep(1.5)
        page.fill('[id="tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input"]', "2003-01-01")
        page.keyboard.press("Escape")
        time.sleep(0.5)
        page.locator('xpath=//li[.//span[contains(@class,"ui-icon-save")]][1]').first.click()
        page.wait_for_load_state("networkidle", timeout=20000)
        time.sleep(2.5)
        print("cleanup: delete gesture done")
    except Exception as e:
        print(f"cleanup FAILED: {str(e)[:160]}")

    # --- 2) dropdown option labels per mandatory dd
    for name, (drow, dds) in PROBES.items():
        try:
            goto_screen(page, name)
            page.locator('xpath=//li[contains(@class,"ui-menu-parent")][.//span[contains(@class,"ui-icon-insert")]]').hover()
            item = page.locator('xpath=//ul[contains(@class,"ui-menu-child")]//li//a[normalize-space(.)="New Object"]')
            item.wait_for(state="visible", timeout=10000)
            item.click()
            page.wait_for_load_state("networkidle", timeout=15000)
            time.sleep(1.5)
            page.fill(f'[id="tab:tabPanel:objectForm:form:G:0:R:{drow}:C:1:da_input"]', "2003-01-01")
            page.keyboard.press("Escape")
            time.sleep(1.0)
            scr = {}
            for label, row in dds:
                base = f"tab:tabPanel:objectForm:form:G:0:R:{row}:C:1"
                cells = page.evaluate(f"""() => [...document.querySelectorAll('[id^="{base}"]')]
                    .map(e => e.id).slice(0, 6)""")
                dd_id = f"{base}:dd"
                opts = []
                try:
                    page.click(f'[id="{dd_id}"]', timeout=5000)
                    page.wait_for_selector(f'[id="{dd_id}_panel"] tr[data-item-label]', timeout=8000)
                    opts = page.evaluate(f"""() => [...document.querySelectorAll('[id="{dd_id}_panel"] tr[data-item-label]')]
                        .map(tr => tr.getAttribute('data-item-label')).slice(0, 12)""")
                    page.keyboard.press("Escape")
                    time.sleep(0.5)
                except Exception as e:
                    opts = [f"DD-OPEN-FAILED: {str(e)[:80]}", f"cells={cells}"]
                scr[label] = opts
            results[name] = scr
            print(f"{name}: " + " | ".join(f"{k} -> {v[:4]}" for k, v in scr.items()))
        except Exception as e:
            results[name] = {"error": str(e)[:200]}
            print(f"!! {name}: {str(e)[:140]}")
    browser.close()

(OUT / "dd_values_probe.json").write_text(json.dumps(results, indent=1), encoding="utf-8")

conn = oracledb.connect(user="ECKERNEL_EC", password="energy",
                        dsn=os.environ.get("EC_DB_DSN", "localhost:1521/ORCL"))
cur = conn.cursor()
cur.execute("SELECT code FROM ov_delivery_stream WHERE code LIKE 'AUTOTEST%'")
print("\nAUTOTEST rows left in ov_delivery_stream after cleanup:", cur.fetchall())
conn.close()
