"""Stability test round 6: the remaining 16 screens (of the 92 total with existing hand-written
drivers) never yet run through the Universal Screen Engine. Production Day Table stays excluded
(self-clean permanently impossible by design, already proven, "run sparingly").

Every config value re-read directly from each screen's own real *_iud.py driver this session -
no extrapolation. Row-identity verification (verify_row_code) applied before every Save that
follows a select_row(), per the standing hard rule from the Contract Inventory incident.

Special-cased (7): Create Calculation (TV dual-grid, VERSIONS panel update, DELETE CALCULATION
button), Financial Item Definition (plain OV via engine.py, no nav - already engine-native),
Financial Item Template (TV via engine.py grid_cell/find_grid_row - already engine-native),
Project Data Mapping Setup (NONSTANDARD StandardNavigator: prefix, Reference-field-blank-on-select
workaround), Reservoir Block Formation (3-object junction: Block+Formation+RBF, teardown in
reverse dependency order), Stream Item (UPDATE deliberately OUT OF SCOPE - EC scheduler job not
configured in this sandbox, owner instruction 2026-08-02; Insert+Delete only), Well Bore /
Well Bore Interval (multi-group per-field nav + screen-local object-picker popup, same class as
round-5's Perforation Interval).

Standard (9): Dummy Tag Event Object, Split Item Other, Test Separator, Transactional Inventory
Layout Set, Transactional Inventory Properties, UOP Key, Well Hole, Well Hookup - all plain-OV or
OV-GM-default-nav screens, same shape proven repeatedly in earlier rounds.
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
from universal_classifier import EC_URL, ajax
from playwright.sync_api import sync_playwright
import DbVerify as db
import ec_object_iud as ec

HEADED = os.environ.get("EC_HEADED", "0") == "1"


def verify_row_code(eng, page, code_label, expected_code):
    f = eng._field(code_label)
    actual = page.locator(css(f["id"])).first.input_value()
    if actual != expected_code:
        raise RuntimeError(
            f"ROW IDENTITY MISMATCH: expected code {expected_code!r}, form shows {actual!r} - "
            f"ABORTING, not touching this row"
        )


SCREENS = [
    {"name": "Dummy Tag Event Object", "view": "ov_dummy_tag_event", "code": "AUTOTEST_R6_DTE", "nav": None,
     "code_label": "Dummy Tag Event Object Code",
     "insert": [("Dummy Tag Event Object Code", None, "text"), ("Dummy Tag Event Object Name", None, "text"),
                ("Start Date", "2000-01-01", "date")],
     "update_label": "Dummy Tag Event Object Name"},
    {"name": "Split Item Other", "view": "ov_split_item_other", "code": "AUTOTEST_R6_SIO", "nav": None,
     "code_label": "Split Item Code",
     "insert": [("Split Item Code", None, "text"), ("Name", None, "text"), ("Start Date", "2000-01-01", "date")],
     "update_label": "Name"},
    {"name": "Test Separator", "view": "ov_testseparator", "code": "AUTOTEST_R6_TSEP", "nav": "ovgm-default",
     "code_label": "Test Separator Code",
     "insert": [("Test Separator Code", None, "text"), ("Test Separator Name", None, "text"),
                ("Start Date", "2000-01-01", "date"), ("Op Production Unit", "__FIRST__", "dropdown")],
     "update_label": "Test Separator Name"},
    {"name": "Transactional Inventory Layout Set", "view": "ov_trans_inv_tmpl_set", "code": "AUTOTEST_R6_TILS", "nav": None,
     "code_label": "Code",
     "insert": [("Code", None, "text"), ("Name", None, "text"), ("Start Date", "2000-01-01", "date")],
     "update_label": "Name"},
    {"name": "Transactional Inventory Properties", "view": "ov_trans_inventory", "code": "AUTOTEST_R6_TIP", "nav": None,
     "code_label": "Code",
     "insert": [("Code", None, "text"), ("Name", None, "text"), ("Start Date", "2000-01-01", "date"),
                ("Sequence Number", "1", "text")],
     "update_label": "Name"},
    {"name": "UOP Key", "view": "ov_fin_uop_depr_key", "code": "AUTOTEST_R6_UOP", "nav": None,
     "code_label": "Code",
     "insert": [("Code", None, "text"), ("Name", None, "text"), ("Start Date", "2000-01-01", "date"),
                ("Company", "__FIRST__", "dropdown"), ("Key Type", "__FIRST__", "dropdown"),
                ("Key Number", "1", "text")],
     "update_label": "Name"},
    {"name": "Well Hole", "view": "ov_well_hole", "code": "AUTOTEST_R6_WHL", "nav": "ovgm-default",
     "code_label": "Well Hole Code",
     "insert": [("Well Hole Code", None, "text"), ("Well Hole Name", None, "text"),
                ("Start Date", "2000-01-01", "date"), ("Op Production Unit", "__FIRST__", "dropdown")],
     "update_label": "Well Hole Name"},
    {"name": "Well Hookup", "view": "ov_well_hookup", "code": "AUTOTEST_R6_WH", "nav": "ovgm-default",
     "code_label": "Well Hookup Code",
     "insert": [("Well Hookup Code", None, "text"), ("Well Hookup Name", None, "text"),
                ("Start Date", "2000-01-01", "date"), ("Op Production Unit", "__FIRST__", "dropdown")],
     "update_label": "Well Hookup Name"},
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

        if cfg["nav"] == "ovgm-default":
            eng.apply_navigator()

        grids = page.evaluate("""() => Array.from(document.querySelectorAll('[id$=":T_data"]')).map(e => e.id)""")
        grid_id = grids[0]

        if eng.select_row(grid_id, code):
            verify_row_code(eng, page, code_label, code)
            eng.fill("End Date", start_date_value)
            eng.click("Save")
            if cfg["nav"] == "ovgm-default":
                eng.apply_navigator()

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


def run_financial_item_definition(page):
    """Real driver: plain OV, custom-URL, no navigator, already engine-native (uses engine.py
    directly). Mandatory: Item Code/Item Name/Start Date/Item Type/Default Cost Object Type/
    Format Mask/Data Fallback Method."""
    name, code, view = "Financial Item Definition", "AUTOTEST_R6_FID", None
    code_label = "Item Code"
    START_DATE = "2000-01-01"
    result = {"insert": "SKIP", "update": "SKIP", "delete": "SKIP", "self_clean": "SKIP", "error": None}
    t0 = time.time()
    try:
        open_screen(page, name)
        eng = Engine(page, name)

        grids = page.evaluate("""() => Array.from(document.querySelectorAll('[id$=":T_data"]')).map(e => e.id)""")
        grid_id = grids[0]

        if eng.select_row(grid_id, code):
            verify_row_code(eng, page, code_label, code)
            eng.fill("End Date", START_DATE)
            eng.click("Save")

        eng.toolbar("New Object")
        page.wait_for_timeout(1000)
        eng.fill("Item Code", code)
        eng.fill("Item Name", code)
        eng.fill("Start Date", START_DATE)
        eng.select("Item Type", "Cost")
        eng.select("Default Cost Object Type", "Cost Center")
        eng.select("Format Mask", "__FIRST__")
        eng.select("Data Fallback Method", "Overridden-Calculated-Interfaced")
        eng.click("Save")
        result["insert"] = "PASS"

        eng.select_row(grid_id, code)
        verify_row_code(eng, page, code_label, code)
        eng.fill("Item Name", code + "_UPD")
        eng.click("Save")
        result["update"] = "PASS"

        eng.select_row(grid_id, code)
        verify_row_code(eng, page, code_label, code)
        sd = eng._field("Start Date")
        sd_val = page.locator(css(sd["id"])).first.input_value()
        eng.fill("End Date", sd_val)
        eng.click("Save")
        result["delete"] = "PASS"

        # No known view name confirmed from the driver comments for this custom class - use
        # the classifier's own grid to confirm absence instead of guessing a view name.
        gone = not eng.select_row(grid_id, code)
        result["self_clean"] = "CLEAN" if gone else "RESIDUAL"

    except Exception as e:
        result["error"] = str(e)[:200]

    result["elapsed_s"] = round(time.time() - t0, 1)
    return result


def run_financial_item_template(page):
    """Real driver: TV (grid templ:form:T_data), physical delete, no navigator. Only Code/Name/
    Valid From are mandatory. Already engine-native (uses eng.grid_cell()/find_grid_row())."""
    name, code = "Financial Item Template", "AUTOTEST_R6_FIT"
    VALID_FROM = "2000-01-01"
    result = {"insert": "SKIP", "update": "SKIP", "delete": "SKIP", "self_clean": "SKIP", "error": None}
    t0 = time.time()
    try:
        open_screen(page, name)
        eng = Engine(page, name)

        grids = page.evaluate("""() => Array.from(document.querySelectorAll('[id$=":T_data"]')).map(e => e.id)""")
        grid_id = grids[0]

        try:
            eng.find_grid_row(grid_id, code)
            pre_exists = True
        except Exception:
            pre_exists = False
        if pre_exists:
            eng.select_grid_row(grid_id, code)
            eng.toolbar("Template", icon="delete")
            page.wait_for_timeout(1000)
            eng.click("Save")

        eng.toolbar("Template", icon="insert")
        page.wait_for_timeout(1000)
        rows = page.evaluate(
            """(gid) => { const tb = document.getElementById(gid);
            return Array.from(tb.querySelectorAll('tr[data-ri]')).map(tr => ({
                ri: parseInt(tr.getAttribute('data-ri'), 10),
                cells: Array.from(tr.querySelectorAll('td')).map(td => {
                    const inp = td.querySelector('input'); return inp ? inp.value : td.textContent.trim();
                }),
            })); }""",
            grid_id,
        )
        row_idx = next(r["ri"] for r in rows if r["cells"][0] == "" and r["cells"][1] == "")
        eng.grid_cell(grid_id, row_idx, "Financial Item Template Code").set(code)
        eng.grid_cell(grid_id, row_idx, "Financial Item Template Name").set(code)
        eng.grid_cell(grid_id, row_idx, "Valid From").set(VALID_FROM)
        eng.click("Save")
        result["insert"] = "PASS"

        row_idx2 = eng.find_grid_row(grid_id, code)
        if row_idx2 is None:
            raise RuntimeError(f"ROW IDENTITY: {code!r} not found in grid for update - aborting")
        eng.grid_cell(grid_id, row_idx2, "Financial Item Template Name").set(code + "_UPD")
        eng.click("Save")
        result["update"] = "PASS"

        row_idx3 = eng.find_grid_row(grid_id, code)
        if row_idx3 is None:
            raise RuntimeError(f"ROW IDENTITY: {code!r} not found in grid for delete - aborting")
        eng.select_grid_row(grid_id, code)
        eng.toolbar("Template", icon="delete")
        page.wait_for_timeout(1000)
        eng.click("Save")
        result["delete"] = "PASS"

        try:
            eng.find_grid_row(grid_id, code)
            gone = False
        except Exception:
            gone = True
        result["self_clean"] = "CLEAN" if gone else "RESIDUAL"

    except Exception as e:
        result["error"] = str(e)[:200]

    result["elapsed_s"] = round(time.time() - t0, 1)
    return result


def run_project_data_mapping_setup(page):
    """Real driver: OV, NONSTANDARD navigator (StandardNavigator:form:..., real GO=buttongo:form:B
    - apply_navigator() doesn't apply). Mandatory: Code/Name/Start Date/Data Entry Source/
    Dataset-Report/Mapping Type + cross-field-OR (Target Property here). KNOWN DEFECT WORKAROUND on
    Update: Reference field fails to auto-populate on row-select - re-select the same value before
    Save."""
    name, code, view = "Project Data Mapping Setup", "AUTOTEST_R6_PDMS", None
    code_label = "Code"
    START_DATE = "2009-01-01"
    DATASET = "Monthly Royalty Calculation Test"
    TARGET_PROPERTY = "Oil Sands Projects"
    REFERENCE = "Allowed Costs - Capital Test"
    result = {"insert": "SKIP", "update": "SKIP", "delete": "SKIP", "self_clean": "SKIP", "error": None}
    t0 = time.time()

    def _apply_dataset_navigator():
        dd_base = "StandardNavigator:form:G:0:R:0:C:3:dd"
        page.locator(css(dd_base + "_button")).first.click()
        page.wait_for_timeout(800)
        page.locator(f"xpath=//*[@id='{dd_base}_panel']//tr[@data-item-label='{DATASET}']").first.click()
        ajax(page)
        page.locator(css("buttongo:form:B")).first.click()
        ajax(page, 15000)

    try:
        open_screen(page, name)
        eng = Engine(page, name)
        _apply_dataset_navigator()

        grids = page.evaluate("""() => Array.from(document.querySelectorAll('[id$=":T_data"]')).map(e => e.id)""")
        grid_id = grids[0] if grids else "manageObject:form:T_data"

        if eng.select_row(grid_id, code):
            verify_row_code(eng, page, code_label, code)
            sd_pre = eng._field("Start Date")
            sd_val_pre = page.locator(css(sd_pre["id"])).first.input_value()
            eng.fill("End Date", sd_val_pre)
            eng.click("Save")
            _apply_dataset_navigator()

        eng.toolbar("New Object")
        page.wait_for_timeout(1000)
        eng.fill("Code", code)
        eng.fill("Name", code)
        eng.fill("Start Date", START_DATE)
        eng.select("Data Entry Source", "__FIRST__")
        eng.select("Dataset/Report", DATASET)
        eng.select("Mapping Type", "__FIRST__")
        eng.select("Target Property", TARGET_PROPERTY)
        eng.select("Reference", REFERENCE)
        eng.click("Save")
        result["insert"] = "PASS"

        eng.select_row(grid_id, code)
        verify_row_code(eng, page, code_label, code)
        eng.fill("Name", code + "_UPD")
        eng.select("Reference", REFERENCE)  # known defect workaround
        eng.click("Save")
        result["update"] = "PASS"

        eng.select_row(grid_id, code)
        verify_row_code(eng, page, code_label, code)
        sd = eng._field("Start Date")
        sd_val = page.locator(css(sd["id"])).first.input_value()
        eng.fill("End Date", sd_val)
        eng.click("Save")
        result["delete"] = "PASS"

        gone = not eng.select_row(grid_id, code)
        result["self_clean"] = "CLEAN" if gone else "RESIDUAL"

    except Exception as e:
        result["error"] = str(e)[:200]

    result["elapsed_s"] = round(time.time() - t0, 1)
    return result


def run_reservoir_block_formation(page):
    """Real driver: 3-object junction (Reservoir Block + Reservoir Formation + Reservoir Block
    Formation, dependent dropdowns). Build parents first, link via RBF, verify I-U-D on RBF, then
    teardown in reverse dependency order (RBF -> Formation -> Block)."""
    SD = "2000-01-01"
    BLK_CODE, BLK_NAME = "AUTOTEST_R6_RBFB", "AUTOTEST R6 RBF Block"
    FRM_CODE, FRM_NAME = "AUTOTEST_R6_RBFF", "AUTOTEST R6 RBF Formation"
    RBF_CODE, RBF_NAME = "AUTOTEST_R6_RBF", "AUTOTEST R6 RBF"
    result = {"insert": "SKIP", "update": "SKIP", "delete": "SKIP", "self_clean": "SKIP", "error": None}
    t0 = time.time()

    def _close_if_present(name, code, code_label, view):
        open_screen(page, name)
        eng = Engine(page, name)
        grids = page.evaluate("""() => Array.from(document.querySelectorAll('[id$=":T_data"]')).map(e => e.id)""")
        grid_id = grids[0]
        if eng.select_row(grid_id, code):
            verify_row_code(eng, page, code_label, code)
            eng.fill("End Date", SD)
            eng.click("Save")

    try:
        # reverse-dependency pre-clean
        _close_if_present("Reservoir Block Formation", RBF_CODE, "Resv Block Formation Code", "ov_resv_block_formation")
        _close_if_present("Reservoir Formation", FRM_CODE, "Reservoir Formation Code", "ov_resv_formation")
        _close_if_present("Reservoir Block", BLK_CODE, "Reservoir Block Code", "ov_resv_block")

        open_screen(page, "Reservoir Block")
        eng_b = Engine(page, "Reservoir Block")
        eng_b.toolbar("New Object")
        page.wait_for_timeout(800)
        eng_b.fill("Reservoir Block Code", BLK_CODE)
        eng_b.fill("Reservoir Block Name", BLK_NAME)
        eng_b.fill("Start Date", SD)
        eng_b.click("Save")

        open_screen(page, "Reservoir Formation")
        eng_f = Engine(page, "Reservoir Formation")
        eng_f.toolbar("New Object")
        page.wait_for_timeout(800)
        eng_f.fill("Reservoir Formation Code", FRM_CODE)
        eng_f.fill("Reservoir Formation Name", FRM_NAME)
        eng_f.fill("Start Date", SD)
        eng_f.click("Save")

        assert db.code_present("ov_resv_block", BLK_CODE), "block not in ov"
        assert db.code_present("ov_resv_formation", FRM_CODE), "formation not in ov"

        open_screen(page, "Reservoir Block Formation")
        eng_r = Engine(page, "Reservoir Block Formation")
        grids = page.evaluate("""() => Array.from(document.querySelectorAll('[id$=":T_data"]')).map(e => e.id)""")
        rbf_grid = grids[0]

        # Real root cause found live (round-6): the "Reservoir Formation" dependent dropdown's
        # data-item-label is keyed by CODE ("AUTOTEST_R6_RBFF"), not by Name - confirmed by
        # dumping the panel's raw HTML. Every earlier failure was searching for FRM_NAME
        # ("AUTOTEST R6 RBF Formation"), which never matches that attribute even though the
        # option is genuinely present and visible (both to a human and in the DOM) the whole
        # time. "Reservoir Block"'s own dropdown happens to key by Name, which is why it always
        # worked and masked this. The pre-existing hand-written driver has the identical mistake,
        # just silently papered over by its own fallback-to-first-available behavior instead of
        # raising an error. Fix: search by FRM_CODE, matching the field's real key.
        eng_r.toolbar("New Object")
        page.wait_for_timeout(800)
        eng_r.fill("Resv Block Formation Code", RBF_CODE)
        eng_r.fill("Resv Block Formation Name", RBF_NAME)
        eng_r.fill("Start Date", SD)
        eng_r.select("Reservoir Block", BLK_NAME)
        eng_r.select("Reservoir Formation", FRM_CODE)
        eng_r.click("Save")
        result["insert"] = "PASS"

        assert db.code_present("ov_resv_block_formation", RBF_CODE), "RBF not in ov"
        ok, act = db.field_equals("ov_resv_block_formation", RBF_CODE, "NAME", RBF_NAME)
        assert ok, f"RBF NAME={act!r} != {RBF_NAME!r}"

        eng_r.select_row(rbf_grid, RBF_CODE)
        verify_row_code(eng_r, page, "Resv Block Formation Code", RBF_CODE)
        eng_r.fill("Resv Block Formation Name", RBF_NAME + "_UPD")
        eng_r.click("Save")
        result["update"] = "PASS"
        ok2, act2 = db.field_equals("ov_resv_block_formation", RBF_CODE, "NAME", RBF_NAME + "_UPD")
        assert ok2, f"RBF NAME={act2!r} != {RBF_NAME + '_UPD'!r}"

        eng_r.select_row(rbf_grid, RBF_CODE)
        verify_row_code(eng_r, page, "Resv Block Formation Code", RBF_CODE)
        eng_r.fill("End Date", SD)
        eng_r.click("Save")

        _close_if_present("Reservoir Formation", FRM_CODE, "Reservoir Formation Code", "ov_resv_formation")
        _close_if_present("Reservoir Block", BLK_CODE, "Reservoir Block Code", "ov_resv_block")
        result["delete"] = "PASS"

        residual = (db.count_like("ov_resv_block_formation", "AUTOTEST")
                    + db.count_like("ov_resv_formation", "AUTOTEST")
                    + db.count_like("ov_resv_block", "AUTOTEST"))
        result["self_clean"] = "CLEAN" if residual == 0 else f"RESIDUAL={residual}"

    except Exception as e:
        result["error"] = str(e)[:200]

    result["elapsed_s"] = round(time.time() - t0, 1)
    return result


def run_stream_item(page):
    """Real driver: custom-URL OV (grid nav:form:T_data), non-standard GO id (buttongo:form:B).
    UPDATE deliberately OUT OF SCOPE - EC scheduler job 'UpdateStreamItem' not configured in this
    sandbox (owner instruction 2026-08-02, reproduced live 3x by the real driver). Name is
    server-derived on Save. Insert + Delete only."""
    name, code, view = "Stream Item", "AUTOTEST_R6_SI", "OV_STREAM_ITEM"
    code_label = "Stream Item Code"
    START_DATE = "2003-01-01"
    POPUP_LABELS = [
        "Stream Item Category", "Product", "Field", "Company", "Stream",
        "Measurement Node", "Calc. Method", "Conversion Method", "Master UOM Group",
        "Daily Accrual Method", "Monthly Accrual Method", "Reporting Category",
    ]
    result = {"insert": "SKIP", "update": "SKIPPED (EC scheduler job not configured, by design)",
              "delete": "SKIP", "self_clean": "SKIP", "error": None}
    t0 = time.time()

    def _go():
        page.locator("#buttongo\\:form\\:B").click()
        ajax(page)
        page.wait_for_timeout(800)

    try:
        open_screen(page, name)
        eng = Engine(page, name)
        _go()

        grids = page.evaluate("""() => Array.from(document.querySelectorAll('[id$=":T_data"]')).map(e => e.id)""")
        grid_id = grids[0]

        if eng.select_row(grid_id, code):
            verify_row_code(eng, page, code_label, code)
            eng.fill("End Date", START_DATE)
            eng.click("Save")
            _go()

        eng.toolbar("New Object")
        page.wait_for_timeout(1000)
        eng.fill("Stream Item Code", code)
        eng.fill("Start Date", START_DATE)
        for lbl in POPUP_LABELS:
            eng.select(lbl, "__FIRST__")
        eng.fill("Name", "AUTOTEST SI R6 (server-derived, ignored)")
        eng.click("Save")
        _go()
        result["insert"] = "PASS"

        assert db.code_present(view, code), "not in OV_STREAM_ITEM"

        eng.select_row(grid_id, code)
        verify_row_code(eng, page, code_label, code)
        eng.fill("End Date", START_DATE)
        eng.click("Save")
        _go()
        result["delete"] = "PASS"

        present = db.code_present(view, code)
        for _ in range(4):
            if not present:
                break
            time.sleep(1.5)
            present = db.code_present(view, code)
        residual = db.count_like(view, "AUTOTEST_R6_SI")
        result["self_clean"] = "CLEAN" if residual == 0 else f"RESIDUAL={residual}"

    except Exception as e:
        result["error"] = str(e)[:200]

    result["elapsed_s"] = round(time.time() - t0, 1)
    return result


def _pick_object_popup(page, pin_id, popup_grid, want):
    """Shared screen-local object-picker (Well Bore / Well Bore Interval): the object popup's list
    grid renders as Objects:form:T_data, already populated on open (NOT PopupList:form:T_data) -
    the generic engine popup helper would false-report an empty source list without this."""
    page.evaluate("(id) => { const b = document.getElementById(id + 'B'); if (b) b.click(); }", pin_id)
    page.wait_for_selector('css=[id="popupIFrame"]', state="visible", timeout=15000)
    page.frame_locator('css=[id="popupIFrame"]').locator(f'css=[id="{popup_grid}"]').first.wait_for(
        state="visible", timeout=15000)
    page.wait_for_timeout(1500)
    fr = None
    for f in page.frames:
        if f != page.main_frame and f.query_selector(f'[id="{popup_grid}"]'):
            fr = f
            break
    if fr is None:
        raise RuntimeError(f"popup frame with {popup_grid} not found")
    picked = fr.evaluate(
        """(args) => { const [gid, want] = args;
            const tb = document.getElementById(gid); if (!tb) return false;
            for (const tr of tb.querySelectorAll('tr')) {
                const inp = tr.querySelector('td input');
                const v = inp ? inp.value.trim() : (tr.innerText || '').trim().split('\\t')[0];
                if (v === want) { const td = tr.querySelector('td'); if (td) { td.click(); return true; } } }
            return false; }""",
        [popup_grid, want])
    if not picked:
        raise RuntimeError(f"popup row {want!r} not found in {popup_grid}")
    page.wait_for_selector('css=[id="popupIFrame"]', state="hidden", timeout=15000)
    page.wait_for_timeout(800)


def run_well_bore(page):
    """Real driver: OV-GM 4-level PER-FIELD nav (G:1..G:4, SPECIFIC values - G:5 zero-options,
    skipped) + mandatory 'Well' popup (first-available under nav scope)."""
    name, code, view = "Well Bore", "AUTOTEST_R6_WB", "ov_well_bore"
    code_label = "Well Bore Code"
    START_DATE = "2020-01-01"
    NAV = ((1, "P1 Production Unit"), (2, "P1 Area"), (3, "P1 Facility 1"), (4, "P1 W008 OP"))
    POPUP_GRID = "Objects:form:T_data"
    result = {"insert": "SKIP", "update": "SKIP", "delete": "SKIP", "self_clean": "SKIP", "error": None}
    t0 = time.time()

    def _raw_select_nav(g, val):
        base = f"nav:form:G:{g}:R:1:C:0:dd_input"
        btn_base = base[: -len("_input")]
        page.locator(css(btn_base + "_button")).first.click()
        page.wait_for_timeout(700)
        page.locator(f"xpath=//*[@id='{btn_base}_panel']//tr[normalize-space(@data-item-label)='{val}']").first.click(timeout=8000)
        page.wait_for_timeout(800)

    def _reapply_nav(eng):
        for g, val in NAV:
            _raw_select_nav(g, val)
        eng._click_go()
        eng._refresh_field_map()

    try:
        open_screen(page, name)
        eng = Engine(page, name)
        _reapply_nav(eng)

        grids = page.evaluate("""() => Array.from(document.querySelectorAll('[id$=":T_data"]')).map(e => e.id)""")
        grid_id = grids[0]

        if eng.select_row(grid_id, code):
            verify_row_code(eng, page, code_label, code)
            eng.fill("End Date", START_DATE)
            eng.click("Save")
            _reapply_nav(eng)

        eng.toolbar("New Object")
        page.wait_for_timeout(800)
        eng.fill("Well Bore Code", code)
        eng.fill("Well Bore Name", code)
        eng.fill("Start Date", START_DATE)
        pin_field = eng._field("Well")
        _pick_object_popup(page, pin_field["id"], POPUP_GRID, NAV[3][1])
        eng._refresh_field_map()
        eng.click("Save")
        result["insert"] = "PASS"

        eng.select_row(grid_id, code)
        verify_row_code(eng, page, code_label, code)
        eng.fill("Well Bore Name", code + "_UPD")
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


def run_well_bore_interval(page):
    """Real driver: OV-GM 6-group PER-FIELD nav (G:1..G:4,G:6 - G:5 zero-options, skipped) +
    mandatory 'Well Bore' popup (the specific nav-scope well bore, not first-available)."""
    name, code, view = "Well Bore Interval", "AUTOTEST_R6_WBI", "ov_well_bore_interval"
    code_label = "Well Bore Interval Code"
    START_DATE = "2020-01-01"
    NAV = ((1, "P1 Production Unit"), (2, "P1 Area"), (3, "P1 Facility 1"),
           (4, "P1 W008 OP"), (6, "P1 W008 WB001"))
    POPUP_GRID = "Objects:form:T_data"
    NAV_WELL_BORE = "P1 W008 WB001"
    result = {"insert": "SKIP", "update": "SKIP", "delete": "SKIP", "self_clean": "SKIP", "error": None}
    t0 = time.time()

    def _raw_select_nav(g, val):
        base = f"nav:form:G:{g}:R:1:C:0:dd_input"
        btn_base = base[: -len("_input")]
        page.locator(css(btn_base + "_button")).first.click()
        page.wait_for_timeout(700)
        page.locator(f"xpath=//*[@id='{btn_base}_panel']//tr[normalize-space(@data-item-label)='{val}']").first.click(timeout=8000)
        page.wait_for_timeout(800)

    def _reapply_nav(eng):
        for g, val in NAV:
            _raw_select_nav(g, val)
        eng._click_go()
        eng._refresh_field_map()

    try:
        open_screen(page, name)
        eng = Engine(page, name)
        _reapply_nav(eng)

        grids = page.evaluate("""() => Array.from(document.querySelectorAll('[id$=":T_data"]')).map(e => e.id)""")
        grid_id = grids[0]

        if eng.select_row(grid_id, code):
            verify_row_code(eng, page, code_label, code)
            eng.fill("End Date", START_DATE)
            eng.click("Save")
            _reapply_nav(eng)

        eng.toolbar("New Object")
        page.wait_for_timeout(800)
        eng.fill("Well Bore Interval Code", code)
        eng.fill("Well Bore Interval Name", code)
        eng.fill("Start Date", START_DATE)
        pin_field = eng._field("Well Bore")
        _pick_object_popup(page, pin_field["id"], POPUP_GRID, NAV_WELL_BORE)
        eng._refresh_field_map()
        eng.click("Save")
        result["insert"] = "PASS"

        eng.select_row(grid_id, code)
        verify_row_code(eng, page, code_label, code)
        eng.fill("Well Bore Interval Name", code + "_UPD")
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


def run_create_calculation(page):
    """Real driver: TV-style dual grid (calculation:form:T_data header + calculation_version
    companion). Nav = ONE mandatory Calculation Context dd (first-available) - fits
    apply_navigator()'s generic discovery cleanly. Insert = toolbar Insert -> dynamically-placed
    blank inline row -> real keystrokes for Code/Name/Start Date + mandatory Period/Type dds.
    Update = edit the VERSIONS panel's own Name cell (the authoritative source for this screen).
    Delete = purpose-built DELETE CALCULATION button + confirm (not End=Start on the header row)."""
    name, code, view = "Create Calculation", "AUTOTEST_R6_CC", "ov_calculation"
    GRID_PREFIX = "calculation:form:T"
    START_DATE = "2020-01-01"
    result = {"insert": "SKIP", "update": "SKIP", "delete": "SKIP", "self_clean": "SKIP", "error": None}
    t0 = time.time()

    def _rows_c0():
        return {int(k): v for k, v in page.evaluate(
            """(pfx) => { const out={};
                document.querySelectorAll("[id^='"+pfx+":'][id$='C0_in']").forEach(e=>{
                  const m=e.id.match(/T:(\\d+):C0_in/); if(m) out[m[1]]=e.value; });
                return out; }""", GRID_PREFIX).items()}

    def _blank_row():
        for r, v in sorted(_rows_c0().items()):
            if not (v or "").strip():
                return r
        return None

    def _row_of(want):
        for r, v in _rows_c0().items():
            if (v or "").strip() == want:
                return r
        return None

    def _tv_fill(cell_id, value):
        sel = f"[id='{cell_id}']"
        page.click(sel)
        page.wait_for_timeout(300)
        page.keyboard.press("Control+a")
        page.keyboard.type(value, delay=25)
        page.keyboard.press("Tab")
        page.wait_for_timeout(500)

    def _tv_insert_blank():
        page.locator("xpath=//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'ui-icon-insert')]]").first.hover()
        page.wait_for_timeout(900)
        links = page.locator("xpath=//ul[contains(@class,'ui-menu-child')]//li//a")
        for i in range(links.count()):
            ln = links.nth(i)
            if ln.is_visible() and (ln.text_content(timeout=800) or "").strip():
                ln.click()
                break
        ec.wait_ajax(page)

    def _delete_calc():
        r = _row_of(code)
        if r is None:
            raise RuntimeError(f"ROW IDENTITY: {code!r} not found for delete - aborting")
        page.click(f"[id='{GRID_PREFIX}:{r}:C0_in']")
        page.wait_for_timeout(1200)
        actual = page.locator(f"[id='{GRID_PREFIX}:{r}:C0_in']").input_value()
        if actual != code:
            raise RuntimeError(f"ROW IDENTITY MISMATCH: expected {code!r}, got {actual!r} - aborting")
        page.locator("xpath=//button[normalize-space(.)='DELETE CALCULATION' or normalize-space(.)='Delete Calculation']").first.click()
        page.wait_for_timeout(1200)
        for sel in ("xpath=//button[normalize-space(.)='YES']", "xpath=//button[normalize-space(.)='Yes']",
                    "[id='dialogForm:dialogMsgOk']"):
            b = page.locator(sel)
            if b.count() and b.first.is_visible():
                b.first.click()
                break
        ec.wait_ajax(page)

    try:
        open_screen(page, name)
        eng = Engine(page, name)
        eng.apply_navigator()  # single mandatory context dd, first-available, + GO

        if _row_of(code) is not None:
            _delete_calc()
            eng.apply_navigator()

        _tv_insert_blank()
        r = _blank_row()
        if r is None:
            raise RuntimeError("no blank insert row appeared")
        _tv_fill(f"{GRID_PREFIX}:{r}:C0_in", code)
        _tv_fill(f"{GRID_PREFIX}:{r}:C1_in", code)
        _tv_fill(f"{GRID_PREFIX}:{r}:C2_da_input", START_DATE)
        ec.select_dropdown(page, f"{GRID_PREFIX}:{r}:C4_dd_input", "Day")
        page.wait_for_timeout(500)
        ec.select_dropdown(page, f"{GRID_PREFIX}:{r}:C5_dd_input", "Equations")
        page.wait_for_timeout(500)
        ec.save(page)
        err = ec.ec_error(page)
        if err:
            raise RuntimeError(f"EC error on insert save: {err}")
        eng._click_go()
        result["insert"] = "PASS"

        assert _row_of(code) is not None, "code not in grid after insert"
        assert db.code_present(view, code), "not in ov_calculation"

        r2 = _row_of(code)
        actual2 = page.locator(f"[id='{GRID_PREFIX}:{r2}:C0_in']").input_value()
        if actual2 != code:
            raise RuntimeError(f"ROW IDENTITY MISMATCH before update: expected {code!r}, got {actual2!r}")
        page.click(f"[id='{GRID_PREFIX}:{r2}:C0_in']")
        page.wait_for_timeout(1200)
        _tv_fill("calculation_version:form:T:0:C0_in", code + "_UPD")
        ec.save(page)
        err2 = ec.ec_error(page)
        if err2:
            raise RuntimeError(f"EC error on update save: {err2}")
        eng._click_go()
        result["update"] = "PASS"

        _delete_calc()
        err3 = ec.ec_error(page)
        if err3:
            raise RuntimeError(f"EC error on delete: {err3}")
        eng._click_go()
        result["delete"] = "PASS"

        assert _row_of(code) is None, "still in grid"
        assert not db.code_present(view, code), "still in ov_calculation"
        residual = db.count_like(view, "AUTOTEST_R6_CC")
        result["self_clean"] = "CLEAN" if residual == 0 else f"RESIDUAL={residual}"

    except Exception as e:
        result["error"] = str(e)[:200]

    result["elapsed_s"] = round(time.time() - t0, 1)
    return result


def run_all():
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

        for label, fn in [
            ("Financial Item Definition", run_financial_item_definition),
            ("Financial Item Template", run_financial_item_template),
            ("Project Data Mapping Setup", run_project_data_mapping_setup),
            ("Reservoir Block Formation", run_reservoir_block_formation),
            ("Stream Item", run_stream_item),
            ("Well Bore", run_well_bore),
            ("Well Bore Interval", run_well_bore_interval),
            ("Create Calculation", run_create_calculation),
        ]:
            r = fn(page)
            overall[label] = r
            print(f"[{label}] insert={r['insert']} update={r['update']} delete={r['delete']} "
                  f"self_clean={r['self_clean']} elapsed={r['elapsed_s']}s error={r['error']}")

        if HEADED:
            page.wait_for_timeout(2000)
        b.close()

    print("\n" + "=" * 70 + "\nSUMMARY")
    for name, r in overall.items():
        ok = (r["insert"] in ("PASS",) and r["delete"] == "PASS"
              and r["update"] in ("PASS",) or str(r["update"]).startswith("SKIPPED"))
        ok = ok and r["self_clean"] in ("CLEAN",)
        print(f"  {'OK ' if ok else 'X  '} {name:<32} {r['elapsed_s']:>5}s  {r['error'] or ''}")

    with open(str(_HERE / "stability_test_round6_results.json"), "w", encoding="utf-8") as f:
        json.dump(overall, f, indent=2)

    n_ok = sum(1 for r in overall.values()
               if r["insert"] == "PASS" and r["delete"] == "PASS"
               and (r["update"] == "PASS" or str(r["update"]).startswith("SKIPPED"))
               and r["self_clean"] == "CLEAN")
    print(f"\n{n_ok}/{len(overall)} screens: full I-U-D (or documented Insert+Delete-only) PASS + self-clean")
    return overall


if __name__ == "__main__":
    run_all()
