"""Full demo (headed, normal watchable speed, ~1s pacing) - Reservoir Block Formation end to end:
create both parent objects (Reservoir Block, Reservoir Formation), link them via Reservoir Block
Formation (Insert), Update the link's Name, Delete it, then tear down the parents in reverse
dependency order. DB-verified at every step. This is the corrected version - Reservoir Formation
is now selected by its CODE (its dropdown's real key), not its Name."""
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

SD = "2000-01-01"
BLK_CODE, BLK_NAME = "AUTOTEST_R6_RBFB", "AUTOTEST R6 RBF Block"
FRM_CODE, FRM_NAME = "AUTOTEST_R6_RBFF", "AUTOTEST R6 RBF Formation"
RBF_CODE, RBF_NAME = "AUTOTEST_R6_RBF", "AUTOTEST R6 RBF"


def pause(page, seconds=1.0):
    page.wait_for_timeout(int(seconds * 1000))


def verify_row_code(eng, page, code_label, expected_code):
    f = eng._field(code_label)
    actual = page.locator(css(f["id"])).first.input_value()
    print(f"  [row-identity check] form shows Code={actual!r} (expected {expected_code!r})")
    if actual != expected_code:
        raise RuntimeError(f"ROW IDENTITY MISMATCH: expected {expected_code!r}, got {actual!r} - ABORTING")


with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=300,
                                 args=["--ignore-certificate-errors", "--start-maximized"])
    ctx = browser.new_context(ignore_https_errors=True, no_viewport=True)
    page = ctx.new_page()
    page.goto(EC_URL, wait_until="domcontentloaded", timeout=45000)
    pause(page, 1.5)

    print("=" * 70)
    print("PART 1: Create Reservoir Block (parent 1)")
    print("=" * 70)
    open_screen(page, "Reservoir Block")
    eng_b = Engine(page, "Reservoir Block")
    pause(page, 1.5)
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
    print("  DB check:", db.code_present("ov_resv_block", BLK_CODE))
    pause(page, 2.0)

    print("\n" + "=" * 70)
    print("PART 2: Create Reservoir Formation (parent 2)")
    print("=" * 70)
    open_screen(page, "Reservoir Formation")
    eng_f = Engine(page, "Reservoir Formation")
    pause(page, 1.5)
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
    print("  DB check:", db.code_present("ov_resv_formation", FRM_CODE))
    pause(page, 2.0)

    print("\n" + "=" * 70)
    print("PART 3: Reservoir Block Formation - INSERT (link the two)")
    print("=" * 70)
    open_screen(page, "Reservoir Block Formation")
    eng_r = Engine(page, "Reservoir Block Formation")
    pause(page, 1.5)
    grids = page.evaluate("""() => Array.from(document.querySelectorAll('[id$=":T_data"]')).map(e => e.id)""")
    rbf_grid = grids[0]

    eng_r.toolbar("New Object")
    pause(page, 1.5)
    eng_r.fill("Resv Block Formation Code", RBF_CODE)
    pause(page, 1.0)
    eng_r.fill("Resv Block Formation Name", RBF_NAME)
    pause(page, 1.0)
    eng_r.fill("Start Date", SD)
    pause(page, 1.0)
    print("  Selecting Reservoir Block by Name (this field's dropdown keys by Name)...")
    eng_r.select("Reservoir Block", BLK_NAME)
    pause(page, 1.5)
    print("  Selecting Reservoir Formation by CODE (this field's dropdown keys by Code, not Name)...")
    eng_r.select("Reservoir Formation", FRM_CODE)
    pause(page, 1.5)
    eng_r.click("Save")
    pause(page, 1.5)
    print("  DB check: RBF present =", db.code_present("ov_resv_block_formation", RBF_CODE))
    ok, act = db.field_equals("ov_resv_block_formation", RBF_CODE, "NAME", RBF_NAME)
    print("  DB NAME check:", ok, act)
    pause(page, 2.0)

    print("\n" + "=" * 70)
    print("PART 4: Reservoir Block Formation - UPDATE")
    print("=" * 70)
    eng_r.select_row(rbf_grid, RBF_CODE)
    pause(page, 1.0)
    verify_row_code(eng_r, page, "Resv Block Formation Code", RBF_CODE)
    pause(page, 1.0)
    eng_r.fill("Resv Block Formation Name", RBF_NAME + " UPDATED")
    pause(page, 1.0)
    eng_r.click("Save")
    pause(page, 1.5)
    ok2, act2 = db.field_equals("ov_resv_block_formation", RBF_CODE, "NAME", RBF_NAME + " UPDATED")
    print("  DB NAME check after update:", ok2, act2)
    pause(page, 2.0)

    print("\n" + "=" * 70)
    print("PART 5: Reservoir Block Formation - DELETE (End = Start)")
    print("=" * 70)
    eng_r.select_row(rbf_grid, RBF_CODE)
    pause(page, 1.0)
    verify_row_code(eng_r, page, "Resv Block Formation Code", RBF_CODE)
    pause(page, 1.0)
    eng_r.fill("End Date", SD)
    pause(page, 1.0)
    eng_r.click("Save")
    pause(page, 1.5)
    print("  DB check: RBF present =", db.code_present("ov_resv_block_formation", RBF_CODE), "(expect False)")
    pause(page, 2.0)

    print("\n" + "=" * 70)
    print("PART 6: Teardown parents (reverse dependency order)")
    print("=" * 70)
    open_screen(page, "Reservoir Formation")
    eng_f2 = Engine(page, "Reservoir Formation")
    pause(page, 1.0)
    grids_f = page.evaluate("""() => Array.from(document.querySelectorAll('[id$=":T_data"]')).map(e => e.id)""")
    if eng_f2.select_row(grids_f[0], FRM_CODE):
        verify_row_code(eng_f2, page, "Reservoir Formation Code", FRM_CODE)
        eng_f2.fill("End Date", SD)
        eng_f2.click("Save")
    pause(page, 1.5)
    print("  Formation still present:", db.code_present("ov_resv_formation", FRM_CODE))

    open_screen(page, "Reservoir Block")
    eng_b2 = Engine(page, "Reservoir Block")
    pause(page, 1.0)
    grids_b = page.evaluate("""() => Array.from(document.querySelectorAll('[id$=":T_data"]')).map(e => e.id)""")
    if eng_b2.select_row(grids_b[0], BLK_CODE):
        verify_row_code(eng_b2, page, "Reservoir Block Code", BLK_CODE)
        eng_b2.fill("End Date", SD)
        eng_b2.click("Save")
    pause(page, 1.5)
    print("  Block still present:", db.code_present("ov_resv_block", BLK_CODE))

    print("\n" + "=" * 70)
    print("SELF-CLEAN CHECK")
    print("=" * 70)
    residual = (db.count_like("ov_resv_block_formation", "AUTOTEST")
                + db.count_like("ov_resv_formation", "AUTOTEST")
                + db.count_like("ov_resv_block", "AUTOTEST"))
    print("  Total AUTOTEST residual rows:", residual)

    pause(page, 3.0)
    ctx.close()
    browser.close()

print("\nFull demo complete.")
