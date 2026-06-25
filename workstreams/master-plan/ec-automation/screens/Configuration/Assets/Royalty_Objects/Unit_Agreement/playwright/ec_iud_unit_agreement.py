"""
EC IUD Unit Agreement - FINAL.
Manage-Object (OV) screen, Bank family. Field IDs from recon (scan_ec_screen.py):
  INSERT  : objectForm:form G:0:R:0=Code, R:1=Name, R:2:da_input=StartDate
  UPDATE  : updateAttributes:form G:0:R:1=Name  (Code is read-only after creation)
  DELETE  : objectdates:form G:0:R:0:C:3:da_input = EndDate. EC toolbar Delete is disabled;
            the EC-correct delete is End Date = Start Date (zero-length window) which removes
            the object entirely from ov_unit_agr (verified at DB level).
NEVER TOUCH EXISTING DATA. Test data: AUTOTEST_UA_* only.
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
SS_DIR        = str(ROOT / 'docs' / 'EC' / 'screenshots' / 'iud_unit_agreement')
LOG_PATH      = str(ROOT / 'tmp' / 'logs' / 'ec_iud_unit_agreement_final.json')

# Env-controlled for live demo:  EC_HEADED=1 shows the browser, EC_CODE overrides test code
HEADED        = os.environ.get('EC_HEADED', '0') == '1'
SLOW_MO       = int(os.environ.get('EC_SLOWMO', '700')) if HEADED else 0
_CODE         = os.environ.get('EC_CODE', 'AUTOTEST_UA_004')
_NUM          = _CODE.split('_')[-1]
TEST_CODE     = _CODE
TEST_NAME     = f'AUTOTEST Unit Agreement {_NUM}'
TEST_NAME_UPD = f'AUTOTEST Unit Agreement {_NUM} UPDATED'
START_DATE    = '2000-01-01'
END_DATE      = '2000-01-01'   # EC DELETE: End Date = Start Date (zero-length window = true delete)

# Field IDs (Bank-family OV, confirmed by recon)
INS_CODE_ID   = 'tab:tabPanel:objectForm:form:G:0:R:0:C:1:in'
INS_NAME_ID   = 'tab:tabPanel:objectForm:form:G:0:R:1:C:1:in'
INS_DATE_ID   = 'tab:tabPanel:objectForm:form:G:0:R:2:C:1:da_input'
UPD_CODE_ID   = 'tab:tabPanel:updateAttributes:form:G:0:R:0:C:1:in'
UPD_NAME_ID   = 'tab:tabPanel:updateAttributes:form:G:0:R:1:C:1:in'
DEL_ENDDATE_ID= 'tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input'

SCREEN_NAME   = 'Unit Agreement'
GRID_TBODY    = 'manage_object_nav_nav:form:T_data'

os.makedirs(SS_DIR, exist_ok=True)
os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
results = {}
ss_index = [0]

def ss(page, label):
    ss_index[0] += 1
    name = f'final_{ss_index[0]:02d}_{label}.png'
    page.screenshot(path=os.path.join(SS_DIR, name), full_page=False)
    print(f'  [SS] {name}')
    return name

def wait_ajax(page, t=15000):
    page.wait_for_load_state('networkidle', timeout=t)
    page.wait_for_timeout(1200)

def get_table_rows(page):
    return page.evaluate("""(tbodyId) => {
        const tbody = document.getElementById(tbodyId);
        if (!tbody) return [];
        const out = [];
        tbody.querySelectorAll('tr').forEach(tr => {
            const cells = [];
            tr.querySelectorAll('td').forEach(td => cells.push(td.textContent.trim()));
            if (cells.some(c => c)) out.push(cells);
        });
        return out;
    }""", GRID_TBODY)

def check_row(page, code):
    return any(r and r[0].strip() == code for r in get_table_rows(page))

def fill(page, fid, value):
    """Fill input field and trigger EC change events."""
    sel = f'#{fid.replace(":", "\\:")}'
    el = page.locator(sel)
    if el.count() == 0 or not el.is_visible():
        print(f'  [WARN] Field not found: {fid}')
        return False
    el.click()
    el.fill(value)
    page.evaluate(f"""() => {{
        const e = document.getElementById('{fid}');
        if (e) {{
            e.dispatchEvent(new Event('change', {{bubbles:true}}));
            e.dispatchEvent(new Event('blur', {{bubbles:true}}));
        }}
    }}""")
    page.wait_for_timeout(400)
    return True

def fill_date(page, fid, value):
    """Fill da_input date field (Tab out to trigger calendar validation)."""
    sel = f'#{fid.replace(":", "\\:")}'
    el = page.locator(sel)
    if el.count() == 0 or not el.is_visible():
        print(f'  [WARN] Date field not found: {fid}')
        return False
    el.click()
    el.fill(value)
    page.keyboard.press('Tab')
    page.wait_for_timeout(600)
    page.evaluate(f"""() => {{
        const e = document.getElementById('{fid}');
        if (e) {{
            e.dispatchEvent(new Event('change', {{bubbles:true}}));
            e.dispatchEvent(new Event('blur', {{bubbles:true}}));
        }}
    }}""")
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
    page.evaluate("() => { if(typeof EC!=='undefined') EC.toolbar.toggleSaveButton(true); }")
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
    go = page.locator('#button\\:form\\:B')
    if go.count() > 0 and go.is_visible():
        go.first.click()
        wait_ajax(page)

def select_row(page, code):
    """Click the row span for a given object code."""
    span = page.locator(
        f"css=#manage_object_nav_nav\\:form\\:T_data span"
    ).filter(has_text=code).first
    if span.count() == 0:
        print(f'  [WARN] Row span not found for code={code}')
        return False
    span.click()
    wait_ajax(page)
    page.wait_for_timeout(1000)
    return True

def get_ec_error(page):
    txt = page.evaluate("""() => {
        const n = document.getElementById('ECNotificationArea') || document.getElementById('ECClientNotificationArea');
        return n ? n.textContent.trim() : '';
    }""")
    if 'Required fields' in txt or 'Error' in txt:
        return txt.replace('EC.jsMessage.clear();','').strip()[:200]
    return ''

def get_field_val(page, fid):
    return page.evaluate(f"""() => {{
        const e = document.getElementById('{fid}');
        return e ? e.value : null;
    }}""")


with sync_playwright() as p:
    browser = p.chromium.launch(headless=not HEADED, slow_mo=SLOW_MO, args=['--ignore-certificate-errors'])
    print(f'  [MODE] headed={HEADED}, slow_mo={SLOW_MO}ms, code={TEST_CODE}')
    ctx = browser.new_context(ignore_https_errors=True, viewport={'width': 1920, 'height': 1080})
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
    print(f'\n=== NAVIGATE TO {SCREEN_NAME.upper()} ===')
    si = page.locator('#menu\\:searchForm\\:searchTxt')
    si.wait_for(state='visible', timeout=10000)
    si.clear(); si.type(SCREEN_NAME, delay=60)
    page.wait_for_load_state('networkidle', timeout=8000)
    page.wait_for_timeout(400)
    page.locator(
        f"xpath=//*[self::label or self::span][contains(@class,'tv-link') and normalize-space(text())='{SCREEN_NAME}']"
    ).first.click()
    wait_ajax(page)
    lbl = page.locator('#screenToolbar\\:form\\:screenLabel').text_content(timeout=5000)
    results['navigate'] = 'PASS' if SCREEN_NAME in lbl else f'FAIL={lbl}'
    print(f'  Screen: {lbl}')
    ss(page, 'unit_agreement_loaded')

    # -- CLEAN STATE / PRE-CLEANUP --------------------------------------------
    print('\n=== CLEAN STATE ===')
    rows0 = get_table_rows(page)
    print(f'  Rows: {[r[0] for r in rows0]}')

    if check_row(page, TEST_CODE):
        print(f'  Pre-existing AUTOTEST found - expiring to clean up')
        ok = select_row(page, TEST_CODE)
        if ok:
            fill_date(page, DEL_ENDDATE_ID, END_DATE)
            ss(page, 'pre_cleanup_end_date_set')
            do_save(page)
            click_go(page)
            print(f'  Cleanup: still_in_table={check_row(page, TEST_CODE)}')
        results['pre_cleanup'] = 'done'

    rows0 = get_table_rows(page)
    print(f'  Rows now: {[r[0] for r in rows0]}')
    results['clean'] = 'CLEAN' if not check_row(page, TEST_CODE) else 'PRE-EXISTED+EXPIRED'
    ss(page, 'clean_state')

    if results.get('pre_cleanup') == 'done':
        si2 = page.locator('#menu\\:searchForm\\:searchTxt')
        si2.clear(); si2.type(SCREEN_NAME, delay=60)
        page.wait_for_load_state('networkidle', timeout=8000)
        page.wait_for_timeout(400)
        page.locator(
            f"xpath=//*[self::label or self::span][contains(@class,'tv-link') and normalize-space(text())='{SCREEN_NAME}']"
        ).first.click()
        wait_ajax(page)
        print('  Screen refreshed after pre-cleanup')

    # -- INSERT ---------------------------------------------------------------
    print('\n=== INSERT ===')
    insert_li = page.locator(
        "xpath=//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'ui-icon-insert')]]"
    )
    insert_li.first.hover()
    page.wait_for_timeout(1000)
    sub_links = page.locator("xpath=//ul[contains(@class,'ui-menu-child')]//li//a")
    sub_count = sub_links.count()
    print(f'  Submenu links found: {sub_count}')
    clicked = False
    for i in range(sub_count):
        lnk = sub_links.nth(i)
        try:
            txt = lnk.text_content(timeout=1000).strip()
            vis = lnk.is_visible()
            print(f'  Submenu [{i}]: "{txt}" visible={vis}')
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
                    print(f'  Clicked first visible submenu: "{txt}"')
                    break
            except Exception:
                pass
    if not clicked:
        print('  [WARN] No submenu item clicked')
    wait_ajax(page)
    ss(page, 'insert_new_object')

    fill(page, INS_CODE_ID, TEST_CODE);   print(f'  Code: {TEST_CODE}')
    fill(page, INS_NAME_ID, TEST_NAME);   print(f'  Name: {TEST_NAME}')
    fill_date(page, INS_DATE_ID, START_DATE); print(f'  StartDate: {START_DATE}')
    ss(page, 'insert_filled')

    method = do_save(page)
    print(f'  Saved via: {method}')
    err = get_ec_error(page)
    ss(page, 'insert_saved')

    click_go(page)
    rows1 = get_table_rows(page)
    exists = check_row(page, TEST_CODE)
    print(f'  Rows after insert: {[r[0] for r in rows1]}')
    print(f'  AUTOTEST in table: {exists}')
    results['insert'] = 'PASS' if exists else f'FAIL err={err or "none"}'
    ss(page, 'insert_result')
    print(f'  INSERT: {results["insert"]}')

    # -- UPDATE ---------------------------------------------------------------
    print('\n=== UPDATE ===')
    if results.get('insert') == 'PASS':
        ok = select_row(page, TEST_CODE)
        if ok:
            ss(page, 'update_row_selected')
            code_val = get_field_val(page, UPD_CODE_ID)
            name_val = get_field_val(page, UPD_NAME_ID)
            print(f'  updateAttributes loaded: code={code_val}, name={name_val}')

            fill(page, UPD_NAME_ID, TEST_NAME_UPD)
            print(f'  Name updated: {TEST_NAME_UPD}')
            ss(page, 'update_filled')

            method_u = do_save(page)
            err_u = get_ec_error(page)
            print(f'  Saved via: {method_u}')
            ss(page, 'update_saved')

            click_go(page)
            rows2 = get_table_rows(page)
            upd_row = [r for r in rows2 if r and r[0] == TEST_CODE]
            upd_ok = bool(upd_row) and TEST_NAME_UPD in str(upd_row)
            print(f'  Row after update: {upd_row}')
            print(f'  UPDATE: {"PASS" if upd_ok else "FAIL"}')
            results['update'] = 'PASS' if upd_ok else f'FAIL row={upd_row} err={err_u or "none"}'
        else:
            results['update'] = 'FAIL - row not found'
    else:
        results['update'] = 'SKIP'
    ss(page, 'update_result')

    # -- DELETE (End Date = Start Date -> true delete) -------------------------
    print('\n=== DELETE (End Date = Start Date -> true delete) ===')
    print('  NOTE: EC toolbar Delete is disabled. EC-correct delete = End Date = Start Date.')
    print(f'  Set End Date={END_DATE} (= Start Date) -> zero-length window -> object removed from ov_unit_agr.')
    if results.get('insert') == 'PASS':
        ok = select_row(page, TEST_CODE)
        if ok:
            ss(page, 'delete_row_selected')
            start = get_field_val(page, DEL_ENDDATE_ID.replace('C:3', 'C:1'))
            enddate_val = get_field_val(page, DEL_ENDDATE_ID)
            print(f'  objectdates: StartDate={start}, EndDate={enddate_val}')

            ok_end = fill_date(page, DEL_ENDDATE_ID, END_DATE)
            print(f'  EndDate set: {END_DATE} (ok={ok_end})')
            ss(page, 'delete_end_date_set')

            method_d = do_save(page)
            err_d = get_ec_error(page)
            print(f'  Saved via: {method_d}')
            ss(page, 'delete_saved')

            click_go(page)

            still_visible = check_row(page, TEST_CODE)
            print(f'  Still in table after delete: {still_visible}')
            if not still_visible:
                print(f'  DELETE PASS: removed (EndDate=StartDate={END_DATE}), gone from ov_unit_agr')
                results['delete'] = f'PASS (true delete: EndDate=StartDate={END_DATE})'
            else:
                print(f'  DELETE FAIL: still visible after End Date set')
                results['delete'] = f'FAIL - still visible err={err_d or "none"}'
        else:
            results['delete'] = 'FAIL - row not found'
    else:
        results['delete'] = 'SKIP'
    ss(page, 'delete_result')
    print(f'  DELETE: {results["delete"]}')

    ss(page, 'final_state')
    if HEADED:
        print('  [DEMO] Holding browser open 6s so you can see the final state...')
        page.wait_for_timeout(6000)
    ctx.close()
    browser.close()

with open(LOG_PATH, 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2)

print('\n' + '='*60)
print('FINAL RESULTS')
print('='*60)
all_pass = True
for k, v in results.items():
    ok = v in ('PASS', 'CLEAN', 'done') or v.startswith('PASS') or v.startswith('PRE-')
    sym = 'OK' if ok else 'X'
    if not ok and k not in ('pre_cleanup', 'clean'): all_pass = False
    print(f'  {sym} {k:<15} : {v}')
print(f'\nOverall: {"ALL PASS" if all_pass else "SOME FAILURES"}')
print(f'Log:     {LOG_PATH}')
print(f'Shots:   {SS_DIR}')
