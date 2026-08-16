"""Round 2: (a) DB row counts for the 7 OV views (pagination risk check),
(b) cleanup orphan Delivery Stream row — WITH the GO click this time,
(c) dropdown option labels via the proper _button gesture."""
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

conn = oracledb.connect(user="ECKERNEL_EC", password="energy",
                        dsn=os.environ.get("EC_DB_DSN", "localhost:1521/ORCL"))
cur = conn.cursor()
for v in ["ov_delivery_point", "ov_delivery_stream", "ov_meter", "ov_nomination_point",
          "ov_pipeline_segment", "ov_transport_system", "ov_transport_zone"]:
    cur.execute(f"SELECT COUNT(*) FROM {v}")
    print(f"{v}: {cur.fetchone()[0]} rows")

PROBES = {
    "Delivery Point":   (3, [("Business Unit Name", 11)]),
    "Meter":            (2, [("Meter Type", 4)]),
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

    # cleanup with GO first
    try:
        goto_screen(page, "Delivery Stream")
        page.click('[id="button:form:B"]')      # Apply Navigator (GO) -> grid loads
        page.wait_for_load_state("networkidle", timeout=20000)
        time.sleep(2)
        n = page.evaluate(f"""() => document.querySelectorAll('[id="manage_object_nav_nav:form:T_data"] tr').length""")
        print(f"\nDelivery Stream grid rows after GO: {n}")
        page.locator(f'xpath=//tbody[@id="manage_object_nav_nav:form:T_data"]//span[normalize-space(text())="{ORPHAN}"]').click(timeout=15000)
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
        print(f"cleanup FAILED: {str(e)[:200]}")
        page.screenshot(path=str(OUT / "cleanup_fail.png"), full_page=True)

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
                dd = f"tab:tabPanel:objectForm:form:G:0:R:{row}:C:1:dd"
                opts = []
                try:
                    page.click(f'[id="{dd}_button"]', timeout=5000)
                    page.wait_for_selector(f'[id="{dd}_panel"] tr[data-item-label]', timeout=8000)
                    opts = page.evaluate(f"""() => [...document.querySelectorAll('[id="{dd}_panel"] tr[data-item-label]')]
                        .map(tr => tr.getAttribute('data-item-label')).slice(0, 12)""")
                    page.keyboard.press("Escape")
                    time.sleep(0.5)
                except Exception as e:
                    opts = [f"FAILED: {str(e)[:80]}"]
                scr[label] = opts
            results[name] = scr
            print(f"{name}: " + " | ".join(f"{k} -> {v[:5]}" for k, v in scr.items()))
        except Exception as e:
            results[name] = {"error": str(e)[:200]}
            print(f"!! {name}: {str(e)[:140]}")
    browser.close()

(OUT / "dd_values_probe2.json").write_text(json.dumps(results, indent=1), encoding="utf-8")
cur.execute("SELECT code FROM ov_delivery_stream WHERE code LIKE 'AUTOTEST%'")
print("\nAUTOTEST rows left in ov_delivery_stream:", cur.fetchall())
conn.close()
