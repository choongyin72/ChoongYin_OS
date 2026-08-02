#!/usr/bin/env python3
"""Read-only: Well Bore Interval - G:5/G:6 options under P1 + real well; grid; popup grid id."""
import os
import sys
from pathlib import Path

EC = Path(r"C:\Projects\ChoongYin_OS\workstreams\master-plan\ec-automation")
sys.path.insert(0, str(EC / "py"))
import ec_object_iud as ec
from playwright.sync_api import sync_playwright

GRID_JS = "() => { const tb = document.getElementById('manageObject:form:T_data'); if (!tb) return 'NO GRID'; const out = []; tb.querySelectorAll('tr').forEach(tr => out.push(tr.innerText.trim().slice(0, 40))); return out.slice(0, 4); }"

with sync_playwright() as p:
    br = p.chromium.launch(headless=True, args=["--ignore-certificate-errors"])
    pg = br.new_context(ignore_https_errors=True, viewport={"width": 1920, "height": 1080}).new_page()
    ec.login(pg, "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/", os.environ.get("EC_USER", "sysadmin"), os.environ.get("EC_PASS", "sysadmin"))
    ec.open_object_screen(pg, "Well Bore Interval")
    pg.wait_for_timeout(1500)
    for g, val in ((1, "P1 Production Unit"), (2, "P1 Area"), (3, "P1 Facility 1"), (4, "P1 W008 OP")):
        ec.select_dropdown(pg, "nav:form:G:%d:R:1:C:0:dd_input" % g, val)
        pg.wait_for_timeout(800)
    for g in (5, 6):
        pg.click("[id='nav:form:G:%d:R:1:C:0:dd_button']" % g)
        pg.wait_for_timeout(1000)
        opts = [tr.get_attribute("data-item-label") for tr in
                pg.locator("[id='nav:form:G:%d:R:1:C:0:dd_panel'] tr[data-item-label]" % g).all()]
        print(f"G:{g} options ({len(opts)}):", opts[:5])
        if opts:
            pg.locator("[id='nav:form:G:%d:R:1:C:0:dd_panel'] tr[data-item-label]" % g).first.click()
            pg.wait_for_timeout(900)
        else:
            pg.keyboard.press("Escape")
    ec.click_go(pg)
    pg.wait_for_timeout(1800)
    print("grid:", pg.evaluate(GRID_JS))

    # popup grid id for the mandatory 'Well Bore' pin
    ec._open_new_object(pg)
    pg.wait_for_timeout(1200)
    r = ec._resolve_field(pg, "objectForm", "Well Bore")
    print("Well Bore pin:", r)
    if r:
        pg.evaluate("(id) => { const b = document.getElementById(id + 'B'); if (b) b.click(); }", r["id"])
        pg.wait_for_selector('css=[id="popupIFrame"]', state="visible", timeout=15000)
        pg.wait_for_timeout(3000)
        for f in pg.frames:
            if f != pg.main_frame:
                for el in f.query_selector_all("tbody[id]"):
                    i = el.get_attribute("id")
                    if i and "T_data" in i:
                        txt = (el.inner_text() or "")[:70].replace("\n", " | ")
                        print(f"  popup tbody {i} -> {txt!r}")
    pg.screenshot(path=r"C:\Projects\ChoongYin_OS\tmp\wbi_recon.png")
    br.close()
