#!/usr/bin/env python3
"""Probe Well form structure — what fields does it actually have?"""
import os, sys
from pathlib import Path

EC = Path(__file__).resolve().parent.parent / "workstreams" / "master-plan" / "ec-automation"
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
    ec.open_object_screen(pg, "Well")
    ec._open_new_object(pg)

    # Scan form for all labels
    print("=== Well New-Object form field labels ===")
    labels = pg.query_selector_all("label")
    for i, lbl in enumerate(labels[:25]):  # first 25 labels
        text = lbl.text_content().strip()
        if text:
            print(f"  R:{i} {text}")

    br.close()
