"""READ-ONLY: (a) which Account Mapping combinations are TAKEN (ALT_CODE space),
(b) what each insert dropdown actually offers (panel labels). Output feeds the
choice of a valid-but-unused test combination."""
import json
from pathlib import Path

import oracledb
from playwright.sync_api import sync_playwright

print("=== taken combinations (ALT_CODE) ===")
conn = oracledb.connect(user="ECKERNEL_EC", password="energy", dsn="localhost:1521/ORCL")
cur = conn.cursor()
cur.execute("SELECT ALT_CODE FROM OV_FIN_ACCOUNT_MAPPING ORDER BY ALT_CODE")
taken = [r[0] for r in cur.fetchall()]
for t in taken:
    print("  ", t)
cur.close()
conn.close()

print("\n=== insert dropdown panel labels ===")
EC_URL = "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"
rec = next(r for r in json.loads(Path(r"c:/Projects/ChoongYin_OS/tmp/screen_scan/financial_objects_recon.json").read_text(encoding="utf-8"))
           if r["screen"] == "Account Mapping")
DDS = [( (f.get("label") or "").strip(), f["id"].rsplit("_", 1)[0] if f["id"].endswith("_button") else f["id"])
       for f in rec["insertPlan"] if f.get("kind") == "dropdown" and f.get("visible")]

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
    page.goto(rec["url"], wait_until="domcontentloaded", timeout=45000)
    page.wait_for_timeout(2500)
    page.hover("xpath=//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'ui-icon-insert')]]")
    item = page.locator("xpath=//li[contains(@class,'ui-menu-parent')]"
                        "[.//span[contains(@class,'ui-icon-insert')]]//ul//a[normalize-space(.)='New Object']")
    item.wait_for(state="visible", timeout=8000)
    item.click()
    page.wait_for_timeout(2000)
    # set start date FIRST (2003) so date-filtered dds (Financial Account) populate correctly
    date_f = next(f for f in rec["insertPlan"] if f.get("kind") == "date" and f.get("visible"))
    page.fill(f"[id='{date_f['id']}']", "2003-01-01")
    page.keyboard.press("Tab")
    page.wait_for_timeout(1000)
    for lab, dd in DDS:
        try:
            page.click(f"[id='{dd}_button']")
            page.wait_for_timeout(2200)
            opts = page.evaluate(
                "(pid)=>Array.from(document.querySelectorAll('#'+CSS.escape(pid)+' tr[data-item-label]')).map(r=>r.getAttribute('data-item-label')).slice(0,12)",
                dd + "_panel")
            print(f"  {lab:22s}: {opts}")
            page.keyboard.press("Escape")
            page.wait_for_timeout(400)
        except Exception as e:
            print(f"  {lab:22s}: ERR {str(e)[:80]}")
    ctx.close()
    b.close()
