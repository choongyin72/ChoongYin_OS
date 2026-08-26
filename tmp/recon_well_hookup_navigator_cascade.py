"""Recon (read-only): capture the EXACT live navigator cascade values that the already-proven
Well Hookup driver's first-available OV-GM navigator selects, so they can be captured as
EXPLICIT values in testdata/well_hookup_navigator.properties (Area-pattern conversion).
Does NOT insert/update/delete anything - navigator fill + GO only, then dump the 3 columns.
Run: py tmp/recon_well_hookup_navigator_cascade.py
"""
import os
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

_HERE = Path(__file__).resolve().parent
_EC = _HERE.parent / "workstreams" / "master-plan" / "ec-automation"
sys.path.insert(0, str(_EC / "py"))
sys.path.insert(0, str(_EC / "libraries"))
import ec_object_iud as ec

URL = os.environ.get("EC_URL", "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/")
USER = os.environ.get("EC_USERNAME", os.environ.get("EC_USER", "sysadmin"))
PW = os.environ.get("EC_PASSWORD", os.environ.get("EC_PASS", "sysadmin"))
SCREEN = "Well Hookup"


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--ignore-certificate-errors"])
        ctx = browser.new_context(ignore_https_errors=True, viewport={"width": 1920, "height": 1080})
        page = ctx.new_page()
        try:
            ec.login(page, URL, USER, PW)
            print("screen:", ec.open_object_screen(page, SCREEN))
            for col in range(1, 5):
                dd = "nav:form:G:0:R:1:C:%d:dd_input" % col
                n = page.locator('css=[id="%s"]' % dd).count()
                if n == 0:
                    print("C:%d -> ABSENT (cascade stops here)" % col)
                    break
                ec.select_dropdown(page, "nav:form:G:0:R:1:C:%d:dd" % col, "__FIRST__")
                page.wait_for_timeout(700)
                val = page.eval_on_selector('css=[id="%s"]' % dd, "e => e.value")
                print("C:%d -> %r" % (col, val))
            ec.click_go(page)
            page.wait_for_timeout(1000)
            page.screenshot(path=str(_HERE / "recon_well_hookup_nav_after_go.png"))
            print("GO clicked, screenshot saved")
        finally:
            ctx.close()
            browser.close()


if __name__ == "__main__":
    main()
