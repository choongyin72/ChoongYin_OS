"""Diagnose the RF dropdown prefix: run the EXACT OV Field Id By Label xpath for 'List Category'
and compare its id/derived-prefix to the engine's dd_input id + check panel/button exist. Read-only."""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright
EC = Path(r"C:\Projects\ChoongYin_OS\workstreams\master-plan\ec-automation")
sys.path.insert(0, str(EC / "py"))
import ec_object_iud as ec
URL = "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"
with sync_playwright() as p:
    br = p.chromium.launch(headless=True, args=["--ignore-certificate-errors"])
    pg = br.new_context(ignore_https_errors=True, viewport={"width": 1920, "height": 1080}).new_page()
    ec.login(pg, URL, "sysadmin", "sysadmin")
    ec.open_object_screen(pg, "Input List"); ec.click_go(pg); ec._open_new_object(pg); pg.wait_for_timeout(600)
    # exact RF resolver xpath
    rf_xpath = ("xpath=//span[contains(@class,'ECCell') and contains(@id,':objectForm:form:') "
                "and normalize-space(text())='List Category']/ancestor::div[contains(@class,'tableCell')][1]"
                "/following-sibling::div[contains(@class,'tableCell')][1]//input")
    loc = pg.locator(rf_xpath)
    print("RF resolver matched inputs:", loc.count())
    for i in range(loc.count()):
        print("  id[%d]=%s" % (i, loc.nth(i).get_attribute("id")))
    rid = loc.first.get_attribute("id") if loc.count() else None
    print("RF first id:", rid)
    if rid:
        pfx = rid.replace("_input", "")
        print("derived prefix:", pfx)
        print("  <prefix>_button exists:", pg.locator("css=[id=\"%s_button\"]" % pfx).count())
        print("  <prefix>_panel exists:", pg.locator("css=[id=\"%s_panel\"]" % pfx).count())
    # engine's known id
    r = ec._resolve_field(pg, "objectForm", "List Category")
    print("engine _resolve_field:", r)
    br.close()
