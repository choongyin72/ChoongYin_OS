"""Production Day Table screen - Insert-only driver (thin). Uses the reusable engine
py/ec_object_iud.py (same folder). UPDATE and DELETE ARE OUT OF SCOPE for this screen -
see the notes below; owner-confirmed live 2026-08-03.

Screen quirks (see ec-ui-knowledge/screens/production_day_table.md for full detail):
- TV-style inline-editable grid (`production_day:form:T_data`), CLASS_TYPE=OBJECT /
  TIME_SCOPE_CODE=INVARIANT per class_cnfg.
- Insert: hover the Insert toolbar icon's own <li> -> click the (already correctly
  title-cased, NOT a CSS-uppercase illusion like Constant Standard) menu item
  "Production Days" -> a blank row appears -> fill cells.
- CRITICAL: cells must be filled with REAL KEYSTROKES + Tab (this project's own
  `Type Cell By Id` convention), NOT `ec.fill_field()`'s plain `.fill()` - using
  `.fill()` silently breaks the NEXT cell's autocomplete dropdown panel from ever
  rendering (confirmed reproducible: with `.fill()` on Object Code first, the
  Time Zone dropdown panel never appears; skip the .fill()-based path entirely,
  skipping straight to the dropdown pick, and it renders fine).
- DELETE IS OUT OF SCOPE, permanently, by design - owner confirmed live 2026-08-03
  ("its business process logic flow.... no deletion is allow in Production Day
  Table screen. such feature been disabled. Production Day Table set object end
  date its not trigger delete record as its implementation are different than
  other objects implementation"). The toolbar Delete icon never enables for ANY
  row (confirmed across 3+ different pre-existing rows, not just test data), and
  setting End Date = Start Date does NOT remove a row from OV_PRODUCTION_DAY
  (confirmed via DB - the view has no date-range filter, matching INVARIANT).
- SELF-CLEAN IS IMPOSSIBLE by design: every Insert (including every future live
  test run) permanently accumulates an AUTOTEST_PDT_* row with NO way to remove
  it via the UI. Owner decision 2026-08-03: ACCEPT this as a permanent, disclosed
  exception (same precedent as Royalty Contract's residual CNTR_PG_SETUP rows) -
  do NOT attempt a raw DB delete. This driver/suite should be run SPARINGLY.

Run headed:   EC_HEADED=1 py -X utf8 workstreams/master-plan/ec-automation/py/production_day_table_iud.py
Env: EC_URL, EC_USERNAME/EC_USER, EC_PASSWORD/EC_PASS (default sandbox + sysadmin);
     EC_DB_DSN/USER/PASS for ground truth; EC_HEADED=1 shows the browser.
"""
import os
import sys
import time
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
SCREEN       = "Production Day Table"
GRID_DATA_ID = "production_day:form:T_data"
VIEW         = "OV_PRODUCTION_DAY"
# Unique-per-run code: this class has NO delete mechanism (see docstring), so a fixed
# code would collide with the permanent row left by the previous run.
CODE         = os.environ.get("EC_CODE", "AUTOTEST_PDT_%d" % int(time.time()))
START_DATE   = "2003-01-01"
NAME         = "AUTOTEST PDT %s" % CODE[-10:]

# ---- env ---------------------------------------------------------------------
URL  = os.environ.get("EC_URL", "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/")
USER = os.environ.get("EC_USERNAME", os.environ.get("EC_USER", "sysadmin"))
PW   = os.environ.get("EC_PASSWORD", os.environ.get("EC_PASS", "sysadmin"))
HEADED = os.environ.get("EC_HEADED", "0") == "1"
SLOWMO = int(os.environ.get("EC_SLOWMO", "500")) if HEADED else 0
EVID = _ROOT / "tmp" / "production_day_table_iud" / "evidence"
EVID.mkdir(parents=True, exist_ok=True)

results = {}


def shot(page, label):
    try:
        page.screenshot(path=str(EVID / f"pdt_{label}.png"))
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


def _type_cell(page, cell_id, value):
    """Real keystrokes + Tab (this project's Type Cell By Id convention) - a plain
    .fill() silently breaks the NEXT cell's autocomplete dropdown from rendering."""
    loc = page.locator('css=[id="%s"]' % cell_id)
    loc.click()
    loc.fill("")
    loc.type(value, delay=30)
    page.keyboard.press("Tab")
    ec.wait_ajax(page)
    page.wait_for_timeout(600)


def _open_insert_menu(page):
    ins_icon = page.locator(
        "xpath=//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'ui-icon-insert')]]"
    )
    ins_icon.first.hover()
    item = page.locator(
        "xpath=//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'ui-icon-insert')]]"
        "//ul[contains(@class,'ui-menu-child')]//a[normalize-space(.)='Production Days']"
    )
    item.first.wait_for(state="visible", timeout=10000)
    item.first.click()
    ec.wait_ajax(page)
    page.wait_for_timeout(1500)


def _blank_row_index(page):
    return page.evaluate(
        "() => { const m = document.querySelectorAll('input[id^=\"production_day:form:T:\"][id$=\":C0_in\"]');"
        " for (const e of m) { if ((e.value||'') === '') { const r = e.id.match(/:T:(\\d+):/); "
        "if (r) return parseInt(r[1]); } } return -1; }"
    )


def insert_record(page, code, name, start_date):
    _open_insert_menu(page)
    row = _blank_row_index(page)
    if row < 0:
        raise RuntimeError("no blank row appeared after Insert")
    base = "production_day:form:T:%d:C" % row
    _type_cell(page, base + "0_in", code)
    ec.select_dropdown(page, base + "1_dd_input", "__FIRST__")
    _type_cell(page, base + "2_da_input", start_date)
    _type_cell(page, base + "4_in", name)
    method = ec.save(page)
    err = ec.ec_error(page)
    # Measured live: this screen's Save commit is NOT immediately visible to a fresh DB
    # session - takes ~8s to become visible (confirmed reproducibly, unlike every other
    # screen built so far where the commit is instant). Wait generously before any DB check.
    page.wait_for_timeout(10000)
    if err:
        raise RuntimeError("insert save error: %s" % err)
    return method


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

            print("=== INSERT ===")
            step(page, "insert_ui", lambda: insert_record(page, CODE, NAME, START_DATE))
            shot(page, "02_inserted")

            def _v_ins():
                assert db.code_present(VIEW, CODE), "not in OV_PRODUCTION_DAY"
                ok_n, act = db.field_equals(VIEW, CODE, "NAME", NAME)
                assert ok_n, f"DB NAME={act!r} != {NAME!r}"
            step(page, "insert_db", _v_ins)
            print("  INSERT verified (OV_PRODUCTION_DAY + NAME)")

            results["update_ui"] = "SKIPPED (no Update path exercised - Insert-only screen)"
            results["delete_ui"] = "OUT OF SCOPE (owner-confirmed: Delete permanently disabled by design)"
            results["self_clean"] = "N/A BY DESIGN (no delete mechanism exists - permanent residual accepted, owner decision 2026-08-03)"
            print("=== UPDATE/DELETE: OUT OF SCOPE (see driver docstring) ===")
            shot(page, "03_final")
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
        mark = "OK" if str(v).startswith(("PASS", "SKIPPED", "OUT OF SCOPE", "N/A")) else "X"
        if mark == "X":
            ok = False
        print(f"  {mark} {k:<12}: {v}")
    print("Overall:", "ALL PASS" if ok else "FAILURES")
    print("Evidence:", EVID)
    sys.exit(0 if ok else 1)
