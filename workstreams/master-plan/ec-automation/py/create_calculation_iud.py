"""Create Calculation - IUD driver (thin-ish, TV-style inline grid). Engine login/nav/save reused.

Screen CO.1042 (Configuration>Assets>Calculation Objects>Create Calculation): context-gated TV-STYLE
dual grid (calculation:form:T_data header + calculation_version/static_param companions). Navigator =
Date + ONE mandatory Calculation Context dd (first-available; 14 contexts) + GO. INSERT = toolbar
Insert -> BLANK INLINE ROW (found dynamically - EC drops it mid-grid) -> fill cells C0 Code / C1 Name
(mandatory-yellow) + C2 Start Date with REAL KEYSTROKES + Tab -> Save. DELETE = row End Date cell
(C3) = Start Date (CALCULATION is date-effective/VERSIONED) -> Save. Header IUD ONLY - no equations/
variables (that is the calc-lab program's scope). DB view OV_CALCULATION.
IMPORTANT prior art: DeepDiveLearnings/ec-calc-lab (branch feature/ec-calc-lab) mapped this screen;
its step-5 rule honoured here: the delete path is part of the SAME self-cleaning run.
Run headed: EC_HEADED=1 py -X utf8 workstreams/master-plan/ec-automation/py/create_calculation_iud.py
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

SCREEN        = "Create Calculation"
GRID_PREFIX   = "calculation:form:T"
GRID_DATA_ID  = "calculation:form:T_data"
VIEW          = "ov_calculation"
CODE          = os.environ.get("EC_CODE", "AUTOTEST_CC_001")
START_DATE    = "2020-01-01"
NAME          = "AUTOTEST Create Calc 001"
NAME_UPD      = "AUTOTEST Create Calc 001 UPDATED"

URL  = os.environ.get("EC_URL", "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/")
USER = os.environ.get("EC_USERNAME", os.environ.get("EC_USER", "sysadmin"))
PW   = os.environ.get("EC_PASSWORD", os.environ.get("EC_PASS", "sysadmin"))
HEADED = os.environ.get("EC_HEADED", "0") == "1"
SLOWMO = int(os.environ.get("EC_SLOWMO", "500")) if HEADED else 0
EVID = _ROOT / "tmp" / "create_calculation" / "evidence"
EVID.mkdir(parents=True, exist_ok=True)
results = {}


def shot(page, label):
    try:
        page.screenshot(path=str(EVID / f"cc_{label}.png"))
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


def _rows_c0(page):
    """{row_index: C0 value} for the calculation grid."""
    return {int(k): v for k, v in page.evaluate(
        """(pfx) => { const out={};
            document.querySelectorAll("[id^='"+pfx+":'][id$='C0_in']").forEach(e=>{
              const m=e.id.match(/T:(\\d+):C0_in/); if(m) out[m[1]]=e.value; });
            return out; }""", GRID_PREFIX).items()}


def _blank_row(page):
    rows = _rows_c0(page)
    for r, v in sorted(rows.items()):
        if not (v or "").strip():
            return r
    return None


def _row_of(page, code):
    for r, v in _rows_c0(page).items():
        if (v or "").strip() == code:
            return r
    return None


def tv_fill(page, cell_id, value):
    """TV cell edit: click, clear, REAL keystrokes, Tab (a fill() no-op stages nothing)."""
    sel = "[id='%s']" % cell_id
    page.click(sel)
    page.wait_for_timeout(300)
    page.keyboard.press("Control+a")
    page.keyboard.type(value, delay=25)
    page.keyboard.press("Tab")
    page.wait_for_timeout(500)


def tv_insert_blank(page):
    page.locator("xpath=//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'ui-icon-insert')]]").first.hover()
    page.wait_for_timeout(900)
    links = page.locator("xpath=//ul[contains(@class,'ui-menu-child')]//li//a")
    for i in range(links.count()):
        ln = links.nth(i)
        if ln.is_visible() and (ln.text_content(timeout=800) or "").strip():
            ln.click()
            break
    ec.wait_ajax(page)


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
            # context nav: ONE mandatory dd (first-available) + GO
            ec.select_dropdown(page, "nav:form:G:1:R:1:C:0:dd_input", "__FIRST__")
            page.wait_for_timeout(700)
            ctx_val = page.eval_on_selector("[id='nav:form:G:1:R:1:C:0:dd_input']", "e => e.value")
            ec.click_go(page)
            results["nav_scope"] = "PASS: context=%s" % ctx_val
            print("  navigator applied: context =", ctx_val)
            shot(page, "01b_nav_applied")

            def _tv_delete_calc():
                """Select the code row + DELETE CALCULATION button (+ confirm), then reload."""
                page.click("[id='%s:%d:C0_in']" % (GRID_PREFIX, _row_of(page, CODE)))
                page.wait_for_timeout(1200)
                page.locator("xpath=//button[normalize-space(.)='DELETE CALCULATION' or normalize-space(.)='Delete Calculation']").first.click()
                page.wait_for_timeout(1200)
                for sel in ("xpath=//button[normalize-space(.)='YES']",
                            "xpath=//button[normalize-space(.)='Yes']",
                            "[id='dialogForm:dialogMsgOk']"):
                    b = page.locator(sel)
                    if b.count() and b.first.is_visible():
                        b.first.click()
                        break
                ec.wait_ajax(page)
                ec.click_go(page)

            if _row_of(page, CODE) is not None:
                print("  pre-existing", CODE, "-> DELETE CALCULATION first")
                _tv_delete_calc()

            print("=== INSERT (TV inline row) ===")
            def _insert():
                tv_insert_blank(page)
                r = _blank_row(page)
                assert r is not None, "no blank insert row appeared"
                print("  blank row index:", r)
                tv_fill(page, "%s:%d:C0_in" % (GRID_PREFIX, r), CODE)
                tv_fill(page, "%s:%d:C1_in" % (GRID_PREFIX, r), NAME)
                tv_fill(page, "%s:%d:C2_da_input" % (GRID_PREFIX, r), START_DATE)
                # C4 Period / C5 Type: mandatory-yellow DROPDOWNS on the blank row (recon-verified);
                # values from the existing sibling rows (scan-existing-row technique)
                ec.select_dropdown(page, "%s:%d:C4_dd_input" % (GRID_PREFIX, r), "Day")
                page.wait_for_timeout(500)
                ec.select_dropdown(page, "%s:%d:C5_dd_input" % (GRID_PREFIX, r), "Equations")
                page.wait_for_timeout(500)
                shot(page, "02a_filled")
                ec.save(page)
                err = ec.ec_error(page)
                assert not err, "EC error on save: %s" % err
                ec.click_go(page)
            step(page, "insert_ui", _insert)
            shot(page, "02_inserted")
            def _v_ins():
                assert _row_of(page, CODE) is not None, "code not in grid after save"
                assert db.code_present(VIEW, CODE), "not in OV_CALCULATION"
                ok, act = db.field_equals(VIEW, CODE, "NAME", NAME)
                assert ok, f"DB NAME={act!r} != {NAME!r}"
            step(page, "insert_db", _v_ins)
            print("  INSERT verified (grid + DB + NAME)")

            print("=== UPDATE (Name via VERSIONS grid - the authoritative source) ===")
            def _update():
                r = _row_of(page, CODE)
                assert r is not None, "row not found for update"
                # select the calc row -> VERSIONS panel loads for it
                page.click("[id='%s:%d:C0_in']" % (GRID_PREFIX, r))
                page.wait_for_timeout(1200)
                # the header C1 mirrors the VERSION row's Calculation Name - edit the version cell
                tv_fill(page, "calculation_version:form:T:0:C0_in", NAME_UPD)
                ec.save(page)
                err = ec.ec_error(page)
                assert not err, "EC error on save: %s" % err
                ec.click_go(page)
            step(page, "update_ui", _update)
            shot(page, "03_updated")
            def _v_upd():
                ok, an = db.field_equals(VIEW, CODE, "NAME", NAME_UPD)
                assert ok, f"DB NAME={an!r} != {NAME_UPD!r}"
            step(page, "update_db", _v_upd)
            print("  UPDATE verified (DB NAME)")

            print("=== DELETE (purpose-built DELETE CALCULATION button) ===")
            def _delete():
                r = _row_of(page, CODE)
                assert r is not None, "row not found for delete"
                page.click("[id='%s:%d:C0_in']" % (GRID_PREFIX, r))   # select the calc row
                page.wait_for_timeout(1200)
                page.locator("xpath=//button[normalize-space(.)='DELETE CALCULATION' or normalize-space(.)='Delete Calculation']").first.click()
                page.wait_for_timeout(1200)
                # confirm dialog if one appears (YES / OK)
                for sel in ("xpath=//button[normalize-space(.)='YES']",
                            "xpath=//button[normalize-space(.)='Yes']",
                            "[id='dialogForm:dialogMsgOk']"):
                    b = page.locator(sel)
                    if b.count() and b.first.is_visible():
                        b.first.click()
                        break
                ec.wait_ajax(page)
                err = ec.ec_error(page)
                assert not err, "EC error on delete: %s" % err
                ec.click_go(page)
            step(page, "delete_ui", _delete)
            shot(page, "04_deleted")
            def _v_del():
                assert _row_of(page, CODE) is None, "still in grid"
                assert not db.code_present(VIEW, CODE), "still in OV_CALCULATION"
            step(page, "delete_db", _v_del)
            print("  DELETE verified (absent grid + DB)")

            residual = db.count_like(VIEW, "AUTOTEST_CC")
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
