"""Recon: what options does objectForm's "Op Production Unit" dropdown actually offer on the
Chemical Tank Insert form, after the navigator is set to AS1 EC Exploration Norway -> AS1_Area ->
AS1_Facility_01? The original page object's own docstring flagged: "the nav PU is not necessarily
a valid Op PU option - probe per screen." Read-only except opening the New Object form (no Save).
Run: py tmp/recon_ct_insert_op_pu_options.py
"""
import os
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parent / "workstreams" / "master-plan" / "ec-automation" / "py"))
import ec_object_iud as ec  # noqa: E402

URL = os.environ.get("EC_URL", "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/")
USER = os.environ.get("EC_USERNAME", os.environ.get("EC_USER", "sysadmin"))
PW = os.environ.get("EC_PASSWORD", os.environ.get("EC_PASS", "sysadmin"))
HEADED = os.environ.get("EC_HEADED", "0") == "1"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=not HEADED,
                                 args=["--ignore-certificate-errors", "--start-maximized"])
    ctx = browser.new_context(ignore_https_errors=True, no_viewport=HEADED,
                               viewport=None if HEADED else {"width": 1920, "height": 1080})
    page = ctx.new_page()
    try:
        ec.login(page, URL, USER, PW)
        label = ec.open_object_screen(page, "Chemical Tank")
        print("[SCREEN]", label)

        for i, val in [(1, "AS1 EC Exploration Norway"), (2, "AS1_Area"), (3, "AS1_Facility_01")]:
            dd = "nav:form:G:0:R:1:C:%d:dd" % i
            page.click("css=[id=\"%s_button\"]" % dd)
            page.wait_for_timeout(800)
            row = page.locator("xpath=//*[@id='%s_panel']//tr[normalize-space(@data-item-label)='%s']" % (dd, val)).first
            row.click()
            page.wait_for_load_state("networkidle", timeout=12000)
            page.wait_for_timeout(700)
        ec.click_go(page)
        page.wait_for_timeout(1500)
        print("[NAV] applied 3-level cascade + GO")

        # open insert form (hover-menu gesture - EC's Insert flyout opens on HOVER, not click;
        # see docs reference_ec_insert_menu_hover_gesture.md)
        li = page.locator(
            "xpath=//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'ui-icon-insert')]]"
        )
        li.first.hover()
        page.wait_for_timeout(900)
        page.locator(
            "xpath=//ul[contains(@class,'ui-menu-child')]//li//a[normalize-space(.)='New Object']"
        ).first.click()
        page.wait_for_load_state("networkidle", timeout=15000)
        page.wait_for_timeout(1200)

        # find the Op Production Unit dropdown by label scan (same xpath shape the shared keyword uses)
        dd_input = page.locator(
            "xpath=//span[contains(@class,'ECCell') and contains(@id,':objectForm:form:') and "
            "normalize-space(text())='Op Production Unit']/ancestor::div[contains(@class,'tableCell')][1]"
            "/following-sibling::div[contains(@class,'tableCell')][1]//input[contains(@id,'dd_input')]"
        ).first
        dd_id = dd_input.get_attribute("id")
        print("[Op Production Unit dd id]", dd_id)
        base_id = dd_id.rsplit("_input", 1)[0]
        page.click("css=[id=\"%s_button\"]" % base_id)
        page.wait_for_timeout(1000)
        opts = page.locator("xpath=//*[@id='%s_panel']//tr" % base_id).all_inner_texts()
        print("[Op Production Unit OPTIONS]", opts)

    finally:
        ctx.close()
        browser.close()
