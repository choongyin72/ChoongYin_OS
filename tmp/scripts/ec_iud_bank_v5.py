"""
EC IUD Bank v5 — Fix: fill required Start Date (OBJECT_START_DATE = R:2:C:1:da_input).
Root cause from v4: save failed with "Required fields are empty: Start Date".
All 3 mandatory fields: Bank Code (R:0), Bank Name (R:1), Start Date (R:2 da_input).
NEVER TOUCH EXISTING DATA — AUTOTEST_BNK_001 only.
"""
from playwright.sync_api import sync_playwright
import json, os

EC_URL        = 'https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/'
SS_DIR        = r'c:\Projects\ChoongYin_OS\docs\EC\screenshots\iud_bank'
LOG_PATH      = r'c:\Projects\ChoongYin_OS\tmp\logs\ec_iud_bank_v5.json'
TEST_CODE     = 'AUTOTEST_BNK_001'
TEST_NAME     = 'AUTOTEST Bank 001'
TEST_NAME_UPD = 'AUTOTEST Bank 001 UPDATED'
START_DATE    = '2000-01-01'   # Effective start date for the test bank

# Known field IDs from v4 DOM inspection
BANK_CODE_ID   = 'tab:tabPanel:objectForm:form:G:0:R:0:C:1:in'
BANK_NAME_ID   = 'tab:tabPanel:objectForm:form:G:0:R:1:C:1:in'
START_DATE_ID  = 'tab:tabPanel:objectForm:form:G:0:R:2:C:1:da_input'

os.makedirs(SS_DIR, exist_ok=True)
os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
results = {}

def ss(page, name, msg=''):
    page.screenshot(path=os.path.join(SS_DIR, name), full_page=False)
    print(f'  [SS] {name}  {msg}')

def wait_ajax(page, t=15000):
    page.wait_for_load_state('networkidle', timeout=t)
    page.wait_for_timeout(1200)

def get_table_rows(page):
    return page.evaluate("""() => {
        const tbody = document.getElementById('manage_object_nav_nav:form:T_data');
        if (!tbody) return [];
        const out = [];
        tbody.querySelectorAll('tr').forEach(tr => {
            const cells = [];
            tr.querySelectorAll('td').forEach(td => cells.push(td.textContent.trim()));
            if (cells.some(c => c)) out.push(cells);
        });
        return out;
    }""")

def check_row_exists(page, code):
    return any(r and r[0].strip() == code for r in get_table_rows(page))

def get_ec_error(page):
    return page.evaluate("""() => {
        const n = document.getElementById('ECNotificationArea') || document.getElementById('ECClientNotificationArea');
        const txt = n ? n.textContent.trim() : '';
        const err = txt.match(/Required fields.*?Ok/s);
        return err ? err[0].replace(/EC\\.jsMessage\\.clear\\(\\);/g,'').trim() : '';
    }""")

def fill_field(page, fid, value, delay=50):
    """Fill a field by ID and trigger EC change events."""
    sel = f'#{fid.replace(":", "\\:")}'
    el = page.locator(sel)
    if el.count() == 0 or not el.is_visible():
        print(f'  [WARN] Field not found/visible: {fid}')
        return False
    el.click()
    el.fill(value)
    # Trigger change + blur for EC/PrimeFaces validation
    page.evaluate(f"""() => {{
        const el = document.getElementById('{fid}');
        if (el) {{
            el.dispatchEvent(new Event('change', {{bubbles:true}}));
            el.dispatchEvent(new Event('blur', {{bubbles:true}}));
        }}
    }}""")
    page.wait_for_timeout(400)
    return True

def fill_date_field(page, fid, date_value):
    """Fill a da_input calendar field — EC expects YYYY-MM-DD format."""
    sel = f'#{fid.replace(":", "\\:")}'
    el = page.locator(sel)
    if el.count() == 0 or not el.is_visible():
        print(f'  [WARN] Date field not found/visible: {fid}')
        return False
    el.click()
    el.fill(date_value)
    page.keyboard.press('Tab')   # Tab out triggers PrimeFaces calendar validation
    page.wait_for_timeout(600)
    page.evaluate(f"""() => {{
        const el = document.getElementById('{fid}');
        if (el) {{
            el.dispatchEvent(new Event('change', {{bubbles:true}}));
            el.dispatchEvent(new Event('blur', {{bubbles:true}}));
        }}
    }}""")
    page.wait_for_timeout(400)
    return True

def do_save(page):
    """Click Save toolbar and wait for AJAX."""
    save_btn = page.locator("xpath=//a[@title='Save [Ctrl+s]']")
    if save_btn.count() > 0:
        cls = save_btn.first.get_attribute('class') or ''
        print(f'  Save btn class: {cls[:60]}')
        if 'disabled' not in cls:
            save_btn.first.click()
            wait_ajax(page)
            return 'button'
    # Fallback: enable via JS then click
    page.evaluate("() => { if(typeof EC !== 'undefined') EC.toolbar.toggleSaveButton(true); }")
    page.wait_for_timeout(300)
    save_btn2 = page.locator("xpath=//a[@title='Save [Ctrl+s]' and not(contains(@class,'ui-state-disabled'))]")
    if save_btn2.count() > 0:
        save_btn2.first.click()
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
        return True
    return False

def hover_insert_and_click_new_object(page):
    insert_li = page.locator(
        "xpath=//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'ui-icon-insert')]]"
    )
    insert_li.first.hover()
    page.wait_for_timeout(800)
    new_obj = page.locator(
        "xpath=//ul[contains(@class,'ui-menu-child')]//li//a[normalize-space(text())='New Object']"
    )
    if new_obj.count() > 0 and new_obj.first.is_visible():
        new_obj.first.click()
        wait_ajax(page)
        return True
    # Fallback: click first visible submenu item
    items = page.locator("xpath=//ul[contains(@class,'ui-menu-child')]//li//a")
    for i in range(items.count()):
        it = items.nth(i)
        try:
            if it.is_visible():
                it.click()
                wait_ajax(page)
                return True
        except Exception:
            pass
    return False


with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=['--ignore-certificate-errors'])
    ctx = browser.new_context(ignore_https_errors=True, viewport={'width': 1920, 'height': 1080})
    page = ctx.new_page()

    # ── LOGIN ────────────────────────────────────────────────────────────────
    print('=== LOGIN ===')
    page.goto(EC_URL, wait_until='domcontentloaded', timeout=30000)
    page.fill('#username', 'sysadmin')
    page.fill('#password', 'sysadmin')
    page.click('#kc-login')
    page.wait_for_url('**/dashboard**', timeout=60000)
    wait_ajax(page)
    results['login'] = 'PASS'
    print('  OK')

    # ── NAVIGATE TO BANK ────────────────────────────────────────────────────
    print('\n=== NAVIGATE TO BANK ===')
    si = page.locator('#menu\\:searchForm\\:searchTxt')
    si.wait_for(state='visible', timeout=10000)
    si.clear(); si.type('Bank', delay=60)
    page.wait_for_load_state('networkidle', timeout=8000)
    page.wait_for_timeout(400)
    page.locator(
        "xpath=//*[self::label or self::span][contains(@class,'tv-link') and normalize-space(text())='Bank']"
    ).first.click()
    wait_ajax(page)
    lbl = page.locator('#screenToolbar\\:form\\:screenLabel').text_content(timeout=5000)
    results['navigate'] = 'PASS' if 'Bank' in lbl else f'FAIL={lbl}'
    print(f'  Screen: {lbl}')
    ss(page, 'v5_01_bank_loaded.png', 'Bank loaded')

    # ── CLEAN STATE (cleanup pre-existing AUTOTEST from partial runs) ────────
    print('\n=== CLEAN STATE ===')
    rows0 = get_table_rows(page)
    print(f'  Existing banks ({len(rows0)}): {[r[0] for r in rows0]}')
    if check_row_exists(page, TEST_CODE):
        print(f'  Pre-existing AUTOTEST record found — cleaning up first...')
        row_pre = page.locator(
            f"xpath=//tbody[@id='manage_object_nav_nav:form:T_data']"
            f"//tr[.//span[normalize-space(text())='{TEST_CODE}']]"
        )
        if row_pre.count() > 0:
            row_pre.first.click()
            wait_ajax(page)
            del_btn_pre = page.locator(
                "xpath=//a[@title='Delete [Ctrl+d]' and not(contains(@class,'ui-state-disabled'))]"
            )
            if del_btn_pre.count() == 0:
                del_btn_pre = page.locator("xpath=//li[.//span[contains(@class,'ui-icon-delete')]]//a")
            if del_btn_pre.count() > 0:
                del_btn_pre.first.click()
                wait_ajax(page)
            confirm = page.locator("button:has-text('Yes'), #confirmationForm\\:yes")
            if confirm.count() > 0 and confirm.first.is_visible():
                confirm.first.click()
                wait_ajax(page)
            do_save(page)
            click_go(page)
            still_pre = check_row_exists(page, TEST_CODE)
            print(f'  Cleanup: still_exists={still_pre}')
        results['pre_cleanup'] = 'done'
    rows0 = get_table_rows(page)
    print(f'  Banks after cleanup ({len(rows0)}): {[r[0] for r in rows0]}')
    assert not check_row_exists(page, TEST_CODE), 'AUTOTEST still exists after cleanup — abort'
    results['clean'] = 'CLEAN'
    ss(page, 'v5_02_clean.png')

    # ── INSERT ───────────────────────────────────────────────────────────────
    print('\n=== INSERT ===')
    ok = hover_insert_and_click_new_object(page)
    print(f'  New Object clicked: {ok}')
    ss(page, 'v5_03_new_object.png', 'After New Object')

    # Fill all 3 mandatory fields
    fill_field(page, BANK_CODE_ID, TEST_CODE)
    print(f'  Bank Code filled: {TEST_CODE}')

    fill_field(page, BANK_NAME_ID, TEST_NAME)
    print(f'  Bank Name filled: {TEST_NAME}')

    fill_date_field(page, START_DATE_ID, START_DATE)
    print(f'  Start Date filled: {START_DATE}')

    ss(page, 'v5_04_insert_filled.png', 'All 3 fields filled')

    method = do_save(page)
    print(f'  Save method: {method}')
    ss(page, 'v5_05_after_save.png', 'After save')

    err = get_ec_error(page)
    print(f'  EC error: {err or "none"}')

    click_go(page)
    ss(page, 'v5_06_after_go.png', 'After Go refresh')

    rows1 = get_table_rows(page)
    print(f'  Rows after insert ({len(rows1)}): {[r[0] for r in rows1]}')
    exists = check_row_exists(page, TEST_CODE)
    print(f'  AUTOTEST in table: {exists}')
    results['insert'] = 'PASS' if exists else f'FAIL err={err or "none"}'
    ss(page, 'v5_07_insert_result.png', f'Insert {results["insert"]}')

    # ── UPDATE ───────────────────────────────────────────────────────────────
    print('\n=== UPDATE ===')
    if results.get('insert') == 'PASS':
        # Use span text match (cells use <span>_la inside <td>, not direct text nodes)
        row_loc = page.locator(
            f"xpath=//tbody[@id='manage_object_nav_nav:form:T_data']"
            f"//tr[.//span[normalize-space(text())='{TEST_CODE}']]"
        )
        print(f'  Row locator count: {row_loc.count()}')
        if row_loc.count() > 0:
            row_loc.first.click()
            wait_ajax(page)
            ss(page, 'v5_08_row_selected.png', 'Row for update')

            fill_field(page, BANK_NAME_ID, TEST_NAME_UPD)
            print(f'  Bank Name updated: {TEST_NAME_UPD}')
            ss(page, 'v5_09_update_filled.png', 'Update filled')

            do_save(page)
            ss(page, 'v5_10_after_update_save.png', 'After update save')
            click_go(page)

            upd_err = get_ec_error(page)
            rows2 = get_table_rows(page)
            upd_row = [r for r in rows2 if r and r[0] == TEST_CODE]
            upd_ok = bool(upd_row) and TEST_NAME_UPD in str(upd_row)
            print(f'  UPDATE {"PASS" if upd_ok else "FAIL"} — row={upd_row}, err={upd_err or "none"}')
            results['update'] = 'PASS' if upd_ok else f'FAIL row={upd_row}'
        else:
            results['update'] = 'FAIL — row not found'
    else:
        results['update'] = 'SKIP'
    print(f'  UPDATE: {results["update"]}')

    # ── DELETE ───────────────────────────────────────────────────────────────
    print('\n=== DELETE ===')
    if results.get('insert') == 'PASS':
        row_d = page.locator(
            f"xpath=//tbody[@id='manage_object_nav_nav:form:T_data']"
            f"//tr[.//span[normalize-space(text())='{TEST_CODE}']]"
        )
        if row_d.count() > 0:
            row_d.first.click()
            wait_ajax(page)
            ss(page, 'v5_11_row_for_delete.png', 'Row for delete')

            del_state = page.evaluate("""() => {
                const d = document.querySelector("a[title='Delete [Ctrl+d]']");
                return d ? {found:true, disabled:d.classList.contains('ui-state-disabled')} : {found:false};
            }""")
            print(f'  Delete button: {del_state}')

            # Click Delete
            del_btn = page.locator("xpath=//a[@title='Delete [Ctrl+d]' and not(contains(@class,'ui-state-disabled'))]")
            if del_btn.count() > 0:
                del_btn.first.click()
            else:
                del_any = page.locator("xpath=//li[.//span[contains(@class,'ui-icon-delete')]]//a")
                if del_any.count() > 0:
                    del_any.first.click()
                else:
                    page.keyboard.press('Control+d')
            wait_ajax(page)
            ss(page, 'v5_12_after_delete_click.png', 'After delete click')

            # Confirm dialog
            confirm = page.locator(
                "xpath=//button[normalize-space(text())='Yes'] | "
                "xpath=//a[normalize-space(text())='Yes'] | "
                "xpath=//button[@id='confirmationForm:yes']"
            )
            if confirm.count() > 0 and confirm.first.is_visible():
                confirm.first.click()
                wait_ajax(page)
                ss(page, 'v5_13_confirmed.png', 'Confirmed')

            do_save(page)
            ss(page, 'v5_14_after_delete_save.png', 'After delete save')
            click_go(page)

            still = check_row_exists(page, TEST_CODE)
            del_err = get_ec_error(page)
            print(f'  DELETE {"PASS" if not still else "FAIL"} — still={still}, err={del_err or "none"}')
            results['delete'] = 'PASS' if not still else f'FAIL still_exists={still}'
        else:
            results['delete'] = 'FAIL — row not found'
    else:
        results['delete'] = 'SKIP'
    print(f'  DELETE: {results["delete"]}')

    ss(page, 'v5_15_final.png', 'Final state')
    ctx.close()
    browser.close()

with open(LOG_PATH, 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2)

print('\n' + '='*60)
print('RESULTS')
print('='*60)
for k, v in results.items():
    emoji = '✓' if v in ('PASS','CLEAN') else '✗'
    print(f'  {emoji} {k:<15} : {v}')
print(f'\nLog:   {LOG_PATH}')
print(f'Shots: {SS_DIR}')
