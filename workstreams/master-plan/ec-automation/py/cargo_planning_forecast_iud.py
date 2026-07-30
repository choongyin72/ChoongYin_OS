"""Cargo Planning Forecast - IUD driver (thin). Reuses shared engine ec_object_iud.py + DbVerify.py.

EC Transport screen (treeview EC Transport>Cargo Planning>Forecast>Cargo Planning Forecast, BF CP.0030).
Custom layout (recon-verified 2026-07-31): nav = per-field groups nav:form:G:1..G:4:R:1:C:0 (PU ->
Area -> FC1 -> Storage) - SPECIFIC P1 values + Storage P1_CRUDE_STOR (owner screenshot); grid =
fcst:form:T_data; the circled new_fcst panel + COPY buttons = the copy-existing dialog (owner-
confirmed, NOT used); the standard tab:tabPanel:objectForm IS the insert form. Mandatory extra:
END DATE (unusual) - Start 2026-01-01 / End 2026-12-31 spans the nav date so the row lists.
Storage Name = nav Storage (parent-matching). View resolved EMPIRICALLY between the resolver's 2
candidates (OV_FCST_MNGR_FCST_LIST / OV_FORECAST_TRAN_CP) after insert.
Run headed: EC_HEADED=1 py -X utf8 workstreams/master-plan/ec-automation/py/cargo_planning_forecast_iud.py
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
SCREEN        = "Cargo Planning Forecast"
GRID_DATA_ID  = "fcst:form:T_data"
VIEW_CANDIDATES = ["ov_fcst_mngr_fcst_list", "ov_forecast_tran_cp"]
CODE          = os.environ.get("EC_CODE", "AUTOTEST_CPF_001")
START_DATE    = "2026-01-01"
END_DATE_INS  = "2026-12-31"   # mandatory at insert; spans the nav date 2026-07-29
NAME          = "AUTOTEST Cargo Planning Forecast 001"
NAME_UPD      = "AUTOTEST Cargo Planning Forecast 001 UPDATED"

NAV_PU        = "P1 Production Unit"
NAV_AREA      = "P1 Area"
NAV_FC1       = "P1 Facility 1"
NAV_STORAGE   = "P1_CRUDE_STOR"

URL  = os.environ.get("EC_URL", "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/")
USER = os.environ.get("EC_USERNAME", os.environ.get("EC_USER", "sysadmin"))
PW   = os.environ.get("EC_PASSWORD", os.environ.get("EC_PASS", "sysadmin"))
HEADED = os.environ.get("EC_HEADED", "0") == "1"
SLOWMO = int(os.environ.get("EC_SLOWMO", "500")) if HEADED else 0
EVID = _ROOT / "tmp" / "cargo_planning_forecast" / "evidence"
EVID.mkdir(parents=True, exist_ok=True)
results = {}
VIEW = None   # resolved after insert


def shot(page, label):
    try:
        page.screenshot(path=str(EVID / f"cpf_{label}.png"))
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


def apply_cpf_navigator(page):
    """Per-field nav groups G:1..G:4 (C:0) with SPECIFIC P1 values + Storage, then GO."""
    for g, val in ((1, NAV_PU), (2, NAV_AREA), (3, NAV_FC1), (4, NAV_STORAGE)):
        ec.select_dropdown(page, "nav:form:G:%d:R:1:C:0:dd_input" % g, val)
        page.wait_for_timeout(700)
    ec.click_go(page)


def main():
    global VIEW
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
            apply_cpf_navigator(page)
            results["nav_scope"] = "PASS: %s -> %s -> %s -> %s" % (NAV_PU, NAV_AREA, NAV_FC1, NAV_STORAGE)
            print("  navigator applied:", results["nav_scope"])
            shot(page, "01b_nav_applied")

            insert_fields = [
                {"label": "Cargo Planning Forecast Code", "value": CODE,         "kind": "text"},
                {"label": "Cargo Planning Forecast Name", "value": NAME,         "kind": "text"},
                {"label": "Start Date",                   "value": START_DATE,   "kind": "date"},
                {"label": "End Date",                     "value": END_DATE_INS, "kind": "date"},
                {"label": "Storage Name",                 "value": NAV_STORAGE,  "kind": "dropdown"},
            ]
            update_fields = [{"label": "Cargo Planning Forecast Name", "value": NAME_UPD, "kind": "text"}]

            if ec.row_exists(page, GRID_DATA_ID, CODE):
                print("  pre-existing", CODE, "-> closing (End=Start) first")
                ec.closeObjectRecord(page, GRID_DATA_ID, CODE, START_DATE)

            print("=== INSERT ===")
            step(page, "insert_ui", lambda: ec.insertObjectRecord(page, GRID_DATA_ID, insert_fields))
            shot(page, "02_inserted")
            def _v_ins():
                global VIEW
                assert ec.wait_for_row(page, GRID_DATA_ID, CODE), "not in grid"
                hits = [v for v in VIEW_CANDIDATES if db.code_present(v, CODE)]
                assert hits, "code in NEITHER candidate view %s" % VIEW_CANDIDATES
                VIEW = hits[0]
                print("  view resolved EMPIRICALLY:", VIEW, "(hits: %s)" % hits)
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

            print("=== DELETE (End=Start attempt 1) ===")
            step(page, "delete_ui", lambda: ec.closeObjectRecord(page, GRID_DATA_ID, CODE, START_DATE))
            shot(page, "04_deleted")
            def _v_del():
                assert ec.wait_for_row_absent(page, GRID_DATA_ID, CODE), "still in grid"
                assert not db.code_present(VIEW, CODE), "still in DB view"
            step(page, "delete_db", _v_del)
            print("  DELETE verified (absent grid + DB)")

            residual = sum(db.count_like(v, "AUTOTEST") for v in VIEW_CANDIDATES)
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
