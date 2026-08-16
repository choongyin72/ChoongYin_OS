"""Read-only structural recon: does Chemical Stream's updateAttributes (row-select/Update) form
even have dropdown fields to stall on? Item 6a groundwork - answer this before any pacing test.
No writes, no Save, no data mutation - field_inventory() only.
Run headed: EC_HEADED=1 py -X utf8 tmp/chs_structural_recon.py
"""
import json
import os
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parents[5] / "py"))
from engine import Engine, open_screen, css  # noqa: E402
from universal_classifier import EC_URL, ajax  # noqa: E402
from playwright.sync_api import sync_playwright

HEADED = os.environ.get("EC_HEADED", "0") == "1"
NAV_PU, NAV_AREA, NAV_FC1 = "P1 Production Unit", "P1 Area", "P1 Facility 1"
REAL_CODE = "P1 CS001 CT001 SI"

with sync_playwright() as p:
    b = p.chromium.launch(headless=not HEADED, slow_mo=300 if HEADED else 0,
                           args=["--ignore-certificate-errors", "--start-maximized"])
    page = b.new_context(ignore_https_errors=True, no_viewport=HEADED).new_page()
    page.goto(EC_URL, wait_until="domcontentloaded", timeout=45000)

    open_screen(page, "Chemical Stream")
    eng = Engine(page, "Chemical Stream")

    print("=== field_inventory() BEFORE navigator applied ===")
    print(json.dumps(eng.field_inventory(), indent=2))

    print("=== applying navigator (specific P1 values) + GO ===")
    eng.apply_navigator(values=[NAV_PU, NAV_AREA, NAV_FC1])

    grids = page.evaluate("""() => Array.from(document.querySelectorAll('[id$=":T_data"]')).map(e => e.id)""")
    grid_id = grids[0]
    print("grid_id:", grid_id)
    print("=== field_inventory(grid_id) AFTER navigator+GO (grid visible) ===")
    print(json.dumps(eng.field_inventory(grid_id), indent=2))

    print("=== selecting real row:", REAL_CODE, "===")
    found = eng.select_row(grid_id, REAL_CODE)
    print("select_row ->", found)

    print("=== field_inventory() AFTER row-select (updateAttributes/objectdates visible) ===")
    print(json.dumps(eng.field_inventory(), indent=2))

    if HEADED:
        page.wait_for_timeout(3000)
    b.close()
