"""Recon: Chemical Tank grid header columns (manageObject:form:T_head) + objectForm label scan
for Op Production Unit/Op Area/Op Facility Class 1 presence. Read-only.
Run: py tmp/recon_ct_grid_headers.py
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
        pu = ec.apply_ovgm_navigator(page)
        print("[NAV PU]", pu)

        headers = page.locator("xpath=//*[@id='manageObject:form:T_head']//th//span").all_inner_texts()
        print("[GRID HEADERS]", headers)

        page.click("css=[id=\"toolbar:form:insertButton\"]", timeout=5000) if page.locator(
            "css=[id=\"toolbar:form:insertButton\"]").count() else None
    finally:
        ctx.close()
        browser.close()
