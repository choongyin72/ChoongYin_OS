"""For each of the 7 Dispatching OV screens: open New Object, fill ONLY Code/Name/Start
Date, Save, and capture the 'Required fields are empty' banner -> the screen's mandatory
extras. If a save unexpectedly SUCCEEDS, immediately true-delete the row (End=Start).
"""
import json
import os
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

URL = os.environ.get("EC_URL", "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/")
USER = os.environ.get("EC_USER", "sysadmin")
PASS = os.environ.get("EC_PASS", "sysadmin")
OUT = Path(r"c:/Projects/ChoongYin_OS/tmp/dispatching_recon")

SCREENS = [  # name, date row
    ("Delivery Point", 3), ("Delivery Stream", 2), ("Meter", 2),
    ("Nomination Point", 3), ("Pipeline Segment", 2),
    ("Transport System", 2), ("Transport Zone", 3),
]

results = {}
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_context(ignore_https_errors=True, viewport={"width": 1920, "height": 1080}).new_page()
    page.goto(URL, wait_until="domcontentloaded", timeout=60000)
    page.fill('[id="username"]', USER)
    page.fill('[id="password"]', PASS)
    page.click('[id="kc-login"]')
    page.wait_for_selector('[id="menu:searchForm:searchTxt"]', timeout=60000)

    for name, drow in SCREENS:
        tag = name.lower().replace(" ", "_")
        code = "AUTOTEST_PRB_" + time.strftime("%H%M%S")
        try:
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
            page.locator('xpath=//li[contains(@class,"ui-menu-parent")][.//span[contains(@class,"ui-icon-insert")]]').hover()
            item = page.locator('xpath=//ul[contains(@class,"ui-menu-child")]//li//a[normalize-space(.)="New Object"]')
            item.wait_for(state="visible", timeout=10000)
            item.click()
            page.wait_for_load_state("networkidle", timeout=15000)
            time.sleep(1.5)
            page.fill('[id="tab:tabPanel:objectForm:form:G:0:R:0:C:1:in"]', code)
            page.fill('[id="tab:tabPanel:objectForm:form:G:0:R:1:C:1:in"]', "Probe")
            page.fill(f'[id="tab:tabPanel:objectForm:form:G:0:R:{drow}:C:1:da_input"]', "2003-01-01")
            page.keyboard.press("Escape")
            time.sleep(0.5)
            page.locator('xpath=//li[.//span[contains(@class,"ui-icon-save")]][1]').first.click()
            page.wait_for_load_state("networkidle", timeout=20000)
            time.sleep(2.5)
            banner = page.evaluate("""() => {
                const t = [...document.querySelectorAll('div,span')]
                  .map(e => (e.textContent||'').trim())
                  .filter(t => t.includes('Required fields are empty') && t.length < 400);
                return t.sort((a,b)=>a.length-b.length)[0] || null; }""")
            results[name] = {"banner": banner, "code": code}
            print(f"{name}: {'REJECTED -> ' + (banner or '')[:160] if banner else 'NO BANNER (likely SAVED!)'}")
            page.screenshot(path=str(OUT / f"{tag}_mand_probe.png"), full_page=True)
        except Exception as e:
            results[name] = {"error": str(e)[:200]}
            print(f"!! {name}: {str(e)[:140]}")
    browser.close()

(OUT / "mandatory_probe.json").write_text(json.dumps(results, indent=1), encoding="utf-8")
print("saved -> mandatory_probe.json")
print("\nNOTE: any 'NO BANNER' screen may have created a probe row - verify in DB and clean up.")
