#!/usr/bin/env python3
"""READ-ONLY recon for Service (CO.2103) - nothing is saved.

Service has FIVE mandatory dropdowns (Service Template, Service Type, Service Status, Contract, Transport
System). Two of them - Contract and Transport System - are exactly the scope-dependent kind of reference
that made Message Group unbuildable (its row landed outside the navigator's scope). So before generating
anything: name the navigator levels, and confirm EVERY mandatory dropdown actually offers options under
the applied nav scope. An empty mandatory dropdown = the screen cannot be inserted in this scope, and I
would rather know that now than after a failed live run.
"""
import os
import sys
from pathlib import Path

EC = Path(r"C:\Projects\ChoongYin_OS\workstreams\master-plan\ec-automation")
sys.path.insert(0, str(EC / "py"))
import ec_object_iud as ec
from playwright.sync_api import sync_playwright

MAND = ["Service Template", "Service Type", "Service Status", "Contract", "Transport System"]


def a(s):
    return str(s).encode("ascii", "replace").decode("ascii")


def options(pg, dd_base):
    try:
        pg.click('[id="%s_button"]' % dd_base)
        pg.wait_for_timeout(900)
        opts = pg.eval_on_selector_all('[id="%s_panel"] tr[data-item-label]' % dd_base,
                                       "els => els.map(e => e.dataset.itemLabel)")
        pg.keyboard.press("Escape")
        pg.wait_for_timeout(200)
        return opts
    except Exception as e:
        return ["ERR %s" % repr(e)[:70]]


with sync_playwright() as p:
    br = p.chromium.launch(headless=True, args=["--ignore-certificate-errors"])
    pg = br.new_context(ignore_https_errors=True, viewport={"width": 1920, "height": 1080}).new_page()
    ec.login(pg, "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/",
             os.environ.get("EC_USER", "sysadmin"), os.environ.get("EC_PASS", "sysadmin"))
    ec.open_object_screen(pg, "Service")
    pg.wait_for_timeout(2500)

    print(a("--- navigator labels ---"))
    for el in pg.locator('[id^="nav:form"][id$=":la"]').all():
        print(a("   %-34s %r" % (el.get_attribute("id"), (el.text_content() or "").strip())))
    print(a("--- navigator dropdown options (before GO) ---"))
    for col in range(1, 5):
        base = "nav:form:G:0:R:1:C:%d:dd" % col
        if pg.locator('[id="%s_input"]' % base).count():
            o = options(pg, base)
            print(a("   C:%d  %d option(s): %s" % (col, len(o), o[:6])))

    # levels=1: this navigator has FOUR dd columns and C:3 exists with ZERO options, so the default
    # levels=4 raises RuntimeError("dropdown has no options"). Only C:1 is mandatory, and filling just
    # C:1 is what made the grid render stably in 3/3 scanner runs.
    top = ec.apply_ovgm_navigator(pg, levels=1)
    print(a("\nnav applied; top-parent = %r" % top))

    ec._open_new_object(pg)
    pg.wait_for_timeout(1800)
    print(a("--- mandatory form dropdowns under this scope ---"))
    empty = []
    for lbl in MAND:
        f = ec._resolve_field(pg, "objectForm", lbl)
        if not f:
            print(a("   %-20s NOT RESOLVED" % lbl))
            empty.append(lbl + " (unresolved)")
            continue
        o = options(pg, f["id"].replace("_input", ""))
        print(a("   %-20s %-44s %d option(s): %s" % (lbl, f["id"].split(":form:")[-1], len(o), o[:4])))
        if not o or (len(o) == 1 and str(o[0]).startswith("ERR")):
            empty.append(lbl)
    print(a("\nEMPTY / unusable mandatory dropdowns: %s" % (empty or "none - screen is insertable here")))
    pg.screenshot(path=r"C:\Projects\ChoongYin_OS\tmp\service_form.png", full_page=True)
    br.close()
    print(a("NOTHING SAVED (read-only)"))
