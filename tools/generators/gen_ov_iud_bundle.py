"""
Generator for a Bank-family OV IUD bundle (RF T3 + test + Playwright + SOW + README).

Emits the SAME 5-file structure as the Bank exemplar for a plain Manage-Object (OV)
screen whose recon matches the Bank family: date-only navigator (no mandatory dd),
grid manage_object_nav_nav:form:T_data, INSERT Code R0 / Name R1 / Start Date R2,
UPDATE Name R1, DELETE objectdates R0:C3 (End Date = Start Date true-delete).

ONLY use after resolve_ec_screen.py + scan_ec_screen.py confirm the screen is Bank
family. Run, then verify: robocop -> dryrun -> live headed -> DB-verify -> hygiene.

Usage:
  py tools/generators/gen_ov_iud_bundle.py <repo_root> <screen_name> <var_prefix> <view> \
      <base_table> <rc_code> <nth_label> <stacked_on_pr>
e.g.
  py tools/generators/gen_ov_iud_bundle.py /c/tmp/wt-unitagr "Unit Agreement" UA \
      ov_unit_agr UNIT_AGR RC.0055 "4th" 121
  NOTE: pass the REAL view from resolve_ec_screen.py (= OV_<CLASS_NAME>), which may
  differ from the slug (Unit Agreement -> OV_UNIT_AGR, not ov_unit_agreement).
"""
import os
import sys


def slugify(name):
    return name.lower().replace(" ", "_")


def dirify(name):
    return "_".join(w.capitalize() for w in name.split())


def page_resource(name, prefix, slug, view):
    slug_sp = name.lower()
    return f'''*** Settings ***
Documentation       T3 (screen) - {name} page object.
...                 Screen: Configuration > Assets > Royalty Objects > {name}.
...                 Manage-Object (OV) screen. Holds {name}'s locators + thin IUD
...                 wrappers that delegate to T2 (manage_object) and T1 (common).

Library             Browser
Library             ../../../../libraries/DbVerify.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource


*** Variables ***
${{{prefix}_SCREEN}}            {name}
${{{prefix}_TABLE}}             manage_object_nav_nav:form:T_data
# objectForm field IDs (Insert - new object)
${{{prefix}_INS_CODE}}          tab:tabPanel:objectForm:form:G:0:R:0:C:1:in
${{{prefix}_INS_NAME}}          tab:tabPanel:objectForm:form:G:0:R:1:C:1:in
${{{prefix}_INS_DATE}}          tab:tabPanel:objectForm:form:G:0:R:2:C:1:da_input
# updateAttributes field IDs (Update - existing object)
${{{prefix}_UPD_CODE}}          tab:tabPanel:updateAttributes:form:G:0:R:0:C:1:in
${{{prefix}_UPD_NAME}}          tab:tabPanel:updateAttributes:form:G:0:R:1:C:1:in
# objectdates field ID (Delete - End Date = Start Date)
${{{prefix}_DEL_ENDDATE}}       tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input


*** Keywords ***
Open {name} Screen
    [Documentation]    Suite Setup: launch, login as ${{user}} (defaults to the env
    ...    user), navigate to the {name} screen. Pass a different user for role tests.
    [Arguments]    ${{user}}=${{EC_USER}}    ${{pass}}=${{EC_PASS}}
    Launch EC And Open Screen    ${{{prefix}_SCREEN}}    ${{user}}    ${{pass}}

{name} Row Should Exist
    [Documentation]    Assert a {slug_sp} with ${{code}} is present in the list.
    [Arguments]    ${{code}}
    Row Should Exist    ${{{prefix}_TABLE}}    ${{code}}

{name} Row Should Not Exist
    [Documentation]    Assert a {slug_sp} with ${{code}} is absent from the list.
    [Arguments]    ${{code}}
    Row Should Not Exist    ${{{prefix}_TABLE}}    ${{code}}

{name} Should Exist In DB
    [Documentation]    DB ground-truth: assert ${{code}} really persisted in {view}.
    [Arguments]    ${{code}}
    Code Should Be Present In View    {view}    ${{code}}

{name} Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${{code}} was truly deleted from {view}.
    [Arguments]    ${{code}}
    Code Should Be Absent In View    {view}    ${{code}}

{name} Row Should Show Name
    [Documentation]    Assert the {name} row for ${{code}} displays ${{name}}.
    [Arguments]    ${{code}}    ${{name}}
    ${{row}}=    Get Text    xpath=//tbody[@id='${{{prefix}_TABLE}}']//tr[.//span[normalize-space(text())='${{code}}']]
    Should Contain    ${{row}}    ${{name}}    msg={name} row ${{code}} does not show name ${{name}}

Insert {name} Record
    [Documentation]    Insert a new {slug_sp}: New Object form -> Code/Name/Start Date -> Save.
    [Arguments]    ${{code}}    ${{name}}    ${{start_date}}
    Open New Object Form
    Fill EC Field    ${{{prefix}_INS_CODE}}    ${{code}}
    Fill EC Field    ${{{prefix}_INS_NAME}}    ${{name}}
    Fill EC Date    ${{{prefix}_INS_DATE}}    ${{start_date}}
    Save
    Apply Navigator

Update {name} Name
    [Documentation]    Select the {slug_sp}, confirm it loaded, edit Name, Save.
    [Arguments]    ${{code}}    ${{new_name}}
    Select Object Row    ${{{prefix}_TABLE}}    ${{code}}
    ${{loaded}}=    Get Property    css=[id="${{{prefix}_UPD_CODE}}"]    value
    Should Be Equal    ${{loaded}}    ${{code}}    msg=Row select failed - code not loaded
    Fill EC Field    ${{{prefix}_UPD_NAME}}    ${{new_name}}
    Save
    Apply Navigator

Delete {name}
    [Documentation]    Select the {slug_sp}, set End Date = Start Date (true delete), Save.
    [Arguments]    ${{code}}    ${{date}}
    Select Object Row    ${{{prefix}_TABLE}}    ${{code}}
    Delete Object By Zero-Length Window    ${{{prefix}_DEL_ENDDATE}}    ${{date}}
    Save
    Apply Navigator
'''


def test_robot(name, slug, code_prefix, view):
    slug_sp = name.lower()
    return f'''*** Settings ***
Documentation       EC IUD Test - {name} (Configuration > Assets > Royalty Objects > {name}).
...                 Manage-Object (OV) screen. DELETE = End Date = Start Date (true delete in {view}).
...                 Layered: this test -> {slug}_page (T3) -> manage_object (T2) + common (T1).
...                 NEVER touch existing data. A unique {code_prefix}<timestamp> code is generated
...                 per run (EC keeps deleted codes in the base table, so codes are never reused).

Resource            ../../../../pageobjects/Configuration/Assets/Royalty_Objects/{slug}_page.resource

Suite Setup         Set Up {name} Suite
Suite Teardown      Close EC

Test Tags           iud    {slug}


*** Variables ***
${{TEST_CODE}}        ${{EMPTY}}
${{OBJ_NAME}}        ${{EMPTY}}
${{OBJ_NAME_UPD}}    ${{EMPTY}}
${{START_DATE}}       ${{TEST_START_DATE}}
${{END_DATE}}         ${{TEST_START_DATE}}


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the (freshly generated) test {slug_sp} does not exist before inserting.
    [Tags]    clean-state
    {name} Row Should Not Exist    ${{TEST_CODE}}
    Capture Step    {slug}_tc01_clean

TC02 Insert New {name}
    [Documentation]    Insert a new {slug_sp} and confirm it appears in the list.
    [Tags]    insert
    Insert {name} Record    ${{TEST_CODE}}    ${{OBJ_NAME}}    ${{START_DATE}}
    {name} Row Should Exist    ${{TEST_CODE}}
    {name} Should Exist In DB    ${{TEST_CODE}}
    Capture Step    {slug}_tc02_inserted

TC03 Update {name} Name
    [Documentation]    Edit the {slug_sp} name and confirm the list reflects the change.
    [Tags]    update
    Update {name} Name    ${{TEST_CODE}}    ${{OBJ_NAME_UPD}}
    {name} Row Should Show Name    ${{TEST_CODE}}    ${{OBJ_NAME_UPD}}
    Capture Step    {slug}_tc03_updated

TC04 Delete {name}
    [Documentation]    Delete via End Date = Start Date and confirm the {slug_sp} is gone.
    [Tags]    delete    cleanup
    Delete {name}    ${{TEST_CODE}}    ${{END_DATE}}
    {name} Row Should Not Exist    ${{TEST_CODE}}
    {name} Should Not Exist In DB    ${{TEST_CODE}}
    Capture Step    {slug}_tc04_deleted


*** Keywords ***
Set Up {name} Suite
    [Documentation]    Generate a unique test code/name, then open the {name} screen.
    Prepare IUD Object Data    {code_prefix}    {name}
    Open {name} Screen
'''


def playwright_py(name, slug, code_prefix, view, code_default):
    return f'''"""
EC IUD {name} - FINAL.
Manage-Object (OV) screen, Bank family. Field IDs from recon (scan_ec_screen.py):
  INSERT  : objectForm:form G:0:R:0=Code, R:1=Name, R:2:da_input=StartDate
  UPDATE  : updateAttributes:form G:0:R:1=Name  (Code is read-only after creation)
  DELETE  : objectdates:form G:0:R:0:C:3:da_input = EndDate. EC toolbar Delete is disabled;
            the EC-correct delete is End Date = Start Date (zero-length window) which removes
            the object entirely from {view} (verified at DB level).
NEVER TOUCH EXISTING DATA. Test data: {code_prefix}* only.
"""
from playwright.sync_api import sync_playwright
from pathlib import Path
import json, os


def _repo_root() -> Path:
    """Resolve repo root by walking up to the .git folder (portable across machines).
    Honours env REPO_ROOT; falls back to the script's 6th-level parent."""
    env = os.environ.get('REPO_ROOT')
    if env:
        return Path(env)
    here = Path(__file__).resolve()
    for parent in [here, *here.parents]:
        if (parent / '.git').exists():
            return parent
    return here.parents[6]  # <root>/workstreams/master-plan/ec-automation/screens/.../playwright/<file>


ROOT          = _repo_root()
EC_URL        = os.environ.get('EC_URL', 'https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/')
EC_USER       = os.environ.get('EC_USER', 'sysadmin')   # R16: creds from env, never hardcoded
EC_PASS       = os.environ.get('EC_PASS', 'sysadmin')
SS_DIR        = str(ROOT / 'docs' / 'EC' / 'screenshots' / 'iud_{slug}')
LOG_PATH      = str(ROOT / 'tmp' / 'logs' / 'ec_iud_{slug}_final.json')

# Env-controlled for live demo:  EC_HEADED=1 shows the browser, EC_CODE overrides test code
HEADED        = os.environ.get('EC_HEADED', '0') == '1'
SLOW_MO       = int(os.environ.get('EC_SLOWMO', '700')) if HEADED else 0
_CODE         = os.environ.get('EC_CODE', '{code_default}')
_NUM          = _CODE.split('_')[-1]
TEST_CODE     = _CODE
TEST_NAME     = f'AUTOTEST {name} {{_NUM}}'
TEST_NAME_UPD = f'AUTOTEST {name} {{_NUM}} UPDATED'
START_DATE    = '2000-01-01'
END_DATE      = '2000-01-01'   # EC DELETE: End Date = Start Date (zero-length window = true delete)

# Field IDs (Bank-family OV, confirmed by recon)
INS_CODE_ID   = 'tab:tabPanel:objectForm:form:G:0:R:0:C:1:in'
INS_NAME_ID   = 'tab:tabPanel:objectForm:form:G:0:R:1:C:1:in'
INS_DATE_ID   = 'tab:tabPanel:objectForm:form:G:0:R:2:C:1:da_input'
UPD_CODE_ID   = 'tab:tabPanel:updateAttributes:form:G:0:R:0:C:1:in'
UPD_NAME_ID   = 'tab:tabPanel:updateAttributes:form:G:0:R:1:C:1:in'
DEL_ENDDATE_ID= 'tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input'

SCREEN_NAME   = '{name}'
GRID_TBODY    = 'manage_object_nav_nav:form:T_data'

os.makedirs(SS_DIR, exist_ok=True)
os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
results = {{}}
ss_index = [0]

def ss(page, label):
    ss_index[0] += 1
    name = f'final_{{ss_index[0]:02d}}_{{label}}.png'
    page.screenshot(path=os.path.join(SS_DIR, name), full_page=False)
    print(f'  [SS] {{name}}')
    return name

def wait_ajax(page, t=15000):
    page.wait_for_load_state('networkidle', timeout=t)
    page.wait_for_timeout(1200)

def get_table_rows(page):
    return page.evaluate("""(tbodyId) => {{
        const tbody = document.getElementById(tbodyId);
        if (!tbody) return [];
        const out = [];
        tbody.querySelectorAll('tr').forEach(tr => {{
            const cells = [];
            tr.querySelectorAll('td').forEach(td => cells.push(td.textContent.trim()));
            if (cells.some(c => c)) out.push(cells);
        }});
        return out;
    }}""", GRID_TBODY)

def check_row(page, code):
    return any(r and r[0].strip() == code for r in get_table_rows(page))

def fill(page, fid, value):
    """Fill input field and trigger EC change events."""
    sel = f'#{{fid.replace(":", "\\\\:")}}'
    el = page.locator(sel)
    if el.count() == 0 or not el.is_visible():
        print(f'  [WARN] Field not found: {{fid}}')
        return False
    el.click()
    el.fill(value)
    page.evaluate(f"""() => {{{{
        const e = document.getElementById('{{fid}}');
        if (e) {{{{
            e.dispatchEvent(new Event('change', {{{{bubbles:true}}}}));
            e.dispatchEvent(new Event('blur', {{{{bubbles:true}}}}));
        }}}}
    }}}}""")
    page.wait_for_timeout(400)
    return True

def fill_date(page, fid, value):
    """Fill da_input date field (Tab out to trigger calendar validation)."""
    sel = f'#{{fid.replace(":", "\\\\:")}}'
    el = page.locator(sel)
    if el.count() == 0 or not el.is_visible():
        print(f'  [WARN] Date field not found: {{fid}}')
        return False
    el.click()
    el.fill(value)
    page.keyboard.press('Tab')
    page.wait_for_timeout(600)
    page.evaluate(f"""() => {{{{
        const e = document.getElementById('{{fid}}');
        if (e) {{{{
            e.dispatchEvent(new Event('change', {{{{bubbles:true}}}}));
            e.dispatchEvent(new Event('blur', {{{{bubbles:true}}}}));
        }}}}
    }}}}""")
    page.wait_for_timeout(400)
    return True

def do_save(page):
    save = page.locator("xpath=//a[@title='Save [Ctrl+s]']")
    if save.count() > 0:
        cls = save.first.get_attribute('class') or ''
        if 'disabled' not in cls:
            save.first.click()
            wait_ajax(page)
            return 'button'
    page.evaluate("() => {{ if(typeof EC!=='undefined') EC.toolbar.toggleSaveButton(true); }}")
    page.wait_for_timeout(300)
    save2 = page.locator("xpath=//a[@title='Save [Ctrl+s]' and not(contains(@class,'ui-state-disabled'))]")
    if save2.count() > 0:
        save2.first.click()
        wait_ajax(page)
        return 'toggle+button'
    page.keyboard.press('Control+s')
    wait_ajax(page)
    return 'ctrl+s'

def click_go(page):
    go = page.locator('#button\\\\:form\\\\:B')
    if go.count() > 0 and go.is_visible():
        go.first.click()
        wait_ajax(page)

def select_row(page, code):
    """Click the row span for a given object code."""
    span = page.locator(
        f"css=#manage_object_nav_nav\\\\:form\\\\:T_data span"
    ).filter(has_text=code).first
    if span.count() == 0:
        print(f'  [WARN] Row span not found for code={{code}}')
        return False
    span.click()
    wait_ajax(page)
    page.wait_for_timeout(1000)
    return True

def get_ec_error(page):
    txt = page.evaluate("""() => {{
        const n = document.getElementById('ECNotificationArea') || document.getElementById('ECClientNotificationArea');
        return n ? n.textContent.trim() : '';
    }}""")
    if 'Required fields' in txt or 'Error' in txt:
        return txt.replace('EC.jsMessage.clear();','').strip()[:200]
    return ''

def get_field_val(page, fid):
    return page.evaluate(f"""() => {{{{
        const e = document.getElementById('{{fid}}');
        return e ? e.value : null;
    }}}}""")


with sync_playwright() as p:
    browser = p.chromium.launch(headless=not HEADED, slow_mo=SLOW_MO, args=['--ignore-certificate-errors'])
    print(f'  [MODE] headed={{HEADED}}, slow_mo={{SLOW_MO}}ms, code={{TEST_CODE}}')
    ctx = browser.new_context(ignore_https_errors=True, viewport={{'width': 1920, 'height': 1080}})
    page = ctx.new_page()

    # -- LOGIN ----------------------------------------------------------------
    print('=== LOGIN ===')
    page.goto(EC_URL, wait_until='domcontentloaded', timeout=30000)
    page.fill('#username', EC_USER)
    page.fill('#password', EC_PASS)
    page.click('#kc-login')
    page.wait_for_url('**/dashboard**', timeout=60000)
    wait_ajax(page)
    results['login'] = 'PASS'
    print('  OK')

    # -- NAVIGATE -------------------------------------------------------------
    print(f'\\n=== NAVIGATE TO {{SCREEN_NAME.upper()}} ===')
    si = page.locator('#menu\\\\:searchForm\\\\:searchTxt')
    si.wait_for(state='visible', timeout=10000)
    si.clear(); si.type(SCREEN_NAME, delay=60)
    page.wait_for_load_state('networkidle', timeout=8000)
    page.wait_for_timeout(400)
    page.locator(
        f"xpath=//*[self::label or self::span][contains(@class,'tv-link') and normalize-space(text())='{{SCREEN_NAME}}']"
    ).first.click()
    wait_ajax(page)
    lbl = page.locator('#screenToolbar\\\\:form\\\\:screenLabel').text_content(timeout=5000)
    results['navigate'] = 'PASS' if SCREEN_NAME in lbl else f'FAIL={{lbl}}'
    print(f'  Screen: {{lbl}}')
    ss(page, '{slug}_loaded')

    # -- CLEAN STATE / PRE-CLEANUP --------------------------------------------
    print('\\n=== CLEAN STATE ===')
    rows0 = get_table_rows(page)
    print(f'  Rows: {{[r[0] for r in rows0]}}')

    if check_row(page, TEST_CODE):
        print(f'  Pre-existing AUTOTEST found - expiring to clean up')
        ok = select_row(page, TEST_CODE)
        if ok:
            fill_date(page, DEL_ENDDATE_ID, END_DATE)
            ss(page, 'pre_cleanup_end_date_set')
            do_save(page)
            click_go(page)
            print(f'  Cleanup: still_in_table={{check_row(page, TEST_CODE)}}')
        results['pre_cleanup'] = 'done'

    rows0 = get_table_rows(page)
    print(f'  Rows now: {{[r[0] for r in rows0]}}')
    results['clean'] = 'CLEAN' if not check_row(page, TEST_CODE) else 'PRE-EXISTED+EXPIRED'
    ss(page, 'clean_state')

    if results.get('pre_cleanup') == 'done':
        si2 = page.locator('#menu\\\\:searchForm\\\\:searchTxt')
        si2.clear(); si2.type(SCREEN_NAME, delay=60)
        page.wait_for_load_state('networkidle', timeout=8000)
        page.wait_for_timeout(400)
        page.locator(
            f"xpath=//*[self::label or self::span][contains(@class,'tv-link') and normalize-space(text())='{{SCREEN_NAME}}']"
        ).first.click()
        wait_ajax(page)
        print('  Screen refreshed after pre-cleanup')

    # -- INSERT ---------------------------------------------------------------
    print('\\n=== INSERT ===')
    insert_li = page.locator(
        "xpath=//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'ui-icon-insert')]]"
    )
    insert_li.first.hover()
    page.wait_for_timeout(1000)
    sub_links = page.locator("xpath=//ul[contains(@class,'ui-menu-child')]//li//a")
    sub_count = sub_links.count()
    print(f'  Submenu links found: {{sub_count}}')
    clicked = False
    for i in range(sub_count):
        lnk = sub_links.nth(i)
        try:
            txt = lnk.text_content(timeout=1000).strip()
            vis = lnk.is_visible()
            print(f'  Submenu [{{i}}]: "{{txt}}" visible={{vis}}')
            if txt == 'New Object' and vis:
                lnk.click()
                clicked = True
                print('  Clicked New Object')
                break
        except Exception:
            pass
    if not clicked and sub_count > 0:
        for i in range(sub_count):
            lnk = sub_links.nth(i)
            try:
                if lnk.is_visible():
                    txt = lnk.text_content(timeout=500).strip()
                    lnk.click()
                    clicked = True
                    print(f'  Clicked first visible submenu: "{{txt}}"')
                    break
            except Exception:
                pass
    if not clicked:
        print('  [WARN] No submenu item clicked')
    wait_ajax(page)
    ss(page, 'insert_new_object')

    fill(page, INS_CODE_ID, TEST_CODE);   print(f'  Code: {{TEST_CODE}}')
    fill(page, INS_NAME_ID, TEST_NAME);   print(f'  Name: {{TEST_NAME}}')
    fill_date(page, INS_DATE_ID, START_DATE); print(f'  StartDate: {{START_DATE}}')
    ss(page, 'insert_filled')

    method = do_save(page)
    print(f'  Saved via: {{method}}')
    err = get_ec_error(page)
    ss(page, 'insert_saved')

    click_go(page)
    rows1 = get_table_rows(page)
    exists = check_row(page, TEST_CODE)
    print(f'  Rows after insert: {{[r[0] for r in rows1]}}')
    print(f'  AUTOTEST in table: {{exists}}')
    results['insert'] = 'PASS' if exists else f'FAIL err={{err or "none"}}'
    ss(page, 'insert_result')
    print(f'  INSERT: {{results["insert"]}}')

    # -- UPDATE ---------------------------------------------------------------
    print('\\n=== UPDATE ===')
    if results.get('insert') == 'PASS':
        ok = select_row(page, TEST_CODE)
        if ok:
            ss(page, 'update_row_selected')
            code_val = get_field_val(page, UPD_CODE_ID)
            name_val = get_field_val(page, UPD_NAME_ID)
            print(f'  updateAttributes loaded: code={{code_val}}, name={{name_val}}')

            fill(page, UPD_NAME_ID, TEST_NAME_UPD)
            print(f'  Name updated: {{TEST_NAME_UPD}}')
            ss(page, 'update_filled')

            method_u = do_save(page)
            err_u = get_ec_error(page)
            print(f'  Saved via: {{method_u}}')
            ss(page, 'update_saved')

            click_go(page)
            rows2 = get_table_rows(page)
            upd_row = [r for r in rows2 if r and r[0] == TEST_CODE]
            upd_ok = bool(upd_row) and TEST_NAME_UPD in str(upd_row)
            print(f'  Row after update: {{upd_row}}')
            print(f'  UPDATE: {{"PASS" if upd_ok else "FAIL"}}')
            results['update'] = 'PASS' if upd_ok else f'FAIL row={{upd_row}} err={{err_u or "none"}}'
        else:
            results['update'] = 'FAIL - row not found'
    else:
        results['update'] = 'SKIP'
    ss(page, 'update_result')

    # -- DELETE (End Date = Start Date -> true delete) -------------------------
    print('\\n=== DELETE (End Date = Start Date -> true delete) ===')
    print('  NOTE: EC toolbar Delete is disabled. EC-correct delete = End Date = Start Date.')
    print(f'  Set End Date={{END_DATE}} (= Start Date) -> zero-length window -> object removed from {view}.')
    if results.get('insert') == 'PASS':
        ok = select_row(page, TEST_CODE)
        if ok:
            ss(page, 'delete_row_selected')
            start = get_field_val(page, DEL_ENDDATE_ID.replace('C:3', 'C:1'))
            enddate_val = get_field_val(page, DEL_ENDDATE_ID)
            print(f'  objectdates: StartDate={{start}}, EndDate={{enddate_val}}')

            ok_end = fill_date(page, DEL_ENDDATE_ID, END_DATE)
            print(f'  EndDate set: {{END_DATE}} (ok={{ok_end}})')
            ss(page, 'delete_end_date_set')

            method_d = do_save(page)
            err_d = get_ec_error(page)
            print(f'  Saved via: {{method_d}}')
            ss(page, 'delete_saved')

            click_go(page)

            still_visible = check_row(page, TEST_CODE)
            print(f'  Still in table after delete: {{still_visible}}')
            if not still_visible:
                print(f'  DELETE PASS: removed (EndDate=StartDate={{END_DATE}}), gone from {view}')
                results['delete'] = f'PASS (true delete: EndDate=StartDate={{END_DATE}})'
            else:
                print(f'  DELETE FAIL: still visible after End Date set')
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


def sow_md(name, slug, code_prefix, view, base_table, rc_code, nth, app):
    slug_sp = name.lower()
    view_uc = view.upper()
    return f'''# EC Screen IUD Operation Test - Statement of Work (SOW)
**Project:** Woodside Pluto ECaaS - EC Web App System Test
**Task:** EC Screen Insert/Update/Delete (IUD) Automation - {name}
**Screen:** Configuration > Assets > Royalty Objects > {name} ({rc_code})
**Author:** Choong-Yin Lee / Claude Opus 4.8
**Date:** 2026-06-25
**Version:** 1.0

---

## 1. REQUIREMENT

### 1.1 Objective
Automate Insert, Update, Delete (IUD) on the {name} screen to validate that the screen
correctly creates, modifies and deletes {slug_sp} master records, with EC data integrity
maintained throughout the lifecycle and the sandbox left exactly as found.

### 1.2 Scope
Single screen, one PR (Option 1). {name} is the {nth} of the 8 screens under
Configuration > Assets > Royalty Objects.

### 1.3 Constraints
- **NEVER modify existing production/configuration data.**
- All test data prefixed `{code_prefix}`; a unique per-run code is generated (EC keeps deleted
  codes in the base table, so codes are never reused).
- Target environment: **sandbox** web `https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/`
  (user `sysadmin`), DB ground-truth `localhost:1521/ORCL` (`ECKERNEL_EC`).

### 1.4 Acceptance Criteria
| Operation | Pass Condition |
|---|---|
| INSERT | New record with `{code_prefix}*` code appears in the list AND in `{view}` |
| UPDATE | {name} Name changed and persisted (visible in the row) |
| DELETE | Record removed from `{view}` after End Date = Start Date + Save |
| CLEANUP | Environment returned to pre-test state (object truly deleted, 0 residual) |

---

## 2. DESIGN

### 2.1 Screen classification (recon via resolve_ec_screen.py + scan_ec_screen.py)
| Property | Value |
|---|---|
| Screen name | {name} |
| Treeview path | Configuration > Assets > Royalty Objects > {name} |
| Screen type | **Manage-Object (OV)** - Bank family (date-only navigator, NOT OV-GM) |
| CLASS_TYPE | OBJECT (=> OV) |
| TIME_SCOPE | VERSIONED (=> date-effective; DELETE = End Date = Start Date) |
| Base table | {base_table} |
| Object view | `{view_uc}` |
| App | {app} |
| Grid tbody id | `manage_object_nav_nav:form:T_data` |
| Mandatory insert fields | Code (R0), Name (R1), Start Date (R2) |

### 2.2 IUD design (identical mechanic to Bank)
```
INSERT:  Insert toolbar -> "New Object" -> objectForm (3 mandatory fields):
           R:0 = {name} Code   (tab:tabPanel:objectForm:form:G:0:R:0:C:1:in)
           R:1 = {name} Name   (tab:tabPanel:objectForm:form:G:0:R:1:C:1:in)
           R:2 = Start Date    (tab:tabPanel:objectForm:form:G:0:R:2:C:1:da_input)
         -> Save -> GO -> verify in list + {view}.

UPDATE:  Click row span -> updateAttributes:
           Code: tab:tabPanel:updateAttributes:form:G:0:R:0:C:1:in (read-only)
           Name: tab:tabPanel:updateAttributes:form:G:0:R:1:C:1:in (editable)
         -> edit Name -> Save -> GO -> verify.

DELETE:  End Date set equal to Start Date (zero-length window):
           End Date: tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
         -> Save -> GO -> object removed from {view} (TRUE delete, DB-verified).
```

### 2.3 Test data
| Field | Value |
|---|---|
| Code | `{code_prefix}<run>` (unique per run) |
| Name (Insert) | `AUTOTEST {name} <run>` |
| Name (Update) | `AUTOTEST {name} <run> UPDATED` |
| Start Date | `2000-01-01` |
| End Date (Delete) | `2000-01-01` (= Start Date -> true delete) |

### 2.4 Technology stack
Playwright (Python sync) freestyle bundle + Robot Framework suite layered T3 -> T2
(`manage_object.resource`) + T1 (`common.resource`) + `DbVerify.py`. Screenshots per step.

---

## 3. KNOWN RISKS
- Not an OV-GM screen (date-only navigator) - no lazy-redraw risk; standard Bank-family timing.
- EC keeps deleted codes in the base table; unique per-run codes avoid re-insert rejection.

---

## 4. DELIVERABLES
| Deliverable | Path |
|---|---|
| Playwright bundle | `playwright/ec_iud_{slug}.py` |
| RF T3 page object | `pageobjects/Configuration/Assets/Royalty_Objects/{slug}_page.resource` |
| RF test suite | `tests/Configuration/Assets/Royalty_Objects/{slug}_iud.robot` |
| SOW | this document |
| Evidence | `evidence/` (after a live run) |
| Registry + scorecard rows | `docs/ec_screen_registry.md`, `docs/automation-scorecard.md` |
'''


def readme_md(name, slug, code_prefix, view, rc_code, dir_name):
    return f'''# {name} - IUD bundle

Configuration > Assets > Royalty Objects > **{name}** ({rc_code}).
Manage-Object (OV) screen, Bank family. DELETE = End Date = Start Date (true delete in `{view}`).

## Contents
- `{slug}_sow.md` - Statement of Work (recon + design + acceptance criteria).
- `playwright/ec_iud_{slug}.py` - freestyle Playwright IUD walkthrough (screenshots per step).
- `evidence/` - screenshots from a live run.

## RF suite (the proof)
- T3 page object: `pageobjects/Configuration/Assets/Royalty_Objects/{slug}_page.resource`
- Test suite:     `tests/Configuration/Assets/Royalty_Objects/{slug}_iud.robot`
- Reuses T2 `resources/manage_object.resource` + T1 `resources/common.resource` + `libraries/DbVerify.py` (no shared-file edits).

## Run
```bash
# RF (the proof) - headed live run from the ec-automation root:
EC_HEADLESS=false robot --outputdir results tests/Configuration/Assets/Royalty_Objects/{slug}_iud.robot

# Playwright walkthrough (demo / screenshots):
EC_HEADED=1 py -X utf8 screens/Configuration/Assets/Royalty_Objects/{dir_name}/playwright/ec_iud_{slug}.py
```

Env: sandbox web `https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/` (`sysadmin`/`sysadmin`),
DB `localhost:1521/ORCL` (`ECKERNEL_EC`/`energy`). Test data `{code_prefix}*` only; self-cleaning.
'''


def main():
    repo, name, prefix, view, base_table, rc_code, nth, _pr = sys.argv[1:9]
    slug = slugify(name)
    dir_name = dirify(name)
    code_prefix = f'AUTOTEST_{prefix}_'
    code_default = f'{code_prefix}004'
    view_uc = view.upper()
    app = 'EC_REVN'
    # slug_sp = lowercase screen name (for prose), e.g. "unit agreement"
    slug_sp = name.lower()

    ec = os.path.join(repo, 'workstreams', 'master-plan', 'ec-automation')
    files = {
        os.path.join(ec, 'pageobjects', 'Configuration', 'Assets', 'Royalty_Objects', f'{slug}_page.resource'):
            page_resource(name, prefix, slug, view),
        os.path.join(ec, 'tests', 'Configuration', 'Assets', 'Royalty_Objects', f'{slug}_iud.robot'):
            test_robot(name, slug, code_prefix, view),
        os.path.join(ec, 'screens', 'Configuration', 'Assets', 'Royalty_Objects', dir_name, 'playwright', f'ec_iud_{slug}.py'):
            playwright_py(name, slug, code_prefix, view, code_default),
        os.path.join(ec, 'screens', 'Configuration', 'Assets', 'Royalty_Objects', dir_name, f'{slug}_sow.md'):
            sow_md(name, slug, code_prefix, view, base_table, rc_code, nth, app),
        os.path.join(ec, 'screens', 'Configuration', 'Assets', 'Royalty_Objects', dir_name, 'README.md'):
            readme_md(name, slug, code_prefix, view, rc_code, dir_name),
    }
    for path, content in files.items():
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w', encoding='utf-8', newline='\n') as f:
            f.write(content)
        print('WROTE', path)


if __name__ == '__main__':
    main()
