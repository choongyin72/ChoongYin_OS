#!/usr/bin/env python3
"""READ-ONLY diagnosis (no Save): the navigator's Functional Area first-available is 'Administration',
but every insert lands in 'ALLOCATION'. Question: does the objectForm's Functional Area panel even OFFER
'Administration'? Opens the New-Object form, lists BOTH panels' options, and closes without saving."""
import os, sys
from pathlib import Path
EC = Path(r"C:\Projects\ChoongYin_OS\workstreams\master-plan\ec-automation")
sys.path.insert(0, str(EC / "py"))
import ec_object_iud as ec
from playwright.sync_api import sync_playwright
def a(s): return str(s).encode("ascii", "replace").decode("ascii")

def opts(pg, dd_id):
    try:
        pg.click('[id="%s_button"]' % dd_id)
        pg.wait_for_timeout(900)
        return pg.eval_on_selector_all(
            '[id="%s_panel"] tr[data-item-label]' % dd_id, "els => els.map(e => e.dataset.itemLabel)")
    except Exception as e:
        return ["ERR %s" % repr(e)[:80]]

with sync_playwright() as p:
    br = p.chromium.launch(headless=True, args=["--ignore-certificate-errors"])
    pg = br.new_context(ignore_https_errors=True, viewport={"width": 1920, "height": 1080}).new_page()
    ec.login(pg, "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/",
             os.environ.get("EC_USER", "sysadmin"), os.environ.get("EC_PASS", "sysadmin"))
    ec.open_object_screen(pg, "Message Group")
    pg.wait_for_timeout(2000)
    print(a("NAVIGATOR Functional Area options: %s" % opts(pg, "nav:form:G:0:R:1:C:1:dd")))
    pg.keyboard.press("Escape")
    ec.apply_ovgm_navigator(pg)
    ec._open_new_object(pg) if hasattr(ec, "_open_new_object") else None
    pg.wait_for_timeout(1500)
    fid = ec._resolve_field(pg, "objectForm", "Functional Area")
    print(a("form field resolved: %s" % fid))
    if fid:
        print(a("FORM Functional Area options: %s" % opts(pg, fid["id"].replace("_input", ""))))
    pg.screenshot(path=r"C:\Projects\ChoongYin_OS\tmp\mg_form_fa.png", full_page=True)
    br.close()
    print("NOTHING SAVED (read-only)")
