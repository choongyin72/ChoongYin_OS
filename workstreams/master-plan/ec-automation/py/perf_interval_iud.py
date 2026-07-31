"""Perforation Interval - IUD driver (thin). Reuses shared engine ec_object_iud.py + DbVerify.py.

OV-GM 7-group nav + mandatory POPUP (inner-GO type) + mandatory dropdown. Recon facts (2026-07-31,
all executed):
 - nav = PER-FIELD groups nav:form:G:1..G:7:R:1:C:0. Used: G:1 PU / G:2 Area / G:3 Facility Class 1 /
   G:4 **P1 W008 OP** (real well) / **G:6 P1 W008 WB001** (well bore) / **G:7 P1 W008 WB001 WBI001**
   (well bore interval). **G:5 returns ZERO options** (unusable filter, skipped - 4th screen with
   this quirk). Grid then shows 'No records found' (that interval has no perforations yet - our
   insert is the first row).
 - form: mandatory 'Well Bore Interval' POPUP (pin R:6). Its frame is well_bore_interval_gm_popup:
   it INHERITS the outer nav scope (G:1-G:4/G:6 pre-filled, recon-verified) but its list grid
   `Objects:form:T_data` is EMPTY until the popup's own **inner GO (button:form:B)** is clicked -
   the generic engine helper waits on PopupList and never drives GO, so it reports a false
   "empty source list". Screen-local picker below.
 - form: mandatory 'Reservoir Block Formation' dropdown (R:7) -> first-available.
Run headed: EC_HEADED=1 py -X utf8 workstreams/master-plan/ec-automation/py/perf_interval_iud.py
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

SCREEN        = "Perforation Interval"
GRID_DATA_ID  = "manageObject:form:T_data"
VIEW          = "ov_perf_interval"
CODE          = os.environ.get("EC_CODE", "AUTOTEST_PI_001")
START_DATE    = "2020-01-01"
END_DATE      = START_DATE
NAME          = "AUTOTEST Perf Interval 001"
NAME_UPD      = "AUTOTEST Perf Interval 001 UPDATED"

NAV = ((1, "P1 Production Unit"), (2, "P1 Area"), (3, "P1 Facility 1"),
       (4, "P1 W008 OP"), (6, "P1 W008 WB001"), (7, "P1 W008 WB001 WBI001"))
POPUP_GRID = "Objects:form:T_data"
NAV_WBI = "P1 W008 WB001 WBI001"

URL  = os.environ.get("EC_URL", "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/")
USER = os.environ.get("EC_USERNAME", os.environ.get("EC_USER", "sysadmin"))
PW   = os.environ.get("EC_PASSWORD", os.environ.get("EC_PASS", "sysadmin"))
HEADED = os.environ.get("EC_HEADED", "0") == "1"
SLOWMO = int(os.environ.get("EC_SLOWMO", "500")) if HEADED else 0
EVID = _ROOT / "tmp" / "perf_interval" / "evidence"
EVID.mkdir(parents=True, exist_ok=True)
results = {}


def shot(page, label):
    try:
        page.screenshot(path=str(EVID / f"pi_{label}.png"))
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


def apply_perf_navigator(page):
    """Per-field groups with SPECIFIC values (G:5 skipped - zero options) + GO."""
    for g, val in NAV:
        ec.select_dropdown(page, "nav:form:G:%d:R:1:C:0:dd_input" % g, val)
        page.wait_for_timeout(800)
    ec.click_go(page)


def pick_wbi_popup(page, pin_id, want=NAV_WBI):
    """Screen-LOCAL picker for the well_bore_interval_gm_popup: it inherits the outer nav scope but
    its list grid (Objects:form:T_data) stays EMPTY until the popup's own inner GO (button:form:B)
    is clicked - recon-verified. Then pick the row whose value == want."""
    page.evaluate("(id) => { const b = document.getElementById(id + 'B'); if (b) b.click(); }", pin_id)
    page.wait_for_selector('css=[id="popupIFrame"]', state="visible", timeout=15000)
    page.wait_for_timeout(2000)
    fl = page.frame_locator('css=[id="popupIFrame"]')
    fl.locator('css=[id="button:form:B"]').click()          # inner GO - populates the list
    page.wait_for_timeout(2500)
    fr = None
    for f in page.frames:
        if f != page.main_frame and f.query_selector('[id="%s"]' % POPUP_GRID):
            fr = f
            break
    assert fr is not None, "popup frame with %s not found" % POPUP_GRID
    picked = fr.evaluate(
        """(args) => { const [gid, want] = args;
            const tb = document.getElementById(gid); if (!tb) return false;
            for (const tr of tb.querySelectorAll('tr')) {
                const inp = tr.querySelector('td input');
                const v = inp ? inp.value.trim() : (tr.innerText || '').trim();
                if (v === want || v.startsWith(want)) {
                    const td = tr.querySelector('td'); if (td) { td.click(); return true; } } }
            return false; }""",
        [POPUP_GRID, want])
    assert picked, "popup row %r not found in %s after inner GO" % (want, POPUP_GRID)
    page.wait_for_selector('css=[id="popupIFrame"]', state="hidden", timeout=15000)
    page.wait_for_timeout(800)
    val = page.eval_on_selector("[id='%s']" % pin_id, "e => e.value")
    assert val and val.strip(), "popup pick did not fill the pin field"
    print("  Well Bore Interval =", val)


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
            apply_perf_navigator(page)
            results["nav_scope"] = "PASS: " + " -> ".join(v for _, v in NAV)
            print("  navigator applied:", results["nav_scope"])
            shot(page, "01b_nav_applied")

            insert_fields = [
                {"label": "Perforation Interval Code", "value": CODE,       "kind": "text"},
                {"label": "Perforation Interval Name", "value": NAME,       "kind": "text"},
                {"label": "Start Date",                "value": START_DATE, "kind": "date"},
            ]   # + mandatory WBI popup and Reservoir Block Formation dd, handled below
            update_fields = [{"label": "Perforation Interval Name", "value": NAME_UPD, "kind": "text"}]

            if ec.row_exists(page, GRID_DATA_ID, CODE):
                print("  pre-existing", CODE, "-> closing (End=Start) first")
                ec.closeObjectRecord(page, GRID_DATA_ID, CODE, END_DATE)

            print("=== INSERT ===")
            def _insert():
                ec._open_new_object(page)
                for f in insert_fields:
                    r = ec._resolve_field(page, "objectForm", f["label"])
                    assert r, "insert: field label not found: %s" % f["label"]
                    ec.fill_field(page, r["id"], f["value"], r["kind"])
                r = ec._resolve_field(page, "objectForm", "Well Bore Interval")
                assert r, "insert: Well Bore Interval pin not found"
                pick_wbi_popup(page, r["id"])
                r = ec._resolve_field(page, "objectForm", "Reservoir Block Formation")
                assert r, "insert: Reservoir Block Formation dd not found"
                ec.fill_field(page, r["id"], "__FIRST__", r["kind"])
                ec.save(page)
                err = ec.ec_error(page)
                assert not err, "EC error on save: %s" % err
                ec.click_go(page)
            step(page, "insert_ui", _insert)
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
