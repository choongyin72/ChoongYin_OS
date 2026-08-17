"""Clean up ALL leftover residual rows from the round-5 Remote Endpoint Configuration attempts
(timestamp-based codes from runs that failed mid-Save before the ec.save() fix). Code-verified
before each delete (row-identity rule)."""
import sys
import time
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parent / "workstreams" / "master-plan" / "ec-automation" / "py"))
sys.path.insert(0, str(_HERE.parent / "workstreams" / "master-plan" / "ec-automation" / "libraries"))
import ec_object_iud as ec
from universal_classifier import EC_URL
from playwright.sync_api import sync_playwright
import DbVerify as db

VIEW = "OV_ENDPOINT_CONFIG"
conn = db._connect()
cur = conn.cursor()
cur.execute("SELECT CODE FROM OV_ENDPOINT_CONFIG WHERE CODE LIKE 'autotest-r5-%'")
CODES = [r[0] for r in cur.fetchall()]
conn.close()
print("residual codes to clean:", CODES)


def _row_by_code(page, code):
    return page.evaluate(
        "(code) => { const m = document.querySelectorAll('input[id^=\"endpointconfig:form:T:\"][id$=\":C0_in\"]');"
        " for (const e of m) { if ((e.value||'') === code) { return parseInt(e.id.split(':')[3]); } }"
        " return -1; }",
        code,
    )


def _menu_item(page, icon_class):
    page.locator(
        f"xpath=//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'{icon_class}')]]"
    ).first.hover()
    return page.locator(
        f"xpath=//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'{icon_class}')]]"
        "//ul[contains(@class,'ui-menu-child')]//a"
    ).first


if not CODES:
    print("no residuals - nothing to clean up")
    sys.exit(0)

with sync_playwright() as p:
    b = p.chromium.launch(headless=True, args=["--ignore-certificate-errors"])
    page = b.new_context(ignore_https_errors=True, viewport={"width": 1920, "height": 1080}).new_page()
    page.goto(EC_URL, wait_until="domcontentloaded", timeout=45000)
    ec.login(page, EC_URL, "sysadmin", "sysadmin")

    for code in CODES:
        ec.open_object_screen(page, "Remote Endpoint Configuration")
        row = _row_by_code(page, code)
        if row < 0:
            print(f"ROW IDENTITY: {code!r} not found in grid - skipping, not deleting anything")
            continue
        check_id = f"endpointconfig:form:T:{row}:C0_in"
        actual = page.locator(f'css=[id="{check_id}"]').first.input_value()
        if actual != code:
            print(f"ROW IDENTITY MISMATCH: expected {code!r}, got {actual!r} - skipping")
            continue

        page.locator(f'css=[id="{check_id}"]').click()
        page.wait_for_timeout(400)
        item = _menu_item(page, "ui-icon-delete")
        item.wait_for(state="visible", timeout=10000)
        item.click()
        page.wait_for_timeout(800)
        ec.save(page)
        page.wait_for_timeout(1200)

        err = ec.ec_error(page)
        if err:
            print(f"delete save error for {code}:", err)
            continue
        print(f"deleted {code}")

    b.close()

time.sleep(1.0)
still = db.count_like(VIEW, "autotest-r5-")
print("remaining residual count:", still)
