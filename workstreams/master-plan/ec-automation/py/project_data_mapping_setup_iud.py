"""Project Data Mapping Setup - IUD driver via the Universal Screen Engine (engine.py).

OV, class COST_MAPPING, NONSTANDARD navigator (StandardNavigator:form:G:0:R:<row>:C:<col>:dd/
da_input, real GO = buttongo:form:B - not the usual nav:form:... prefix). Phase 4 Pilot 3, by far
the deepest pilot (docs/universal_screen_engine_design.md "Pilot 3" section + follow-up); item #7
of the open-items tracker closes the packaging gap this driver fills.

Mandatory Insert fields (confirmed live via Engine.field_inventory()): Code, Name, Start Date,
Data Entry Source, Dataset/Report, Mapping Type. Cross-field OR-mandatory rule (neither field is
individually yellow): Target Property OR Target Project/Product Stream must be set - satisfied
here with Target Property = "Oil Sands Projects" (real, confirmed-existing option).

KNOWN DEFECT + FIX applied on Update (open-items #7, design doc section 24): the Reference field
(REPORT_REF_ID) fails to auto-populate its displayed value on row-select, even when the row's own
Reference is genuinely set - re-selecting the SAME already-correct value from the dropdown before
Save restores it with zero data loss. This driver demonstrates that fix explicitly on Update.

Run headed: EC_HEADED=1 py -X utf8 <this file>
"""
import os
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))
from engine import Engine, open_screen, SaveFailed, css  # noqa: E402
from universal_classifier import EC_URL, ajax  # noqa: E402
from playwright.sync_api import sync_playwright

CODE = os.environ.get("EC_CODE", "AUTOTEST_PDMS_007")
NAME = "AUTOTEST Project Data Mapping Setup 007"
NAME_UPD = NAME + " UPDATED"
START_DATE = "2009-01-01"  # must be >= BOTH Target Property "Oil Sands Projects" (2003-01-01) AND Reference "Allowed Costs - Capital Test" (2009-01-01) own OBJECT_START_DATE, both confirmed via DB
DATASET = "Monthly Royalty Calculation Test"
TARGET_PROPERTY = "Oil Sands Projects"
REFERENCE = "Allowed Costs - Capital Test"  # real Report Reference under Dataset=MRC_TEST, confirmed earlier this session

HEADED = os.environ.get("EC_HEADED", "0") == "1"
EVID = _HERE.parent / "screens" / "Configuration" / "Assets" / "Data_Mapping_Objects" / \
    "Project_Data_Mapping_Setup" / "evidence"
EVID.mkdir(parents=True, exist_ok=True)
results = {}


def shot(page, label):
    try:
        page.screenshot(path=str(EVID / (label + ".png")))
    except Exception:
        pass


def apply_dataset_navigator(page, dataset_label):
    """NONSTANDARD navigator - not nav:form:..., so apply_navigator() doesn't apply here."""
    dd_base = "StandardNavigator:form:G:0:R:0:C:3:dd"
    page.locator(css(dd_base + "_button")).first.click()
    page.wait_for_timeout(800)
    page.locator(
        f"xpath=//*[@id='{dd_base}_panel']//tr[@data-item-label='{dataset_label}']"
    ).first.click()
    ajax(page)
    page.locator(css("buttongo:form:B")).first.click()
    ajax(page, 15000)


with sync_playwright() as p:
    b = p.chromium.launch(headless=not HEADED, slow_mo=200 if HEADED else 0,
                           args=["--ignore-certificate-errors", "--start-maximized"])
    page = b.new_context(ignore_https_errors=True, no_viewport=HEADED).new_page()
    page.goto(EC_URL, wait_until="domcontentloaded", timeout=45000)
    open_screen(page, "Project Data Mapping Setup")
    eng = Engine(page, "Project Data Mapping Setup")
    shot(page, "01_loaded")

    apply_dataset_navigator(page, DATASET)
    shot(page, "01b_nav_applied")

    grids0 = page.evaluate("""() => Array.from(document.querySelectorAll('[id$=":T_data"]')).map(e => e.id)""")
    grid_id0 = grids0[0] if grids0 else "manageObject:form:T_data"
    if eng.select_row(grid_id0, CODE):
        print("  pre-existing", CODE, "from a prior partial run - closing (End=Start) first")
        sd_pre = eng._field("Start Date")
        sd_val_pre = page.locator(css(sd_pre["id"])).first.input_value()
        eng.fill("End Date", sd_val_pre)
        eng.click("Save")
        page.wait_for_timeout(1000)

    print("=== INSERT ===")
    eng.toolbar("New Object")
    page.wait_for_timeout(1000)
    eng.fill("Code", CODE)
    eng.fill("Name", NAME)
    eng.fill("Start Date", START_DATE)
    eng.select("Data Entry Source", "__FIRST__")
    eng.select("Dataset/Report", DATASET)
    eng.select("Mapping Type", "__FIRST__")
    eng.select("Target Property", TARGET_PROPERTY)
    eng.select("Reference", REFERENCE)
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

    print("=== UPDATE (with Reference-field-blank-on-select defect workaround) ===")
    grids = page.evaluate("""() => Array.from(document.querySelectorAll('[id$=":T_data"]')).map(e => e.id)""")
    grid_id = grids[0]
    found = eng.select_row(grid_id, CODE)
    print("row selected:", found)
    eng.fill("Name", NAME_UPD)
    # KNOWN DEFECT WORKAROUND (item #7): Reference display fails to carry over on row-select even
    # though the DB value is intact - re-select the same already-correct value before Save.
    eng.select("Reference", REFERENCE)
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
