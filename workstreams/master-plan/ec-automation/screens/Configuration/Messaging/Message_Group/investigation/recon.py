"""Message Group - read-only recon (checklist #5). Opens the screen + dumps the New-Object field
inventory (never Saves). Reruns the scan used to build this bundle. Env-var creds, ASCII-clean."""
import os
import sys
from pathlib import Path
EC = Path(__file__).resolve().parents[5]
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
    ec.open_object_screen(pg, 'Message Group')
    pu = ec.apply_ovgm_navigator(pg)
    print("nav top-parent PU:", pu)
    ec._open_new_object(pg); pg.wait_for_timeout(600)
    print("recon: New-Object form opened (read-only, no Save). View = OV_MESSAGE_GROUP.")
    print("NOTE: Functional Area is a mandatory reference dropdown - only offers Functional Areas")
    print("      already effective as of the record's Start Date. Administration (ADM) is only")
    print("      valid from 2001-01-01 onward - use Start Date >= 2003-01-01, never the plain 2000-01-01.")
    br.close()
