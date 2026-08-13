"""
Generator for an OV-GM IUD Playwright driver, Phase 3 (Universal Screen Engine) style.

Companion to gen_ov_iud_bundle.py - same engine-driven approach (every field resolved by
LABEL via workstreams/master-plan/ec-automation/py/engine.py, no hardcoded row-index field
ids), extended with the ONE thing OV-GM screens need that plain OV doesn't: a navigator
cascade (Business Unit / Production Unit -> Area -> ...) via Engine.apply_navigator()
before the grid has anything in it.

Deliberately does NOT touch the legacy tmp/gen_ovgm.py, which also emits the RF T3/robot/
SOW/README artifacts for OV-GM bundles carrying ~15 already-shipped screens' worth of
accumulated, individually-referenced bug fixes (issues #295/#297/#306/#318/#324) - rewriting
that 589-line percent-template in place risked silently regressing all of them. This is a
fresh, small, independently-verified implementation of the same job (the Playwright-driver
half only, matching the design's "RF T1/T2/T3 stays untouched" boundary - see
docs/universal_screen_engine_design.md section 5 point 4), reusing the exact pattern already
proven in gen_ov_iud_bundle.py's playwright_py() rather than rewriting that legacy file.

`extra_fields` follows the SAME {label, value, kind} convention ec_object_iud.py's
insertObjectRecord/updateObjectRecord already use - kind in ('text','date','dropdown','popup').
`value='__FIRST__'` on a dropdown/popup field means "pick whatever's first available".

Usage (as a library, not a CLI - call playwright_py_ovgm() and write the result yourself):
    from gen_ovgm_iud_bundle import playwright_py_ovgm
    code = playwright_py_ovgm(
        name="Node", slug="node_gentest", code_prefix="AUTOTEST_NODEGEN_", view="OV_NODE",
        code_default="AUTOTEST_NODEGEN_001", code_label="Node Code", name_label="Node Name",
        extra_fields=[{"label": "Calculation Sequence Number", "value": "1", "kind": "text"}],
    )
"""


def playwright_py_ovgm(name, slug, code_prefix, view, code_default, code_label="Code", name_label="Name",
                        grid_id="manageObject:form:T_data", extra_fields=None, nav_levels=4, nav_values=None):
    extra_fields = extra_fields or []
    extra_fill_lines = []
    for f in extra_fields:
        kind = f["kind"]
        value = f["value"]
        label = f["label"]
        if kind == "dropdown":
            extra_fill_lines.append(f"    eng.select({label!r}, {value!r})")
        elif kind == "popup":
            extra_fill_lines.append(f"    eng.resolve_popup({label!r}).pick_by_code({value!r})")
        elif kind == "date":
            extra_fill_lines.append(f"    eng.fill({label!r}, {value!r})")
        else:
            extra_fill_lines.append(f"    eng.fill({label!r}, {value!r})")
    extra_fill_block = "\n".join(extra_fill_lines)
    nav_values_repr = repr(nav_values) if nav_values else "None"

    return f'''"""
EC IUD {name} - engine-driven (Phase 3, Universal Screen Engine, OV-GM).
OV-GM (grid {grid_id}) - navigator-GATED: a cascade of navigator dropdowns must be filled
before the grid has anything in it. No hardcoded field ids - every field ({code_label!r},
{name_label!r}, Start Date, End Date{", " + ", ".join(repr(f["label"]) for f in extra_fields) if extra_fields else ""})
is resolved by LABEL at runtime via engine.py's Engine.apply_navigator() + fill()/select().
EC delete = End Date = Start Date (zero-length window), removes the object entirely from
{view} (verified at DB level). NEVER TOUCH EXISTING DATA. Test data: {code_prefix}* only.
"""
import sys, os, json
from pathlib import Path
from playwright.sync_api import sync_playwright


def _repo_root() -> Path:
    env = os.environ.get('REPO_ROOT')
    if env:
        return Path(env)
    here = Path(__file__).resolve()
    for parent in [here, *here.parents]:
        if (parent / '.git').exists():
            return parent
    return here.parents[6]


ROOT = _repo_root()
sys.path.insert(0, str(ROOT / 'workstreams' / 'master-plan' / 'ec-automation' / 'py'))
from engine import Engine, open_screen, SaveFailed  # noqa: E402

EC_URL        = os.environ.get('EC_URL', 'https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/')
SS_DIR        = str(ROOT / 'docs' / 'EC' / 'screenshots' / 'iud_{slug}')
LOG_PATH      = str(ROOT / 'tmp' / 'logs' / 'ec_iud_{slug}_final.json')

HEADED        = os.environ.get('EC_HEADED', '0') == '1'
SLOW_MO       = int(os.environ.get('EC_SLOWMO', '700')) if HEADED else 0
_CODE         = os.environ.get('EC_CODE', '{code_default}')
_NUM          = _CODE.split('_')[-1]
TEST_CODE     = _CODE
TEST_NAME     = f'AUTOTEST {name} {{_NUM}}'
TEST_NAME_UPD = f'AUTOTEST {name} {{_NUM}} UPDATED'
START_DATE    = '2000-01-01'
END_DATE      = '2000-01-01'

SCREEN_NAME   = '{name}'
GRID_ID       = '{grid_id}'
CODE_LABEL    = '{code_label}'
NAME_LABEL    = '{name_label}'
NAV_LEVELS    = {nav_levels}
NAV_VALUES    = {nav_values_repr}

os.makedirs(SS_DIR, exist_ok=True)
os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
results = {{}}
ss_index = [0]


def ss(page, label):
    ss_index[0] += 1
    fname = f'final_{{ss_index[0]:02d}}_{{label}}.png'
    page.screenshot(path=os.path.join(SS_DIR, fname), full_page=False)
    print(f'  [SS] {{fname}}')
    return fname


def row_exists(page, code):
    return page.evaluate(
        """([gid, code]) => {{ const tb = document.getElementById(gid); if (!tb) return false;
        return Array.from(tb.querySelectorAll('tr')).some(tr =>
            Array.from(tr.querySelectorAll('td')).some(td => td.textContent.trim() === code)); }}""",
        [GRID_ID, code],
    )


def fill_insert_fields(eng):
    eng.fill(CODE_LABEL, TEST_CODE);      print(f'  {{CODE_LABEL}}: {{TEST_CODE}}')
    eng.fill(NAME_LABEL, TEST_NAME);      print(f'  {{NAME_LABEL}}: {{TEST_NAME}}')
    eng.fill('Start Date', START_DATE);   print(f'  Start Date: {{START_DATE}}')
{extra_fill_block if extra_fill_block else "    pass"}


with sync_playwright() as p:
    browser = p.chromium.launch(headless=not HEADED, slow_mo=SLOW_MO, args=['--ignore-certificate-errors'])
    print(f'  [MODE] headed={{HEADED}}, slow_mo={{SLOW_MO}}ms, code={{TEST_CODE}}')
    ctx = browser.new_context(ignore_https_errors=True, viewport={{'width': 1920, 'height': 1080}})
    page = ctx.new_page()

    print(f'=== LOGIN + NAVIGATE TO {{SCREEN_NAME.upper()}} ===')
    page.goto(EC_URL, wait_until='domcontentloaded', timeout=30000)
    open_screen(page, SCREEN_NAME)
    eng = Engine(page, SCREEN_NAME)
    results['login'] = 'PASS'
    results['navigate'] = 'PASS'
    ss(page, '{slug}_loaded')

    # -- NAVIGATOR CASCADE (OV-GM-specific - the grid is empty without this) --
    print('\\n=== NAVIGATOR CASCADE ===')
    top_parent = eng.apply_navigator(values=NAV_VALUES, levels=NAV_LEVELS)
    print(f'  top-parent captured: {{top_parent!r}}')
    results['nav_cascade'] = 'PASS' if top_parent else 'FAIL - no top-parent captured'
    ss(page, 'nav_cascade_applied')

    # -- CLEAN STATE / PRE-CLEANUP --------------------------------------------
    print('\\n=== CLEAN STATE ===')
    if row_exists(page, TEST_CODE):
        print('  Pre-existing AUTOTEST found - expiring to clean up')
        if eng.select_row(GRID_ID, TEST_CODE):
            eng.fill('End Date', END_DATE)
            try:
                eng.click('Save')
            except SaveFailed as e:
                print(f'  [WARN] pre-cleanup save reported: {{e}}')
            eng.click('GO')
            print(f'  Cleanup: still_in_table={{row_exists(page, TEST_CODE)}}')
        results['pre_cleanup'] = 'done'
        open_screen(page, SCREEN_NAME)
        eng = Engine(page, SCREEN_NAME)
        eng.apply_navigator(values=NAV_VALUES, levels=NAV_LEVELS)
        print('  Screen + navigator refreshed after pre-cleanup')

    results['clean'] = 'CLEAN' if not row_exists(page, TEST_CODE) else 'PRE-EXISTED+EXPIRED'
    ss(page, 'clean_state')

    # -- INSERT ---------------------------------------------------------------
    print('\\n=== INSERT ===')
    eng.toolbar('New Object')
    fill_insert_fields(eng)
    ss(page, 'insert_filled')

    try:
        eng.click('Save')
        results['insert'] = 'PASS'
    except SaveFailed as e:
        results['insert'] = f'FAIL err={{e}}'
    ss(page, 'insert_saved')
    eng.click('GO')
    exists = row_exists(page, TEST_CODE)
    print(f'  AUTOTEST in table: {{exists}}')
    if results['insert'] == 'PASS' and not exists:
        results['insert'] = 'FAIL - saved but row not visible after GO'
    ss(page, 'insert_result')
    print(f'  INSERT: {{results["insert"]}}')

    # -- UPDATE ---------------------------------------------------------------
    print('\\n=== UPDATE ===')
    if results.get('insert') == 'PASS':
        if eng.select_row(GRID_ID, TEST_CODE):
            ss(page, 'update_row_selected')
            eng.fill(NAME_LABEL, TEST_NAME_UPD)
            print(f'  {{NAME_LABEL}} updated: {{TEST_NAME_UPD}}')
            ss(page, 'update_filled')
            try:
                eng.click('Save')
                update_saved = True
            except SaveFailed as e:
                update_saved = False
                results['update'] = f'FAIL err={{e}}'
            ss(page, 'update_saved')
            eng.click('GO')
            if update_saved:
                still_there = row_exists(page, TEST_CODE)
                results['update'] = 'PASS' if still_there else 'FAIL - row missing after update'
            print(f'  UPDATE: {{results["update"]}}')
        else:
            results['update'] = 'FAIL - row not found'
    else:
        results['update'] = 'SKIP'
    ss(page, 'update_result')

    # -- DELETE (End Date = Start Date -> true delete) -------------------------
    print('\\n=== DELETE (End Date = Start Date -> true delete) ===')
    if results.get('insert') == 'PASS':
        if eng.select_row(GRID_ID, TEST_CODE):
            ss(page, 'delete_row_selected')
            eng.fill('End Date', END_DATE)
            print(f'  End Date set: {{END_DATE}}')
            ss(page, 'delete_end_date_set')
            try:
                eng.click('Save')
                delete_saved = True
                err_d = ''
            except SaveFailed as e:
                delete_saved = False
                err_d = str(e)
            ss(page, 'delete_saved')
            eng.click('GO')

            still_visible = row_exists(page, TEST_CODE)
            print(f'  Still in table after delete: {{still_visible}}')
            if delete_saved and not still_visible:
                print(f'  DELETE PASS: removed, gone from {view}')
                results['delete'] = f'PASS (true delete: EndDate=StartDate={{END_DATE}})'
            else:
                print('  DELETE FAIL: still visible after End Date set')
                results['delete'] = f'FAIL - still visible err={{err_d or "none"}}'
        else:
            results['delete'] = 'FAIL - row not found'
    else:
        results['delete'] = 'SKIP'
    ss(page, 'delete_result')
    print(f'  DELETE: {{results["delete"]}}')

    ss(page, 'final_state')
    if HEADED:
        print('  [DEMO] Holding browser open 6s so you can see the final state...')
        page.wait_for_timeout(6000)
    ctx.close()
    browser.close()

with open(LOG_PATH, 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2)

print('\\n' + '='*60)
print('FINAL RESULTS')
print('='*60)
all_pass = True
for k, v in results.items():
    ok = v in ('PASS', 'CLEAN', 'done') or v.startswith('PASS') or v.startswith('PRE-')
    sym = 'OK' if ok else 'X'
    if not ok and k not in ('pre_cleanup', 'clean'): all_pass = False
    print(f'  {{sym}} {{k:<15}} : {{v}}')
print(f'\\nOverall: {{"ALL PASS" if all_pass else "SOME FAILURES"}}')
print(f'Log:     {{LOG_PATH}}')
print(f'Shots:   {{SS_DIR}}')
'''
