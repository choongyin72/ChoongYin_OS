"""Recon: Chemical Tank OV-GM navigator cascade addressing + real PU/Area/Facility Class 1
values + dependent-dropdown timing. Read-only (no Insert/Update/Delete/Save). Confirms the
3-level same-row cascade (nav:form:G:0:R:1:C:1/C:2/C:3) fits the shared T2 "Apply Navigator
From Properties" keyword, and captures the ACTUAL first-available resolved values at each
level (same discipline as tmp/recon_fc1_navigator_cascade.py's 2-level FC1 recon).

Run: py tmp/recon_ct_navigator_cascade.py
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

        cols = ["nav:form:G:0:R:1:C:%d:dd" % i for i in range(1, 5)]
        picked = []

        for i, dd in enumerate(cols, start=1):
            n = page.locator("css=[id=\"%s_input\"]" % dd).count()
            print("[SHAPE] C:%d present=%s" % (i, bool(n)))
            if not n:
                break
            page.click("css=[id=\"%s_button\"]" % dd)
            page.wait_for_timeout(1000)
            opts = page.locator("xpath=//*[@id='%s_panel']//tr" % dd).all_inner_texts()
            print("[C%d OPTIONS]" % i, opts)
            if not opts:
                print("[C%d] no options rendered - stop" % i)
                break
            first_row = page.locator("xpath=//*[@id='%s_panel']//tr" % dd).first
            pick_label = first_row.get_attribute("data-item-label")
            print("[C%d PICK]" % i, pick_label)
            picked.append(pick_label)
            first_row.click()
            page.wait_for_load_state("networkidle", timeout=12000)
            page.wait_for_timeout(700)

        print("[RESULT] picked cascade values (parent->child):", picked)

        # click GO to confirm the grid loads under this scope
        try:
            ec.click_go(page)
            page.wait_for_timeout(1500)
            print("[GO] clicked ok")
        except Exception as e:
            print("[GO] FAILED", repr(e)[:200])

    finally:
        ctx.close()
        browser.close()
