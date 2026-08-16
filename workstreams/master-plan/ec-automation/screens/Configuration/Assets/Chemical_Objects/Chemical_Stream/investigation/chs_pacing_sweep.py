"""Item 6a: does Chemical Stream's updateAttributes dropdown sweep stall under the PRODUCTION
engine's own select() (already properly paced via ajax() = networkidle+900ms wait), on a fresh
page load, no prior re-navigation? Read-only test - no Save, nothing persisted.
Run headed: EC_HEADED=1 py -X utf8 tmp/chs_pacing_sweep.py
"""
import json
import os
import sys
import time
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parents[5] / "py"))
from engine import Engine, open_screen, FieldNotFound  # noqa: E402
from universal_classifier import EC_URL  # noqa: E402
from playwright.sync_api import sync_playwright

HEADED = os.environ.get("EC_HEADED", "0") == "1"
NAV_PU, NAV_AREA, NAV_FC1 = "P1 Production Unit", "P1 Area", "P1 Facility 1"
REAL_CODE = "P1 CS001 CT001 SI"

DROPDOWNS = [
    "Actual Dosage Method", "Alloc Data Frequency", "Alloc Fixed", "Alloc Period",
    "Chemical Stream Type", "Class Attribute", "Class Name", "Cp Area",
    "Cp Collection Point", "Cp Operator Route", "Cp Production Unit", "Geo Area",
    "Geo Field", "Injection Phase", "Op Area", "Op Facility Class 1",
    "Op Production Unit", "Stream Category", "Stream Phase", "Stream Type",
    "Usage Reporting",
]

results = {}

with sync_playwright() as p:
    b = p.chromium.launch(headless=not HEADED, slow_mo=200 if HEADED else 0,
                           args=["--ignore-certificate-errors", "--start-maximized"])
    page = b.new_context(ignore_https_errors=True, no_viewport=HEADED).new_page()
    page.goto(EC_URL, wait_until="domcontentloaded", timeout=45000)

    open_screen(page, "Chemical Stream")
    eng = Engine(page, "Chemical Stream")
    eng.apply_navigator(values=[NAV_PU, NAV_AREA, NAV_FC1])
    grids = page.evaluate("""() => Array.from(document.querySelectorAll('[id$=":T_data"]')).map(e => e.id)""")
    grid_id = grids[0]
    eng.select_row(grid_id, REAL_CODE)

    print(f"=== sweeping {len(DROPDOWNS)} dropdown fields via engine.select() (fresh page, no re-nav) ===")
    for label in DROPDOWNS:
        t0 = time.time()
        try:
            val = eng.select(label, "__FIRST__")
            dt = time.time() - t0
            results[label] = ("PASS", dt, val)
            print(f"  OK  {label:<28} {dt:5.2f}s -> {val!r}")
        except FieldNotFound as e:
            results[label] = ("SKIP-NOFIRST", time.time() - t0, str(e)[:80])
            print(f"  SKIP {label:<28} (no default option / type-to-search): {e}")
        except Exception as e:
            dt = time.time() - t0
            results[label] = ("STALL/FAIL", dt, str(e)[:120])
            print(f"  X   {label:<28} {dt:5.2f}s -> {e}")

    if HEADED:
        page.wait_for_timeout(2000)
    b.close()

stalled = [k for k, v in results.items() if v[0] == "STALL/FAIL"]
print("\n" + "=" * 60)
print(f"RESULT: {len(stalled)}/{len(DROPDOWNS)} stalled")
if stalled:
    print("stalled fields:", stalled)
sys.exit(1 if stalled else 0)
