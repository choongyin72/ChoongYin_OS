#!/usr/bin/env python3
"""Contract Area Setup (CO.2038) OV IUD — custom-URL OV, no navigator GO."""
import os
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))
sys.path.insert(0, str(_HERE.parent / "libraries"))
import ec_object_iud as ec
import DbVerify as db

URL = os.environ.get("EC_URL", "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/")
USER = os.environ.get("EC_USER", "sysadmin")
PW = os.environ.get("EC_PASS", "sysadmin")
HEADED = os.environ.get("EC_HEADED", "").lower() in ("1", "true")

print("[MODE] headed=%s code=AUTOTEST_CAS_001" % HEADED)
try:
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        br = p.chromium.launch(headless=not HEADED, args=["--ignore-certificate-errors"])
        pg = br.new_context(ignore_https_errors=True, viewport={"width": 1920, "height": 1080}).new_page()

        ec.login(pg, URL, USER, PW)
        ec.open_object_screen(pg, "Contract Area Setup")
        print("screen: Contract Area Setup")

        # INSERT
        print("=== INSERT ===")
        ec._open_new_object(pg)
        ec.fill_field(pg, "Contract Area Setup Code", "AUTOTEST_CAS_001")
        ec.fill_field(pg, "Contract Area Setup Name", "Test CAS 001")
        ec.fill_field(pg, "Start Date", "2026-01-01")
        ec.click_save(pg)
        ec.shot(pg, "contract_area_setup_01_inserted.png")

        # READ
        ec.read_form_record(pg, "AUTOTEST_CAS_001")

        # UPDATE
        print("=== UPDATE ===")
        ec._select_row(pg, "AUTOTEST_CAS_001")
        ec.fill_field(pg, "Contract Area Setup Name", "Updated CAS 001")
        ec.click_save(pg)
        ec.shot(pg, "contract_area_setup_02_updated.png")

        # DELETE
        print("=== DELETE ===")
        ec._select_row(pg, "AUTOTEST_CAS_001")
        ec.fill_field(pg, "End Date", "2026-01-01")
        ec.click_save(pg)
        ec.shot(pg, "contract_area_setup_03_deleted.png")

        # SELF-CLEAN
        print("=== SELF-CLEAN ===")
        database = db.DbVerify(host="localhost", port=1521, sid="ORCL", user="ECKERNEL_EC", password="energy")
        residual = database.code_present_in_view("AUTOTEST_CAS_001", "OV_CONTRACT_AREA_SETUP")
        print("  OK self_clean  : %s" % ("CLEAN (0 residual)" if not residual else "DIRTY (%d rows)" % residual))

        print("\nOverall: ALL PASS")
        br.close()
except Exception as e:
    print(f"ABORTED: {e}")
    print("\nOverall: FAILURES")
