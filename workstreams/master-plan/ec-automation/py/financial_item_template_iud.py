"""Financial Item Template - IUD driver via the Universal Screen Engine (engine.py).

TV (grid templ:form:T_data), physical delete (no navigator scoping needed - Business Unit/
Contract Area/Date are all optional filter fields, confirmed mandatory=false via
Engine.field_inventory()). Phase 4 Pilot 2 (2026-08-14) - see
docs/universal_screen_engine_design.md section 23 for the 3 real gaps found+fixed here
(Insert/Delete flyout text = "Template" not the screen title; mandatory Valid From/DAYTIME field;
date-in-grid-cell wrapper-vs-nested-input gap in universal_classifier.py).

Only Code, Name, Valid From are filled (the only mandatory fields) - per this project's
"only fill needed fields" convention.
Run headed: EC_HEADED=1 py -X utf8 <this file>
"""
import os
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))
from engine import Engine, open_screen  # noqa: E402
from universal_classifier import EC_URL  # noqa: E402
from playwright.sync_api import sync_playwright

CODE = os.environ.get("EC_CODE", "AUTOTEST_FIT_001")
NAME = "AUTOTEST Financial Item Template 001"
NAME_UPD = NAME + " UPDATED"
VALID_FROM = "2000-01-01"

HEADED = os.environ.get("EC_HEADED", "0") == "1"
EVID = _HERE.parent / "screens" / "EC_Revenue" / "Financial_Item" / "Financial_Item_Template" / "evidence"
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
    open_screen(page, "Financial Item Template")
    eng = Engine(page, "Financial Item Template")
    shot(page, "01_loaded")

    grids = page.evaluate("""() => Array.from(document.querySelectorAll('[id$=":T_data"]')).map(e => e.id)""")
    grid_id = grids[0]

    print("=== INSERT ===")
    eng.toolbar("Template", icon="insert")
    page.wait_for_timeout(1000)
    # find_grid_row("") matches the FIRST row with any blank cell (e.g. an optional column on an
    # existing row), not necessarily the truly-blank new row - resolve directly by requiring BOTH
    # Code and Name cells empty, the real signature of the new blank row.
    rows = page.evaluate(
        """(gid) => { const tb = document.getElementById(gid);
        return Array.from(tb.querySelectorAll('tr[data-ri]')).map(tr => ({
            ri: parseInt(tr.getAttribute('data-ri'), 10),
            cells: Array.from(tr.querySelectorAll('td')).map(td => {
                const inp = td.querySelector('input'); return inp ? inp.value : td.textContent.trim();
            }),
        })); }""",
        grid_id,
    )
    row_idx = next(r["ri"] for r in rows if r["cells"][0] == "" and r["cells"][1] == "")
    print("new blank row index:", row_idx)
    eng.grid_cell(grid_id, row_idx, "Financial Item Template Code").set(CODE)
    eng.grid_cell(grid_id, row_idx, "Financial Item Template Name").set(NAME)
    eng.grid_cell(grid_id, row_idx, "Valid From").set(VALID_FROM)
    shot(page, "02_insert_filled")
    eng.click("Save")
    results["insert"] = "PASS"
    print("Insert Save OK")
    shot(page, "03_insert_result")

    print("=== UPDATE ===")
    row_idx = eng.find_grid_row(grid_id, CODE)
    eng.grid_cell(grid_id, row_idx, "Financial Item Template Name").set(NAME_UPD)
    shot(page, "04_update_filled")
    eng.click("Save")
    results["update"] = "PASS"
    print("Update Save OK")
    shot(page, "05_update_result")

    print("=== DELETE (physical) ===")
    row_idx = eng.find_grid_row(grid_id, CODE)
    eng.select_grid_row(grid_id, CODE)
    eng.toolbar("Template", icon="delete")
    page.wait_for_timeout(1000)
    shot(page, "06_delete_filled")
    eng.click("Save")
    results["delete"] = "PASS"
    print("Delete Save OK")
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
