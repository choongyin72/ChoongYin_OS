#!/usr/bin/env python3
"""Read-only: Create Calculation blank insert row - full cell list with kinds, both grids."""
import os
import sys
from pathlib import Path

EC = Path(r"C:\Projects\ChoongYin_OS\workstreams\master-plan\ec-automation")
sys.path.insert(0, str(EC / "py"))
import ec_object_iud as ec
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    br = p.chromium.launch(headless=True, args=["--ignore-certificate-errors"])
    pg = br.new_context(ignore_https_errors=True, viewport={"width": 1920, "height": 1080}).new_page()
    ec.login(pg, "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/", os.environ.get("EC_USER", "sysadmin"), os.environ.get("EC_PASS", "sysadmin"))
    ec.open_object_screen(pg, "Create Calculation")
    pg.wait_for_timeout(1500)

    print("--- nav G:1 dd options (Calculation Contexts) ---")
    pg.click("[id='nav:form:G:1:R:1:C:0:dd_button']")
    pg.wait_for_timeout(800)
    for tr in pg.locator("[id='nav:form:G:1:R:1:C:0:dd_panel'] tr[data-item-label]").all():
        print("  ", tr.get_attribute("data-item-label"))
    pg.keyboard.press("Escape")

    # pick first context + GO
    ec.select_dropdown(pg, "nav:form:G:1:R:1:C:0:dd_input", "__FIRST__")
    pg.wait_for_timeout(700)
    ec.click_go(pg)
    pg.wait_for_timeout(1500)
    pg.screenshot(path=r"C:\Projects\ChoongYin_OS\tmp\create_calc_01.png")

    print("\n--- ALL input-ish elements in calculation:form rows T:0..T:2 (id | tag | value) ---")
    for el in pg.locator("[id^='calculation:form:T:']").all():
        try:
            i = el.get_attribute("id")
            if i and any(i.endswith(s) for s in ("_in", "_da_input", "_dd_input", "_cb", "_ta")):
                v = ""
                try: v = el.input_value()
                except Exception: pass
                print(f"  {i:<50} val={v[:30]!r}")
        except Exception:
            pass
    print("\n--- calculation_version:form rows ---")
    for el in pg.locator("[id^='calculation_version:form:T:']").all():
        try:
            i = el.get_attribute("id")
            if i and any(i.endswith(s) for s in ("_in", "_da_input", "_dd_input", "_cb", "_ta")):
                v = ""
                try: v = el.input_value()
                except Exception: pass
                print(f"  {i:<50} val={v[:30]!r}")
        except Exception:
            pass
    print("\n--- other grids on screen ---")
    for el in pg.locator("tbody[id]").all():
        i = el.get_attribute("id")
        if i and "T_data" in i:
            print("  ", i)
    br.close()
