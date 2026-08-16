#!/usr/bin/env python3
"""READ-ONLY: check if Location Name's panel rows carry a code/value attribute (not just the label),
which would resolve TS5_DP_GP_GSP -> label exactly instead of guessing. Nothing saved."""
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
    lf = ec._resolve_field(pg, "objectForm", "Location Name")
    lbase = lf["id"].replace("_input", "")
    pg.click('[id="%s_button"]' % lbase); pg.wait_for_timeout(1200)
    attrs = pg.eval_on_selector('[id="%s_panel"] tr[data-item-label]' % lbase,
                                "e => Array.from(e.attributes).map(a => a.name)")
    print(a("first row's dataset attributes: %s" % attrs))
    row1 = pg.eval_on_selector('[id="%s_panel"] tr[data-item-label]' % lbase, "e => e.outerHTML")
    print(a("first row outerHTML (truncated): %s" % row1[:400]))
    br.close()
    print(a("NOTHING SAVED"))
