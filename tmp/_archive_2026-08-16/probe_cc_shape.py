#!/usr/bin/env python3
"""READ-ONLY: Contract Capacity resolves to 3 TABLE classes (CAPACITY_REL_CNTR_CAP, CAPACITY_BID_CNTR_CAP,
CONTRACT_CAPACITY). Scanner found grid manageObject:form:T_data but no blank insert row - probe for tabs/
sub-grids before assuming a plain TV shape."""
import os, sys
from pathlib import Path
EC = Path(r"C:\Projects\ChoongYin_OS\workstreams\master-plan\ec-automation")
sys.path.insert(0, str(EC / "py"))
import ec_object_iud as ec
from playwright.sync_api import sync_playwright
def a(s): return str(s).encode("ascii","replace").decode("ascii")
with sync_playwright() as p:
    br = p.chromium.launch(headless=True, args=["--ignore-certificate-errors"])
    pg = br.new_context(ignore_https_errors=True, viewport={"width":1920,"height":1080}).new_page()
    ec.login(pg, "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/",
             os.environ.get("EC_USER","sysadmin"), os.environ.get("EC_PASS","sysadmin"))
    ec.open_object_screen(pg, "Contract Capacity")
    pg.wait_for_timeout(2000)
    ec.select_dropdown(pg, "nav:form:G:0:R:1:C:1:dd_input", "__FIRST__")
    ec.click_go(pg); ec.wait_ajax(pg); pg.wait_for_timeout(3000)
    print(a("--- tabs ---"))
    for el in pg.locator("a[role='tab'], .ui-tabs-anchor").all():
        print(a("   %r" % (el.text_content() or "").strip()))
    print(a("--- all tbody[id] grids ---"))
    for el in pg.locator("tbody[id]").all():
        i = el.get_attribute("id") or ""
        print(a("   %-46s rows=%d" % (i, el.locator("tr").count())))
    print(a("--- toolbar insert icon present? ---"))
    print(a("   ui-icon-insert count: %d" % pg.locator("span.ui-icon-insert").count()))
    br.close()
