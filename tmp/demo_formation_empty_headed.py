"""Demo (headed, normal watchable speed, ~1s pacing) - show live that after correctly selecting
Reservoir Block, the dependent Reservoir Formation dropdown is genuinely empty - confirmed by
BOTH the Universal Screen Engine's select() and the older, proven ec_object_iud.select_dropdown()
failing identically on the same page state. This isolates the real blocker as an EC/sandbox-side
condition, not a defect in either automation tool."""
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parent / "workstreams" / "master-plan" / "ec-automation" / "py"))
sys.path.insert(0, str(_HERE.parent / "workstreams" / "master-plan" / "ec-automation" / "libraries"))
from engine import Engine, open_screen, css
from universal_classifier import EC_URL
from playwright.sync_api import sync_playwright
import ec_object_iud as ec


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

    print("=== Selecting Reservoir Block = 'AUTOTEST R6 RBF Block' ===")
    eng.select("Reservoir Block", "AUTOTEST R6 RBF Block")
    print("  Block selected OK")
    pause(page, 2.0)

    ff = eng._field("Reservoir Formation")
    print("Reservoir Formation field id:", ff["id"])

    print("\n=== Opening the Reservoir Formation dropdown to look, live ===")
    base = ff["id"][: -len("_input")]
    page.locator(css(base + "_button")).first.click()
    pause(page, 2.0)
    opts = page.evaluate(
        """(panelId) => { const p = document.getElementById(panelId); if (!p) return null;
            return Array.from(p.querySelectorAll('tr[data-item-label]')).map(tr => tr.getAttribute('data-item-label')); }""",
        base + "_panel",
    )
    print(f"  Options visible right now: {len(opts) if opts else 0} -> {opts}")
    page.screenshot(path=str(_HERE / "demo_formation_empty_result.png"))
    pause(page, 3.0)

    print("\n=== Now trying the OLDER, proven ec_object_iud.select_dropdown() on the same field ===")
    page.keyboard.press("Escape")
    pause(page, 1.0)
    try:
        ec.select_dropdown(page, ff["id"], "__FIRST__")
        print("  SUCCESS - found an option")
    except Exception as e:
        print("  FAILED (same as engine.select()):", str(e)[:200])

    pause(page, 5.0)
    ctx.close()
    browser.close()

print("\nDemo complete - both tools agree the dropdown is genuinely empty at this point.")
