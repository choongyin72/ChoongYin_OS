"""Recon: reproduce insert EXACTLY as Insert Object From Properties would (Chemical Tank Code,
Chemical Tank Name, Start Date, Measure unit, Op Production Unit) including the change/blur
event dispatch after text/date fields (Fill EC Field / Fill EC Date's real behavior), to find
whether the TC02 live timeout is a genuine race tied to filling Start Date right before the
dropdowns, or something else. Read-only except opening + filling the New Object form (no Save).
Run: py tmp/recon_ct_insert_exact_properties_order.py
"""
import os
import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parent / "workstreams" / "master-plan" / "ec-automation" / "py"))
import ec_object_iud as ec  # noqa: E402


def label_id(page, form, label, kind_hint=None):
    for suffix in ("in", "da_input", "dd_input", "pin"):
        loc = page.locator(
            "xpath=//span[contains(@class,'ECCell') and contains(@id,':%s:form:') and "
            "normalize-space(text())='%s']/ancestor::div[contains(@class,'tableCell')][1]"
            "/following-sibling::div[contains(@class,'tableCell')][1]//input[contains(@id,'%s')]"
            % (form, label, suffix)
        ).first
        if loc.count():
            return loc.get_attribute("id")
    return None


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

        # Code (text)
        code_id = label_id(page, "objectForm", "Chemical Tank Code")
        print("[Code id]", code_id)
        page.fill("css=[id=\"%s\"]" % code_id, "AUTOTEST_CT")
        page.evaluate("(id) => { const e=document.getElementById(id); if(e){e.dispatchEvent(new Event('change',{bubbles:true}));e.dispatchEvent(new Event('blur',{bubbles:true}));} }", code_id)
        page.wait_for_timeout(400)

        # Name (text)
        name_id = label_id(page, "objectForm", "Chemical Tank Name")
        print("[Name id]", name_id)
        page.fill("css=[id=\"%s\"]" % name_id, "Automation Test Chemical Tank")
        page.evaluate("(id) => { const e=document.getElementById(id); if(e){e.dispatchEvent(new Event('change',{bubbles:true}));e.dispatchEvent(new Event('blur',{bubbles:true}));} }", name_id)
        page.wait_for_timeout(400)

        # Start Date (date) - Tab-out triggers PrimeFaces validation, per Fill EC Date
        date_id = label_id(page, "objectForm", "Start Date")
        print("[Start Date id]", date_id)
        page.fill("css=[id=\"%s\"]" % date_id, "2000-01-01")
        page.keyboard.press("Tab")
        page.wait_for_timeout(600)
        page.evaluate("(id) => { const e=document.getElementById(id); if(e){e.dispatchEvent(new Event('change',{bubbles:true}));e.dispatchEvent(new Event('blur',{bubbles:true}));} }", date_id)
        page.wait_for_timeout(400)
        print("[Start Date] filled + blurred")

        # Measure unit (dropdown, first-available)
        mu_id = label_id(page, "objectForm", "Measure unit")
        print("[Measure unit dd id]", mu_id)
        mu_dd = mu_id.rsplit("_input", 1)[0]
        t0 = time.time()
        page.click("css=[id=\"%s_button\"]" % mu_dd)
        try:
            page.locator("xpath=//*[@id='%s_panel']//tr" % mu_dd).first.wait_for(state="visible", timeout=6000)
        except Exception as e:
            print("[Measure unit] panel open FAILED", repr(e)[:200])
        mu_first = page.locator("xpath=//*[@id='%s_panel']//tr" % mu_dd).first
        mu_label = mu_first.get_attribute("data-item-label")
        print("[Measure unit PICK]", mu_label, "elapsed=%.2fs" % (time.time() - t0))
        mu_first.click()
        page.wait_for_load_state("networkidle", timeout=12000)
        page.wait_for_timeout(600)

        # Op Production Unit (dropdown, specific value) - exactly what the robot run does next
        opu_id = label_id(page, "objectForm", "Op Production Unit")
        print("[Op Production Unit dd id]", opu_id)
        opu_dd = opu_id.rsplit("_input", 1)[0]
        t1 = time.time()
        page.click("css=[id=\"%s_button\"]" % opu_dd)
        try:
            page.locator(
                "xpath=//*[@id='%s_panel']//tr[normalize-space(@data-item-label)='AS1 EC Exploration Norway']" % opu_dd
            ).first.wait_for(state="visible", timeout=6000)
            print("[Op Production Unit] found target option, elapsed=%.2fs" % (time.time() - t1))
        except Exception as e:
            print("[Op Production Unit] FIRST ATTEMPT FAILED", repr(e)[:250], "elapsed=%.2fs" % (time.time() - t1))
            page.keyboard.press("Escape")
            page.wait_for_timeout(1500)
            t2 = time.time()
            page.click("css=[id=\"%s_button\"]" % opu_dd)
            try:
                page.locator(
                    "xpath=//*[@id='%s_panel']//tr[normalize-space(@data-item-label)='AS1 EC Exploration Norway']" % opu_dd
                ).first.wait_for(state="visible", timeout=10000)
                print("[Op Production Unit] RETRY found target option, elapsed=%.2fs" % (time.time() - t2))
            except Exception as e2:
                print("[Op Production Unit] RETRY ALSO FAILED", repr(e2)[:250])
                opts_now = page.locator("xpath=//*[@id='%s_panel']//tr" % opu_dd).all_inner_texts()
                print("[Op Production Unit] whatever options DID render:", opts_now)

    finally:
        ctx.close()
        browser.close()
