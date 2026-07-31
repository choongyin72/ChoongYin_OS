#!/usr/bin/env python3
"""READ-ONLY (nothing saved): are my explicit labels actually IN the Contract / Transport System panels,
under the correct nav scope (BU 'TS3 BU1') and the correct start date (2003-01-01)?

Why this matters: ec.select_dropdown SILENTLY falls back to the first option when the requested label is
not found (a deliberate fallback for cascade children whose options appear only after the parent is set).
So a wrong value produces NO error - Service saved contract TRANS_INV_BLEND and transport system TS5_TS
instead of the TS3 values I asked for. Either my labels are wrong, or they are absent from the panel.
"""
import os
import sys
from pathlib import Path

EC = Path(r"C:\Projects\ChoongYin_OS\workstreams\master-plan\ec-automation")
sys.path.insert(0, str(EC / "py"))
import ec_object_iud as ec
from playwright.sync_api import sync_playwright

WANT = {"Contract": "TS3 GTA Shipper A", "Transport System": "TS3 Transport System"}


def a(s):
    return str(s).encode("ascii", "replace").decode("ascii")


with sync_playwright() as p:
    br = p.chromium.launch(headless=True, args=["--ignore-certificate-errors"])
    pg = br.new_context(ignore_https_errors=True, viewport={"width": 1920, "height": 1080}).new_page()
    ec.login(pg, "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/",
             os.environ.get("EC_USER", "sysadmin"), os.environ.get("EC_PASS", "sysadmin"))
    ec.open_object_screen(pg, "Service")
    pg.wait_for_timeout(2500)
    ec.select_dropdown(pg, "nav:form:G:0:R:1:C:1:dd_input", "TS3 BU1")
    ec.click_go(pg)
    ec.wait_ajax(pg)
    print(a("nav set to TS3 BU1"))

    ec._open_new_object(pg)
    pg.wait_for_timeout(1500)
    # set the start date FIRST - reference dropdowns are filtered by it
    d = ec._resolve_field(pg, "objectForm", "Start Date")
    if d:
        ec.fill_field(pg, d["id"], "2003-01-01", d["kind"])
        pg.wait_for_timeout(800)
        print(a("start date set to 2003-01-01"))

    for label, want in WANT.items():
        f = ec._resolve_field(pg, "objectForm", label)
        if not f:
            print(a("%-18s NOT RESOLVED" % label))
            continue
        base = f["id"].replace("_input", "")
        pg.click('[id="%s_button"]' % base)
        pg.wait_for_timeout(1200)
        opts = pg.eval_on_selector_all('[id="%s_panel"] tr[data-item-label]' % base,
                                       "els => els.map(e => e.dataset.itemLabel)")
        pg.keyboard.press("Escape")
        pg.wait_for_timeout(300)
        exact = want in opts
        near = [o for o in opts if want.split()[0] in o][:6]
        print(a("%-18s %d options | wanted %r present=%s" % (label, len(opts), want, exact)))
        print(a("   first 3: %s" % opts[:3]))
        print(a("   containing %r: %s" % (want.split()[0], near)))
    pg.screenshot(path=r"C:\Projects\ChoongYin_OS\tmp\service_panels.png", full_page=True)
    br.close()
    print(a("NOTHING SAVED (read-only)"))
