#!/usr/bin/env python3
"""Read-only recon: Cargo Planning Forecast under P1 scope - nav ids, insert menu items,
NEW OBJECT panel field ids. Screenshots at each step."""
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
    ec.open_object_screen(pg, "Cargo Planning Forecast")
    pg.wait_for_timeout(1500)
    pg.screenshot(path=r"C:\Projects\ChoongYin_OS\tmp\cpf_01_loaded.png")

    print("--- nav inputs (pre-fill) ---")
    for el in pg.locator("input[id^='nav:form']").all():
        i = el.get_attribute("id")
        if i and "hinput" not in i and "ViewState" not in i:
            print(" ", i, "=", (el.input_value() or "")[:30])

    # fill nav: G:1..G:4 with P1 values + GO
    for g, val in ((1, "P1 Production Unit"), (2, "P1 Area"), (3, "P1 Facility 1"), (4, "P1_CRUDE_STOR")):
        ec.select_dropdown(pg, "nav:form:G:%d:R:1:C:0:dd_input" % g, val)
        pg.wait_for_timeout(700)
    ec.click_go(pg)
    pg.screenshot(path=r"C:\Projects\ChoongYin_OS\tmp\cpf_02_nav.png")

    print("--- grid tbody ids ---")
    for el in pg.locator("tbody[id]").all():
        i = el.get_attribute("id")
        if i and "T_data" in i:
            print(" ", i)

    # insert menu items
    li = pg.locator("xpath=//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'ui-icon-insert')]]")
    li.first.hover()
    pg.wait_for_timeout(1000)
    print("--- insert submenu items ---")
    for a in pg.locator("xpath=//ul[contains(@class,'ui-menu-child')]//li//a").all():
        try:
            t = a.text_content().strip()
            if t and a.is_visible():
                print(" ", repr(t))
        except Exception:
            pass
    # click New Object (whatever its exact text)
    for a in pg.locator("xpath=//ul[contains(@class,'ui-menu-child')]//li//a").all():
        try:
            if a.is_visible() and "object" in a.text_content().strip().lower():
                a.click()
                break
        except Exception:
            pass
    pg.wait_for_timeout(2000)
    pg.screenshot(path=r"C:\Projects\ChoongYin_OS\tmp\cpf_03_newobject.png")

    print("--- NEW OBJECT panel inputs (id | value) ---")
    for el in pg.locator("input, select").all():
        try:
            i = el.get_attribute("id")
            if i and ("nav:form" not in i) and ("menu" not in i) and ("ViewState" not in i) and ("screenToolbar" not in i):
                if el.is_visible():
                    print(" ", i)
        except Exception:
            pass
    print("--- visible buttons ---")
    for el in pg.locator("button:visible, a.ui-button:visible").all():
        try:
            t = (el.text_content() or "").strip()
            i = el.get_attribute("id")
            if t or i:
                print(" ", i, "|", t[:30])
        except Exception:
            pass
    br.close()
