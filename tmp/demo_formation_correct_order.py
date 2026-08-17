"""Demo (headed, normal watchable speed, ~1s pacing) - redo the Reservoir Formation dropdown
check with the CORRECT field fill order this time: Code -> Name -> Start Date -> Reservoir Block
-> Reservoir Formation, exactly matching the real harness's own sequence (top-to-bottom form
order). Earlier tests skipped straight to selecting Reservoir Block without filling the preceding
fields first - not a faithful reproduction. This corrects that."""
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parent / "workstreams" / "master-plan" / "ec-automation" / "py"))
sys.path.insert(0, str(_HERE.parent / "workstreams" / "master-plan" / "ec-automation" / "libraries"))
from engine import Engine, open_screen, css
from universal_classifier import EC_URL
from playwright.sync_api import sync_playwright

SD = "2000-01-01"


def pause(page, seconds=1.0):
    page.wait_for_timeout(int(seconds * 1000))


with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=300,
                                 args=["--ignore-certificate-errors", "--start-maximized"])
    ctx = browser.new_context(ignore_https_errors=True, no_viewport=True)
    page = ctx.new_page()
    page.goto(EC_URL, wait_until="domcontentloaded", timeout=45000)
    pause(page, 1.5)

    print("=== Opening Reservoir Block Formation, New Object ===")
    open_screen(page, "Reservoir Block Formation")
    eng = Engine(page, "Reservoir Block Formation")
    pause(page, 1.5)
    eng.toolbar("New Object")
    pause(page, 1.5)

    print("=== Filling in the CORRECT sequence order ===")
    print("  1. Resv Block Formation Code")
    eng.fill("Resv Block Formation Code", "AUTOTEST_R6_RBF")
    pause(page, 1.0)
    print("  2. Resv Block Formation Name")
    eng.fill("Resv Block Formation Name", "AUTOTEST R6 RBF")
    pause(page, 1.0)
    print("  3. Start Date")
    eng.fill("Start Date", SD)
    pause(page, 1.0)
    print("  4. Reservoir Block = 'AUTOTEST R6 RBF Block'")
    eng.select("Reservoir Block", "AUTOTEST R6 RBF Block")
    pause(page, 2.0)

    print("\n=== NOW checking the Reservoir Formation dropdown (step 5) ===")
    ff = eng._field("Reservoir Formation")
    print("Reservoir Formation field id:", ff["id"])
    base = ff["id"][: -len("_input")]
    page.locator(css(base + "_button")).first.click()
    pause(page, 2.0)
    opts = page.evaluate(
        """(panelId) => { const p = document.getElementById(panelId); if (!p) return null;
            return Array.from(p.querySelectorAll('tr[data-item-label]')).map(tr => tr.getAttribute('data-item-label')); }""",
        base + "_panel",
    )
    print(f"  Options visible right now: {len(opts) if opts else 0} -> {opts}")
    page.screenshot(path=str(_HERE / "demo_formation_correct_order_result.png"))

    pause(page, 5.0)
    ctx.close()
    browser.close()

print("\nDemo complete.")
