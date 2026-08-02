"""Stream Item screen - Insert + Delete driver (thin). Uses the reusable engine
py/ec_object_iud.py (same folder). UPDATE IS DELIBERATELY OUT OF SCOPE for this
screen - see the note below; owner instruction 2026-08-02.

Screen quirks (see ec-ui-knowledge/screens/stream_item.md for full detail):
- The 12 fields the Save-error message lists as "...POPUP" (Stream Item Category,
  Product, Field, Company, Stream, Measurement Node, Calc. Method, Conversion
  Method, Master UOM Group, Daily/Monthly Accrual Method, Reporting Category) are
  ordinary autocomplete DROPDOWNS on the live form, not "Pick from EC Object"
  popups - `ec.select_dropdown(..., '__FIRST__')` picks the first available option.
- Name is server-derived on Save (EC's own online help confirms this: left blank,
  the system auto-generates it from Category/Product/Field/[Well/]Company). Any
  typed value is discarded - Name is still filled here only because it is a
  mandatory-to-Save field, not because the value sticks.
- UPDATE is skipped: any Save on `updateAttributes` (even an unrelated field like
  Description) fails with EC's own error "Cannot run schedule job UpdateStreamItem
  because it has not been configured" - a genuine, EC-documented sandbox
  configuration gap (BF VO.0031 - Daily SI Pending Calculation scheduler job is not
  enabled here), not a code defect. Reproduced live 3x, confirmed against EC's own
  online help page. Owner instruction: skip Update, cover Insert + Delete only.
- The screen's own navigator GO button has the non-standard id `buttongo:form:B`
  (not the generic `button:form:B` the shared engine's `click_go()` expects) - this
  driver clicks it directly rather than relying on `click_go()`'s Refresh fallback.
- Grid id for this custom-URL OV is `nav:form:T_data` (confirmed live, not the
  generic `manage_object_nav_nav:form:T_data`/`manageObject:form:T_data`).

Run headed:   EC_HEADED=1 py -X utf8 workstreams/master-plan/ec-automation/py/stream_item_iud.py
Env: EC_URL, EC_USERNAME/EC_USER, EC_PASSWORD/EC_PASS (default sandbox + sysadmin);
     EC_DB_DSN/USER/PASS for ground truth; EC_HEADED=1 shows the browser.
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

# ---- screen config (the only per-screen part) --------------------------------
SCREEN       = "Stream Item"
GRID_DATA_ID = "nav:form:T_data"
VIEW         = "OV_STREAM_ITEM"
CODE         = os.environ.get("EC_CODE", "AUTOTEST_SI_001")
START_DATE   = "2003-01-01"
END_DATE     = START_DATE                                        # EC delete = End = Start

POPUP_LABELS = [
    "Stream Item Category", "Product", "Field", "Company", "Stream",
    "Measurement Node", "Calc. Method", "Conversion Method", "Master UOM Group",
    "Daily Accrual Method", "Monthly Accrual Method", "Reporting Category",
]

INSERT_FIELDS = (
    [{"label": "Stream Item Code", "value": CODE, "kind": "text"},
     {"label": "Start Date", "value": START_DATE, "kind": "date"}]
    + [{"label": lbl, "value": "__FIRST__", "kind": "dropdown"} for lbl in POPUP_LABELS]
    + [{"label": "Name", "value": "AUTOTEST SI (server-derived, ignored)", "kind": "text"}]
)

# ---- env ---------------------------------------------------------------------
URL  = os.environ.get("EC_URL", "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/")
USER = os.environ.get("EC_USERNAME", os.environ.get("EC_USER", "sysadmin"))
PW   = os.environ.get("EC_PASSWORD", os.environ.get("EC_PASS", "sysadmin"))
HEADED = os.environ.get("EC_HEADED", "0") == "1"
SLOWMO = int(os.environ.get("EC_SLOWMO", "500")) if HEADED else 0
EVID = _ROOT / "tmp" / "stream_item_iud" / "evidence"
EVID.mkdir(parents=True, exist_ok=True)

results = {}


def shot(page, label):
    try:
        page.screenshot(path=str(EVID / f"stream_item_{label}.png"))
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


def _go(page):
    """This screen's navigator GO has the non-standard id buttongo:form:B - the shared
    engine's click_go() only knows button:form:B / the toolbar Refresh fallback, neither
    of which reliably re-lists a just-inserted row on this screen's grid tab."""
    page.locator("#buttongo\\:form\\:B").click()
    ec.wait_ajax(page)
    page.wait_for_timeout(800)


def _insert(page, grid_data_id, fields):
    """Thin twin of ec.insertObjectRecord() that calls this screen's real GO (_go)
    instead of the engine's click_go() (which doesn't know buttongo:form:B)."""
    ec._open_new_object(page)
    for f in fields:
        r = ec._resolve_field(page, "objectForm", f["label"])
        if not r:
            raise RuntimeError("insert: field label not found: %s" % f["label"])
        ec.fill_field(page, r["id"], f["value"], r["kind"])
    ec.save(page)
    err = ec.ec_error(page)
    _go(page)
    if err:
        raise RuntimeError("insert save error: %s" % err)


def _close(page, grid_data_id, code, end_date):
    """Thin twin of ec.closeObjectRecord() using this screen's real GO (_go)."""
    if not ec.select_row(page, grid_data_id, code):
        raise RuntimeError("delete: row not found: %s" % code)
    ec.fill_field(page, ec.END_DATE_ID, end_date, "date")
    ec.save(page)
    err = ec.ec_error(page)
    _go(page)
    if err:
        raise RuntimeError("delete save error: %s" % err)


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
            _go(page)
            shot(page, "01_loaded")

            # -- pre-clean (idempotent): if a prior AUTOTEST row lingers, close it first
            if ec.row_exists(page, GRID_DATA_ID, CODE):
                print("  pre-existing", CODE, "-> closing (End=Start) before test")
                _close(page, GRID_DATA_ID, CODE, END_DATE)
                ec.open_object_screen(page, SCREEN)
                _go(page)

            # -- INSERT
            print("=== INSERT ===")
            step(page, "insert_ui", lambda: _insert(page, GRID_DATA_ID, INSERT_FIELDS))
            shot(page, "02_inserted")

            def _v_ins():
                assert ec.row_exists(page, GRID_DATA_ID, CODE), "not in grid"
                assert db.code_present(VIEW, CODE), "not in OV_STREAM_ITEM"
            step(page, "insert_db", _v_ins)
            print("  INSERT verified (grid + OV_STREAM_ITEM)")

            # -- UPDATE: SKIPPED (owner instruction 2026-08-02) - EC scheduler job
            # 'UpdateStreamItem' (BF VO.0031 - Daily SI Pending Calculation) is not
            # configured in this sandbox; any Save on updateAttributes fails with
            # EC's own "Cannot run schedule job..." error, confirmed live 3x + against
            # EC's own online help page. See ec-ui-knowledge/screens/stream_item.md.
            results["update_ui"] = "SKIPPED (EC scheduler job UpdateStreamItem not configured)"
            print("=== UPDATE: SKIPPED (see note) ===")

            # -- DELETE (End Date = Start Date)
            print("=== DELETE (End=Start) ===")
            step(page, "delete_ui", lambda: _close(page, GRID_DATA_ID, CODE, END_DATE))
            shot(page, "03_deleted")

            def _v_del():
                assert not ec.row_exists(page, GRID_DATA_ID, CODE), "still in grid"
                assert not db.code_present(VIEW, CODE), "still in OV_STREAM_ITEM"
            step(page, "delete_db", _v_del)
            print("  DELETE verified (absent grid + OV_STREAM_ITEM)")

            # -- self-clean confirm
            residual = db.count_like(VIEW, "AUTOTEST_SI_")
            results["self_clean"] = "CLEAN (0 residual)" if residual == 0 else f"RESIDUAL={residual}"
            print("  self-clean:", results["self_clean"])
            shot(page, "04_final")
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
        mark = "OK" if str(v).startswith(("PASS", "CLEAN", "SKIPPED")) else "X"
        if mark == "X" and not str(v).startswith("RESIDUAL"):
            ok = False
        print(f"  {mark} {k:<12}: {v}")
    print("Overall:", "ALL PASS" if ok else "FAILURES")
    print("Evidence:", EVID)
    sys.exit(0 if ok else 1)
