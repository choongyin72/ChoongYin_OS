#!/usr/bin/env python3
"""Read-only: open Chemical Stream under P1 scope, open New Object, launch the From Connection popup,
dump the popup iframe's inputs/buttons + grid state, screenshot."""
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
    pg.wait_for_timeout(2500)
    pg.screenshot(path=r"C:\Projects\ChoongYin_OS\tmp\chs_popup_recon.png")

    fr = None
    for f in pg.frames:
        try:
            if "Popup" in (f.url or "") or f.query_selector("[id^='PopupList']") or f.query_selector("[id^='nav:form']"):
                if f != pg.main_frame:
                    fr = f
        except Exception:
            pass
    frames_info = [(f.url[:100]) for f in pg.frames]
    print("frames:", *frames_info, sep="\n  ")
    if fr:
        print("\n--- popup frame inputs ---")
        for el in fr.query_selector_all("input"):
            try:
                i = el.get_attribute("id")
                if i and "ViewState" not in i:
                    print(" ", i, "=", (el.input_value() or "")[:40])
            except Exception:
                pass
        print("--- popup frame buttons/links ---")
        for el in fr.query_selector_all("button, a[id]"):
            try:
                i = el.get_attribute("id")
                if i:
                    print(" ", i)
            except Exception:
                pass
        print("--- grid present? ---")
        print("PopupList:form:T_data:", bool(fr.query_selector('[id="PopupList:form:T_data"]')))
    br.close()
