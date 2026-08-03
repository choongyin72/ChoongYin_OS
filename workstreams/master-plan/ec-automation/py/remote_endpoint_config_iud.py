"""Remote Endpoint Configuration screen - IUD driver (thin). Uses the reusable engine
py/ec_object_iud.py (same folder). TV-style inline-editable grid, no navigator,
INVARIANT (physical delete) - matches the proven Language exemplar pattern.

Screen quirks (see ec-ui-knowledge/screens/remote_endpoint_config.md for full detail):
- Code must be lowercase alphanumeric with hyphens only (a DNS-slug format), NOT this
  project's usual AUTOTEST_XX_ convention - confirmed live: "Invalid Code, must consist
  of lower case alphanumeric characters or '-', and must start and end with an
  alphanumeric character (e.g. 'my-name', or '123-abc')". Uses `autotest-rec-<ts>`.
- Insert/Delete toolbar submenu text is already correctly title-cased ("Remote Endpoint
  configuration") - no CSS-uppercase illusion, no ambiguous Insert/Delete collision.
- Real keystrokes + Tab required for every cell (this project's own Type Cell By Id
  convention for inline grids).

Run headed:   EC_HEADED=1 py -X utf8 workstreams/master-plan/ec-automation/py/remote_endpoint_config_iud.py
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
SCREEN       = "Remote Endpoint Configuration"
GRID_DATA_ID = "endpointconfig:form:T_data"
VIEW         = "OV_ENDPOINT_CONFIG"
CODE         = os.environ.get("EC_CODE", "autotest-rec-%d" % int(time.time()))
NAME         = "AUTOTEST REC %s" % CODE[-10:]

# ---- env ---------------------------------------------------------------------
URL  = os.environ.get("EC_URL", "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/")
USER = os.environ.get("EC_USERNAME", os.environ.get("EC_USER", "sysadmin"))
PW   = os.environ.get("EC_PASSWORD", os.environ.get("EC_PASS", "sysadmin"))
HEADED = os.environ.get("EC_HEADED", "0") == "1"
SLOWMO = int(os.environ.get("EC_SLOWMO", "500")) if HEADED else 0
EVID = _ROOT / "tmp" / "remote_endpoint_config_iud" / "evidence"
EVID.mkdir(parents=True, exist_ok=True)

results = {}


def shot(page, label):
    try:
        page.screenshot(path=str(EVID / f"rec_{label}.png"))
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
    loc = page.locator('css=[id="%s"]' % cell_id)
    loc.click()
    loc.fill("")
    loc.type(value, delay=30)
    page.keyboard.press("Tab")
    ec.wait_ajax(page)
    page.wait_for_timeout(600)


def _menu_item(page, icon_class):
    page.locator(
        "xpath=//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'%s')]]" % icon_class
    ).first.hover()
    return page.locator(
        "xpath=//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'%s')]]"
        "//ul[contains(@class,'ui-menu-child')]//a" % icon_class
    ).first


def _blank_row_index(page):
    return page.evaluate(
        "() => { const m = document.querySelectorAll('input[id^=\"endpointconfig:form:T:\"][id$=\":C0_in\"]');"
        " for (const e of m) { if ((e.value||'') === '') { return parseInt(e.id.split(':')[3]); } }"
        " return -1; }"
    )


def _row_by_code(page, code):
    return page.evaluate(
        "(code) => { const m = document.querySelectorAll('input[id^=\"endpointconfig:form:T:\"][id$=\":C0_in\"]');"
        " for (const e of m) { if ((e.value||'') === code) { return parseInt(e.id.split(':')[3]); } }"
        " return -1; }",
        code,
    )


def insert_record(page, code, name):
    item = _menu_item(page, "ui-icon-insert")
    item.wait_for(state="visible", timeout=10000)
    item.click()
    ec.wait_ajax(page)
    page.wait_for_timeout(1000)
    row = _blank_row_index(page)
    if row < 0:
        raise RuntimeError("no blank row appeared after Insert")
    base = "endpointconfig:form:T:%d:C" % row
    _type_cell(page, base + "0_in", code)
    _type_cell(page, base + "1_in", name)
    ec.select_dropdown(page, base + "2_dd_input", "__FIRST__")
    method = ec.save(page)
    err = ec.ec_error(page)
    if err:
        raise RuntimeError("insert save error: %s" % err)
    return method


def update_name(page, code, new_name):
    row = _row_by_code(page, code)
    if row < 0:
        raise RuntimeError("row not found for update: %s" % code)
    _type_cell(page, "endpointconfig:form:T:%d:C1_in" % row, new_name)
    method = ec.save(page)
    err = ec.ec_error(page)
    if err:
        raise RuntimeError("update save error: %s" % err)
    return method


def delete_record(page, code):
    row = _row_by_code(page, code)
    if row < 0:
        raise RuntimeError("row not found for delete: %s" % code)
    page.locator('css=[id="endpointconfig:form:T:%d:C0_in"]' % row).click()
    page.wait_for_timeout(400)
    item = _menu_item(page, "ui-icon-delete")
    item.wait_for(state="visible", timeout=10000)
    item.click()
    ec.wait_ajax(page)
    page.wait_for_timeout(800)
    method = ec.save(page)
    err = ec.ec_error(page)
    if err:
        raise RuntimeError("delete save error: %s" % err)
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
            step(page, "insert_ui", lambda: insert_record(page, CODE, NAME))
            shot(page, "02_inserted")

            def _v_ins():
                assert db.code_present(VIEW, CODE), "not in OV_ENDPOINT_CONFIG"
                ok_n, act = db.field_equals(VIEW, CODE, "NAME", NAME)
                assert ok_n, f"DB NAME={act!r} != {NAME!r}"
            step(page, "insert_db", _v_ins)
            print("  INSERT verified (OV_ENDPOINT_CONFIG + NAME)")

            print("=== UPDATE ===")
            NAME_UPD = NAME + " UPDATED"
            step(page, "update_ui", lambda: update_name(page, CODE, NAME_UPD))
            shot(page, "03_updated")

            def _v_upd():
                ok_n, act = db.field_equals(VIEW, CODE, "NAME", NAME_UPD)
                assert ok_n, f"DB NAME={act!r} != {NAME_UPD!r}"
            step(page, "update_db", _v_upd)
            print("  UPDATE verified (DB NAME)")

            print("=== DELETE (physical) ===")
            step(page, "delete_ui", lambda: delete_record(page, CODE))
            shot(page, "04_deleted")

            def _v_del():
                assert not db.code_present(VIEW, CODE), "still in OV_ENDPOINT_CONFIG"
            step(page, "delete_db", _v_del)
            print("  DELETE verified (absent OV_ENDPOINT_CONFIG)")

            residual = db.count_like(VIEW, "autotest-rec-")
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
