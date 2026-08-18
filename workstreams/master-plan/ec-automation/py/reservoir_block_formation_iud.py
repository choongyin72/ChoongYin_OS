"""Reservoir Block Formation (CO.0137) - MULTI-OBJECT IUD driver.

RBF is a JUNCTION object: its Reservoir Block + Reservoir Formation are dependent dropdowns (Formation
options only appear once a Block is chosen), so a valid pair can't be picked from unrelated seed data.
Per the owner's flow: create a fresh Reservoir Block + Reservoir Formation, link them via RBF, verify
I-U-D, then tear down in reverse dependency order (RBF -> Formation -> Block). All 3 DB-verified, self-clean.
Reuses the shared engine py/ec_object_iud.py + DbVerify.py. Dropdowns reference the parents BY NAME.
Run: EC_HEADED=0 py -X utf8 workstreams/master-plan/ec-automation/py/reservoir_block_formation_iud.py
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
GRID = "manage_object_nav_nav:form:T_data"
SD = "2000-01-01"

# --- three related objects (unique-per-run kept short for CODE columns) ---
BLK_SCREEN, BLK_VIEW = "Reservoir Block", "ov_resv_block"
BLK_CODE, BLK_NAME = "AUTOTEST_RBFB_001", "AUTOTEST RBF Block 001"
FRM_SCREEN, FRM_VIEW = "Reservoir Formation", "ov_resv_formation"
FRM_CODE, FRM_NAME = "AUTOTEST_RBFF_001", "AUTOTEST RBF Formation 001"
RBF_SCREEN, RBF_VIEW = "Reservoir Block Formation", "ov_resv_block_formation"
RBF_CODE, RBF_NAME, RBF_NAME_UPD = "AUTOTEST_RBF_001", "AUTOTEST RBF 001", "AUTOTEST RBF 001 UPDATED"

URL = os.environ.get("EC_URL", "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/")
USER = os.environ.get("EC_USERNAME", os.environ.get("EC_USER", "sysadmin"))
PW = os.environ.get("EC_PASSWORD", os.environ.get("EC_PASS", "sysadmin"))
HEADED = os.environ.get("EC_HEADED", "0") == "1"
SLOWMO = int(os.environ.get("EC_SLOWMO", "500")) if HEADED else 0
EVID = _ROOT / "tmp" / "reservoir_block_formation" / "evidence"
EVID.mkdir(parents=True, exist_ok=True)
results = {}


def shot(page, label):
    try:
        page.screenshot(path=str(EVID / ("rbf_%s.png" % label)))
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


def _open(page, screen):
    ec.open_object_screen(page, screen)
    ec.click_go(page)


def _insert(page, screen, fields):
    _open(page, screen)
    ec.insertObjectRecord(page, GRID, fields)


def _close(page, screen, code):
    _open(page, screen)
    if ec.row_exists(page, GRID, code):
        ec.closeObjectRecord(page, GRID, code, SD)


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=not HEADED, slow_mo=SLOWMO,
                                    args=["--ignore-certificate-errors", "--start-maximized"])
        ctx = browser.new_context(ignore_https_errors=True, no_viewport=HEADED,
                                  viewport=None if HEADED else {"width": 1920, "height": 1080})
        page = ctx.new_page()
        try:
            print("[MODE] headed=%s" % HEADED)
            ec.login(page, URL, USER, PW)
            # pre-clean (reverse dependency order) in case a prior run left rows
            for scr, code in [(RBF_SCREEN, RBF_CODE), (FRM_SCREEN, FRM_CODE), (BLK_SCREEN, BLK_CODE)]:
                _close(page, scr, code)

            print("=== 1. INSERT Reservoir Block ===")
            step(page, "block_insert", lambda: _insert(page, BLK_SCREEN, [
                {"label": "Reservoir Block Code", "value": BLK_CODE, "kind": "text"},
                {"label": "Reservoir Block Name", "value": BLK_NAME, "kind": "text"},
                {"label": "Start Date", "value": SD, "kind": "date"}]))
            step(page, "block_db", lambda: (_ for _ in ()).throw(AssertionError("block not in ov")) if not db.code_present(BLK_VIEW, BLK_CODE) else None)
            shot(page, "01_block")

            print("=== 2. INSERT Reservoir Formation ===")
            step(page, "formation_insert", lambda: _insert(page, FRM_SCREEN, [
                {"label": "Reservoir Formation Code", "value": FRM_CODE, "kind": "text"},
                {"label": "Reservoir Formation Name", "value": FRM_NAME, "kind": "text"},
                {"label": "Start Date", "value": SD, "kind": "date"}]))
            step(page, "formation_db", lambda: (_ for _ in ()).throw(AssertionError("formation not in ov")) if not db.code_present(FRM_VIEW, FRM_CODE) else None)
            shot(page, "02_formation")

            print("=== 3. INSERT RBF (Block selected first -> Formation populates) ===")
            step(page, "rbf_insert", lambda: _insert(page, RBF_SCREEN, [
                {"label": "Resv Block Formation Code", "value": RBF_CODE, "kind": "text"},
                {"label": "Resv Block Formation Name", "value": RBF_NAME, "kind": "text"},
                {"label": "Start Date", "value": SD, "kind": "date"},
                {"label": "Reservoir Block", "value": BLK_NAME, "kind": "dropdown"},
                # "Reservoir Formation"'s dropdown keys its data-item-label by CODE, not Name -
                # unlike its sibling "Reservoir Block" above, which keys by Name (confirmed live,
                # round-6 stability testing, docs/JOURNAL-engine-stability-round6.md). This driver
                # previously searched by FRM_NAME here, which the shared select_dropdown() silently
                # treats as "value not found -> fall back to first available" rather than raising -
                # so every historical PASS from this driver proved A Formation was linked, never
                # proved it was the INTENDED one (Issue #401).
                {"label": "Reservoir Formation", "value": FRM_CODE, "kind": "dropdown"}]))
            def _v_rbf_ins():
                assert ec.wait_for_row(page, GRID, RBF_CODE), "RBF not in grid"
                assert db.code_present(RBF_VIEW, RBF_CODE), "RBF not in ov"
                ok, act = db.field_equals(RBF_VIEW, RBF_CODE, "NAME", RBF_NAME)
                assert ok, "RBF NAME=%r != %r" % (act, RBF_NAME)
            step(page, "rbf_insert_db", _v_rbf_ins)
            shot(page, "03_rbf_inserted")

            print("=== 4. UPDATE RBF name ===")
            step(page, "rbf_update", lambda: (ec.open_object_screen(page, RBF_SCREEN), ec.click_go(page),
                  ec.updateObjectRecord(page, GRID, RBF_CODE, [{"label": "Resv Block Formation Name", "value": RBF_NAME_UPD, "kind": "text"}]))[-1])
            def _v_rbf_upd():
                ok, act = db.field_equals(RBF_VIEW, RBF_CODE, "NAME", RBF_NAME_UPD)
                assert ok, "RBF NAME=%r != %r" % (act, RBF_NAME_UPD)
            step(page, "rbf_update_db", _v_rbf_upd)
            shot(page, "04_rbf_updated")

            print("=== 5-7. TEARDOWN (RBF -> Formation -> Block) ===")
            step(page, "rbf_delete", lambda: _close(page, RBF_SCREEN, RBF_CODE))
            step(page, "rbf_delete_db", lambda: (_ for _ in ()).throw(AssertionError("RBF still present")) if db.code_present(RBF_VIEW, RBF_CODE) else None)
            step(page, "formation_delete", lambda: _close(page, FRM_SCREEN, FRM_CODE))
            step(page, "formation_delete_db", lambda: (_ for _ in ()).throw(AssertionError("formation still present")) if db.code_present(FRM_VIEW, FRM_CODE) else None)
            step(page, "block_delete", lambda: _close(page, BLK_SCREEN, BLK_CODE))
            step(page, "block_delete_db", lambda: (_ for _ in ()).throw(AssertionError("block still present")) if db.code_present(BLK_VIEW, BLK_CODE) else None)
            shot(page, "05_torndown")

            residual = db.count_like(RBF_VIEW, "AUTOTEST") + db.count_like(FRM_VIEW, "AUTOTEST") + db.count_like(BLK_VIEW, "AUTOTEST")
            results["self_clean"] = "CLEAN (0 residual)" if residual == 0 else ("RESIDUAL=%d" % residual)
            print("  self-clean:", results["self_clean"])
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
        if mark == "X":
            ok = False
        print("  %s %-20s: %s" % (mark, k, v))
    print("Overall:", "ALL PASS" if ok else "FAILURES")
    print("Evidence:", EVID)
    sys.exit(0 if ok else 1)
