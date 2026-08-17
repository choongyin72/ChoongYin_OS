"""Walkthrough (headed, normal watchable speed, ~1s pacing) - the 3 screens involved in
Reservoir Block Formation, stopping exactly at the blocker (the dependent dropdown not showing
the just-created Reservoir Block). No further hypothesis-testing beyond this - just a clean,
observable reproduction of Issue 2 as it currently stands."""
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
    print("SCREEN 1 of 3: Reservoir Block - creating the first parent object")
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
    print(f"  Saved. DB check: {BLK_CODE} present =", db.code_present("ov_resv_block", BLK_CODE))
    pause(page, 2.0)

    print("\n" + "=" * 70)
    print("SCREEN 2 of 3: Reservoir Formation - creating the second parent object")
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
    print(f"  Saved. DB check: {FRM_CODE} present =", db.code_present("ov_resv_formation", FRM_CODE))
    pause(page, 2.0)

    print("\n" + "=" * 70)
    print("SCREEN 3 of 3: Reservoir Block Formation - linking the two via New Object")
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

    print("\n>>> BLOCKER: opening the 'Reservoir Block' dropdown to pick the Block we just made <<<")
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
    page.screenshot(path=str(_HERE / "walkthrough_rbf_blocker.png"))
    print("  Screenshot saved: tmp/walkthrough_rbf_blocker.png")
    print("\nStopping here - this is the blocker. Not proceeding further.")

    pause(page, 5.0)
    ctx.close()
    browser.close()
