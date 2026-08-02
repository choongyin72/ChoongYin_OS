"""Constant Standard - IUD driver (thin). Reuses shared engine ec_object_iud.py + DbVerify.py.

TV-style inline-editable grid (cstandard:form:T_data), despite CLASS_TYPE=OBJECT/VERSIONED per
class_cnfg. Insert: hover the toolbar Insert icon (scoped to its OWN <li>, since the Delete icon's
li has an identically-worded item) -> click the menu item by its REAL text ("Constant Standard",
title-case - the visible ALL-CAPS display is CSS text-transform, not the actual DOM text; every
earlier attempt this session failed on a silent case mismatch) -> a blank row appears -> fill
Standard Code / Standard Name / Start Date / Daytime (Daytime is a genuinely separate mandatory
field, not derived from Start Date). Delete: this class IS date-effective (VERSIONED) despite the
TV-looking grid - set End Date = Start Date directly in the inline cell + Save (the standard OV
close gesture), NOT a physical toolbar delete.
Run headed: EC_HEADED=1 py -X utf8 workstreams/master-plan/ec-automation/py/constant_standard_iud.py
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

SCREEN     = "Constant Standard"
GRID_ID    = "cstandard:form:T_data"
VIEW       = "ov_constant_standard"
CODE       = os.environ.get("EC_CODE", "AUTOTEST_CS_001")
START_DATE = "2000-01-01"
NAME       = "AUTOTEST Constant Standard 001"
NAME_UPD   = NAME + " UPDATED"

URL  = os.environ.get("EC_URL", "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/")
USER = os.environ.get("EC_USERNAME", os.environ.get("EC_USER", "sysadmin"))
PW   = os.environ.get("EC_PASSWORD", os.environ.get("EC_PASS", "sysadmin"))
HEADED = os.environ.get("EC_HEADED", "0") == "1"
SLOWMO = int(os.environ.get("EC_SLOWMO", "500")) if HEADED else 0
EVID = _ROOT / "tmp" / "constant_standard" / "evidence"
EVID.mkdir(parents=True, exist_ok=True)
results = {}


def shot(page, label):
    try:
        page.screenshot(path=str(EVID / ("CS_" + label + ".png")))
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


def _insert_menu_item(page):
    """Insert icon's OWN <li> -> hover -> the real (title-case) menu item text."""
    return page.locator(
        "xpath=//li[contains(@class,'ui-menu-parent')]"
        "[.//span[contains(@class,'ui-icon-insert')]]"
        "//ul[contains(@class,'ui-menu-child')]//a[normalize-space(.)='Constant Standard']"
    )


def _row_index_by_code(page, code):
    idx = page.evaluate(
        "(code) => { const m = document.querySelectorAll('input[id^=\"cstandard:form:T:\"][id$=\":C0_in\"]');"
        " for (const e of m) { if ((e.value||'') === code) { const r = e.id.match(/:T:(\\d+):/); if (r) return parseInt(r[1]); } }"
        " return -1; }",
        code,
    )
    return idx


def _type_cell(page, cell_id, value):
    loc = page.locator("#" + cell_id.replace(":", "\\:"))
    loc.click()
    loc.fill(value)
    loc.press("Tab")
    ec.wait_ajax(page)
    page.wait_for_timeout(400)


def insert_record(page, code, name, start_date):
    ins_icon = page.locator(
        "xpath=//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'ui-icon-insert')]]"
    )
    ins_icon.first.hover()
    item = _insert_menu_item(page)
    item.first.wait_for(state="visible", timeout=6000)
    item.first.click()
    ec.wait_ajax(page)
    page.wait_for_timeout(500)
    row = _row_index_by_code(page, "")
    if row < 0:
        raise RuntimeError("no blank row appeared after Insert")
    _type_cell(page, "cstandard:form:T:%d:C0_in" % row, code)
    _type_cell(page, "cstandard:form:T:%d:C1_in" % row, name)
    _type_cell(page, "cstandard:form:T:%d:C2_da_input" % row, start_date)
    _type_cell(page, "cstandard:form:T:%d:C4_da_input" % row, start_date)  # Daytime
    method = ec.save(page)
    err = ec.ec_error(page)
    if err:
        raise RuntimeError("insert save error: %s" % err)
    return method


def update_name(page, code, new_name):
    row = _row_index_by_code(page, code)
    if row < 0:
        raise RuntimeError("row not found for update: %s" % code)
    _type_cell(page, "cstandard:form:T:%d:C1_in" % row, new_name)
    method = ec.save(page)
    err = ec.ec_error(page)
    if err:
        raise RuntimeError("update save error: %s" % err)
    return method


def close_record(page, code, start_date):
    """This class is date-effective (VERSIONED) - End Date = Start Date via the inline cell."""
    row = _row_index_by_code(page, code)
    if row < 0:
        raise RuntimeError("row not found for delete: %s" % code)
    _type_cell(page, "cstandard:form:T:%d:C3_da_input" % row, start_date)
    method = ec.save(page)
    err = ec.ec_error(page)
    if err:
        raise RuntimeError("delete save error: %s" % err)
    return method


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

            if _row_index_by_code(page, CODE) >= 0:
                print("  pre-existing", CODE, "-> closing (End=Start) first")
                close_record(page, CODE, START_DATE)

            print("=== INSERT ===")
            step(page, "insert_ui", lambda: insert_record(page, CODE, NAME, START_DATE))
            shot(page, "02_inserted")
            def _v_ins():
                assert db.code_present(VIEW, CODE), "not in ov view"
                ok, act = db.field_equals(VIEW, CODE, "NAME", NAME)
                assert ok, "DB NAME=%r != %r" % (act, NAME)
            step(page, "insert_db", _v_ins)
            print("  INSERT verified (DB + NAME)")

            print("=== UPDATE ===")
            step(page, "update_ui", lambda: update_name(page, CODE, NAME_UPD))
            shot(page, "03_updated")
            def _v_upd():
                ok, an = db.field_equals(VIEW, CODE, "NAME", NAME_UPD)
                assert ok, "DB NAME=%r != %r" % (an, NAME_UPD)
            step(page, "update_db", _v_upd)
            print("  UPDATE verified (DB NAME)")

            print("=== DELETE (End=Start) ===")
            step(page, "delete_ui", lambda: close_record(page, CODE, START_DATE))
            shot(page, "04_deleted")
            def _v_del():
                assert not db.code_present(VIEW, CODE), "still in DB view"
            step(page, "delete_db", _v_del)
            print("  DELETE verified (absent DB)")

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
