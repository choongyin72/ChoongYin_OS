#!/usr/bin/env python3
"""Read-only: button:form:B EXISTS in Report Group's DOM but the navigator has zero fields.
Decide the reload gesture from facts: is that GO actually VISIBLE/enabled, or a hidden leftover?
(feedback_verify_visible_locator - an id match is not proof it is the intended element.)"""
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
    b = pg.locator('[id="button:form:B"]')
    print(a("GO count=%d visible=%s enabled=%s box=%s" % (
        b.count(), b.first.is_visible(), b.first.is_enabled(), b.first.bounding_box())))
    print(a("GO outerHTML: %s" % (b.first.evaluate("e => e.outerHTML")[:200] if b.count() else "-")))
    # what does the one existing grid row look like (header vs data)?
    t = pg.locator('[id="report_group_table:form:T_data"]')
    print(a("grid rows=%d  text=%r" % (t.locator("tr").count(), (t.inner_text() or "")[:120])))
    br.close()
