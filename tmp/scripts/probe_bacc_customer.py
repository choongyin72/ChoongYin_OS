"""Bank Account: do the Customer / Vendor dropdowns have options?"""
import json
from pathlib import Path

from playwright.sync_api import sync_playwright

EC_URL = "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"
rec = next(r for r in json.loads(Path(r"c:/Projects/ChoongYin_OS/tmp/screen_scan/financial_objects_recon.json").read_text(encoding="utf-8"))
           if r["screen"] == "Bank Account")
DDS = {(f.get("label") or "").strip(): (f["id"].rsplit("_", 1)[0] if f["id"].endswith("_button") else f["id"])
       for f in rec["insertPlan"] if f.get("kind") == "dropdown" and f.get("visible")}

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
    for lab in ["Customer", "Vendor"]:
        dd = DDS.get(lab)
        page.click(f"[id='{dd}_button']")
        page.wait_for_timeout(2500)
        opts = page.evaluate(
            "(pid)=>Array.from(document.querySelectorAll('#'+CSS.escape(pid)+' tr[data-item-label]')).map(r=>r.getAttribute('data-item-label')).slice(0,5)",
            dd + "_panel")
        print(f"{lab}: id={dd} options={opts}")
        page.keyboard.press("Escape")
        page.wait_for_timeout(500)
    ctx.close()
    b.close()
