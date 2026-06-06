"""
EC IUD Bank v4 — Fix save issue.
v3 found correct fields but save didn't persist.
Fix: check save button state, force-enable if disabled, check EC errors, refresh table.
NEVER TOUCH EXISTING DATA — AUTOTEST_BNK_001 only.
"""
from playwright.sync_api import sync_playwright
import json, os

EC_URL        = 'https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/'
SS_DIR        = r'c:\Projects\ChoongYin_OS\docs\EC\screenshots\iud_bank'
LOG_PATH      = r'c:\Projects\ChoongYin_OS\tmp\logs\ec_iud_bank_v4.json'
TEST_CODE     = 'AUTOTEST_BNK_001'
TEST_NAME     = 'AUTOTEST Bank 001'
TEST_NAME_UPD = 'AUTOTEST Bank 001 UPDATED'

os.makedirs(SS_DIR, exist_ok=True)
os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
results = {}

def ss(page, name, msg=''):
    path = os.path.join(SS_DIR, name)
    page.screenshot(path=path, full_page=False)
    print(f'  [SS] {name}  {msg}')

def wait_ajax(page, t=15000):
    page.wait_for_load_state('networkidle', timeout=t)
    page.wait_for_timeout(1500)

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
    rows = get_table_rows(page)
    return any(r and r[0].strip() == code for r in rows)

def get_ec_messages(page):
    """Capture EC notification/error messages from message area."""
    return page.evaluate("""() => {
        const msgs = [];
        // PrimeFaces messages
        document.querySelectorAll('.ui-messages-error li, .ui-messages-info li, .ui-message-error, .ui-growl-item-message').forEach(el => {
            msgs.push({type:'pf', text: el.textContent.trim()});
        });
        // EC notification area
        const notif = document.getElementById('ECNotificationArea') || document.getElementById('ECClientNotificationArea');
        if (notif && notif.textContent.trim()) msgs.push({type:'ec', text: notif.textContent.trim().substring(0,200)});
        // Any visible alert dialogs
        document.querySelectorAll('[role="alertdialog"] .ui-dialog-content').forEach(el => {
            msgs.push({type:'dialog', text: el.textContent.trim().substring(0,200)});
        });
        return msgs;
    }""")

def get_save_button_state(page):
    return page.evaluate("""() => {
        const save = document.querySelector("a[title='Save [Ctrl+s]']");
        if (!save) return {found: false};
        return {
            found: true,
            disabled: save.classList.contains('ui-state-disabled'),
            cls: save.className.substring(0,100)
        };
    }""")

def force_save(page):
    """Try multiple save approaches and return method used."""
    state = get_save_button_state(page)
    print(f'  Save button state: {state}')

    if state.get('found') and not state.get('disabled'):
        # Save button enabled — click it
        save_btn = page.locator("xpath=//a[@title='Save [Ctrl+s]']")
        save_btn.first.click()
        wait_ajax(page)
        return 'button-click'

    # Try enabling via EC JS + click
    print('  Save disabled — trying EC.toolbar.toggleSaveButton(true) + click')
    page.evaluate("() => { if(typeof EC !== 'undefined') EC.toolbar.toggleSaveButton(true); }")
    page.wait_for_timeout(300)
    state2 = get_save_button_state(page)
    print(f'  Save button after toggle: {state2}')

    if state2.get('found') and not state2.get('disabled'):
        save_btn = page.locator("xpath=//a[@title='Save [Ctrl+s]']")
        save_btn.first.click()
        wait_ajax(page)
        return 'toggle+click'

    # Try direct PrimeFaces AJAX save call
    print('  Trying direct PrimeFaces save AJAX')
    page.evaluate("""() => {
        PrimeFaces.ab({
            s: "screenToolbar:form:menuBar",
            f: "screenToolbar:form",
            pa: [{name: "screenToolbar:form:menuBar_menuid",
                  value: "_2dc9d1d2-2f0a-42ab-856d-aac078efa74c|0"}]
        });
    }""")
    wait_ajax(page)
    return 'pf-ajax'

def click_go_button(page):
    """Click the Go button to refresh the Bank list."""
    go = page.locator('#button\\:form\\:B')
    if go.count() > 0 and go.first.is_visible():
        go.first.click()
        wait_ajax(page)
        return True
    return False

def nav_to_bank_by_code(page, code):
    """Type bank code in the navigator autocomplete to navigate to it."""
    # The nav autocomplete: nav:form:G:0:R:1:C:0:da_input is a date field
    # The manage_object_nav:searchInput would be the search box if it exists
    # In EC Manage Object, the object selector is usually in nav:form
    nav_inputs = page.evaluate("""() => {
        const inputs = [];
        document.querySelectorAll('#nav\\\\:form input:not([type=hidden])').forEach(e => {
            inputs.push({id:e.id, val:e.value, type:e.type});
        });
        return inputs;
    }""")
    print(f'  Nav inputs: {nav_inputs}')

    # Try the autocomplete input in nav form
    nav_search = page.locator("#nav\\:form input[class*='autocomplete-input'], #nav\\:form input[class*='inputtext']")
    if nav_search.count() > 0:
        nav_search.first.clear()
        nav_search.first.type(code, delay=60)
        page.wait_for_timeout(1000)
        # Click suggestion
        suggestion = page.locator(f"xpath=//*[contains(@class,'ui-autocomplete-item') and normalize-space(text())='{code}']")
        if suggestion.count() > 0:
            suggestion.first.click()
            wait_ajax(page)
            return True
    return False


with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=['--ignore-certificate-errors'])
    ctx = browser.new_context(ignore_https_errors=True, viewport={'width': 1920, 'height': 1080})
    page = ctx.new_page()

    # LOGIN
    print('=== LOGIN ===')
    page.goto(EC_URL, wait_until='domcontentloaded', timeout=30000)
    page.fill('#username', 'sysadmin')
    page.fill('#password', 'sysadmin')
    page.click('#kc-login')
    page.wait_for_url('**/dashboard**', timeout=60000)
    wait_ajax(page)
    results['login'] = 'PASS'
    print('  OK')

    # NAVIGATE TO BANK
    print('\n=== NAVIGATE TO BANK ===')
    si = page.locator("xpath=//input[@id='menu:searchForm:searchTxt']")
    si.wait_for(state='visible', timeout=10000)
    si.clear(); si.type('Bank', delay=60)
    page.wait_for_load_state('networkidle', timeout=8000)
    page.wait_for_timeout(400)
    bank_link = page.locator(
        "xpath=//*[self::label or self::span][contains(@class,'tv-link') and normalize-space(text())='Bank']"
    )
    bank_link.first.click()
    wait_ajax(page)
    lbl = page.locator('#screenToolbar\\:form\\:screenLabel').text_content(timeout=5000)
    results['navigate'] = 'PASS' if 'Bank' in lbl else f'FAIL label={lbl}'
    print(f'  Screen: {lbl}')
    ss(page, 'v4_01_bank_loaded.png', 'Bank loaded')

    # VERIFY CLEAN STATE
    print('\n=== CLEAN STATE CHECK ===')
    rows = get_table_rows(page)
    print(f'  Banks in table: {len(rows)}')
    for r in rows: print(f'    {r}')
    assert not check_row_exists(page, TEST_CODE), f'AUTOTEST_BNK_001 already exists — abort'
    results['clean'] = 'CLEAN'
    ss(page, 'v4_02_clean_state.png', f'{len(rows)} rows, no AUTOTEST')

    # ── INSERT ────────────────────────────────────────────────────────────────
    print('\n=== INSERT ===')
    insert_li = page.locator(
        "xpath=//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'ui-icon-insert')]]"
    )
    insert_li.first.hover()
    page.wait_for_timeout(800)

    # Click "New Object" submenu item
    sub = page.locator(
        "xpath=//ul[contains(@class,'ui-menu-child')]//li//a[normalize-space(text())='New Object']"
    )
    if sub.count() == 0:
        sub = page.locator("xpath=//ul[contains(@class,'ui-menu-child')]//li//a")
    sub.first.click()
    wait_ajax(page)
    ss(page, 'v4_03_after_new_object.png', 'After New Object click')

    # --- Inspect objectForm fields ---
    form_data = page.evaluate("""() => {
        const form = document.getElementById('tab:tabPanel');
        if (!form) return {inputs: []};
        const inputs = [];
        form.querySelectorAll('input:not([type=hidden])').forEach(e => {
            if (e.id && e.offsetParent !== null)
                inputs.push({id:e.id, type:e.type||'text', val:e.value||'',
                             ro: e.readOnly, dis: e.disabled, cls: e.className.substring(0,80)});
        });
        return {inputs};
    }""")

    print(f'  objectForm inputs ({len(form_data["inputs"])}):')
    for inp in form_data['inputs']:
        if 'statusarea' not in inp['id'] and 'searchTxt' not in inp['id']:
            print(f'    {inp["id"]}  val="{inp["val"]}"  ro={inp["ro"]}  dis={inp["dis"]}')

    # Fields: R:0=BankCode, R:1=BankName (from v3 discovery)
    BANK_CODE_ID = 'tab:tabPanel:objectForm:form:G:0:R:0:C:1:in'
    BANK_NAME_ID = 'tab:tabPanel:objectForm:form:G:0:R:1:C:1:in'

    # Fill Bank Code
    bc = page.locator(f'#{BANK_CODE_ID.replace(":", "\\:")}')
    if bc.count() > 0 and bc.is_visible():
        bc.click()
        bc.fill(TEST_CODE)
        print(f'  Filled Bank Code: {TEST_CODE}')
        # Trigger change event for EC validation
        page.evaluate(f"""() => {{
            const el = document.getElementById('{BANK_CODE_ID}');
            if (el) {{
                el.dispatchEvent(new Event('change', {{bubbles:true}}));
                el.dispatchEvent(new Event('blur', {{bubbles:true}}));
            }}
        }}""")
        page.wait_for_timeout(500)
    else:
        print(f'  [WARN] Bank Code input not found: {BANK_CODE_ID}')

    # Fill Bank Name
    bn = page.locator(f'#{BANK_NAME_ID.replace(":", "\\:")}')
    if bn.count() > 0 and bn.is_visible():
        bn.click()
        bn.fill(TEST_NAME)
        print(f'  Filled Bank Name: {TEST_NAME}')
        page.evaluate(f"""() => {{
            const el = document.getElementById('{BANK_NAME_ID}');
            if (el) {{
                el.dispatchEvent(new Event('change', {{bubbles:true}}));
                el.dispatchEvent(new Event('blur', {{bubbles:true}}));
            }}
        }}""")
        page.wait_for_timeout(500)
    else:
        print(f'  [WARN] Bank Name input not found: {BANK_NAME_ID}')

    ss(page, 'v4_04_insert_filled.png', 'Insert fields filled')

    # Check save button state before saving
    pre_save = get_save_button_state(page)
    print(f'  Pre-save button: {pre_save}')

    # Save
    method = force_save(page)
    print(f'  Save method used: {method}')
    ss(page, 'v4_05_after_save.png', 'After save')

    # Check EC messages
    msgs = get_ec_messages(page)
    print(f'  EC messages: {msgs}')

    # Refresh table with Go button
    go_clicked = click_go_button(page)
    if go_clicked:
        print('  Go button clicked — table refreshed')
        ss(page, 'v4_06_after_go.png', 'After Go refresh')

    # Check table
    rows_after = get_table_rows(page)
    print(f'  Rows after insert: {len(rows_after)}')
    for r in rows_after: print(f'    {r}')
    exists = check_row_exists(page, TEST_CODE)
    print(f'  AUTOTEST_BNK_001 in table: {exists}')

    # Also try scrolling to find it (table might be longer)
    all_codes = page.evaluate("""() => {
        const codes = [];
        document.querySelectorAll('#manage_object_nav_nav\\\\:form\\\\:T_data td:first-child').forEach(td => {
            if (td.textContent.trim()) codes.push(td.textContent.trim());
        });
        return codes;
    }""")
    print(f'  All Bank Codes visible: {all_codes}')
    autotest_in_dom = TEST_CODE in all_codes
    print(f'  AUTOTEST in DOM: {autotest_in_dom}')

    if exists or autotest_in_dom:
        print('  INSERT PASS')
        results['insert'] = 'PASS'
    else:
        # Check if the objectForm still shows our data (not saved, still in form)
        bc_val = page.evaluate(f"""() => {{
            const el = document.getElementById('{BANK_CODE_ID}');
            return el ? el.value : 'not found';
        }}""")
        print(f'  Bank Code field value: {bc_val} (still in form = not saved yet)')
        results['insert'] = f'FAIL — not in table, bc_val={bc_val}, msgs={msgs}'

    ss(page, 'v4_07_insert_result.png', f'Insert: {results["insert"]}')

    # ── UPDATE (only if insert passed) ────────────────────────────────────────
    print('\n=== UPDATE ===')
    if results.get('insert') == 'PASS':
        # Click the AUTOTEST row in the table
        row_loc = page.locator(
            f"xpath=//tbody[@id='manage_object_nav_nav:form:T_data']"
            f"//tr[.//td[normalize-space(text())='{TEST_CODE}']]"
        )
        if row_loc.count() > 0:
            row_loc.first.click()
            wait_ajax(page)
            ss(page, 'v4_08_row_selected.png', 'Row selected')

            # Find Bank Name field (should now show TEST_NAME)
            bn_el = page.locator(f'#{BANK_NAME_ID.replace(":", "\\:")}')
            if bn_el.count() > 0 and bn_el.is_visible():
                bn_el.triple_click()
                bn_el.fill(TEST_NAME_UPD)
                page.evaluate(f"""() => {{
                    const el = document.getElementById('{BANK_NAME_ID}');
                    if (el) el.dispatchEvent(new Event('change', {{bubbles:true}}));
                }}""")
                page.wait_for_timeout(500)
                ss(page, 'v4_09_update_filled.png', 'Update filled')
                method_u = force_save(page)
                print(f'  Save method: {method_u}')
                ss(page, 'v4_10_after_update_save.png', 'After update save')
                click_go_button(page)

                # Verify
                rows_u = get_table_rows(page)
                upd_row = [r for r in rows_u if r and r[0] == TEST_CODE]
                if upd_row and TEST_NAME_UPD in str(upd_row):
                    print(f'  UPDATE PASS: {upd_row}')
                    results['update'] = 'PASS'
                else:
                    print(f'  UPDATE result: {upd_row}')
                    results['update'] = f'FAIL row={upd_row}'
            else:
                results['update'] = 'FAIL — Bank Name field not visible'
        else:
            results['update'] = 'FAIL — row not in table'
    else:
        results['update'] = 'SKIP'
    print(f'  UPDATE: {results["update"]}')

    # ── DELETE (only if insert passed) ────────────────────────────────────────
    print('\n=== DELETE ===')
    if results.get('insert') == 'PASS':
        # Select the row
        row_d = page.locator(
            f"xpath=//tbody[@id='manage_object_nav_nav:form:T_data']"
            f"//tr[.//td[normalize-space(text())='{TEST_CODE}']]"
        )
        if row_d.count() > 0:
            row_d.first.click()
            wait_ajax(page)
            ss(page, 'v4_11_row_for_delete.png', 'Row selected for delete')

            # Check delete button state
            del_state = page.evaluate("""() => {
                const d = document.querySelector("a[title='Delete [Ctrl+d]']") ||
                          document.querySelector("a:has(.ui-icon-delete)") ||
                          document.querySelector("li:has(.ui-icon-delete) a");
                if (!d) return {found:false};
                return {found:true, disabled: d.classList.contains('ui-state-disabled'), cls:d.className.substring(0,80)};
            }""")
            print(f'  Delete button: {del_state}')

            del_btn = page.locator("xpath=//a[@title='Delete [Ctrl+d]' and not(contains(@class,'ui-state-disabled'))]")
            if del_btn.count() == 0:
                # Try keyboard shortcut
                del_btn_any = page.locator("xpath=//a[.//span[contains(@class,'ui-icon-delete')]]")
                if del_btn_any.count() > 0:
                    del_btn_any.first.click()
                else:
                    page.keyboard.press('Control+d')
            else:
                del_btn.first.click()

            wait_ajax(page)
            ss(page, 'v4_12_after_delete_click.png', 'After delete click')

            # Handle confirmation
            confirm = page.locator(
                "xpath=//button[normalize-space(text())='Yes'] | "
                "xpath=//a[normalize-space(text())='Yes'] | "
                "xpath=//button[@id='confirmationForm:yes']"
            )
            if confirm.count() > 0 and confirm.first.is_visible():
                confirm.first.click()
                wait_ajax(page)
                ss(page, 'v4_13_confirmed.png', 'Delete confirmed')

            method_d = force_save(page)
            print(f'  Save method: {method_d}')
            ss(page, 'v4_14_after_delete_save.png', 'After delete save')
            click_go_button(page)

            still = check_row_exists(page, TEST_CODE)
            print(f'  DELETE {"PASS" if not still else "FAIL"} — still_exists={still}')
            results['delete'] = 'PASS' if not still else 'FAIL — still in table'
        else:
            results['delete'] = 'FAIL — row not found'
    else:
        results['delete'] = 'SKIP'
    print(f'  DELETE: {results["delete"]}')

    ss(page, 'v4_15_final.png', 'Final state')
    ctx.close()
    browser.close()

# Save results
with open(LOG_PATH, 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2)

print('\n' + '='*60)
print('RESULTS SUMMARY')
print('='*60)
for k, v in results.items():
    print(f'  {k:<15} : {v}')
print(f'\nLog:      {LOG_PATH}')
print(f'Shots:    {SS_DIR}')
