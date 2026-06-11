"""READ-ONLY: Sub Area screen - pick PU 'Production Unit', dump the Area
cascade dropdown's CURRENT options + the navigator date, plus OV_AREA rows
under that PU from the DB for comparison."""
import json
from pathlib import Path

import oracledb
from playwright.sync_api import sync_playwright

EC_URL = "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"
_scan = json.loads(Path(r"c:/Projects/ChoongYin_OS/tmp/screen_scan/assets_scan.json").read_text(encoding="utf-8"))
URL = next(r["url"] for r in _scan.values()
           if r.get("section") == "Basic Objects" and r["screen"] == "Sub Area")

print("--- DB: areas (any PU) ---")
conn = oracledb.connect(user="ECKERNEL_EC", password="energy", dsn="localhost:1521/ORCL")
cur = conn.cursor()
cur.execute("SELECT CODE, NAME, OBJECT_START_DATE, OBJECT_END_DATE FROM OV_AREA ORDER BY CODE FETCH FIRST 30 ROWS ONLY")
for r in cur.fetchall():
    print("  ", r)
cur.close()
conn.close()

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
    page.goto(URL, wait_until="domcontentloaded", timeout=45000)
    page.wait_for_timeout(2500)
    date_val = page.evaluate(
        "() => { const e = document.querySelector(\"input[id$='da_input']\"); return e ? e.value : null }")
    print("navigator date:", date_val)
    dd1 = "nav:form:G:0:R:1:C:1:dd"
    page.click(f"[id='{dd1}_button']")
    page.wait_for_selector(f"[id='{dd1}_panel'] tr[data-item-label]", state="visible", timeout=10000)
    page.click(f"[id='{dd1}_panel'] tr[data-item-label='Production Unit']")
    page.wait_for_timeout(2500)
    dd2 = "nav:form:G:0:R:1:C:2:dd"
    page.click(f"[id='{dd2}_button']")
    page.wait_for_timeout(3000)
    labels = page.evaluate(
        "(pid) => { const p=document.getElementById(pid); if(!p) return null; "
        "return {text: p.innerText.trim().substring(0,300), "
        "labels: Array.from(p.querySelectorAll('tr[data-item-label]')).map(r=>r.getAttribute('data-item-label'))}; }",
        f"{dd2}_panel")
    print("Area cascade options:", labels)
    ctx.close()
    b.close()
