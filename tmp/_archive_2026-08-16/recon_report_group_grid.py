#!/usr/bin/env python3
"""Read-only: the standard scan returned grid=None and an EMPTY navigator for Report Group (CO.0158),
so neither the doc's 'OV-GM / manageObject:form:T_data' nor my 'date nav + report_group_table:form:T_data'
is right. Find how rows actually list: dump every tbody/table id, the frame URL, and the toolbar shape."""
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
    print(a("frame url: %s" % pg.url[:140]))

    print("--- ALL tbody[id] ---")
    for el in pg.locator("tbody[id]").all():
        i = el.get_attribute("id") or ""
        rows = el.locator("tr").count()
        print(a("   %-52s rows=%d" % (i, rows)))
    print("--- ALL table[id] ---")
    for el in pg.locator("table[id]").all()[:25]:
        print(a("   %s" % (el.get_attribute("id") or "")))
    print("--- GO button present? ---")
    for sel in ('[id="button:form:B"]', "xpath=//button[normalize-space(.)='GO']",
                "xpath=//*[@title='Refresh']", "xpath=//a[contains(@title,'Refresh')]"):
        c = pg.locator(sel).count()
        print(a("   %-46s count=%d" % (sel, c)))
    print("--- toolbar items (title attr) ---")
    for el in pg.locator("xpath=//a[@title]").all()[:20]:
        t = el.get_attribute("title") or ""
        if t: print(a("   %s" % t[:60]))
    pg.screenshot(path=r"C:\Projects\ChoongYin_OS\tmp\report_group_open.png", full_page=True)
    br.close()
