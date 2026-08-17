"""Demo (headed, normal watchable speed, ~1s pacing) - directly test the suspect sequence:
CLOSE an existing Reservoir Block/Formation (End Date = Start Date, per EC's date-effective
delete convention) then immediately RECREATE at the SAME Start Date - exactly what every failing
harness run's pre-clean step does - then check the Reservoir Block Formation dropdown right after.
This isolates whether close-then-recreate-at-same-date is the real trigger, as opposed to a plain
fresh-create (which worked cleanly in the prior walkthrough)."""
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
BLK_CODE, BLK_NAME = "AUTOTEST_R6_RBFB", "AUTOTEST R6 RBF Block"
FRM_CODE, FRM_NAME = "AUTOTEST_R6_RBFF", "AUTOTEST R6 RBF Formation"


def pause(page, seconds=1.0):
    page.wait_for_timeout(int(seconds * 1000))


with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=300,
                                 args=["--ignore-certificate-errors", "--start-maximized"])
    ctx = browser.new_context(ignore_https_errors=True, no_viewport=True)
    page = ctx.new_page()
    page.goto(EC_URL, wait_until="domcontentloaded", timeout=45000)
    pause(page, 1.5)

    print("=" * 70)
    print("STEP 1: CLOSE the existing Reservoir Block (End Date = Start Date = 2000-01-01)")
    print("=" * 70)
    open_screen(page, "Reservoir Block")
    eng_b = Engine(page, "Reservoir Block")
    pause(page, 1.5)
    grids_b = page.evaluate("""() => Array.from(document.querySelectorAll('[id$=":T_data"]')).map(e => e.id)""")
    grid_b = grids_b[0]
    found_b = eng_b.select_row(grid_b, BLK_CODE)
    print("  found existing row:", found_b)
    pause(page, 1.0)
    eng_b.fill("End Date", SD)
    pause(page, 1.0)
    eng_b.click("Save")
    pause(page, 1.5)
    print("  Closed. DB check (should be absent from ov_resv_block now):",
          db.code_present("ov_resv_block", BLK_CODE))
    pause(page, 2.0)

    print("\n" + "=" * 70)
    print("STEP 2: RECREATE the Reservoir Block at the SAME Start Date 2000-01-01")
    print("=" * 70)
    eng_b.toolbar("New Object")
    pause(page, 1.5)
    eng_b.fill("Reservoir Block Code", BLK_CODE)
    pause(page, 1.0)
    eng_b.fill("Reservoir Block Name", BLK_NAME)
    pause(page, 1.0)
    eng_b.fill("Start Date", SD)
    pause(page, 1.0)
    eng_b.click("Save")
    pause(page, 1.5)
    print("  Recreated. DB check:", db.code_present("ov_resv_block", BLK_CODE))
    pause(page, 2.0)

    print("\n" + "=" * 70)
    print("STEP 3: CLOSE the existing Reservoir Formation (End Date = Start Date = 2000-01-01)")
    print("=" * 70)
    open_screen(page, "Reservoir Formation")
    eng_f = Engine(page, "Reservoir Formation")
    pause(page, 1.5)
    grids_f = page.evaluate("""() => Array.from(document.querySelectorAll('[id$=":T_data"]')).map(e => e.id)""")
    grid_f = grids_f[0]
    found_f = eng_f.select_row(grid_f, FRM_CODE)
    print("  found existing row:", found_f)
    pause(page, 1.0)
    eng_f.fill("End Date", SD)
    pause(page, 1.0)
    eng_f.click("Save")
    pause(page, 1.5)
    print("  Closed. DB check (should be absent from ov_resv_formation now):",
          db.code_present("ov_resv_formation", FRM_CODE))
    pause(page, 2.0)

    print("\n" + "=" * 70)
    print("STEP 4: RECREATE the Reservoir Formation at the SAME Start Date 2000-01-01")
    print("=" * 70)
    eng_f.toolbar("New Object")
    pause(page, 1.5)
    eng_f.fill("Reservoir Formation Code", FRM_CODE)
    pause(page, 1.0)
    eng_f.fill("Reservoir Formation Name", FRM_NAME)
    pause(page, 1.0)
    eng_f.fill("Start Date", SD)
    pause(page, 1.0)
    eng_f.click("Save")
    pause(page, 1.5)
    print("  Recreated. DB check:", db.code_present("ov_resv_formation", FRM_CODE))
    pause(page, 2.0)

    print("\n" + "=" * 70)
    print("STEP 5: Open Reservoir Block Formation, check the dependent dropdown NOW")
    print("=" * 70)
    open_screen(page, "Reservoir Block Formation")
    eng_r = Engine(page, "Reservoir Block Formation")
    pause(page, 1.5)
    eng_r.toolbar("New Object")
    pause(page, 1.5)
    eng_r.fill("Resv Block Formation Code", "AUTOTEST_R6_RBF")
    pause(page, 1.0)
    eng_r.fill("Resv Block Formation Name", "AUTOTEST R6 RBF")
    pause(page, 1.0)
    eng_r.fill("Start Date", SD)
    pause(page, 1.0)

    print("\n>>> Checking the 'Reservoir Block' dropdown <<<")
    f = eng_r._field("Reservoir Block")
    base = f["id"][: -len("_input")] if f["id"].endswith("_input") else f["id"]
    page.locator(css(base + "_button")).first.click()
    pause(page, 2.0)
    opts = page.evaluate(
        """(panelId) => { const p = document.getElementById(panelId); if (!p) return null;
            return Array.from(p.querySelectorAll('tr[data-item-label]')).map(tr => tr.getAttribute('data-item-label')); }""",
        base + "_panel",
    )
    print(f"  Dropdown shows {len(opts) if opts else 0} total options.")
    matching = [o for o in (opts or []) if BLK_NAME in o]
    print(f"  Looking for {BLK_NAME!r} -> found: {matching if matching else 'NOT FOUND'}")
    page.screenshot(path=str(_HERE / "demo_rbf_close_recreate_result.png"))
    print("  Screenshot saved: tmp/demo_rbf_close_recreate_result.png")

    if matching:
        print("\nRESULT: option WAS found - close-then-recreate-at-same-date is NOT the trigger.")
    else:
        print("\nRESULT: option NOT found - close-then-recreate-at-same-date REPRODUCES the blocker.")

    pause(page, 5.0)
    ctx.close()
    browser.close()
