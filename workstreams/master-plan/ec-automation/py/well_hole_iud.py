"""Well Hole - IUD driver (thin). Reuses shared engine ec_object_iud.py + DbVerify.py.

OV-GM (grid manageObject:form:T_data) = navigator-GATED (cascade + GO before the grid loads). Built on the
gated-navigator capability (apply_ovgm_navigator). Fields by label. Extra dropdowns + Op Production Unit set
first-available (probe per screen - the nav PU is not necessarily a valid Op PU option).
Run headed: EC_HEADED=1 py -X utf8 workstreams/master-plan/ec-automation/py/well_hole_iud.py
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

SCREEN        = 'Well Hole'
GRID_DATA_ID  = "manageObject:form:T_data"
VIEW          = 'ov_well_hole'
CODE          = os.environ.get("EC_CODE", "AUTOTEST_WELL_HOLE_001")
START_DATE    = "2000-01-01"
END_DATE      = START_DATE
NAME          = 'AUTOTEST Well Hole 001'
NAME_UPD      = 'AUTOTEST Well Hole 001' + " UPDATED"

URL  = os.environ.get("EC_URL", "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/")
USER = os.environ.get("EC_USERNAME", os.environ.get("EC_USER", "sysadmin"))
PW   = os.environ.get("EC_PASSWORD", os.environ.get("EC_PASS", "sysadmin"))
HEADED = os.environ.get("EC_HEADED", "0") == "1"
SLOWMO = int(os.environ.get("EC_SLOWMO", "500")) if HEADED else 0
EVID = _ROOT / "tmp" / 'well_hole' / "evidence"
EVID.mkdir(parents=True, exist_ok=True)
results = {}


def shot(page, label):
    try:
        page.screenshot(path=str(EVID / ("we_" + label + ".png")))
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
            pu = ec.apply_ovgm_navigator(page)
            results["nav_pu"] = "PASS: PU=%r" % pu
            print("  navigator applied; top-parent PU =", repr(pu))
            assert pu, "navigator cascade returned no top-parent PU"

            insert_fields = [
                {"label": 'Well Hole Code', "value": CODE,       "kind": "text"},
                {"label": 'Well Hole Name', "value": NAME,       "kind": "text"},
                {"label": "Start Date", "value": START_DATE, "kind": "date"},
                {"label": "Op Production Unit", "value": "__FIRST__", "kind": "dropdown"},
            ]
            update_fields = [{"label": 'Well Hole Name', "value": NAME_UPD, "kind": "text"}]

            if ec.row_exists(page, GRID_DATA_ID, CODE):
                print("  pre-existing", CODE, "-> closing (End=Start) first")
                ec.closeObjectRecord(page, GRID_DATA_ID, CODE, END_DATE)

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

            print("=== DELETE (End=Start) ===")
            step(page, "delete_ui", lambda: ec.closeObjectRecord(page, GRID_DATA_ID, CODE, END_DATE))
            shot(page, "04_deleted")
            def _v_del():
                assert ec.wait_for_row_absent(page, GRID_DATA_ID, CODE), "still in grid"
                assert not db.code_present(VIEW, CODE), "still in DB view"
            step(page, "delete_db", _v_del)
            print("  DELETE verified (absent grid + DB)")

            residual = db.count_like(VIEW, "AUTOTEST")
            results["self_clean"] = "CLEAN (0 residual)" if residual == 0 else ("RESIDUAL=%d" % residual)
            print("  self-clean:", results["self_clean"])
            shot(page, "05_final")
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
        mark = "OK" if str(v).startswith(("PASS", "CLEAN")) else "X"
        if mark == "X" and not str(v).startswith("RESIDUAL"):
            ok = False
        print("  %s %-12s: %s" % (mark, k, v))
    print("Overall:", "ALL PASS" if ok else "FAILURES")
    print("Evidence:", EVID)
    sys.exit(0 if ok else 1)
