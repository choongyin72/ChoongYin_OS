#!/usr/bin/env python3
"""READ-ONLY: resolve Contract Name / Location Name panel labels for the proven pair
(TS5_FTR_SHB_01 / TS5_DP_GP_GSP), and find the correct nav Business Unit (via contract_area TS5_CA).
Nothing saved."""
import os, sys
from pathlib import Path
EC = Path(r"C:\Projects\ChoongYin_OS\workstreams\master-plan\ec-automation")
sys.path.insert(0, str(EC / "py"))
import ec_object_iud as ec
from playwright.sync_api import sync_playwright
def a(s): return str(s).encode("ascii","replace").decode("ascii")

with sync_playwright() as p:
    br = p.chromium.launch(headless=True, args=["--ignore-certificate-errors"])
    pg = br.new_context(ignore_https_errors=True, viewport={"width":1920,"height":1080}).new_page()
    ec.login(pg, "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/",
             os.environ.get("EC_USER","sysadmin"), os.environ.get("EC_PASS","sysadmin"))
    ec.open_object_screen(pg, "Contract Capacity")
    pg.wait_for_timeout(2000)
    ec.select_dropdown(pg, "nav:form:G:0:R:1:C:1:dd_input", "__FIRST__")
    ec.click_go(pg); ec.wait_ajax(pg); pg.wait_for_timeout(2000)
    ec._open_new_object(pg); pg.wait_for_timeout(1500)

    def find_label(field_label, code_fragment):
        f = ec._resolve_field(pg, "objectForm", field_label)
        if not f:
            print(a("%s: NOT RESOLVED" % field_label)); return
        base = f["id"].replace("_input", "")
        pg.click('[id="%s_button"]' % base); pg.wait_for_timeout(1200)
        opts = pg.eval_on_selector_all('[id="%s_panel"] tr[data-item-label]' % base,
                                       "els => els.map(e => e.dataset.itemLabel)")
        pg.keyboard.press("Escape"); pg.wait_for_timeout(300)
        match = [o for o in opts if code_fragment.lower().replace("_"," ").split()[0] in o.lower()
                 or code_fragment.lower() in o.lower().replace(" ","_")]
        print(a("%s: %d options; containing %r: %s" % (field_label, len(opts), code_fragment, match[:8])))
        print(a("   first 5: %s" % opts[:5]))

    find_label("Contract Name", "TS5 Shipper B Firm")
    find_label("Location Name", "TS5_DP_GP_GSP")
    br.close()
    print(a("NOTHING SAVED"))
