#!/usr/bin/env python3
"""Read-only: Message Group (CO.0236) is OV-GM per scan (mandatory nav dropdown + date + GO, grid
manageObject:form:T_data). gen_ovgm.py needs the nav LEVEL LABELS, which the scan does not print."""
import os, sys
from pathlib import Path
EC = Path(r"C:\Projects\ChoongYin_OS\workstreams\master-plan\ec-automation")
sys.path.insert(0, str(EC / "py"))
import ec_object_iud as ec
from playwright.sync_api import sync_playwright
def a(s): return str(s).encode("ascii", "replace").decode("ascii")

with sync_playwright() as p:
    br = p.chromium.launch(headless=True, args=["--ignore-certificate-errors"])
    pg = br.new_context(ignore_https_errors=True, viewport={"width": 1920, "height": 1080}).new_page()
    ec.login(pg, "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/",
             os.environ.get("EC_USER", "sysadmin"), os.environ.get("EC_PASS", "sysadmin"))
    ec.open_object_screen(pg, "Message Group")
    pg.wait_for_timeout(2500)
    rows = pg.evaluate("""() => Array.from(document.querySelectorAll('[id^="nav:form"]'))
        .filter(e => e.id.match(/:(la|dd|da)(_input)?$/))
        .map(e => e.id + ' :: ' + (e.tagName.toLowerCase()==='span' ? e.textContent.trim() :
             (e.value || '')) + (e.offsetParent===null ? ' [HIDDEN]' : ''))""")
    print(a("nav elements:"))
    for r in rows: print(a("   %s" % r))
    print(a("\nnav labels (fieldset text):"))
    for el in pg.locator('[id^="nav:form"][id$=":la"]').all():
        print(a("   %s -> %r" % (el.get_attribute("id"), (el.text_content() or "").strip())))
    br.close()
