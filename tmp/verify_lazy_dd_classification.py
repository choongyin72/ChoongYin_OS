import json
import os
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parent / "workstreams" / "master-plan" / "ec-automation" / "py"))
from engine import Engine, open_screen, css
from universal_classifier import EC_URL, ajax
from playwright.sync_api import sync_playwright

HEADED = os.environ.get("EC_HEADED", "0") == "1"

with sync_playwright() as p:
    b = p.chromium.launch(headless=not HEADED, slow_mo=400 if HEADED else 0,
                          args=["--ignore-certificate-errors", "--start-maximized"])
    page = b.new_context(ignore_https_errors=True, no_viewport=HEADED).new_page()
    page.goto(EC_URL, wait_until="domcontentloaded", timeout=45000)

    open_screen(page, "Project Data Mapping Setup")
    eng = Engine(page, "Project Data Mapping Setup")

    dd_base = "StandardNavigator:form:G:0:R:0:C:3:dd"
    page.locator(css(dd_base + "_button")).first.click()
    page.wait_for_timeout(800)
    page.locator(f"xpath=//*[@id='{dd_base}_panel']//tr[@data-item-label='Monthly Royalty Calculation Test']").first.click()
    ajax(page)
    page.locator(css("buttongo:form:B")).first.click()
    ajax(page, 15000)

    eng.toolbar("New Object")
    page.wait_for_timeout(1000)

    inv_before = eng.field_inventory().get("objectForm", [])
    unresolved_before = [f["label"] for f in inv_before if f["primitive"] == "dropdown_or_popup"]
    print("dd fields UNRESOLVED before touching anything:", unresolved_before)

    eng.fill("Code", "AUTOTEST_LAZY_CHECK")

    inv_after = eng.field_inventory().get("objectForm", [])
    unresolved_after = [f["label"] for f in inv_after if f["primitive"] == "dropdown_or_popup"]
    resolved_after = [f["label"] for f in inv_after if f["primitive"] in ("dropdown", "popup")]
    print("dd fields still UNRESOLVED after filling only 'Code' (a text field):", unresolved_after)
    print("dd fields RESOLVED after filling only 'Code':", resolved_after)
    print("\nPASS" if unresolved_after == unresolved_before and not resolved_after else "\nFAIL - resolution happened without being touched")

    eng.select("Data Entry Source", "__FIRST__")
    inv_after2 = eng.field_inventory().get("objectForm", [])
    unresolved_after2 = [f["label"] for f in inv_after2 if f["primitive"] == "dropdown_or_popup"]
    resolved_after2 = [f["label"] for f in inv_after2 if f["primitive"] in ("dropdown", "popup")]
    print("\ndd fields still UNRESOLVED after also selecting 'Data Entry Source':", unresolved_after2)
    print("dd fields RESOLVED after also selecting 'Data Entry Source':", resolved_after2)
    only_one_resolved = resolved_after2 == ["Data Entry Source"]
    print("\nPASS" if only_one_resolved else "\nFAIL - more than the touched field got resolved")

    if HEADED:
        page.wait_for_timeout(8000)
    b.close()
