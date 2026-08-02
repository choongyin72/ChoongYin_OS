#!/usr/bin/env python3
"""Read-only-ish: insert a blank row on Create Calculation, dump ALL its element ids, then
DISCARD (click NO on unsaved-changes / just close) - nothing saved."""
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
    ec.select_dropdown(pg, "nav:form:G:1:R:1:C:0:dd_input", "__FIRST__")
    pg.wait_for_timeout(700)
    ec.click_go(pg)
    pg.wait_for_timeout(1500)

    # insert blank row
    pg.locator("xpath=//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'ui-icon-insert')]]").first.hover()
    pg.wait_for_timeout(900)
    links = pg.locator("xpath=//ul[contains(@class,'ui-menu-child')]//li//a")
    for i in range(links.count()):
        ln = links.nth(i)
        if ln.is_visible() and (ln.text_content(timeout=800) or "").strip():
            print("insert item clicked:", repr(ln.text_content().strip()))
            ln.click()
            break
    ec.wait_ajax(pg)

    # find blank row index
    rows = pg.evaluate("""() => { const out={};
        document.querySelectorAll("[id^='calculation:form:T:'][id$='C0_in']").forEach(e=>{
          const m=e.id.match(/T:(\\d+):C0_in/); if(m) out[m[1]]=e.value; });
        return out; }""")
    blank = None
    for r, v in sorted(rows.items(), key=lambda x: int(x[0])):
        if not (v or "").strip():
            blank = r
            break
    print("blank row:", blank, "| all rows:", rows)

    if blank is not None:
        ids = pg.evaluate("""(r) => {
            const out=[];
            document.querySelectorAll("[id^='calculation:form:T:"+r+":']").forEach(e=>{
              out.push(e.tagName + ' ' + e.id); });
            return out; }""", blank)
        print("--- ALL elements of blank row ---")
        for i in ids:
            print(" ", i)
    pg.screenshot(path=r"C:\Projects\ChoongYin_OS\tmp\cc_blankrow.png")
    br.close()   # discard staged row - nothing saved
