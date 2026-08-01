#!/usr/bin/env python3
"""READ-ONLY: External Location (CO.0227) - the scanner found per-field nav groups (none mandatory), no
grid and no objectForm, and correctly refused to call that the screen's shape. Click GO with no filters and
see what renders."""
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
    ec.open_object_screen(pg, "External Location")
    pg.wait_for_timeout(2500)
    print(a("url: %s" % pg.url[:110]))
    print(a("nav labels:"))
    for el in pg.locator('[id^="nav:form"][id$=":la"]').all():
        print(a("   %-30s %r" % (el.get_attribute("id"), (el.text_content() or "").strip())))
    ec.click_go(pg); ec.wait_ajax(pg); pg.wait_for_timeout(3000)
    print(a("after GO - tbody[id] present:"))
    for el in pg.locator("tbody[id]").all():
        i = el.get_attribute("id") or ""
        print(a("   %-46s rows=%d" % (i, el.locator("tr").count())))
    br.close()
