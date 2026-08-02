#!/usr/bin/env python3
"""Read-only: Well Bore - does the grid list bores with P1 cascade + a real well in G:4 (G:5 empty)?"""
import os
import sys
from pathlib import Path

EC = Path(r"C:\Projects\ChoongYin_OS\workstreams\master-plan\ec-automation")
sys.path.insert(0, str(EC / "py"))
import ec_object_iud as ec
from playwright.sync_api import sync_playwright

JS = "() => { const tb = document.getElementById('manageObject:form:T_data'); if (!tb) return 'NO GRID'; const out = []; tb.querySelectorAll('tr').forEach(tr => out.push(tr.innerText.trim().slice(0, 40))); return out.slice(0, 6); }"

with sync_playwright() as p:
    br = p.chromium.launch(headless=True, args=["--ignore-certificate-errors"])
    pg = br.new_context(ignore_https_errors=True, viewport={"width": 1920, "height": 1080}).new_page()
    ec.login(pg, "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/", os.environ.get("EC_USER", "sysadmin"), os.environ.get("EC_PASS", "sysadmin"))
    ec.open_object_screen(pg, "Well Bore")
    pg.wait_for_timeout(1500)
    for g, val in ((1, "P1 Production Unit"), (2, "P1 Area"), (3, "P1 Facility 1"), (4, "P1 W008 OP")):
        ec.select_dropdown(pg, "nav:form:G:%d:R:1:C:0:dd_input" % g, val)
        pg.wait_for_timeout(800)
    ec.click_go(pg)
    pg.wait_for_timeout(1800)
    print("grid rows:", pg.evaluate(JS))
    pg.screenshot(path=r"C:\Projects\ChoongYin_OS\tmp\wellbore_p1b.png")

    # also probe the form's mandatory Well popup under this scope
    ec._open_new_object(pg)
    pg.wait_for_timeout(1200)
    r = ec._resolve_field(pg, "objectForm", "Well")
    print("Well pin resolved:", r)
    br.close()
