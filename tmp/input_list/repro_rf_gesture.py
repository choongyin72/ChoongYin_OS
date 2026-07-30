"""Decisive: mimic the RF dropdown gesture (button-click + tr-click) vs the engine, then read the
dd model value + EC notification + DB. Isolates whether the click commits. Self-cleans. tmp scratch."""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright
EC = Path(r"C:\Projects\ChoongYin_OS\workstreams\master-plan\ec-automation")
sys.path.insert(0, str(EC / "py")); sys.path.insert(0, str(EC / "libraries"))
import ec_object_iud as ec
import DbVerify as db
URL = "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"
CODE = "AUTOTEST_INPUTLIST_REPRO"
GRID = "manage_object_nav_nav:form:T_data"


def dd_value(pg, prefix):
    return pg.evaluate("(p)=>{const i=document.getElementById(p+'_input');const h=document.getElementById(p+'_hinput');"
                       "return {input:i?i.value:null, hidden:h?h.value:null};}", prefix)


with sync_playwright() as p:
    br = p.chromium.launch(headless=True, args=["--ignore-certificate-errors"])
    pg = br.new_context(ignore_https_errors=True, viewport={"width": 1920, "height": 1080}).new_page()
    ec.login(pg, URL, "sysadmin", "sysadmin")
    ec.open_object_screen(pg, "Input List"); ec.click_go(pg)
    if ec.row_exists(pg, GRID, CODE):
        ec.closeObjectRecord(pg, GRID, CODE, "2000-01-01"); ec.open_object_screen(pg, "Input List"); ec.click_go(pg)
    ec._open_new_object(pg); pg.wait_for_timeout(500)
    ec.fill_field(pg, "tab:tabPanel:objectForm:form:G:0:R:0:C:1:in", CODE, "text")
    ec.fill_field(pg, "tab:tabPanel:objectForm:form:G:0:R:1:C:1:in", "AUTOTEST Repro", "text")
    ec.fill_field(pg, "tab:tabPanel:objectForm:form:G:0:R:2:C:1:da_input", "2000-01-01", "date")
    prefix = "tab:tabPanel:objectForm:form:G:0:R:6:C:1:dd"
    # --- RF-STYLE gesture: click button, wait tr, click tr (NO engine helper) ---
    pg.locator("css=[id=\"%s_button\"]" % prefix).first.click()
    item = "xpath=//*[@id='%s_panel']//tr[normalize-space(@data-item-label)='INPUT']" % prefix
    pg.locator(item).first.wait_for(state="visible", timeout=8000)
    pg.locator(item).first.click()
    pg.wait_for_load_state("networkidle"); pg.wait_for_timeout(600)
    print("after RF-style click, dd value:", dd_value(pg, prefix))
    ec.save(pg)
    print("ec_error after save:", repr(ec.ec_error(pg)))
    ec.click_go(pg); pg.wait_for_timeout(800)
    print("DB present after RF-style insert:", db.code_present("ov_stream_item_collection", CODE))
    # self-clean
    if ec.row_exists(pg, GRID, CODE):
        ec.closeObjectRecord(pg, GRID, CODE, "2000-01-01")
    print("residual after clean:", db.count_like("ov_stream_item_collection", "AUTOTEST"))
    br.close()
