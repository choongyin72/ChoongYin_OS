"""Constant Standard - read-only recon (checklist #5). Opens the screen (never Saves). Reruns the
scan used to build this bundle. Env-var creds, ASCII-clean."""
import os
import sys
from pathlib import Path
EC = Path(__file__).resolve().parents[6]
sys.path.insert(0, str(EC / "py"))
import ec_object_iud as ec
from playwright.sync_api import sync_playwright

URL = os.environ.get("EC_URL", "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/")
USER = os.environ.get("EC_USER", "sysadmin")
PW = os.environ.get("EC_PASS", "sysadmin")
with sync_playwright() as p:
    br = p.chromium.launch(headless=True, args=["--ignore-certificate-errors"])
    pg = br.new_context(ignore_https_errors=True, viewport={"width": 1920, "height": 1080}).new_page()
    ec.login(pg, URL, USER, PW)
    ec.open_object_screen(pg, "Constant Standard")
    pg.wait_for_timeout(800)
    print("recon: Constant Standard opened (read-only, no Save). View = OV_CONSTANT_STANDARD.")
    print("NOTE: TV-style inline-editable grid (cstandard:form:T_data), but CLASS_TYPE=OBJECT/")
    print("      VERSIONED per class_cnfg - delete = End Date = Start Date in the inline cell, NOT")
    print("      a physical toolbar delete. Insert menu item's real DOM text is title-case")
    print("      ('Constant Standard') - the visible ALL-CAPS is CSS text-transform, not the actual")
    print("      text; must be scoped to the Insert icon's OWN <li> since Delete's <li> has an")
    print("      identically-worded item. Mandatory insert fields: Standard Code, Standard Name,")
    print("      Start Date, and Daytime (a genuinely separate field, not derived from Start Date).")
    br.close()
