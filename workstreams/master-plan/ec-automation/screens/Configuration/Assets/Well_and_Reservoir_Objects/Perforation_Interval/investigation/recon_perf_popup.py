#!/usr/bin/env python3
"""Read-only: Perforation Interval's 'Well Bore Interval' popup - inner nav/GO structure."""
import sys
from pathlib import Path

EC = Path(r"C:\Projects\ChoongYin_OS\workstreams\master-plan\ec-automation")
sys.path.insert(0, str(EC / "py"))
import ec_object_iud as ec
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    br = p.chromium.launch(headless=True, args=["--ignore-certificate-errors"])
    pg = br.new_context(ignore_https_errors=True, viewport={"width": 1920, "height": 1080}).new_page()
    ec.login(pg, "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/", "sysadmin", "sysadmin")
    ec.open_object_screen(pg, "Perforation Interval")
    pg.wait_for_timeout(1500)
    for g, val in ((1, "P1 Production Unit"), (2, "P1 Area"), (3, "P1 Facility 1"),
                   (4, "P1 W008 OP"), (6, "P1 W008 WB001"), (7, "P1 W008 WB001 WBI001")):
        ec.select_dropdown(pg, "nav:form:G:%d:R:1:C:0:dd_input" % g, val)
        pg.wait_for_timeout(800)
    ec.click_go(pg)
    ec._open_new_object(pg)
    pg.wait_for_timeout(1200)
    pin = "tab:tabPanel:objectForm:form:G:0:R:6:C:1:pin"
    pg.evaluate("(id) => { const b = document.getElementById(id + 'B'); if (b) b.click(); }", pin)
    pg.wait_for_selector('css=[id="popupIFrame"]', state="visible", timeout=15000)
    pg.wait_for_timeout(3000)
    pg.screenshot(path=r"C:\Projects\ChoongYin_OS\tmp\perf_popup.png")

    fr = None
    for f in pg.frames:
        if f != pg.main_frame and f.query_selector("[id$='T_data']"):
            fr = f
    print("popup frame:", (fr.url[:100] if fr else None))
    if fr:
        print("--- popup nav inputs ---")
        for el in fr.query_selector_all("input"):
            i = el.get_attribute("id")
            if i and "ViewState" not in i and "hinput" not in i and ("nav:" in i or "dd_input" in i):
                v = ""
                try: v = el.input_value()
                except Exception: pass
                print(f"  {i} = {v[:30]!r}")
        print("--- popup GO / buttons ---")
        for el in fr.query_selector_all("button[id]"):
            i = el.get_attribute("id")
            t = (el.text_content() or "").strip()[:18]
            if i and ("button:form:B" in i or "dd_button" in i):
                print(f"  {i} | {t}")
        print("--- popup tbodies ---")
        for el in fr.query_selector_all("tbody[id]"):
            i = el.get_attribute("id")
            if i and "T_data" in i:
                print(f"  {i} -> {(el.inner_text() or '')[:70]!r}")
    br.close()
