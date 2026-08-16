#!/usr/bin/env python3
"""READ-ONLY: fix 2 issues from the first probe - (1) date-effectivity may hide TS5 objects at the default
2000-01-01 start date (same as Service's TS3 trap), (2) Location Name may be a CASCADE CHILD of Contract
Name (only populates after Contract Name is set). Nothing saved."""
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
    ec.click_go(pg); ec.wait_ajax(pg); pg.wait_for_timeout(2000)
    ec._open_new_object(pg); pg.wait_for_timeout(1500)

    d = ec._resolve_field(pg, "objectForm", "Start Date")
    ec.fill_field(pg, d["id"], "2020-01-01", d["kind"])
    pg.wait_for_timeout(800)
    print(a("start date set to 2020-01-01"))

    cf = ec._resolve_field(pg, "objectForm", "Contract Name")
    cbase = cf["id"].replace("_input", "")
    pg.click('[id="%s_button"]' % cbase); pg.wait_for_timeout(1200)
    opts = pg.eval_on_selector_all('[id="%s_panel"] tr[data-item-label]' % cbase,
                                   "els => els.map(e => e.dataset.itemLabel)")
    exact = [o for o in opts if "shipper b firm" in o.lower()]
    print(a("Contract Name: %d options; exact 'Shipper B Firm' match: %s" % (len(opts), exact)))
    if not exact:
        print(a("  first 10: %s" % opts[:10]))
    br.close()
    print(a("NOTHING SAVED"))
