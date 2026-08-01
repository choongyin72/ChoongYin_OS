#!/usr/bin/env python3
"""READ-ONLY: check the grid's actual row text and what clicking Insert does (TV inline-add-row vs
OV New-Object dialog). Nothing saved."""
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
    grid = pg.locator('[id="manageObject:form:T_data"]')
    print(a("grid text: %r" % (grid.inner_text() or "")[:200]))
    pg.locator("span.ui-icon-insert").first.click()
    pg.wait_for_timeout(1500)
    print(a("--- after clicking Insert icon ---"))
    print(a("menu items visible: %s" % [ (el.text_content() or "").strip()
        for el in pg.locator("li a, .ui-menuitem-text").all()[:15] ]))
    print(a("objectForm present: %d" % pg.locator('[id*="objectForm"]').count()))
    br.close()
