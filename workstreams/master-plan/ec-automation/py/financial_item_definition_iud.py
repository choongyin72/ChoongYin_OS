"""Financial Item Definition - IUD driver via the Universal Screen Engine (engine.py).

OV, custom-URL (grid manageObject:form:T_data), no navigator. First genuinely-new screen the
engine ever built cold (Phase 4 Pilot 1, 2026-08-14) - see
docs/universal_screen_engine_design.md section 23 for the 3 real engine gaps found+fixed here
(extra_fields convention, pagination-awareness, input-vs-span grid-cell rendering).

Mandatory Insert fields (confirmed live via Engine.field_inventory()): Item Code, Item Name,
Start Date, Item Type, Default Cost Object Type, Format Mask, Data Fallback Method - only these
are filled, per this project's "only fill needed fields" convention.
Run headed: EC_HEADED=1 py -X utf8 <this file>
"""
import os
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))
from engine import Engine, open_screen, SaveFailed, css  # noqa: E402
from universal_classifier import EC_URL  # noqa: E402
from playwright.sync_api import sync_playwright

CODE = os.environ.get("EC_CODE", "AUTOTEST_FID_006")
NAME = "AUTOTEST Financial Item Definition 006"
NAME_UPD = NAME + " UPDATED"
START_DATE = "2000-01-01"

HEADED = os.environ.get("EC_HEADED", "0") == "1"
EVID = _HERE.parent / "screens" / "EC_Revenue" / "Financial_Item" / "Financial_Item_Definition" / "evidence"
EVID.mkdir(parents=True, exist_ok=True)
results = {}


def shot(page, label):
    try:
        page.screenshot(path=str(EVID / (label + ".png")))
    except Exception:
        pass


with sync_playwright() as p:
    b = p.chromium.launch(headless=not HEADED, slow_mo=200 if HEADED else 0,
                           args=["--ignore-certificate-errors", "--start-maximized"])
    page = b.new_context(ignore_https_errors=True, no_viewport=HEADED).new_page()
    page.goto(EC_URL, wait_until="domcontentloaded", timeout=45000)
    open_screen(page, "Financial Item Definition")
    eng = Engine(page, "Financial Item Definition")
    shot(page, "01_loaded")

    print("=== INSERT ===")
    eng.toolbar("New Object")
    page.wait_for_timeout(1000)
    eng.fill("Item Code", CODE)
    eng.fill("Item Name", NAME)
    eng.fill("Start Date", START_DATE)
    eng.select("Item Type", "Cost")
    eng.select("Default Cost Object Type", "Cost Center")
    eng.select("Format Mask", "__FIRST__")
    eng.select("Data Fallback Method", "Overridden-Calculated-Interfaced")
    shot(page, "02_insert_filled")
    try:
        eng.click("Save")
        results["insert"] = "PASS"
        print("Insert Save OK")
    except SaveFailed as e:
        results["insert"] = "FAIL: %s" % str(e)[:150]
        shot(page, "insert_FAIL")
        raise
    shot(page, "03_insert_result")

    print("=== UPDATE ===")
    grids = page.evaluate("""() => Array.from(document.querySelectorAll('[id$=":T_data"]')).map(e => e.id)""")
    grid_id = grids[0]
    found = eng.select_row(grid_id, CODE)
    print("row selected:", found)
    eng.fill("Item Name", NAME_UPD)
    shot(page, "04_update_filled")
    try:
        eng.click("Save")
        results["update"] = "PASS"
        print("Update Save OK")
    except SaveFailed as e:
        results["update"] = "FAIL: %s" % str(e)[:150]
        shot(page, "update_FAIL")
        raise
    shot(page, "05_update_result")

    print("=== DELETE (End=Start) ===")
    found2 = eng.select_row(grid_id, CODE)
    print("row selected for delete:", found2)
    sd = eng._field("Start Date")
    sd_val = page.locator(css(sd["id"])).first.input_value()
    eng.fill("End Date", sd_val)
    shot(page, "06_delete_filled")
    try:
        eng.click("Save")
        results["delete"] = "PASS"
        print("Delete Save OK")
    except SaveFailed as e:
        results["delete"] = "FAIL: %s" % str(e)[:150]
        shot(page, "delete_FAIL")
        raise
    shot(page, "07_final_state")

    if HEADED:
        page.wait_for_timeout(3000)
    b.close()

print("\n" + "=" * 40 + "\nRESULTS")
ok = True
for k, v in results.items():
    mark = "OK" if v == "PASS" else "X"
    if mark == "X":
        ok = False
    print("  %s %-10s: %s" % (mark, k, v))
print("Overall:", "ALL PASS" if ok else "FAILURES")
sys.exit(0 if ok else 1)
