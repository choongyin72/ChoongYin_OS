"""Investigate: round-5 batch reported Service's Update as PASS, but DB shows NAME never changed
to the _UPD value. Row-identity guard did NOT fire at the update step (meaning select_row DID find
the right row then). Reproduce live, headed, checking DB immediately after each sub-step to pinpoint
exactly where the update is lost - no guessing."""
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
VIEW = "ov_service"

with sync_playwright() as p:
    b = p.chromium.launch(headless=False, slow_mo=200, args=["--ignore-certificate-errors", "--start-maximized"])
    page = b.new_context(ignore_https_errors=True, no_viewport=True).new_page()
    page.goto(EC_URL, wait_until="domcontentloaded", timeout=45000)

    open_screen(page, "Service")
    eng = Engine(page, "Service")
    eng.apply_navigator(values=["TS3 BU1"])

    grids = page.evaluate("""() => Array.from(document.querySelectorAll('[id$=":T_data"]')).map(e => e.id)""")
    grid_id = grids[0]
    print("grid_id:", grid_id)

    print("row in DB before:", db.code_present(VIEW, CODE))
    ok, name = db.field_equals(VIEW, CODE, "NAME", CODE.replace("AUTOTEST", "AUTOTEST Service").replace("_", " "))
    print("current NAME field_equals check (informational):", ok, name)

    found = eng.select_row(grid_id, CODE)
    print("select_row found:", found)
    if found:
        f = eng._field("Service Code")
        actual_code = page.locator(css(f["id"])).first.input_value()
        print("form Code field shows:", actual_code)
        f2 = eng._field("Service Name")
        actual_name_before = page.locator(css(f2["id"])).first.input_value()
        print("form Name field BEFORE fill:", actual_name_before)

        NEW_NAME = CODE + "_UPD_INVESTIGATE"
        eng.fill("Service Name", NEW_NAME)
        actual_name_after_fill = page.locator(css(f2["id"])).first.input_value()
        print("form Name field AFTER fill (before Save):", actual_name_after_fill)

        page.screenshot(path=str(_HERE / "investigate_service_before_save.png"))

        eng.click("Save")
        print("Save clicked, GO re-queried")

        time.sleep(1.0)
        ok2, name2 = db.field_equals(VIEW, CODE, "NAME", NEW_NAME)
        print("DB NAME immediately after Save:", ok2, name2)

        time.sleep(3.0)
        ok3, name3 = db.field_equals(VIEW, CODE, "NAME", NEW_NAME)
        print("DB NAME 3s after Save:", ok3, name3)

    page.wait_for_timeout(3000)
    b.close()
