#!/usr/bin/env python3
"""ITEM 5 - the OV-GM parent-dropdown risk, tested READ-ONLY (nothing is ever saved).

Symptom: on Message Group a form dropdown set to 'Administration' persisted as 'Allocation' - the very
next option in an identical list. Two candidate causes were undistinguished: (a) the pick lands one row
off, or (b) the write silently fails and EC defaults. This matters beyond Message Group: the same
select_dropdown / Fill OV Dropdown By Label is used by all 22 OV-GM screens, and no suite asserts the
parent dropdown - only CODE and NAME.

Decisive test without a Save: set the field, then READ BACK the input's value.
  - reads back 'Administration' -> the pick is FAITHFUL; the divergence happens at save time (cause b,
    an EC-side default/override) and is NOT a shared-engine bug.
  - reads back 'Allocation'     -> the pick itself is off by one (cause a) -> shared-engine defect
    affecting every OV-GM screen's parent-dd.
"""
import os
import sys
from pathlib import Path

EC = Path(r"C:\Projects\ChoongYin_OS\workstreams\master-plan\ec-automation")
sys.path.insert(0, str(EC / "py"))
import ec_object_iud as ec
from playwright.sync_api import sync_playwright


def a(s):
    return str(s).encode("ascii", "replace").decode("ascii")


def read_back(pg, fid):
    return pg.eval_on_selector('[id="%s"]' % fid, "e => e.value")


with sync_playwright() as p:
    br = p.chromium.launch(headless=True, args=["--ignore-certificate-errors"])
    pg = br.new_context(ignore_https_errors=True, viewport={"width": 1920, "height": 1080}).new_page()
    ec.login(pg, "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/",
             os.environ.get("EC_USER", "sysadmin"), os.environ.get("EC_PASS", "sysadmin"))
    ec.open_object_screen(pg, "Message Group")
    pg.wait_for_timeout(2000)

    top = ec.apply_ovgm_navigator(pg)
    print(a("navigator top-parent captured: %r" % top))
    nav_val = read_back(pg, "nav:form:G:0:R:1:C:1:dd_input")
    print(a("navigator dd reads back as: %r  (matches captured: %s)" % (nav_val, nav_val == top)))

    ec._open_new_object(pg)
    pg.wait_for_timeout(1500)
    f = ec._resolve_field(pg, "objectForm", "Functional Area")
    print(a("form field: %s" % f))
    fid = f["id"]

    print(a("\n-- case 1: select_dropdown(__FIRST__) --"))
    ec.select_dropdown(pg, fid, "__FIRST__")
    pg.wait_for_timeout(800)
    v1 = read_back(pg, fid)
    print(a("   reads back: %r" % v1))

    print(a("-- case 2: select_dropdown(%r) (the captured nav value) --" % top))
    ec.select_dropdown(pg, fid, top)
    pg.wait_for_timeout(800)
    v2 = read_back(pg, fid)
    print(a("   reads back: %r" % v2))

    print(a("\nVERDICT:"))
    if v2 == top:
        print(a("   PICK IS FAITHFUL - the field holds %r before save. The Administration->Allocation"
                % v2))
        print(a("   divergence therefore happens AT SAVE (EC-side default/override), NOT in the shared"))
        print(a("   engine. Other OV-GM screens' parent-dd picks are not implicated by this evidence."))
    else:
        print(a("   PICK IS WRONG - asked for %r, field holds %r. Shared-engine defect; every OV-GM"
                % (top, v2)))
        print(a("   screen's parent-dd is suspect and none of their suites would have caught it."))
    pg.screenshot(path=r"C:\Projects\ChoongYin_OS\tmp\mg_dd_fidelity.png", full_page=True)
    br.close()
    print(a("\nNOTHING SAVED (read-only probe; form abandoned)"))
