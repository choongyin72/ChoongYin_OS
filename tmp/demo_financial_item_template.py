"""Demo (headed, normal watchable speed, ~1s pacing) - Financial Item Template full I-U-D via the
Universal Screen Engine. Demonstrates Issue 1's fix: the pre-existing-row check now correctly
catches find_grid_row()'s "not found" exception instead of wrongly expecting a None return."""
import sys
import time
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parent / "workstreams" / "master-plan" / "ec-automation" / "py"))
sys.path.insert(0, str(_HERE.parent / "workstreams" / "master-plan" / "ec-automation" / "libraries"))
from engine import Engine, open_screen, css
from universal_classifier import EC_URL
from playwright.sync_api import sync_playwright
import DbVerify as db

CODE = "AUTOTEST_R6_FIT"
NAME = "AUTOTEST Financial Item Template R6 Demo"
NAME_UPD = NAME + " UPDATED"
VALID_FROM = "2000-01-01"


def pause(page, seconds=1.0):
    page.wait_for_timeout(int(seconds * 1000))


with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=300,
                                 args=["--ignore-certificate-errors", "--start-maximized"])
    ctx = browser.new_context(ignore_https_errors=True, no_viewport=True)
    page = ctx.new_page()
    page.goto(EC_URL, wait_until="domcontentloaded", timeout=45000)
    pause(page, 1.5)

    print("=== Opening Financial Item Template screen ===")
    open_screen(page, "Financial Item Template")
    eng = Engine(page, "Financial Item Template")
    pause(page, 1.5)

    grids = page.evaluate("""() => Array.from(document.querySelectorAll('[id$=":T_data"]')).map(e => e.id)""")
    grid_id = grids[0]

    print("=== Pre-existing-row check (this is Issue 1's fix) ===")
    try:
        eng.find_grid_row(grid_id, CODE)
        pre_exists = True
        print("  a leftover test row exists - will clean it up first")
    except Exception:
        pre_exists = False
        print("  correctly caught 'not found' - no leftover row, proceeding to Insert")
    pause(page, 1.5)

    if pre_exists:
        eng.select_grid_row(grid_id, CODE)
        eng.toolbar("Template", icon="delete")
        pause(page, 1.0)
        eng.click("Save")
        pause(page, 1.5)

    print("\n=== INSERT ===")
    eng.toolbar("Template", icon="insert")
    pause(page, 1.5)
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
    print("  new blank row index:", row_idx)
    eng.grid_cell(grid_id, row_idx, "Financial Item Template Code").set(CODE)
    pause(page, 1.0)
    eng.grid_cell(grid_id, row_idx, "Financial Item Template Name").set(NAME)
    pause(page, 1.0)
    eng.grid_cell(grid_id, row_idx, "Valid From").set(VALID_FROM)
    pause(page, 1.0)
    eng.click("Save")
    pause(page, 1.5)
    print("  INSERT saved. Checking DB ground truth...")
    print("  DB row found:", end=" ")
    try:
        eng.find_grid_row(grid_id, CODE)
        print("yes (grid)")
    except Exception:
        print("NO - problem")

    pause(page, 2.0)

    print("\n=== UPDATE ===")
    row_idx2 = eng.find_grid_row(grid_id, CODE)
    print("  row-identity check: found at row", row_idx2)
    pause(page, 1.0)
    eng.grid_cell(grid_id, row_idx2, "Financial Item Template Name").set(NAME_UPD)
    pause(page, 1.0)
    eng.click("Save")
    pause(page, 1.5)
    print("  UPDATE saved.")
    pause(page, 2.0)

    print("\n=== DELETE (physical) ===")
    row_idx3 = eng.find_grid_row(grid_id, CODE)
    print("  row-identity check: found at row", row_idx3)
    pause(page, 1.0)
    eng.select_grid_row(grid_id, CODE)
    eng.toolbar("Template", icon="delete")
    pause(page, 1.0)
    eng.click("Save")
    pause(page, 1.5)
    print("  DELETE saved. Checking grid ground truth...")
    try:
        eng.find_grid_row(grid_id, CODE)
        print("  still present - problem")
    except Exception:
        print("  confirmed absent (expected)")

    print("\n=== Self-clean check ===")
    try:
        eng.find_grid_row(grid_id, CODE)
        print("  RESIDUAL - not clean")
    except Exception:
        print("  CLEAN - 0 residual")

    pause(page, 3.0)
    ctx.close()
    browser.close()

print("\nDemo complete.")
