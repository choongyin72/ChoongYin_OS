"""Lifting Account - IUD driver (thin). Reuses shared engine ec_object_iud.py + DbVerify.py.

OV-GM 4-LEVEL nav variant: standard cascade (Production Unit -> Area -> Facility Class 1, C:1..3)
PLUS a mandatory Storage dropdown on a SECOND navigator row (nav:form:G:0:R:3:C:0) - the level that
is EMPTY under the first-available AS1 path (why the generic apply_ovgm_navigator failed). Owner-
provided working scope: P1 Production Unit -> P1 Area -> P1 Facility 1 -> Storage P1_CRUDE_STOR.
Insert extras: Company Name (first-available) + Storage Name = the nav storage (parent-matching rule,
or the row never lists). Start Date 2020-01-01 (P1_CRUDE_STOR effective 2010-01-01; 146 companies
effective - DB-checked).
Run headed: EC_HEADED=1 py -X utf8 workstreams/master-plan/ec-automation/py/lifting_account_iud.py
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
SCREEN        = "Lifting Account"
GRID_DATA_ID  = "manageObject:form:T_data"
VIEW          = "ov_lifting_account"
CODE          = os.environ.get("EC_CODE", "AUTOTEST_LA_001")
START_DATE    = "2020-01-01"
END_DATE      = START_DATE
NAME          = "AUTOTEST Lifting Account 001"
NAME_UPD      = "AUTOTEST Lifting Account 001 UPDATED"

# owner-provided nav scope (4th level empty under first-available AS1 path)
NAV_PU        = "P1 Production Unit"
NAV_AREA      = "P1 Area"
NAV_FC1       = "P1 Facility 1"
NAV_STORAGE   = "P1_CRUDE_STOR"
NAV_STORAGE_DD = "nav:form:G:0:R:3:C:0:dd_input"   # second nav row (recon-verified id)

URL  = os.environ.get("EC_URL", "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/")
USER = os.environ.get("EC_USERNAME", os.environ.get("EC_USER", "sysadmin"))
PW   = os.environ.get("EC_PASSWORD", os.environ.get("EC_PASS", "sysadmin"))
HEADED = os.environ.get("EC_HEADED", "0") == "1"
SLOWMO = int(os.environ.get("EC_SLOWMO", "500")) if HEADED else 0
EVID = _ROOT / "tmp" / "lifting_account" / "evidence"
EVID.mkdir(parents=True, exist_ok=True)
results = {}


def shot(page, label):
    try:
        page.screenshot(path=str(EVID / f"la_{label}.png"))
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


def apply_lifting_account_navigator(page):
    """4-level nav with SPECIFIC owner-provided values: 3-col cascade on row 1 + Storage dd on row 3, then GO."""
    for col, val in ((1, NAV_PU), (2, NAV_AREA), (3, NAV_FC1)):
        ec.select_dropdown(page, "nav:form:G:0:R:1:C:%d:dd_input" % col, val)
        page.wait_for_timeout(700)
    ec.select_dropdown(page, NAV_STORAGE_DD, NAV_STORAGE)
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
            apply_lifting_account_navigator(page)
            results["nav_scope"] = "PASS: %s -> %s -> %s -> %s" % (NAV_PU, NAV_AREA, NAV_FC1, NAV_STORAGE)
            print("  navigator applied:", results["nav_scope"])
            shot(page, "01b_nav_applied")

            insert_fields = [
                {"label": "Lifting Account Code", "value": CODE,        "kind": "text"},
                {"label": "Lifting Account Name", "value": NAME,        "kind": "text"},
                {"label": "Start Date",           "value": START_DATE,  "kind": "date"},
                {"label": "Company Name",         "value": "__FIRST__", "kind": "dropdown"},
                # parent-matching: form Storage Name = nav Storage or the row never lists under this scope
                {"label": "Storage Name",         "value": NAV_STORAGE, "kind": "dropdown"},
            ]
            update_fields = [{"label": "Lifting Account Name", "value": NAME_UPD, "kind": "text"}]

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
