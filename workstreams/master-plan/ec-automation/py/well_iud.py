"""Well - IUD driver (thin). Reuses shared engine ec_object_iud.py + DbVerify.py.

OV-GM with a 5-dd navigator, but ONLY the standard 3-level cascade is needed (owner screenshot
2026-07-30): with P1 Production Unit -> P1 Area -> P1 Facility 1 + GO the grid lists wells while the
second-row dds (Well & Well Hookup / Well) stay EMPTY - the original '5th level empty' park was moot
under the P1 scope. Insert extra: Well Type (mandatory dropdown, first-available). Start Date
2020-01-01 (P1 wells effective 2010-01-01, DB-checked; OV_WELL confirmed via 'P1 W001 OP').
Run headed: EC_HEADED=1 py -X utf8 workstreams/master-plan/ec-automation/py/well_iud.py
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

# ---- screen config -----------------------------------------------------------
SCREEN        = "Well"
GRID_DATA_ID  = "manageObject:form:T_data"
VIEW          = "ov_well"
CODE          = os.environ.get("EC_CODE", "AUTOTEST_WE_001")
START_DATE    = "2020-01-01"
END_DATE      = START_DATE
NAME          = "AUTOTEST Well 001"
NAME_UPD      = "AUTOTEST Well 001 UPDATED"

# owner-provided working nav scope (screenshot 2026-07-30): 3 levels only, 2nd-row dds left empty
NAV_PU        = "P1 Production Unit"
NAV_AREA      = "P1 Area"
NAV_FC1       = "P1 Facility 1"

URL  = os.environ.get("EC_URL", "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/")
USER = os.environ.get("EC_USERNAME", os.environ.get("EC_USER", "sysadmin"))
PW   = os.environ.get("EC_PASSWORD", os.environ.get("EC_PASS", "sysadmin"))
HEADED = os.environ.get("EC_HEADED", "0") == "1"
SLOWMO = int(os.environ.get("EC_SLOWMO", "500")) if HEADED else 0
EVID = _ROOT / "tmp" / "well" / "evidence"
EVID.mkdir(parents=True, exist_ok=True)
results = {}


def shot(page, label):
    try:
        page.screenshot(path=str(EVID / f"we_{label}.png"))
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


def apply_well_navigator(page):
    """3-level cascade with SPECIFIC P1 values + GO; the 2nd-row dds (Well & Well Hookup / Well)
    are optional filters and stay EMPTY (owner screenshot ground truth)."""
    for col, val in ((1, NAV_PU), (2, NAV_AREA), (3, NAV_FC1)):
        ec.select_dropdown(page, "nav:form:G:0:R:1:C:%d:dd_input" % col, val)
        page.wait_for_timeout(700)
    ec.click_go(page)


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=not HEADED, slow_mo=SLOWMO,
                                    args=["--ignore-certificate-errors", "--start-maximized"])
        ctx = browser.new_context(ignore_https_errors=True, no_viewport=HEADED,
                                  viewport=None if HEADED else {"width": 1920, "height": 1080})
        page = ctx.new_page()
        try:
            print(f"[MODE] headed={HEADED} code={CODE}")
            ec.login(page, URL, USER, PW)
            print("  screen:", ec.open_object_screen(page, SCREEN))
            shot(page, "01_loaded")
            apply_well_navigator(page)
            results["nav_scope"] = "PASS: %s -> %s -> %s (2nd-row dds empty)" % (NAV_PU, NAV_AREA, NAV_FC1)
            print("  navigator applied:", results["nav_scope"])
            shot(page, "01b_nav_applied")

            insert_fields = [
                {"label": "Well Code",  "value": CODE,        "kind": "text"},
                {"label": "Well Name",  "value": NAME,        "kind": "text"},
                {"label": "Start Date", "value": START_DATE,  "kind": "date"},
                {"label": "Well Type",  "value": "__FIRST__", "kind": "dropdown"},
            ]
            update_fields = [{"label": "Well Name", "value": NAME_UPD, "kind": "text"}]

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
                assert ok, f"DB NAME={act!r} != {NAME!r}"
            step(page, "insert_db", _v_ins)
            print("  INSERT verified (grid + DB + NAME)")

            print("=== UPDATE ===")
            step(page, "update_ui", lambda: ec.updateObjectRecord(page, GRID_DATA_ID, CODE, update_fields))
            shot(page, "03_updated")
            def _v_upd():
                ok, an = db.field_equals(VIEW, CODE, "NAME", NAME_UPD)
                assert ok, f"DB NAME={an!r} != {NAME_UPD!r}"
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
            results["self_clean"] = "CLEAN (0 residual)" if residual == 0 else f"RESIDUAL={residual}"
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
        print(f"  {mark} {k:<12}: {v}")
    print("Overall:", "ALL PASS" if ok else "FAILURES")
    print("Evidence:", EVID)
    sys.exit(0 if ok else 1)
