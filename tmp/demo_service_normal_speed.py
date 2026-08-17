"""Demo (headed, normal human-watchable speed, ~1s pacing) - Service EC screen full I-U-D via the
Universal Screen Engine, using the fixed apply_navigator() (levels now defaults to len(values),
so this single call correctly touches only nav column 1 - "TS3 BU1" - matching the real driver."""
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

CODE = "AUTOTEST_R5_SV"
NAME = "AUTOTEST Service R5 Demo"
NAME_UPD = NAME + " UPDATED"
START_DATE = "2011-01-01"
VIEW = "ov_service"
CODE_LABEL = "Service Code"


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

    print("=== Opening Service screen ===")
    open_screen(page, "Service")
    eng = Engine(page, "Service")
    pause(page, 1.5)

    print("=== Applying navigator: TS3 BU1 (fixed apply_navigator, levels=len(values)=1) ===")
    top = eng.apply_navigator(values=["TS3 BU1"])
    print("  top-parent selected:", top)
    pause(page, 1.5)

    grids = page.evaluate("""() => Array.from(document.querySelectorAll('[id$=":T_data"]')).map(e => e.id)""")
    grid_id = grids[0]
    row_count = page.evaluate(
        "(gid) => document.getElementById(gid) ? document.getElementById(gid).querySelectorAll('tr[data-ri]').length : 0",
        grid_id,
    )
    print(f"  grid now shows {row_count} rows under TS3 BU1 scope")
    pause(page, 1.5)

    if eng.select_row(grid_id, CODE):
        print("  pre-existing test row found - cleaning it up first")
        verify_row_code(eng, page, CODE_LABEL, CODE)
        eng.fill("End Date", START_DATE)
        eng.click("Save")
        eng.apply_navigator(values=["TS3 BU1"])
        pause(page, 1.5)

    print("\n=== INSERT ===")
    eng.toolbar("New Object")
    pause(page, 1.5)
    eng.fill("Service Code", CODE)
    pause(page, 1.0)
    eng.fill("Service Name", NAME)
    pause(page, 1.0)
    eng.fill("Start Date", START_DATE)
    pause(page, 1.0)
    eng.select("Service Template", "__FIRST__")
    pause(page, 1.0)
    eng.select("Service Type", "__FIRST__")
    pause(page, 1.0)
    eng.select("Service Status", "__FIRST__")
    pause(page, 1.0)
    eng.select("Contract", "TS3 GTA Shipper A")
    pause(page, 1.0)
    eng.select("Transport System", "TS3 Transport System")
    pause(page, 1.0)
    eng.click("Save")
    pause(page, 1.5)
    print("  INSERT saved. Checking DB ground truth...")
    print("  DB code_present:", db.code_present(VIEW, CODE))
    ok, act = db.field_equals(VIEW, CODE, "NAME", NAME)
    print(f"  DB NAME check: {ok} (actual={act!r})")
    pause(page, 2.0)

    print("\n=== UPDATE ===")
    eng.select_row(grid_id, CODE)
    pause(page, 1.0)
    verify_row_code(eng, page, CODE_LABEL, CODE)
    pause(page, 1.0)
    eng.fill("Service Name", NAME_UPD)
    pause(page, 1.0)
    eng.click("Save")
    pause(page, 1.5)
    print("  UPDATE saved. Checking DB ground truth...")
    ok, act = db.field_equals(VIEW, CODE, "NAME", NAME_UPD)
    print(f"  DB NAME check: {ok} (actual={act!r})")
    pause(page, 2.0)

    print("\n=== DELETE (End Date = Start Date) ===")
    eng.select_row(grid_id, CODE)
    pause(page, 1.0)
    verify_row_code(eng, page, CODE_LABEL, CODE)
    pause(page, 1.0)
    eng.fill("End Date", START_DATE)
    pause(page, 1.0)
    eng.click("Save")
    pause(page, 1.5)
    print("  DELETE saved. Checking DB ground truth...")
    present = db.code_present(VIEW, CODE)
    for _ in range(4):
        if not present:
            break
        time.sleep(1.5)
        present = db.code_present(VIEW, CODE)
    print("  DB code_present after delete:", present, "(expect False)")

    print("\n=== Self-clean check ===")
    residual = db.count_like(VIEW, "AUTOTEST")
    print(f"  AUTOTEST residual count in {VIEW}: {residual}")

    pause(page, 3.0)
    ctx.close()
    browser.close()

print("\nDemo complete.")
