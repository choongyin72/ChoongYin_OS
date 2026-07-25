"""Bank screen - IUD driver (thin). Uses the reusable engine ec-ui-knowledge/lib/ec_object_iud.py.

This is the PER-SCREEN template: to cover a new OV object screen, copy this file, change
SCREEN / GRID_DATA_ID / VIEW / the field_maps. The engine + DB-verify never change.

Run headed:   EC_HEADED=1 py -X utf8 ec-ui-knowledge/screens/bank_iud.py
Env: EC_URL, EC_USERNAME/EC_USER, EC_PASSWORD/EC_PASS (default sandbox + sysadmin);
     EC_DB_DSN/USER/PASS for ground truth; EC_HEADED=1 shows the browser.
"""
import os
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

_ROOT = Path(__file__).resolve().parents[2]                       # C:\Projects\ChoongYin_OS
sys.path.insert(0, str(_ROOT / "ec-ui-knowledge" / "lib"))
import ec_object_iud as ec
import ec_db_verify as db

# ---- screen config (the only per-screen part) --------------------------------
SCREEN        = "Bank"
GRID_DATA_ID  = "manage_object_nav_nav:form:T_data"
VIEW          = "ov_bank"
CODE          = os.environ.get("EC_CODE", "AUTOTEST_BNK_001")
START_DATE    = "2000-01-01"
END_DATE      = START_DATE                                        # EC delete = End = Start
NAME          = "AUTOTEST Bank 001"
NAME_UPD      = "AUTOTEST Bank 001 UPDATED"
DESC          = "AUTOTEST desc"
DESC_UPD      = "AUTOTEST desc UPDATED"

INSERT_FIELDS = [
    {"label": "Code",        "value": CODE,       "kind": "text"},
    {"label": "Name",        "value": NAME,       "kind": "text"},
    {"label": "Start Date",  "value": START_DATE, "kind": "date"},
    {"label": "Description", "value": DESC,       "kind": "text"},
]
UPDATE_FIELDS = [
    {"label": "Name",        "value": NAME_UPD,   "kind": "text"},
    {"label": "Description", "value": DESC_UPD,   "kind": "text"},
]

# ---- env ---------------------------------------------------------------------
URL  = os.environ.get("EC_URL", "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/")
USER = os.environ.get("EC_USERNAME", os.environ.get("EC_USER", "sysadmin"))
PW   = os.environ.get("EC_PASSWORD", os.environ.get("EC_PASS", "sysadmin"))
HEADED = os.environ.get("EC_HEADED", "0") == "1"
SLOWMO = int(os.environ.get("EC_SLOWMO", "500")) if HEADED else 0
EVID = _ROOT / "tmp" / "bank_iud" / "evidence"
EVID.mkdir(parents=True, exist_ok=True)

results = {}


def shot(page, label):
    try:
        page.screenshot(path=str(EVID / f"bank_{label}.png"))
    except Exception:
        pass


def step(page, name, fn):
    """Run a step; screenshot + record on failure, never swallow the reason."""
    try:
        fn()
        results[name] = "PASS"
    except Exception as e:
        results[name] = "FAIL: %s" % (repr(e)[:160])
        shot(page, name + "_FAIL")
        raise


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=not HEADED, slow_mo=SLOWMO,
            args=["--ignore-certificate-errors", "--start-maximized"],
        )
        ctx = browser.new_context(ignore_https_errors=True, no_viewport=HEADED,
                                  viewport=None if HEADED else {"width": 1920, "height": 1080})
        page = ctx.new_page()
        try:
            print(f"[MODE] headed={HEADED} code={CODE}")
            ec.login(page, URL, USER, PW)
            lbl = ec.open_object_screen(page, SCREEN)
            print("  screen:", lbl)
            shot(page, "01_loaded")

            # -- pre-clean (idempotent): if a prior AUTOTEST row lingers, close it first
            if ec.row_exists(page, GRID_DATA_ID, CODE):
                print("  pre-existing", CODE, "-> closing (End=Start) before test")
                ec.closeObjectRecord(page, GRID_DATA_ID, CODE, END_DATE)
                ec.open_object_screen(page, SCREEN)

            # -- INSERT
            print("=== INSERT ===")
            step(page, "insert_ui", lambda: ec.insertObjectRecord(page, GRID_DATA_ID, INSERT_FIELDS))
            shot(page, "02_inserted")
            def _v_ins():
                assert ec.row_exists(page, GRID_DATA_ID, CODE), "not in grid"
                assert db.is_present(VIEW, CODE), "not in ov_bank"
                ok_n, act = db.field_equals(VIEW, CODE, "NAME", NAME)
                assert ok_n, f"DB NAME={act!r} != {NAME!r}"
            step(page, "insert_db", _v_ins)
            print("  INSERT verified (grid + ov_bank + NAME)")

            # -- UPDATE
            print("=== UPDATE ===")
            step(page, "update_ui", lambda: ec.updateObjectRecord(page, GRID_DATA_ID, CODE, UPDATE_FIELDS))
            shot(page, "03_updated")
            def _v_upd():
                ok_n, an = db.field_equals(VIEW, CODE, "NAME", NAME_UPD)
                ok_d, ad = db.field_equals(VIEW, CODE, "DESCRIPTION", DESC_UPD)
                assert ok_n, f"DB NAME={an!r} != {NAME_UPD!r}"
                assert ok_d, f"DB DESCRIPTION={ad!r} != {DESC_UPD!r}"
            step(page, "update_db", _v_upd)
            print("  UPDATE verified (ov_bank NAME + DESCRIPTION)")

            # -- DELETE (End Date = Start Date)
            print("=== DELETE (End=Start) ===")
            step(page, "delete_ui", lambda: ec.closeObjectRecord(page, GRID_DATA_ID, CODE, END_DATE))
            shot(page, "04_deleted")
            def _v_del():
                assert not ec.row_exists(page, GRID_DATA_ID, CODE), "still in grid"
                assert not db.is_present(VIEW, CODE), "still in ov_bank"
            step(page, "delete_db", _v_del)
            print("  DELETE verified (absent grid + ov_bank)")

            # -- self-clean confirm
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
        print("ABORTED:", repr(e)[:200])
        ok = False
    print("\n" + "=" * 56 + "\nRESULTS")
    for k, v in results.items():
        mark = "OK" if str(v).startswith(("PASS", "CLEAN")) else "X"
        if mark == "X" and not str(v).startswith("RESIDUAL"):
            ok = False
        print(f"  {mark} {k:<12}: {v}")
    print("Overall:", "ALL PASS" if ok else "FAILURES")
    print("Evidence:", EVID)
    sys.exit(0 if ok else 1)
