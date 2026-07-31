"""Truck - IUD driver (thin). Reuses shared engine ec_object_iud.py + DbVerify.py.

PLAIN OV (Bank family, grid manage_object_nav_nav:form:T_data): navigator is date-only - no mandatory
cascade, just GO to populate the grid. Fields resolved BY LABEL; extra mandatory dropdowns set
first-available. DELETE = End Date = Start Date. Template: bank_iud.py / disposition_type_iud.py.
Run headed: EC_HEADED=1 py -X utf8 workstreams/master-plan/ec-automation/py/truck_iud.py
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

SCREEN        = 'Truck'
GRID_DATA_ID  = "truck_object:form:T_data"
VIEW          = 'ov_truck'
CODE          = os.environ.get("EC_CODE", "AUTOTEST_TK_001")
START_DATE    = "2000-01-01"
END_DATE      = START_DATE
NAME          = 'AUTOTEST Truck 001'
NAME_UPD      = 'AUTOTEST Truck 001' + " UPDATED"

URL  = os.environ.get("EC_URL", "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/")
USER = os.environ.get("EC_USERNAME", os.environ.get("EC_USER", "sysadmin"))
PW   = os.environ.get("EC_PASSWORD", os.environ.get("EC_PASS", "sysadmin"))
HEADED = os.environ.get("EC_HEADED", "0") == "1"
SLOWMO = int(os.environ.get("EC_SLOWMO", "500")) if HEADED else 0
EVID = _ROOT / "tmp" / 'truck' / "evidence"
EVID.mkdir(parents=True, exist_ok=True)
results = {}


def shot(page, label):
    try:
        page.screenshot(path=str(EVID / ("tk_" + label + ".png")))
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


def commit_unsaved_changes(page):
    """Plain-OV screens pop an 'UNSAVED CHANGES' dialog (YES/NO) when a GO/navigation happens with a
    pending edit - e.g. right after the End Date = Start Date close. It BLOCKS the GO button until
    answered. YES commits the pending change (which is exactly the intended delete). Returns True if
    a dialog was present."""
    for sel in ("xpath=//button[normalize-space(.)='YES']",
                "xpath=//button[normalize-space(.)='Yes']"):
        b = page.locator(sel)
        if b.count() and b.first.is_visible():
            b.first.click()
            ec.wait_ajax(page)
            page.wait_for_timeout(800)
            return True
    return False


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
            ec.click_go(page)   # date-only navigator: GO populates the grid
            results["nav"] = "PASS: date-only navigator + GO"
            print("  grid populated via GO (plain OV)")

            insert_fields = [
                {"label": 'Truck Code', "value": CODE,       "kind": "text"},
                {"label": 'Truck Name', "value": NAME,       "kind": "text"},
                {"label": "Start Date", "value": START_DATE, "kind": "date"},
                {"label": 'Licence Plate No', "value": 'AUTOTEST-PLATE-001', "kind": "text"},
                {"label": 'Tractor Gross Vehicle Quantity', "value": '1000', "kind": "text"},
                {"label": 'Vehicle Gross Combined Quantity', "value": '2000', "kind": "text"},
                {"label": 'Unladen Truck Quantity', "value": '500', "kind": "text"},
                {"label": 'UOM', "value": "__FIRST__", "kind": "dropdown"},
                {"label": 'Transport Company', "value": "__FIRST__", "kind": "dropdown"},
            ]
            update_fields = [{"label": 'Truck Name', "value": NAME_UPD, "kind": "text"}]

            if ec.row_exists(page, GRID_DATA_ID, CODE):
                print("  pre-existing", CODE, "-> closing (End=Start) first")
                ec.closeObjectRecord(page, GRID_DATA_ID, CODE, END_DATE)
                commit_unsaved_changes(page)
                ec.click_go(page)   # plain OV: re-query the grid after the pre-clean
                commit_unsaved_changes(page)

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
            def _delete():
                ec.closeObjectRecord(page, GRID_DATA_ID, CODE, END_DATE)
                commit_unsaved_changes(page)
            step(page, "delete_ui", _delete)
            shot(page, "04_deleted")
            def _v_del():
                # plain OV: the grid only drops the closed row after an explicit GO re-query
                ec.click_go(page)
                commit_unsaved_changes(page)
                assert ec.wait_for_row_absent(page, GRID_DATA_ID, CODE), "still in grid after GO"
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
