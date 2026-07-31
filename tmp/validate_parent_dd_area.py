#!/usr/bin/env python3
"""ITEM 1: prove the `parent_dd` WIRING end-to-end. Live, one AUTOTEST row, self-cleaning.

WHY AREA AND NOT NODE (both facts read out of shipped code, not assumed):
 - Node's own driver documents that its Op PU panel offers only 5 PUs and the navigator's first-available
   PU is NOT one of them - so binding the form dd to the captured nav value cannot work there, for a
   reason unrelated to the capability. Node is the wrong bed.
 - Area's T3 says the opposite: "the inserted area must carry the same Op Production Unit to appear in the
   filtered grid", and its live-passing suite passes ${NAV_PU} to BOTH the navigator and the form. So the
   PATTERN is already proven on Area; what is unproven is MY wiring - binding the value CAPTURED by
   apply_ovgm_navigator instead of a literal passed in by hand.

WHAT THIS TESTS: nav PU set explicitly to the same PU the merged Area suite uses -> capture what the
navigator actually holds -> bind THAT captured value into the form's Op Production Unit -> Save -> the row
must LIST in the grid -> the DB must store that same PU in OP_PRODUCTIONUNIT_CODE (the assertion existing
suites never make) -> delete via End=Start -> 0 residual.

Fails => I delete parent_dd from gen_ovgm.py rather than leave a broken key in master.
"""
import os
import sys
from pathlib import Path

EC = Path(r"C:\Projects\ChoongYin_OS\workstreams\master-plan\ec-automation")
sys.path.insert(0, str(EC / "py"))
sys.path.insert(0, str(EC / "libraries"))
import ec_object_iud as ec
import DbVerify as db
from playwright.sync_api import sync_playwright

SCREEN = "Area"
GRID = "manageObject:form:T_data"
VIEW = "ov_area"
NAV_PU_DD = "nav:form:G:0:R:1:C:1:dd_input"
NAV_PU_VALUE = "Production Unit"          # the PU the merged Area suite uses (user-approved 2026-06-11)
CODE = "AUTOTEST_PDD_AREA_001"
NAME = "AUTOTEST parent_dd validation"
# 2003-01-01, NOT 2000-01-01: Area's Op Production Unit dropdown only offers PUs effective at the form's
# START DATE, and 'Production Unit' starts 2002-01-01. My first run used 2000-01-01, so the value was not
# offered at all - the row saved with a different PU and I nearly reported an engine defect off my own bad
# test input. This is the value the merged suite uses (environment.py TEST_START_DATE_REFDD).
START = "2003-01-01"
results = {}


def a(s):
    return str(s).encode("ascii", "replace").decode("ascii")


def check(name, ok, detail=""):
    results[name] = (bool(ok), detail)
    print(a("   [%s] %-42s %s" % ("PASS" if ok else "FAIL", name, detail)))
    return ok


def db_one(sql, **kw):
    con = db._connect()
    cur = con.cursor()
    cur.execute(sql, kw)
    row = cur.fetchone()
    cur.close()
    con.close()
    return row


def cleanup():
    """Close any AUTOTEST row this script created (End Date = Start Date, EC's delete)."""
    con = db._connect()
    cur = con.cursor()
    cur.execute("select code from %s where code = :c and object_end_date is null" % VIEW, c=CODE)
    rows = [r[0] for r in cur.fetchall()]
    for c in rows:
        cur.execute("update %s set object_end_date = object_start_date where code = :c" % VIEW, c=c)
        print(a("   cleanup: closed %s (rowcount=%d)" % (c, cur.rowcount)))
    con.commit()
    cur.execute("select count(*) from %s where code = :c and object_end_date is null" % VIEW, c=CODE)
    left = cur.fetchone()[0]
    cur.close()
    con.close()
    return left


print(a("=== ITEM 1: parent_dd wiring validation on Area (live, self-cleaning) ==="))
pre = db_one("select count(*) from %s where code = :c and object_end_date is null" % VIEW, c=CODE)[0]
print(a("pre-run open rows for %s: %d" % (CODE, pre)))

try:
    with sync_playwright() as p:
        br = p.chromium.launch(headless=True, args=["--ignore-certificate-errors"])
        pg = br.new_context(ignore_https_errors=True,
                            viewport={"width": 1920, "height": 1080}).new_page()
        ec.login(pg, "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/",
                 os.environ.get("EC_USER", "sysadmin"), os.environ.get("EC_PASS", "sysadmin"))
        ec.open_object_screen(pg, SCREEN)
        pg.wait_for_timeout(2500)

        # nav: set the SAME PU the merged suite uses, then read back what the navigator holds
        ec.select_dropdown(pg, NAV_PU_DD, NAV_PU_VALUE)
        pg.wait_for_timeout(800)
        captured = pg.eval_on_selector('[id="%s"]' % NAV_PU_DD, "e => e.value")
        ec.click_go(pg)
        ec.wait_ajax(pg)
        check("navigator holds the PU", captured == NAV_PU_VALUE, "captured=%r" % captured)

        if ec.row_exists(pg, GRID, CODE):
            ec.closeObjectRecord(pg, GRID, CODE, START)
            ec.click_go(pg)

        # THE THING UNDER TEST: form parent dd bound to the CAPTURED value (what parent_dd generates)
        fields = [
            {"label": "Area Code", "value": CODE, "kind": "text"},
            {"label": "Area Name", "value": NAME, "kind": "text"},
            {"label": "Start Date", "value": START, "kind": "date"},
            {"label": "Op Production Unit", "value": captured, "kind": "dropdown"},
        ]
        ec.insertObjectRecord(pg, GRID, fields)
        err = ec.ec_error(pg)
        check("save raised no EC error", not err, err or "(none)")
        check("row LISTS in the grid (the untested half)", ec.wait_for_row(pg, GRID, CODE))
        check("row present in %s" % VIEW, db.code_present(VIEW, CODE))

        # The dropdown shows the PU NAME; the DB stores its CODE. Resolve the label to a code before
        # comparing - my first assertion compared 'Production Unit' (label) with 'EEAL' (code) and
        # reported a failure that did not exist.
        stored = db_one("select op_productionunit_code from %s where code = :c" % VIEW, c=CODE)
        expect = db_one("select code from ov_productionunit where name = :n", n=captured)
        check("DB parent == captured nav value (label resolved to code)",
              bool(stored) and bool(expect) and stored[0] == expect[0],
              "stored=%r expected=%r for name %r" % (stored[0] if stored else None,
                                                     expect[0] if expect else None, captured))

        ec.closeObjectRecord(pg, GRID, CODE, START)
        ec.click_go(pg)
        check("row absent from %s after End=Start" % VIEW, not db.code_present(VIEW, CODE))
        br.close()
finally:
    left = cleanup()
    check("self-clean: 0 open AUTOTEST rows left", left == 0, "open=%d" % left)

print(a("\n=== RESULT ==="))
ok = all(v[0] for v in results.values())
for k, (v, d) in results.items():
    print(a("   %-4s %s" % ("PASS" if v else "FAIL", k)))
print(a("OVERALL: %s  (%d/%d checks)" % ("PASS" if ok else "FAIL",
                                         sum(1 for v in results.values() if v[0]), len(results))))
sys.exit(0 if ok else 1)
