import json
import os
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.resolve().parents[5] / "py"))
from engine import Engine, open_screen, css
from universal_classifier import EC_URL, ajax
from playwright.sync_api import sync_playwright

HEADED = os.environ.get("EC_HEADED", "0") == "1"

with sync_playwright() as p:
    b = p.chromium.launch(headless=not HEADED, slow_mo=200 if HEADED else 0,
                           args=["--ignore-certificate-errors", "--start-maximized"])
    page = b.new_context(ignore_https_errors=True, no_viewport=HEADED).new_page()
    page.goto(EC_URL, wait_until="domcontentloaded", timeout=45000)

    open_screen(page, "Project Data Mapping Setup")
    eng = Engine(page, "Project Data Mapping Setup")

    dd_base = "StandardNavigator:form:G:0:R:0:C:3:dd"
    page.locator(css(dd_base + "_button")).first.click()
    page.wait_for_timeout(800)
    page.locator(
        f"xpath=//*[@id='{dd_base}_panel']//tr[@data-item-label='Monthly Royalty Calculation Test']"
    ).first.click()
    ajax(page)
    page.locator(css("buttongo:form:B")).first.click()
    ajax(page, 15000)

    print("=== toolbar / New Object ===")
    eng.toolbar("New Object")
    page.wait_for_timeout(1500)

    inv = eng.field_inventory()
    print(json.dumps(inv.get("objectForm", []), indent=2))

    b.close()
