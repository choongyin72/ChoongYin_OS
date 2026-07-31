"""Well Bore - IUD driver (thin). Reuses shared engine ec_object_iud.py + DbVerify.py.

OV-GM 4-level nav + mandatory POPUP. Recon facts (2026-07-31, all executed):
 - nav = PER-FIELD groups nav:form:G:1..G:4:R:1:C:0 = Production Unit / Area / Facility Class 1 /
   'Well & Well Hookup'. A 5th group G:5 ('Well') exists and the scan flags it mandatory, but it
   offers ZERO options under every scope tried (AS1 first-available AND P1 with a real well) -> it
   is an unusable filter; the grid loads on 4 levels (verified: 'P1 W008 WB001' lists).
 - SPECIFIC values needed: P1 Production Unit -> P1 Area -> P1 Facility 1 -> **P1 W008 OP**
   (a REAL well; the first-available G:4 option is 'P1 Graph 001', a graph object with no bores).
 - form: mandatory 'Well' POPUP (pin at R:7) -> first-available under the nav scope.
Run headed: EC_HEADED=1 py -X utf8 workstreams/master-plan/ec-automation/py/well_bore_iud.py
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

SCREEN        = "Well Bore"
GRID_DATA_ID  = "manageObject:form:T_data"
VIEW          = "ov_well_bore"
CODE          = os.environ.get("EC_CODE", "AUTOTEST_WB_001")
START_DATE    = "2020-01-01"
END_DATE      = START_DATE
NAME          = "AUTOTEST Well Bore 001"
NAME_UPD      = "AUTOTEST Well Bore 001 UPDATED"

NAV = ((1, "P1 Production Unit"), (2, "P1 Area"), (3, "P1 Facility 1"), (4, "P1 W008 OP"))

URL  = os.environ.get("EC_URL", "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/")
USER = os.environ.get("EC_USERNAME", os.environ.get("EC_USER", "sysadmin"))
PW   = os.environ.get("EC_PASSWORD", os.environ.get("EC_PASS", "sysadmin"))
HEADED = os.environ.get("EC_HEADED", "0") == "1"
SLOWMO = int(os.environ.get("EC_SLOWMO", "500")) if HEADED else 0
EVID = _ROOT / "tmp" / "well_bore" / "evidence"
EVID.mkdir(parents=True, exist_ok=True)
results = {}


def shot(page, label):
    try:
        page.screenshot(path=str(EVID / f"wb_{label}.png"))
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


def apply_well_bore_navigator(page):
    """Per-field groups G:1..G:4 with SPECIFIC values + GO (G:5 'Well' has no options - skipped)."""
    for g, val in NAV:
        ec.select_dropdown(page, "nav:form:G:%d:R:1:C:0:dd_input" % g, val)
        page.wait_for_timeout(800)
    ec.click_go(page)


WELL_POPUP_GRID = "Objects:form:T_data"   # recon-verified: NOT PopupList:form:T_data
NAV_WELL = NAV[3][1]                      # 'P1 W008 OP' - parent-match the nav scope


def pick_well_popup(page, pin_id, want=NAV_WELL):
    """Screen-LOCAL popup picker (shared engine untouched): this object popup's list grid is
    'Objects:form:T_data' (recon-verified 40 rows, already populated on open) - the generic
    ec.pick_popup waits for 'PopupList:form:T_data' and so reports a false 'empty source list'.
    Picks the row whose input value == want (the nav-scope well; the FIRST row is 'P1 Graph 001',
    a graph object - deliberately not used)."""
    page.evaluate("(id) => { const b = document.getElementById(id + 'B'); if (b) b.click(); }", pin_id)
    page.wait_for_selector('css=[id="popupIFrame"]', state="visible", timeout=15000)
    page.frame_locator('css=[id="popupIFrame"]').locator(
        'css=[id="%s"]' % WELL_POPUP_GRID).first.wait_for(state="visible", timeout=15000)
    page.wait_for_timeout(1500)
    fr = None
    for f in page.frames:
        if f != page.main_frame and f.query_selector('[id="%s"]' % WELL_POPUP_GRID):
            fr = f
            break
    assert fr is not None, "popup frame with %s not found" % WELL_POPUP_GRID
    picked = fr.evaluate(
        """(args) => { const [gid, want] = args;
            const tb = document.getElementById(gid); if (!tb) return false;
            for (const tr of tb.querySelectorAll('tr')) {
                const inp = tr.querySelector('td input');
                const v = inp ? inp.value.trim() : (tr.innerText || '').trim().split('\\t')[0];
                if (v === want) { const td = tr.querySelector('td'); if (td) { td.click(); return true; } } }
            return false; }""",
        [WELL_POPUP_GRID, want])
    assert picked, "popup row %r not found in %s" % (want, WELL_POPUP_GRID)
    page.wait_for_selector('css=[id="popupIFrame"]', state="hidden", timeout=15000)
    page.wait_for_timeout(800)
    val = page.eval_on_selector("[id='%s']" % pin_id, "e => e.value")
    assert val and val.strip(), "popup pick did not fill the pin field"
    print("  Well =", val)


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
            apply_well_bore_navigator(page)
            results["nav_scope"] = "PASS: " + " -> ".join(v for _, v in NAV)
            print("  navigator applied:", results["nav_scope"])
            shot(page, "01b_nav_applied")

            insert_fields = [
                {"label": "Well Bore Code", "value": CODE,        "kind": "text"},
                {"label": "Well Bore Name", "value": NAME,        "kind": "text"},
                {"label": "Start Date",     "value": START_DATE,  "kind": "date"},
            ]   # mandatory 'Well' popup handled separately (screen-local picker)
            update_fields = [{"label": "Well Bore Name", "value": NAME_UPD, "kind": "text"}]

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
                r = ec._resolve_field(page, "objectForm", "Well")
                assert r, "insert: Well pin not found"
                pick_well_popup(page, r["id"])
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
