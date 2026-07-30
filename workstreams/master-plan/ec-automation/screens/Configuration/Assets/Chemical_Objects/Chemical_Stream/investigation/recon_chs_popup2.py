#!/usr/bin/env python3
"""Read-only: drive the From Connection popup to the list state, dump the REAL grid/tbody ids."""
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
    ec.open_object_screen(pg, "Chemical Stream")
    for col, val in ((1, "P1 Production Unit"), (2, "P1 Area"), (3, "P1 Facility 1")):
        ec.select_dropdown(pg, "nav:form:G:0:R:1:C:%d:dd_input" % col, val)
        pg.wait_for_timeout(700)
    ec.click_go(pg)
    ec._open_new_object(pg)
    pg.wait_for_timeout(1000)

    pin_id = "tab:tabPanel:objectForm:form:G:0:R:20:C:1:pin"
    pg.evaluate("(id) => { const b = document.getElementById(id + 'B'); if (b) b.click(); }", pin_id)
    pg.wait_for_selector('css=[id="popupIFrame"]', state="visible", timeout=15000)
    pg.wait_for_timeout(1500)
    fl = pg.frame_locator('css=[id="popupIFrame"]')
    fl.locator('css=[id="nav:form:G:4:R:1:C:0:dd_button"]').click()
    fl.locator("xpath=//*[@id='nav:form:G:4:R:1:C:0:dd_panel']//tr[normalize-space(@data-item-label)='CHEM_TANK']").first.click(timeout=10000)
    pg.wait_for_timeout(1000)
    fl.locator('css=[id="button:form:B"]').click()
    pg.wait_for_timeout(4000)
    pg.screenshot(path=r"C:\Projects\ChoongYin_OS\tmp\chs_popup_recon2.png")

    fr = None
    for f in pg.frames:
        if "stream_node_ref_popup" in (f.url or ""):
            fr = f
            break
    print("popup frame:", fr.url[:100] if fr else None)
    if fr:
        print("--- tbody ids ---")
        for el in fr.query_selector_all("tbody[id]"):
            print(" ", el.get_attribute("id"))
        print("--- tables with rows containing 'CT0' ---")
        for el in fr.query_selector_all("tbody"):
            txt = (el.inner_text() or "")[:80].replace("\n", " | ")
            if "CT0" in txt:
                print("  id=", el.get_attribute("id"), "text=", txt)
    br.close()
