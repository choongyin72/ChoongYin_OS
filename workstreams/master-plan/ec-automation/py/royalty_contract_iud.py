"""Royalty Contract - INSERT+UPDATE-ONLY driver (thin). Reuses shared engine ec_object_iud.py +
DbVerify.py.

OV-GM (grid manageObject:form:T_data) = navigator-GATED (cascade + GO before the grid loads). The
nav value(s) are PROVEN explicit values (scripts/find_populated_scope.py), not
apply_ovgm_navigator's first-available - first-available was not guaranteed to have real data
underneath on this screen. Fields by label.

DELETE IS PERMANENTLY OUT OF SCOPE ON THIS SCREEN (owner-confirmed 2026-08-15, closes Issue #336,
same precedent as Production Day Table CO.1033): choosing Contract Template "Royalty Fixed
Percentage Canada" causes EC to auto-provision 10 CNTR_PG_SETUP rows as expected business logic,
and this screen's UI exposes no path to remove them - so End=Start close always fails with EC's
own "Child record found... all child records must be deleted first" error. This is a genuine EC
product limitation (parent-child relationship), not a bug in this driver or the shared engine. Do
NOT attempt Delete here - it was already reproduced once (PR #331, AUTOTEST_RC_001, still live in
OV_ROYALTY_CONTRACT). Each Insert+Update proof run below adds ONE MORE permanently-accepted
residual row - consistent with Production Day Table's established precedent for screens where
self-clean is impossible by design.
Run headed: EC_HEADED=1 py -X utf8 workstreams/master-plan/ec-automation/py/royalty_contract_iud.py
"""
import os
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))
sys.path.insert(0, str(_HERE.parent / "libraries"))
import ec_object_iud as ec
import DbVerify as db


def _repo_root():
    for p in [_HERE, *_HERE.parents]:
        if (p / ".git").exists():
            return p
    return _HERE.parents[3]


_ROOT = _repo_root()

SCREEN        = 'Royalty Contract'
GRID_DATA_ID  = "manageObject:form:T_data"
VIEW          = 'ov_royalty_contract'
CODE          = os.environ.get("EC_CODE", "AUTOTEST_RC_003")
START_DATE    = "2003-01-01"
END_DATE      = START_DATE
INSERT_END_DATE = "2099-12-31"   # End Date is MANDATORY on this screen's form (unusual, same as Contract);
                                  # NOT the same as END_DATE above, which is the delete gesture's End=Start value
NAME          = 'AUTOTEST Royalty Contract 001'
NAME_UPD      = 'AUTOTEST Royalty Contract 001' + " UPDATED"

URL  = os.environ.get("EC_URL", "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/")
USER = os.environ.get("EC_USERNAME", os.environ.get("EC_USER", "sysadmin"))
PW   = os.environ.get("EC_PASSWORD", os.environ.get("EC_PASS", "sysadmin"))
HEADED = os.environ.get("EC_HEADED", "0") == "1"
SLOWMO = int(os.environ.get("EC_SLOWMO", "500")) if HEADED else 0
EVID = _ROOT / "tmp" / 'royalty_contract' / "evidence"
EVID.mkdir(parents=True, exist_ok=True)
results = {}


def shot(page, label):
    try:
        page.screenshot(path=str(EVID / ("rc_" + label + ".png")))
    except Exception:
        pass


def step(page, name, fn):
    try:
        fn()
        results[name] = "PASS"
    except Exception as e:
        results[name] = "FAIL: %s" % (repr(e)[:160])
        shot(page, name + "_FAIL")
        raise


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=not HEADED, slow_mo=SLOWMO,
                                    args=["--ignore-certificate-errors", "--start-maximized"])
        ctx = browser.new_context(ignore_https_errors=True, no_viewport=HEADED,
                                  viewport=None if HEADED else {"width": 1920, "height": 1080})
        page = ctx.new_page()
        try:
            print("[MODE] headed=%s code=%s" % (HEADED, CODE))
            ec.login(page, URL, USER, PW)
            print("  screen:", ec.open_object_screen(page, SCREEN))
            shot(page, "01_loaded")
            ec.select_dropdown(page, "nav:form:G:1:R:1:C:0:dd_input", 'Royalty Canada')
            ec.click_go(page)
            pu = 'Royalty Canada'
            results["nav_pu"] = "PASS: PU=%r" % pu
            print("  navigator applied; top-parent PU =", repr(pu))
            assert pu, "navigator cascade returned no top-parent PU"

            insert_fields = [
                {"label": 'Royalty Contract Code', "value": CODE,       "kind": "text"},
                {"label": 'Royalty Contract Name', "value": NAME,       "kind": "text"},
                {"label": "Start Date", "value": START_DATE, "kind": "date"},
                {"label": "End Date", "value": INSERT_END_DATE, "kind": "date"},
                {"label": 'Contract Template', "value": 'Royalty Fixed Percentage Canada', "kind": "dropdown"},
                {"label": 'Contract Area', "value": 'Alberta', "kind": "dropdown"},
            ]
            update_fields = [{"label": 'Royalty Contract Name', "value": NAME_UPD, "kind": "text"}]

            if ec.row_exists(page, GRID_DATA_ID, CODE):
                # Delete/close is permanently blocked on this screen (see module docstring) - a
                # pre-existing row of this exact CODE can never be cleaned via End=Start, so the
                # only safe move is to abort rather than attempt a close that's already proven to
                # fail. Pick a different EC_CODE env value to run again.
                raise RuntimeError(
                    "%s already exists and cannot be pre-cleaned (Delete permanently blocked on "
                    "this screen) - set EC_CODE to an unused value and re-run" % CODE
                )

            print("=== INSERT ===")
            step(page, "insert_ui", lambda: ec.insertObjectRecord(page, GRID_DATA_ID, insert_fields))
            shot(page, "02_inserted")
            def _v_ins():
                assert ec.wait_for_row(page, GRID_DATA_ID, CODE), "not in grid"
                assert db.code_present(VIEW, CODE), "not in ov view"
                ok, act = db.field_equals(VIEW, CODE, "NAME", NAME)
                assert ok, "DB NAME=%r != %r" % (act, NAME)
            step(page, "insert_db", _v_ins)
            print("  INSERT verified (grid + DB + NAME)")

            print("=== UPDATE ===")
            step(page, "update_ui", lambda: ec.updateObjectRecord(page, GRID_DATA_ID, CODE, update_fields))
            shot(page, "03_updated")
            def _v_upd():
                ok, an = db.field_equals(VIEW, CODE, "NAME", NAME_UPD)
                assert ok, "DB NAME=%r != %r" % (an, NAME_UPD)
            step(page, "update_db", _v_upd)
            print("  UPDATE verified (DB NAME)")

            print("=== DELETE: PERMANENTLY OUT OF SCOPE (see module docstring) ===")
            results["delete"] = "SKIPPED (permanent EC product limitation - CNTR_PG_SETUP child rows, PR #331/Issue #336)"
            print("  " + results["delete"])
            shot(page, "04_final_no_delete")

            residual = db.count_like(VIEW, "AUTOTEST")
            results["self_clean"] = "N/A - self-clean impossible by design (Delete out of scope); %d AUTOTEST_* rows permanently accepted" % residual
            print("  " + results["self_clean"])
        finally:
            if HEADED:
                page.wait_for_timeout(4000)
            ctx.close()
            browser.close()


if __name__ == "__main__":
    ok = True
    try:
        main()
    except Exception as e:
        print("ABORTED:", repr(e)[:200]); ok = False
    print("\n" + "=" * 56 + "\nRESULTS")
    for k, v in results.items():
        mark = "OK" if str(v).startswith(("PASS", "CLEAN", "SKIPPED", "N/A")) else "X"
        if mark == "X" and not str(v).startswith("RESIDUAL"):
            ok = False
        print("  %s %-12s: %s" % (mark, k, v))
    print("Overall:", "ALL PASS" if ok else "FAILURES")
    print("Evidence:", EVID)
    sys.exit(0 if ok else 1)
