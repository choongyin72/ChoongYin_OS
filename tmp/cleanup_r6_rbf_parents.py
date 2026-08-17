"""Clean up the 2 leftover parent objects from Reservoir Block Formation's unfinished round-6 run
(AUTOTEST_R6_RBFB / AUTOTEST_R6_RBFF) - the junction object itself never got created, so these are
orphaned test data with no dependent RBF row to clean first. Row-identity verified before delete."""
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parent / "workstreams" / "master-plan" / "ec-automation" / "py"))
sys.path.insert(0, str(_HERE.parent / "workstreams" / "master-plan" / "ec-automation" / "libraries"))
from engine import Engine, open_screen, css
from universal_classifier import EC_URL
from playwright.sync_api import sync_playwright
import DbVerify as db

SD = "2000-01-01"
TARGETS = [
    ("Reservoir Formation", "AUTOTEST_R6_RBFF", "Reservoir Formation Code", "ov_resv_formation"),
    ("Reservoir Block", "AUTOTEST_R6_RBFB", "Reservoir Block Code", "ov_resv_block"),
]

with sync_playwright() as p:
    b = p.chromium.launch(headless=True, args=["--ignore-certificate-errors"])
    page = b.new_context(ignore_https_errors=True, viewport={"width": 1920, "height": 1080}).new_page()
    page.goto(EC_URL, wait_until="domcontentloaded", timeout=45000)

    for name, code, code_label, view in TARGETS:
        open_screen(page, name)
        eng = Engine(page, name)
        grids = page.evaluate("""() => Array.from(document.querySelectorAll('[id$=":T_data"]')).map(e => e.id)""")
        grid_id = grids[0]
        found = eng.select_row(grid_id, code)
        if not found:
            print(f"{code}: not found in grid, skipping")
            continue
        f = eng._field(code_label)
        actual = page.locator(css(f["id"])).first.input_value()
        if actual != code:
            print(f"ROW IDENTITY MISMATCH for {code}: form shows {actual!r} - ABORTING, not touching")
            continue
        eng.fill("End Date", SD)
        eng.click("Save")
        print(f"{code}: deleted (End=Start), DB still present = {db.code_present(view, code)}")

    b.close()
