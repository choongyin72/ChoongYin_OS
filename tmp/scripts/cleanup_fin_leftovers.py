"""Clean the 3 AUTOTEST leftovers from the GO-timeout suites (their inserts
saved before the suite failed, so TC04 never ran): standard End=Start true
delete via the UI, then DB-verify gone."""
import json
from pathlib import Path

import oracledb
from playwright.sync_api import sync_playwright

EC_URL = "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"
RECON = Path(r"c:/Projects/ChoongYin_OS/tmp/screen_scan/financial_objects_recon.json")
records = {r["screen"]: r for r in json.loads(RECON.read_text(encoding="utf-8"))}

TARGETS = [("Cost Centre", "AUTOTEST_CC_20260611211236"),
           ("Revenue Order", "AUTOTEST_RO_20260611211905"),
           ("WBS", "AUTOTEST_WBS_20260611212317")]
END_ID = "tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input"


def _css(fid):
    return "#" + fid.replace(":", "\\:")


with sync_playwright() as p:
    b = p.chromium.launch(headless=True, args=["--ignore-certificate-errors"])
    ctx = b.new_context(ignore_https_errors=True, viewport={"width": 1680, "height": 1200})
    page = ctx.new_page()
    page.goto(EC_URL, wait_until="domcontentloaded", timeout=45000)
    page.fill("#username", "sysadmin")
    page.fill("#password", "sysadmin")
    page.click("#kc-login")
    page.wait_for_url("**/dashboard**", timeout=60000)
    page.wait_for_timeout(1500)
    for screen, code in TARGETS:
        rec = records[screen]
        print(f"== {screen}: {code}")
        page.goto(rec["url"], wait_until="domcontentloaded", timeout=45000)
        try:
            page.wait_for_load_state("networkidle", timeout=20000)
        except Exception:
            pass
        page.wait_for_timeout(1500)
        row = page.locator(f"xpath=//tbody[@id='{rec['gridId']}']//span[normalize-space(text())='{code}']")
        if row.count() == 0:
            print("   not in grid (already cleaned) - skip")
            continue
        row.first.click()
        page.wait_for_timeout(1800)
        el = page.locator(_css(END_ID))
        el.click()
        el.fill("2000-01-01")
        page.keyboard.press("Tab")
        page.wait_for_timeout(600)
        page.evaluate("(id)=>{const e=document.getElementById(id); if(e){"
                      "e.dispatchEvent(new Event('change',{bubbles:true}));"
                      "e.dispatchEvent(new Event('blur',{bubbles:true}));}}", END_ID)
        page.wait_for_timeout(800)
        save = page.locator("xpath=//a[@title='Save [Ctrl+s]' and not(contains(@class,'ui-state-disabled'))]")
        if save.count():
            save.first.click()
        else:
            page.keyboard.press("Control+s")
        try:
            page.wait_for_load_state("networkidle", timeout=15000)
        except Exception:
            pass
        page.wait_for_timeout(1500)
        print("   deleted (End=Start)")
    ctx.close()
    b.close()

conn = oracledb.connect(user="ECKERNEL_EC", password="energy", dsn="localhost:1521/ORCL")
cur = conn.cursor()
for screen, code in TARGETS:
    v = records[screen]["dbView"]
    cur.execute(f"SELECT COUNT(*) FROM {v} WHERE CODE = :c", c=code)
    n = cur.fetchone()[0]
    print(f"DB {v}: {code} remaining={n} {'OK' if n == 0 else 'STILL THERE!'}")
cur.close()
conn.close()
