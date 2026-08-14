"""
Generator for a TV (Table-class, grid-cell-editing) IUD Playwright driver - Phase 4 pilot,
Universal Screen Engine style. Companion to gen_ov_iud_bundle.py/gen_ovgm_iud_bundle.py; no TV
generator existed before this (Language, the Phase 2 exemplar, was only ever driven by a one-off
validation script, never a reusable generator).

TV-specific mechanics this encodes (all proven live on Language in Phase 2, reused here as a
generic template): Insert/Delete flyout link text is the class's OWN label (e.g. 'Language'), not
a fixed generic string, and is IDENTICAL under both icons - so toolbar() calls always pass an
`icon` hint to disambiguate. Insert opens a blank row at some index (found via find_grid_row on a
sentinel, not assumed); a Save can re-sort the grid, so any row referenced again afterward must be
re-resolved via find_grid_row(), never a remembered index. Delete = select_grid_row() + toolbar
Delete (icon-pinned) + Save = physical delete (no End Date=Start Date convention here).

Usage (as a library - call playwright_py_tv() and write the result yourself):
    from gen_tv_iud_bundle import playwright_py_tv
    code = playwright_py_tv(
        name="Financial Item Template", slug="fin_item_template", code_prefix="AUTOTEST_FIT_",
        view=None, code_default="AUTOTEST_FIT_001", grid_id="templ:form:T_data",
        code_label="Financial Item Template Code", name_label="Financial Item Template Name",
        class_label="Financial Item Template",
    )
"""


def playwright_py_tv(name, slug, code_prefix, code_default, grid_id, code_label, name_label,
                      class_label, extra_fields=None):
    extra_fields = extra_fields or []
    extra_fill_lines = []
    for ef in extra_fields:
        label = ef["label"]
        value = ef["value"]
        extra_fill_lines.append(f"        eng.grid_cell(GRID_ID, blank_row_idx, {label!r}).set({value!r})")
    extra_fill_block = "\n".join(extra_fill_lines)

    return f'''"""
EC IUD {name} - engine-driven (Phase 4 pilot, Universal Screen Engine, TV).
Table-class (TV) screen, grid-cell editing. No hardcoded field ids - every cell resolved by
COLUMN LABEL at runtime via engine.py's grid_cell()/find_grid_row(), the same generic interaction
layer proven on Language. Physical delete (no End Date=Start Date - that's the OV/OV-GM
convention only). NEVER TOUCH EXISTING DATA. Test data: {code_prefix}* only.
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

EC_URL      = os.environ.get('EC_URL', 'https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/')
SS_DIR      = str(ROOT / 'docs' / 'EC' / 'screenshots' / 'iud_{slug}')
LOG_PATH    = str(ROOT / 'tmp' / 'logs' / 'ec_iud_{slug}_final.json')

HEADED      = os.environ.get('EC_HEADED', '0') == '1'
SLOW_MO     = int(os.environ.get('EC_SLOWMO', '700')) if HEADED else 0
_CODE       = os.environ.get('EC_CODE', '{code_default}')
_NUM        = _CODE.split('_')[-1]
TEST_CODE   = _CODE
TEST_NAME   = f'AUTOTEST {name} {{_NUM}}'
TEST_NAME_UPD = f'AUTOTEST {name} {{_NUM}} UPDATED'

SCREEN_NAME = '{name}'
GRID_ID     = '{grid_id}'
CODE_LABEL  = '{code_label}'
NAME_LABEL  = '{name_label}'
CLASS_LABEL = '{class_label}'

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

    # -- CLEAN STATE / PRE-CLEANUP ---------------------------------------------
    print('\\n=== CLEAN STATE ===')
    try:
        pre_idx = eng.find_grid_row(GRID_ID, TEST_CODE)
        print(f'  Pre-existing AUTOTEST found at row {{pre_idx}} - deleting to clean up')
        eng.select_grid_row(GRID_ID, TEST_CODE)
        eng.toolbar(CLASS_LABEL, icon='delete')
        try:
            eng.click('Save')
        except SaveFailed as e:
            print(f'  [WARN] pre-cleanup save reported: {{e}}')
        results['pre_cleanup'] = 'done'
    except Exception:
        pass
    try:
        eng.find_grid_row(GRID_ID, TEST_CODE)
        results['clean'] = 'PRE-EXISTED+EXPIRED'
    except Exception:
        results['clean'] = 'CLEAN'
    ss(page, 'clean_state')

    # -- INSERT -----------------------------------------------------------------
    print('\\n=== INSERT ===')
    eng.toolbar(CLASS_LABEL, icon='insert')
    # a blank row appears at SOME index after Insert - find it by its own emptiness,
    # not assumed, since the position isn't guaranteed across screens/data volumes
    blank_row_idx = eng.page.evaluate(
        """(gid) => {{ const tb = document.getElementById(gid);
        const rows = Array.from(tb.querySelectorAll('tr[data-ri]'));
        const idx = rows.findIndex(tr => Array.from(tr.querySelectorAll('input')).every(i => !i.value));
        return idx >= 0 ? parseInt(rows[idx].getAttribute('data-ri'), 10) : -1; }}""",
        GRID_ID,
    )
    print(f'  Blank insert row found at index: {{blank_row_idx}}')
    if blank_row_idx < 0:
        results['insert'] = 'FAIL - no blank row found after Insert'
    else:
        eng.grid_cell(GRID_ID, blank_row_idx, CODE_LABEL).set(TEST_CODE)
        eng.grid_cell(GRID_ID, blank_row_idx, NAME_LABEL).set(TEST_NAME)
{extra_fill_block if extra_fill_block else ""}
        ss(page, 'insert_filled')
        try:
            eng.click('Save')
            results['insert'] = 'PASS'
        except SaveFailed as e:
            results['insert'] = f'FAIL err={{e}}'
        ss(page, 'insert_saved')
        try:
            eng.find_grid_row(GRID_ID, TEST_CODE)
        except Exception:
            if results['insert'] == 'PASS':
                results['insert'] = 'FAIL - saved but row not found after Save'
    ss(page, 'insert_result')
    print(f'  INSERT: {{results["insert"]}}')

    # -- UPDATE -------------------------------------------------------------
    print('\\n=== UPDATE ===')
    if results.get('insert') == 'PASS':
        try:
            row_idx = eng.find_grid_row(GRID_ID, TEST_CODE)
            print(f'  Row re-resolved at index {{row_idx}} (never assumed - Save can re-sort)')
            eng.grid_cell(GRID_ID, row_idx, NAME_LABEL).set(TEST_NAME_UPD)
            ss(page, 'update_filled')
            try:
                eng.click('Save')
                results['update'] = 'PASS'
            except SaveFailed as e:
                results['update'] = f'FAIL err={{e}}'
            ss(page, 'update_saved')
        except Exception as e:
            results['update'] = f'FAIL - row not found: {{e}}'
    else:
        results['update'] = 'SKIP'
    print(f'  UPDATE: {{results["update"]}}')

    # -- DELETE (physical - no End Date=Start Date on TV) -------------------
    print('\\n=== DELETE (physical delete) ===')
    if results.get('insert') == 'PASS':
        try:
            eng.select_grid_row(GRID_ID, TEST_CODE)
            ss(page, 'delete_row_selected')
            eng.toolbar(CLASS_LABEL, icon='delete')
            try:
                eng.click('Save')
                deleted = True
            except SaveFailed as e:
                deleted = False
                print(f'  [WARN] delete save reported: {{e}}')
            ss(page, 'delete_saved')
            try:
                eng.find_grid_row(GRID_ID, TEST_CODE)
                results['delete'] = 'FAIL - still present after delete+Save'
            except Exception:
                results['delete'] = 'PASS (physical delete)' if deleted else 'PASS (row gone despite save warning)'
        except Exception as e:
            results['delete'] = f'FAIL - row not found for delete: {{e}}'
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
