#!/usr/bin/env python3
"""Read-only: does Report Group really have NO navigator fields, or did the scanner's
nav:form:G:*:R:1:C:0 pattern just miss them? Dump EVERY element whose id starts with 'nav:form'."""
import os, sys
from pathlib import Path
EC = Path(r"C:\Projects\ChoongYin_OS\workstreams\master-plan\ec-automation")
sys.path.insert(0, str(EC / "py"))
import ec_object_iud as ec
from playwright.sync_api import sync_playwright
def a(s): return str(s).encode("ascii", "replace").decode("ascii")

with sync_playwright() as p:
    br = p.chromium.launch(headless=True, args=["--ignore-certificate-errors"])
    pg = br.new_context(ignore_https_errors=True, viewport={"width": 1920, "height": 1080}).new_page()
    ec.login(pg, "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/",
             os.environ.get("EC_USER", "sysadmin"), os.environ.get("EC_PASS", "sysadmin"))
    ec.open_object_screen(pg, "Report Group")
    pg.wait_for_timeout(3000)
    ids = pg.evaluate("""() => Array.from(document.querySelectorAll('[id^="nav:form"]'))
        .map(e => e.id + ' <' + e.tagName.toLowerCase() + '>' +
             (e.offsetParent === null ? ' HIDDEN' : ' visible'))""")
    print(a("elements with id ^= 'nav:form' : %d" % len(ids)))
    for i in ids[:40]: print(a("   %s" % i))
    labels = pg.evaluate("""() => Array.from(document.querySelectorAll('label'))
        .map(e => e.textContent.trim()).filter(t => t).slice(0, 25)""")
    print(a("labels on screen: %s" % labels))
    br.close()
