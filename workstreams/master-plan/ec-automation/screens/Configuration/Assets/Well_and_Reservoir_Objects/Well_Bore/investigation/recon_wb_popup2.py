#!/usr/bin/env python3
"""Read-only: is 'P1 W008 OP' present in the Well popup list (Objects:form:T_data)?"""
import os
import sys
from pathlib import Path

EC = Path(r"C:\Projects\ChoongYin_OS\workstreams\master-plan\ec-automation")
sys.path.insert(0, str(EC / "py"))
import ec_object_iud as ec
from playwright.sync_api import sync_playwright

JS = "() => { const tb = document.getElementById('Objects:form:T_data'); if (!tb) return 'NO GRID'; const out = []; tb.querySelectorAll('tr').forEach(tr => { const inp = tr.querySelector('td input'); out.push(inp ? inp.value.trim() : tr.innerText.trim().split('\\t')[0]); }); return out; }"

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
    ec._open_new_object(pg)
    pg.wait_for_timeout(1200)
    pin = "tab:tabPanel:objectForm:form:G:0:R:7:C:1:pin"
    pg.evaluate("(id) => { const b = document.getElementById(id + 'B'); if (b) b.click(); }", pin)
    pg.wait_for_selector('css=[id="popupIFrame"]', state="visible", timeout=15000)
    pg.wait_for_timeout(3000)
    fl = pg.frame_locator('css=[id="popupIFrame"]')
    vals = None
    for f in pg.frames:
        if f != pg.main_frame and f.query_selector('[id="Objects:form:T_data"]'):
            vals = f.evaluate(JS)
            break
    print("popup row count:", len(vals) if isinstance(vals, list) else vals)
    if isinstance(vals, list):
        print("first 12:", vals[:12])
        print("'P1 W008 OP' in list:", "P1 W008 OP" in vals)
        print("real OP wells present:", [v for v in vals if v.endswith(" OP") and "PLN" not in v][:6])
    br.close()
