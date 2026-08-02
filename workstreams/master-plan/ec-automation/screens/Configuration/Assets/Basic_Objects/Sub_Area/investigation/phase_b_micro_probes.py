"""READ-ONLY micro-probes to sharpen the phase-B question list:
1. Sub Area cascade: pick 'EC-UT-GENERIC Production Unit' (and one alternative)
   in dd1, read which Areas appear in dd2.
2. DB: sample codes from OV_BANK (candidate Object List items) and row counts of
   OV_AREA / OV_SUB_AREA / OV_PROD_SUB_UNIT for context."""
import os
import json
from pathlib import Path

import oracledb
from playwright.sync_api import sync_playwright

EC_URL = "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"
SCAN = Path(r"c:/Projects/ChoongYin_OS/tmp/screen_scan/assets_scan.json")
scan = json.loads(SCAN.read_text(encoding="utf-8"))
SUB_AREA_URL = next(r["url"] for r in scan.values()
                    if r.get("section") == "Basic Objects" and r["screen"] == "Sub Area")

PUS = ["EC-UT-GENERIC Production Unit", "Production Unit 1", "AS1 EC Exploration Norway"]

print("--- DB context ---")
conn = oracledb.connect(user="ECKERNEL_EC", password="energy",
                        dsn="localhost:1521/ORCL", tcp_connect_timeout=15)
cur = conn.cursor()
for view in ["OV_BANK", "OV_AREA", "OV_SUB_AREA", "OV_PROD_SUB_UNIT", "OV_OBJECT_LIST_SETUP"]:
    try:
        cur.execute(f"SELECT COUNT(*) FROM {view}")
        n = cur.fetchone()[0]
        sample = []
        if n and view == "OV_BANK":
            cur.execute(f"SELECT OBJECT_CODE FROM {view} FETCH FIRST 5 ROWS ONLY")
            sample = [r[0] for r in cur.fetchall()]
        print(f"  {view}: {n} rows {sample}")
    except Exception as e:
        print(f"  {view}: ERR {str(e)[:80]}")
cur.close()
conn.close()

print("--- Sub Area cascade probe ---")
with sync_playwright() as p:
    b = p.chromium.launch(headless=True, args=["--ignore-certificate-errors"])
    ctx = b.new_context(ignore_https_errors=True, viewport={"width": 1680, "height": 1200})
    page = ctx.new_page()
    page.on("dialog", lambda d: d.accept())
    page.goto(EC_URL, wait_until="domcontentloaded", timeout=45000)
    page.fill("#username", os.environ.get("EC_USER", "sysadmin"))
    page.fill("#password", os.environ.get("EC_PASS", "sysadmin"))
    page.click("#kc-login")
    page.wait_for_url("**/dashboard**", timeout=60000)
    page.wait_for_timeout(1500)
    for pu in PUS:
        page.goto(SUB_AREA_URL, wait_until="domcontentloaded", timeout=45000)
        try:
            page.wait_for_load_state("networkidle", timeout=20000)
        except Exception:
            pass
        page.wait_for_timeout(1500)
        try:
            dd1 = "nav:form:G:0:R:1:C:1:dd"
            page.click(f"[id='{dd1}_button']")
            page.wait_for_selector(f"[id='{dd1}_panel']", state="visible", timeout=10000)
            page.wait_for_timeout(1200)
            page.click(f"[id='{dd1}_panel'] >> text=\"{pu}\"")
            page.wait_for_timeout(1500)
            dd2 = "nav:form:G:0:R:1:C:2:dd"
            page.click(f"[id='{dd2}_button']")
            page.wait_for_selector(f"[id='{dd2}_panel']", state="visible", timeout=10000)
            page.wait_for_timeout(1500)
            txt = page.evaluate(
                "(pid) => { const e=document.getElementById(pid); return e ? e.innerText.trim().substring(0,300) : null }",
                f"{dd2}_panel")
            print(f"  PU '{pu}' -> Areas: {txt!r}")
            page.keyboard.press("Escape")
        except Exception as e:
            print(f"  PU '{pu}': ERR {str(e)[:100]}")
    ctx.close()
    b.close()
