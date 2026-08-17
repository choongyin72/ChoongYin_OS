"""Stability test round 5: 15 MORE real screens with existing hand-written drivers, different from
all 60 already tested (rounds 1-4). Every config value taken directly from each screen's own real
*_iud.py driver (ec_object_iud-based), re-read in full this session before writing this harness - no
extrapolation from a similar-looking screen (round-1 mistake, never repeated since).

Row-identity hard rule (added this branch after the Contract Inventory production-data-corruption
incident): after every select_row() and before any Save that follows it, verify_row_code() reads the
row's own Code field back from the form and aborts loudly if it does not match the code this script
intended to act on - never trust that a grid match is the right row.

Special-cased: Perforation Interval (7-group PER-FIELD nav, G:5 skipped/zero options, + a
screen-local Well Bore Interval popup needing an INNER GO before its list populates, + mandatory
Reservoir Block Formation dd), Remote Endpoint Configuration (TV-style inline grid, physical delete,
DNS-slug code format - NOT the usual AUTOTEST_ prefix), Report Group (date-only nav + GO pops an
UNSAVED CHANGES YES/NO dialog that blocks the next GO, same class as round-1's Driver/Truck/Trailer).
Production Day Table was deliberately EXCLUDED from this batch: its own driver documents self-clean
as permanently impossible by design (owner-accepted precedent, same class as Royalty Contract) and
instructs running it SPARINGLY - already proven, re-running it would only add another permanent,
unremovable residual row for a fact this project already has on record.
"""
import json
import os
import sys
import time
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parent / "workstreams" / "master-plan" / "ec-automation" / "py"))
sys.path.insert(0, str(_HERE.parent / "workstreams" / "master-plan" / "ec-automation" / "libraries"))
from engine import Engine, open_screen, SaveFailed, css
from universal_classifier import EC_URL
from playwright.sync_api import sync_playwright
import DbVerify as db
import ec_object_iud as ec

HEADED = os.environ.get("EC_HEADED", "0") == "1"


def verify_row_code(eng, page, code_label, expected_code):
    """Row-identity hard rule: read the selected row's own Code field back from the form and abort
    if it does not match. Never Save/Update/Delete on an unverified row (Contract Inventory lesson)."""
    f = eng._field(code_label)
    actual = page.locator(css(f["id"])).first.input_value()
    if actual != expected_code:
        raise RuntimeError(
            f"ROW IDENTITY MISMATCH: expected code {expected_code!r}, form shows {actual!r} - "
            f"ABORTING, not touching this row"
        )


SCREENS = [
    {"name": "Orifice Plate", "view": "ov_orifice_plate", "code": "AUTOTEST_R5_OP", "nav": None,
     "code_label": "Orifice Code",
     "insert": [("Orifice Code", None, "text"), ("Orifice Name", None, "text"),
                ("Start Date", "2000-01-01", "date"), ("Material", "304/316 Stainless Steel", "dropdown"),
                ("Diameter [mm]", "1", "text"), ("Measurement Temp [\u00b0R]", "1", "text")],
     "update_label": "Orifice Name"},
    {"name": "Pilot Boat", "view": "ov_pilot_boat", "code": "AUTOTEST_R5_PB", "nav": "ovgm-default",
     "code_label": "Pilot Boat Code",
     "insert": [("Pilot Boat Code", None, "text"), ("Pilot Boat Name", None, "text"),
                ("Start Date", "2000-01-01", "date"), ("Op Production Unit", "__FIRST__", "dropdown")],
     "update_label": "Pilot Boat Name"},
    {"name": "Process Train", "view": "ov_process_train", "code": "AUTOTEST_R5_PT", "nav": None,
     "code_label": "Process Train Code",
     "insert": [("Process Train Code", None, "text"), ("Process Train Name", None, "text"),
                ("Start Date", "2000-01-01", "date"), ("Production Facility Class 1", "__FIRST__", "dropdown")],
     "update_label": "Process Train Name"},
    {"name": "Production Separator", "view": "ov_prodseparator", "code": "AUTOTEST_R5_PSEP", "nav": "ovgm-default",
     "code_label": "Production Separator Code",
     "insert": [("Production Separator Code", None, "text"), ("Production Separator Name", None, "text"),
                ("Start Date", "2000-01-01", "date"), ("Op Production Unit", "__FIRST__", "dropdown")],
     "update_label": "Production Separator Name"},
    {"name": "Reservoir Block", "view": "ov_resv_block", "code": "AUTOTEST_R5_RESVB", "nav": None,
     "code_label": "Reservoir Block Code",
     "insert": [("Reservoir Block Code", None, "text"), ("Reservoir Block Name", None, "text"),
                ("Start Date", "2000-01-01", "date")],
     "update_label": "Reservoir Block Name"},
    {"name": "Reservoir Formation", "view": "ov_resv_formation", "code": "AUTOTEST_R5_RESVF", "nav": None,
     "code_label": "Reservoir Formation Code",
     "insert": [("Reservoir Formation Code", None, "text"), ("Reservoir Formation Name", None, "text"),
                ("Start Date", "2000-01-01", "date")],
     "update_label": "Reservoir Formation Name"},
    {"name": "Revenue Stream Category", "view": "ov_stream_category", "code": "AUTOTEST_R5_RSC", "nav": None,
     "code_label": "Stream Category Code",
     "insert": [("Stream Category Code", None, "text"), ("Name", None, "text"),
                ("Start Date", "2000-01-01", "date")],
     "update_label": "Name"},
    {"name": "Service", "view": "ov_service", "code": "AUTOTEST_R5_SV", "nav": ["TS3 BU1"], "nav_levels": 1,
     "code_label": "Service Code",
     "insert": [("Service Code", None, "text"), ("Service Name", None, "text"),
                ("Start Date", "2011-01-01", "date"), ("Service Template", "__FIRST__", "dropdown"),
                ("Service Type", "__FIRST__", "dropdown"), ("Service Status", "__FIRST__", "dropdown"),
                ("Contract", "TS3 GTA Shipper A", "dropdown"), ("Transport System", "TS3 Transport System", "dropdown")],
     "update_label": "Service Name"},
    {"name": "Storage Flow", "view": "ov_storage_flow", "code": "AUTOTEST_R5_SF", "nav": None,
     "code_label": "Storage Flow Code",
     "insert": [("Storage Flow Code", None, "text"), ("Storage Flow Name", None, "text"),
                ("Start Date", "2000-01-01", "date"), ("Flow Direction", "__FIRST__", "dropdown"),
                ("Storage", "__FIRST__", "dropdown")],
     "update_label": "Storage Flow Name"},
    {"name": "Stream Item Category", "view": "ov_stream_item_category", "code": "AUTOTEST_R5_SIC", "nav": None,
     "code_label": "Code",
     "insert": [("Code", None, "text"), ("Name", None, "text"), ("Start Date", "2000-01-01", "date")],
     "update_label": "Name"},
    {"name": "Task Process", "view": "ov_task_process", "code": "AUTOTEST_R5_TP", "nav": None,
     "code_label": "Task Process Code",
     "insert": [("Task Process Code", None, "text"), ("Task Process Name", None, "text"),
                ("Start date", "2000-01-01", "date")],
     "update_label": "Task Process Name"},
]


def run_standard_ov(page, cfg):
    name = cfg["name"]
    code = cfg["code"]
    code_label = cfg["code_label"]
    start_date_value = next(v for l, v, k in cfg["insert"] if l.lower().startswith("start"))
    result = {"insert": "SKIP", "update": "SKIP", "delete": "SKIP", "self_clean": "SKIP", "error": None}
    t0 = time.time()
    try:
        open_screen(page, name)
        eng = Engine(page, name)

        nav_levels = cfg.get("nav_levels")

        if cfg["nav"] == "ovgm-default":
            eng.apply_navigator()
        elif isinstance(cfg["nav"], list):
            eng.apply_navigator(values=cfg["nav"], levels=nav_levels)

        grids = page.evaluate("""() => Array.from(document.querySelectorAll('[id$=":T_data"]')).map(e => e.id)""")
        grid_id = grids[0]

        if eng.select_row(grid_id, code):
            verify_row_code(eng, page, code_label, code)
            eng.fill("End Date", start_date_value)
            eng.click("Save")
            if cfg["nav"] == "ovgm-default":
                eng.apply_navigator()
            elif isinstance(cfg["nav"], list):
                eng.apply_navigator(values=cfg["nav"], levels=nav_levels)

        eng.toolbar("New Object")
        page.wait_for_timeout(800)
        for label, value, kind in cfg["insert"]:
            v = code if value is None else value
            if kind == "dropdown":
                eng.select(label, v)
            else:
                eng.fill(label, v)
        eng.click("Save")
        result["insert"] = "PASS"

        eng.select_row(grid_id, code)
        verify_row_code(eng, page, code_label, code)
        eng.fill(cfg["update_label"], code + "_UPD")
        eng.click("Save")
        result["update"] = "PASS"

        eng.select_row(grid_id, code)
        verify_row_code(eng, page, code_label, code)
        eng.fill("End Date", start_date_value)
        eng.click("Save")
        result["delete"] = "PASS"

        present = db.code_present(cfg["view"], code)
        for _ in range(4):
            if not present:
                break
            time.sleep(1.5)
            present = db.code_present(cfg["view"], code)
        result["self_clean"] = "CLEAN" if not present else "RESIDUAL"

    except Exception as e:
        result["error"] = str(e)[:200]

    result["elapsed_s"] = round(time.time() - t0, 1)
    return result


def run_shift(page):
    """Real driver: OV-GM explicit 3-level nav (P1 Production Unit/Area/Facility 1) + a MANDATORY
    FREE-TEXT 'Start Time (HH:MI)' field (a field-class the generator can't fill) + Op Production
    Unit must equal the nav PU (parent-matching)."""
    name, code, view = "Shift", "AUTOTEST_R5_SH", "ov_shift"
    code_label = "Shift Code"
    START_DATE = "2020-01-01"
    NAV_PU, NAV_AREA, NAV_FC1 = "P1 Production Unit", "P1 Area", "P1 Facility 1"
    result = {"insert": "SKIP", "update": "SKIP", "delete": "SKIP", "self_clean": "SKIP", "error": None}
    t0 = time.time()
    try:
        open_screen(page, name)
        eng = Engine(page, name)
        eng.apply_navigator(values=[NAV_PU, NAV_AREA, NAV_FC1], levels=3)

        grids = page.evaluate("""() => Array.from(document.querySelectorAll('[id$=":T_data"]')).map(e => e.id)""")
        grid_id = grids[0]

        if eng.select_row(grid_id, code):
            verify_row_code(eng, page, code_label, code)
            eng.fill("End Date", START_DATE)
            eng.click("Save")
            eng.apply_navigator(values=[NAV_PU, NAV_AREA, NAV_FC1], levels=3)

        eng.toolbar("New Object")
        page.wait_for_timeout(800)
        eng.fill("Shift Code", code)
        eng.fill("Shift Name", code)
        eng.fill("Start Date", START_DATE)
        eng.fill("Start Time (HH:MI)", "07:00")
        eng.select("Op Production Unit", NAV_PU)
        eng.click("Save")
        result["insert"] = "PASS"

        eng.select_row(grid_id, code)
        verify_row_code(eng, page, code_label, code)
        eng.fill("Shift Name", code + "_UPD")
        eng.click("Save")
        result["update"] = "PASS"

        eng.select_row(grid_id, code)
        verify_row_code(eng, page, code_label, code)
        eng.fill("End Date", START_DATE)
        eng.click("Save")
        result["delete"] = "PASS"

        present = db.code_present(view, code)
        for _ in range(4):
            if not present:
                break
            time.sleep(1.5)
            present = db.code_present(view, code)
        result["self_clean"] = "CLEAN" if not present else "RESIDUAL"

    except Exception as e:
        result["error"] = str(e)[:200]

    result["elapsed_s"] = round(time.time() - t0, 1)
    return result


def _commit_unsaved_changes(page):
    """Plain-OV UNSAVED CHANGES YES/NO dialog (Report Group's real driver handles this) - blocks the
    next GO after a pending edit like End=Start. YES commits the intended change."""
    for sel in ("xpath=//button[normalize-space(.)='YES']", "xpath=//button[normalize-space(.)='Yes']"):
        b = page.locator(sel)
        if b.count() and b.first.is_visible():
            b.first.click()
            page.wait_for_timeout(800)
            return True
    return False


def run_report_group(page):
    """Real driver: plain OV, date-only navigator (no cascade, just GO). Pops an UNSAVED CHANGES
    YES/NO dialog after End=Start that blocks the next GO - same class as round-1's Driver/Truck/Trailer."""
    name, code, view = "Report Group", "AUTOTEST_R5_RG", "ov_report_group"
    code_label = "Reporting Group Code"
    START_DATE = "2000-01-01"
    result = {"insert": "SKIP", "update": "SKIP", "delete": "SKIP", "self_clean": "SKIP", "error": None}
    t0 = time.time()
    try:
        open_screen(page, name)
        eng = Engine(page, name)
        eng.click("GO")
        _commit_unsaved_changes(page)

        grids = page.evaluate("""() => Array.from(document.querySelectorAll('[id$=":T_data"]')).map(e => e.id)""")
        grid_id = grids[0]

        if eng.select_row(grid_id, code):
            verify_row_code(eng, page, code_label, code)
            eng.fill("End Date", START_DATE)
            eng.click("Save")
            _commit_unsaved_changes(page)
            eng.click("GO")
            _commit_unsaved_changes(page)

        eng.toolbar("New Object")
        page.wait_for_timeout(800)
        eng.fill("Reporting Group Code", code)
        eng.fill("Reporting Group Name", code)
        eng.fill("Start Date", START_DATE)
        eng.fill("Description", "AUTOTEST Report Group R5 description")
        eng.select("Business Area", "__FIRST__")
        eng.click("Save")
        result["insert"] = "PASS"

        eng.select_row(grid_id, code)
        verify_row_code(eng, page, code_label, code)
        eng.fill("Reporting Group Name", code + "_UPD")
        eng.click("Save")
        result["update"] = "PASS"

        eng.select_row(grid_id, code)
        verify_row_code(eng, page, code_label, code)
        eng.fill("End Date", START_DATE)
        eng.click("Save")
        _commit_unsaved_changes(page)
        result["delete"] = "PASS"

        eng.click("GO")
        _commit_unsaved_changes(page)

        present = db.code_present(view, code)
        for _ in range(4):
            if not present:
                break
            time.sleep(1.5)
            present = db.code_present(view, code)
        result["self_clean"] = "CLEAN" if not present else "RESIDUAL"

    except Exception as e:
        result["error"] = str(e)[:200]

    result["elapsed_s"] = round(time.time() - t0, 1)
    return result


def run_perf_interval(page):
    """Real driver: OV-GM 7-group PER-FIELD nav (G:5 skipped, zero options) + a screen-local Well
    Bore Interval popup needing an INNER GO before its list populates (the generic engine popup
    helper would false-report 'empty source list' without this) + mandatory Reservoir Block
    Formation dd. Nav cascade driven via raw select_dropdown-equivalent (per-field groups, not the
    generic apply_navigator single-row cascade)."""
    name, code, view = "Perforation Interval", "AUTOTEST_R5_PI", "ov_perf_interval"
    code_label = "Perforation Interval Code"
    START_DATE = "2020-01-01"
    NAV = ((1, "P1 Production Unit"), (2, "P1 Area"), (3, "P1 Facility 1"),
           (4, "P1 W008 OP"), (6, "P1 W008 WB001"), (7, "P1 W008 WB001 WBI001"))
    POPUP_GRID = "Objects:form:T_data"
    NAV_WBI = "P1 W008 WB001 WBI001"
    result = {"insert": "SKIP", "update": "SKIP", "delete": "SKIP", "self_clean": "SKIP", "error": None}
    t0 = time.time()

    def _raw_select_nav(g, val):
        base = f"nav:form:G:{g}:R:1:C:0:dd_input"
        btn_base = base[: -len("_input")]
        page.locator(css(btn_base + "_button")).first.click()
        page.wait_for_timeout(700)
        page.locator(f"xpath=//*[@id='{btn_base}_panel']//tr[normalize-space(@data-item-label)='{val}']").first.click(timeout=8000)
        page.wait_for_timeout(800)

    def _pick_wbi_popup(pin_id):
        page.evaluate("(id) => { const b = document.getElementById(id + 'B'); if (b) b.click(); }", pin_id)
        page.wait_for_selector('css=[id="popupIFrame"]', state="visible", timeout=15000)
        page.wait_for_timeout(2000)
        fl = page.frame_locator('css=[id="popupIFrame"]')
        fl.locator('css=[id="button:form:B"]').click()
        page.wait_for_timeout(2500)
        fr = None
        for f in page.frames:
            if f != page.main_frame and f.query_selector(f'[id="{POPUP_GRID}"]'):
                fr = f
                break
        if fr is None:
            raise RuntimeError(f"popup frame with {POPUP_GRID} not found")
        picked = fr.evaluate(
            """(args) => { const [gid, want] = args;
                const tb = document.getElementById(gid); if (!tb) return false;
                for (const tr of tb.querySelectorAll('tr')) {
                    const inp = tr.querySelector('td input');
                    const v = inp ? inp.value.trim() : (tr.innerText || '').trim();
                    if (v === want || v.startsWith(want)) {
                        const td = tr.querySelector('td'); if (td) { td.click(); return true; } } }
                return false; }""",
            [POPUP_GRID, NAV_WBI])
        if not picked:
            raise RuntimeError(f"popup row {NAV_WBI!r} not found in {POPUP_GRID} after inner GO")
        page.wait_for_selector('css=[id="popupIFrame"]', state="hidden", timeout=15000)
        page.wait_for_timeout(800)

    try:
        open_screen(page, name)
        eng = Engine(page, name)
        for g, val in NAV:
            _raw_select_nav(g, val)
        eng._click_go()
        eng._refresh_field_map()

        grids = page.evaluate("""() => Array.from(document.querySelectorAll('[id$=":T_data"]')).map(e => e.id)""")
        grid_id = grids[0]

        def _reapply_nav():
            for g, val in NAV:
                _raw_select_nav(g, val)
            eng._click_go()
            eng._refresh_field_map()

        if eng.select_row(grid_id, code):
            verify_row_code(eng, page, code_label, code)
            eng.fill("End Date", START_DATE)
            eng.click("Save")
            _reapply_nav()

        eng.toolbar("New Object")
        page.wait_for_timeout(800)
        eng.fill("Perforation Interval Code", code)
        eng.fill("Perforation Interval Name", code)
        eng.fill("Start Date", START_DATE)
        pin_field = eng._field("Well Bore Interval")
        _pick_wbi_popup(pin_field["id"])
        eng._refresh_field_map()
        eng.select("Reservoir Block Formation", "__FIRST__")
        eng.click("Save")
        result["insert"] = "PASS"

        eng.select_row(grid_id, code)
        verify_row_code(eng, page, code_label, code)
        eng.fill("Perforation Interval Name", code + "_UPD")
        eng.click("Save")
        result["update"] = "PASS"

        eng.select_row(grid_id, code)
        verify_row_code(eng, page, code_label, code)
        eng.fill("End Date", START_DATE)
        eng.click("Save")
        result["delete"] = "PASS"

        present = db.code_present(view, code)
        for _ in range(4):
            if not present:
                break
            time.sleep(1.5)
            present = db.code_present(view, code)
        result["self_clean"] = "CLEAN" if not present else "RESIDUAL"

    except Exception as e:
        result["error"] = str(e)[:200]

    result["elapsed_s"] = round(time.time() - t0, 1)
    return result


def run_remote_endpoint_config(page):
    """Real driver: TV-style inline-editable grid, no navigator, INVARIANT (physical delete). Code
    must be a lowercase DNS-slug (NOT AUTOTEST_ prefix - confirmed live rejection otherwise). Grid
    interaction driven raw (matching the real driver exactly) since this is a TV inline-grid pattern,
    distinct from the Engine's OV/OV-GM row-select+form path."""
    name, view = "Remote Endpoint Configuration", "OV_ENDPOINT_CONFIG"
    grid_id = "endpointconfig:form:T_data"
    code = f"autotest-r5-{int(time.time())}"
    name_val = f"AUTOTEST REC R5 {code[-10:]}"
    result = {"insert": "SKIP", "update": "SKIP", "delete": "SKIP", "self_clean": "SKIP", "error": None}
    t0 = time.time()

    def _type_cell(cell_id, value):
        loc = page.locator(f'css=[id="{cell_id}"]')
        loc.click()
        loc.fill("")
        loc.type(value, delay=30)
        page.keyboard.press("Tab")
        page.wait_for_timeout(600)

    def _menu_item(icon_class):
        page.locator(
            f"xpath=//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'{icon_class}')]]"
        ).first.hover()
        return page.locator(
            f"xpath=//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'{icon_class}')]]"
            "//ul[contains(@class,'ui-menu-child')]//a"
        ).first

    def _blank_row_index():
        return page.evaluate(
            "() => { const m = document.querySelectorAll('input[id^=\"endpointconfig:form:T:\"][id$=\":C0_in\"]');"
            " for (const e of m) { if ((e.value||'') === '') { return parseInt(e.id.split(':')[3]); } }"
            " return -1; }"
        )

    def _row_by_code(want):
        return page.evaluate(
            "(code) => { const m = document.querySelectorAll('input[id^=\"endpointconfig:form:T:\"][id$=\":C0_in\"]');"
            " for (const e of m) { if ((e.value||'') === code) { return parseInt(e.id.split(':')[3]); } }"
            " return -1; }",
            want,
        )

    def _save():
        # Bug found live (round-5 first attempt): a naive title-based locator here found ZERO
        # matches on the 2nd+ Save call - EC blanks the anchor's title attribute after the first
        # Save/hover interaction (same gotcha engine.py's own _save() already documents and works
        # around). Fix: reuse the real driver's own ec.save(), which has the toggle+Ctrl+S fallback.
        ec.save(page)
        page.wait_for_timeout(1000)

    try:
        open_screen(page, name)

        row = _blank_row_index()
        if row < 0:
            item = _menu_item("ui-icon-insert")
            item.wait_for(state="visible", timeout=10000)
            item.click()
            page.wait_for_timeout(1000)
            row = _blank_row_index()
        if row < 0:
            raise RuntimeError("no blank row appeared after Insert")
        base = f"endpointconfig:form:T:{row}:C"
        _type_cell(base + "0_in", code)
        _type_cell(base + "1_in", name_val)
        page.locator(css(base + "2_dd_button")).first.click()
        page.wait_for_timeout(700)
        page.locator(f"xpath=//*[@id='{base}2_dd_panel']//tr[1]").first.click()
        page.wait_for_timeout(500)
        _save()
        result["insert"] = "PASS"

        present = db.code_present(view, code)
        for _ in range(4):
            if present:
                break
            time.sleep(1.5)
            present = db.code_present(view, code)
        assert present, "not in OV_ENDPOINT_CONFIG"
        ok, act = db.field_equals(view, code, "NAME", name_val)
        assert ok, f"DB NAME={act!r} != {name_val!r}"

        row = _row_by_code(code)
        if row < 0:
            raise RuntimeError(f"ROW IDENTITY: code {code!r} not found for update - aborting")
        name_upd = name_val + " UPDATED"
        _type_cell(f"endpointconfig:form:T:{row}:C1_in", name_upd)
        _save()
        result["update"] = "PASS"

        def _v_upd():
            ok, act = db.field_equals(view, code, "NAME", name_upd)
            assert ok, f"DB NAME={act!r} != {name_upd!r}"
        _v_upd()

        row = _row_by_code(code)
        if row < 0:
            raise RuntimeError(f"ROW IDENTITY: code {code!r} not found for delete - aborting")
        check_id = f"endpointconfig:form:T:{row}:C0_in"
        actual_code = page.locator(f'css=[id="{check_id}"]').first.input_value()
        if actual_code != code:
            raise RuntimeError(f"ROW IDENTITY MISMATCH before delete: expected {code!r}, got {actual_code!r}")
        page.locator(f'css=[id="{check_id}"]').click()
        page.wait_for_timeout(400)
        item = _menu_item("ui-icon-delete")
        item.wait_for(state="visible", timeout=10000)
        item.click()
        page.wait_for_timeout(800)
        _save()
        result["delete"] = "PASS"

        def _v_del():
            assert not db.code_present(view, code), "still in OV_ENDPOINT_CONFIG"
        _v_del()

        residual = db.count_like(view, "autotest-r5-")
        result["self_clean"] = "CLEAN" if residual == 0 else f"RESIDUAL={residual}"

    except Exception as e:
        result["error"] = str(e)[:200]

    result["elapsed_s"] = round(time.time() - t0, 1)
    return result


overall = {}

with sync_playwright() as p:
    b = p.chromium.launch(headless=not HEADED, slow_mo=150 if HEADED else 0,
                           args=["--ignore-certificate-errors", "--start-maximized"])
    page = b.new_context(ignore_https_errors=True, no_viewport=HEADED).new_page()
    page.goto(EC_URL, wait_until="domcontentloaded", timeout=45000)

    for cfg in SCREENS:
        r = run_standard_ov(page, cfg)
        overall[cfg["name"]] = r
        print(f"[{cfg['name']}] insert={r['insert']} update={r['update']} delete={r['delete']} "
              f"self_clean={r['self_clean']} elapsed={r['elapsed_s']}s error={r['error']}")

    for label, fn in [("Shift", run_shift), ("Report Group", run_report_group),
                       ("Perforation Interval", run_perf_interval),
                       ("Remote Endpoint Configuration", run_remote_endpoint_config)]:
        r = fn(page)
        overall[label] = r
        print(f"[{label}] insert={r['insert']} update={r['update']} delete={r['delete']} "
              f"self_clean={r['self_clean']} elapsed={r['elapsed_s']}s error={r['error']}")

    if HEADED:
        page.wait_for_timeout(2000)
    b.close()

print("\n" + "=" * 70 + "\nSUMMARY")
for name, r in overall.items():
    ok = r["insert"] == "PASS" and r["update"] == "PASS" and r["delete"] == "PASS" and r["self_clean"] == "CLEAN"
    print(f"  {'OK ' if ok else 'X  '} {name:<32} {r['elapsed_s']:>5}s  {r['error'] or ''}")

with open(str(_HERE / "stability_test_round5_results.json"), "w", encoding="utf-8") as f:
    json.dump(overall, f, indent=2)

n_ok = sum(1 for r in overall.values() if r["insert"] == "PASS" and r["update"] == "PASS" and r["delete"] == "PASS" and r["self_clean"] == "CLEAN")
print(f"\n{n_ok}/{len(overall)} screens: full I-U-D PASS + self-clean")
