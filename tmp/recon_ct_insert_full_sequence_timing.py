"""Recon: reproduce the EXACT insert-form field order the properties-driven Insert Object From
Properties uses (Chemical Tank Code, Chemical Tank Name, Start Date, Measure unit, Op Production
Unit) and find out WHY the live robot run's TC02 timed out waiting for the Op Production Unit
panel option after Measure unit was filled - timing race from a form re-render, or a genuinely
different dd id/row after Measure unit's selection. Read-only except opening + filling the New
Object form (no Save).
Run: py tmp/recon_ct_insert_full_sequence_timing.py
"""
import os
import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parent / "workstreams" / "master-plan" / "ec-automation" / "py"))
import ec_object_iud as ec  # noqa: E402

URL = os.environ.get("EC_URL", "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/")
USER = os.environ.get("EC_USERNAME", os.environ.get("EC_USER", "sysadmin"))
PW = os.environ.get("EC_PASSWORD", os.environ.get("EC_PASS", "sysadmin"))
HEADED = os.environ.get("EC_HEADED", "0") == "1"


def op_label_id(page, form, label):
    loc = page.locator(
        "xpath=//span[contains(@class,'ECCell') and contains(@id,':%s:form:') and "
        "normalize-space(text())='%s']/ancestor::div[contains(@class,'tableCell')][1]"
        "/following-sibling::div[contains(@class,'tableCell')][1]//input[contains(@id,'dd_input')]"
        % (form, label)
    ).first
    return loc.get_attribute("id")


with sync_playwright() as p:
    browser = p.chromium.launch(headless=not HEADED,
                                 args=["--ignore-certificate-errors", "--start-maximized"])
    ctx = browser.new_context(ignore_https_errors=True, no_viewport=HEADED,
                               viewport=None if HEADED else {"width": 1920, "height": 1080})
    page = ctx.new_page()
    try:
        ec.login(page, URL, USER, PW)
        ec.open_object_screen(page, "Chemical Tank")

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
        print("[NAV] applied")

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
        print("[FORM] opened")

        # Chemical Tank Code / Name / Start Date via plain fill (text/date), skip - not relevant
        # to the dropdown race. Go straight to Measure unit then Op Production Unit, exactly the
        # properties file's order, WITH live timing/state prints at each step.
        mu_id = op_label_id(page, "objectForm", "Measure unit")
        print("[Measure unit dd id]", mu_id)
        mu_dd = mu_id.rsplit("_input", 1)[0]
        page.click("css=[id=\"%s_button\"]" % mu_dd)
        page.wait_for_timeout(800)
        mu_first = page.locator("xpath=//*[@id='%s_panel']//tr" % mu_dd).first
        mu_label = mu_first.get_attribute("data-item-label")
        print("[Measure unit PICK]", mu_label)
        mu_first.click()
        t0 = time.time()
        page.wait_for_load_state("networkidle", timeout=12000)
        print("[Measure unit] networkidle after %.2fs" % (time.time() - t0))
        page.wait_for_timeout(600)

        # NOW immediately try Op Production Unit, mirroring the properties-driven fill's lack of
        # extra buffer between fields
        opu_id = op_label_id(page, "objectForm", "Op Production Unit")
        print("[Op Production Unit dd id AFTER Measure unit pick]", opu_id)
        opu_dd = opu_id.rsplit("_input", 1)[0]
        t1 = time.time()
        try:
            page.click("css=[id=\"%s_button\"]" % opu_dd, timeout=10000)
            page.wait_for_timeout(500)
            opts = page.locator("xpath=//*[@id='%s_panel']//tr" % opu_dd).all_inner_texts()
            print("[Op Production Unit OPTIONS immediately after]", opts, "elapsed=%.2fs" % (time.time() - t1))
        except Exception as e:
            print("[Op Production Unit OPEN FAILED immediately after]", repr(e)[:300], "elapsed=%.2fs" % (time.time() - t1))
            # retry after a longer settle
            page.wait_for_timeout(3000)
            opu_id_retry = op_label_id(page, "objectForm", "Op Production Unit")
            print("[Op Production Unit dd id on RETRY]", opu_id_retry, "(changed=%s)" % (opu_id_retry != opu_id))
            opu_dd_retry = opu_id_retry.rsplit("_input", 1)[0]
            page.click("css=[id=\"%s_button\"]" % opu_dd_retry)
            page.wait_for_timeout(800)
            opts_retry = page.locator("xpath=//*[@id='%s_panel']//tr" % opu_dd_retry).all_inner_texts()
            print("[Op Production Unit OPTIONS on RETRY]", opts_retry)

    finally:
        ctx.close()
        browser.close()
