"""
EC IUD Bank v3 — Manage Object Insert/Update/Delete.
Bank screen type: manage_object_nav (TABLE screenlet) + nav (date FormScreenlet).
Insert pattern: hover Insert toolbar → submenu "Bank" → objectForm appears → fill + save.
NEVER TOUCH EXISTING DATA — all ops on AUTOTEST_BNK_001 only.
"""
from playwright.sync_api import sync_playwright
import json, os, time

EC_URL       = 'https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/'
SS_DIR       = r'c:\Projects\ChoongYin_OS\docs\EC\screenshots\iud_bank'
LOG_PATH     = r'c:\Projects\ChoongYin_OS\tmp\logs\ec_iud_bank_v3.json'
TEST_CODE    = 'AUTOTEST_BNK_001'
TEST_NAME    = 'AUTOTEST Bank 001'
TEST_NAME_UPD = 'AUTOTEST Bank 001 UPDATED'

os.makedirs(SS_DIR, exist_ok=True)
os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)

results = {}

def ss(page, name, msg=''):
    path = os.path.join(SS_DIR, name)
    page.screenshot(path=path, full_page=False)
    print(f'  [SS] {name}  {msg}')
    return path

def wait_ajax(page, timeout=15000):
    page.wait_for_load_state('networkidle', timeout=timeout)
    page.wait_for_timeout(1200)

def get_table_rows(page):
    """Read all visible rows from manage_object_nav_nav:form:T."""
    rows = page.evaluate("""() => {
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
    return rows

def find_input_in_form(page, form_id):
    """Return all non-hidden inputs inside a form/div."""
    return page.evaluate(f"""() => {{
        const el = document.getElementById('{form_id}') ||
                   document.querySelector('[id^="{form_id}"]');
        if (!el) return {{found: false, inputs: []}};
        const inputs = [];
        el.querySelectorAll('input:not([type=hidden]),textarea').forEach(e => {{
            if (e.id && e.offsetParent) inputs.push({{
                id: e.id, type: e.type||'text', val: e.value, ph: e.placeholder||'',
                cls: e.className.substring(0,60)
            }});
        }});
        return {{found: true, inputs: inputs}};
    }}""")

def click_insert_submenu(page):
    """Hover Insert toolbar button → find submenu item → click it."""
    # Find Insert parent LI
    insert_li = page.locator("xpath=//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'ui-icon-insert')]]")
    if insert_li.count() == 0:
        print('  [WARN] Insert LI not found')
        return False
    print(f'  Insert LI found, class: {insert_li.first.get_attribute("class")}')

    # Hover to show submenu
    insert_li.first.hover()
    page.wait_for_timeout(800)

    # Look for visible submenu items
    sub_items = page.locator("xpath=//ul[contains(@class,'ui-menu-child')]//li[contains(@class,'ui-menuitem')]//a")
    vis_count = 0
    for i in range(sub_items.count()):
        item = sub_items.nth(i)
        try:
            if item.is_visible():
                vis_count += 1
                txt = item.text_content().strip()
                print(f'  Submenu item {i}: "{txt}"')
        except Exception:
            pass

    print(f'  Visible submenu items: {vis_count}')

    if vis_count > 0:
        # Click the first visible submenu item
        for i in range(sub_items.count()):
            item = sub_items.nth(i)
            try:
                if item.is_visible():
                    item.click()
                    print('  Clicked submenu item')
                    return True
            except Exception:
                pass

    # Fallback: direct PrimeFaces.ab() call using onclick from toolbar
    print('  [FALLBACK] Using direct PrimeFaces.ab() insert call')
    try:
        page.evaluate("""() => {
            if (typeof EC !== 'undefined' && typeof PrimeFaces !== 'undefined') {
                EC.toolbar.toggleSaveButton(true);
                PrimeFaces.ab({
                    s: "screenToolbar:form:menuBar",
                    f: "screenToolbar:form",
                    pa: [
                        {name: "screenletId", value: "objectForm"},
                        {name: "eventType",   value: "insert"},
                        {name: "sortOrder",   value: "1"}
                    ]
                });
                return true;
            }
            return false;
        }""")
        return True
    except Exception as e:
        print(f'  [ERR] Fallback failed: {e}')
        return False

def find_object_form_fields(page):
    """After insert, find the fields in the newly opened object form."""
    # Look for objectForm or any new form screenlet
    obj_form = page.evaluate("""() => {
        // Common names for the object form after insert
        const candidates = ['objectForm:form', 'objectForm', 'ec-screen-content'];
        for (const id of candidates) {
            const el = document.getElementById(id);
            if (el) {
                const inputs = [];
                el.querySelectorAll('input:not([type=hidden]),textarea').forEach(e => {
                    if (e.id && e.offsetParent !== null)
                        inputs.push({id:e.id, type:e.type||'text', val:e.value||'',
                                     ph:e.placeholder||'', cls:e.className.substring(0,80)});
                });
                return {source: id, inputs: inputs, found: true};
            }
        }
        // Last resort: all visible inputs on page
        const all = [];
        document.querySelectorAll('input:not([type=hidden]),textarea').forEach(e => {
            if (e.id && e.offsetParent !== null)
                all.push({id:e.id, type:e.type||'text', val:e.value||'',
                           ph:e.placeholder||'', cls:e.className.substring(0,80)});
        });
        return {source: 'page-all', inputs: all, found: true};
    }""")
    return obj_form

def save_page(page):
    """Click the Save toolbar button."""
    save_btn = page.locator("xpath=//a[@title='Save [Ctrl+s]' and not(contains(@class,'ui-state-disabled'))]")
    if save_btn.count() > 0 and save_btn.first.is_visible():
        save_btn.first.click()
        wait_ajax(page)
        return True
    # Try Ctrl+S
    page.keyboard.press('Control+s')
    wait_ajax(page)
    return True

def check_row_exists(page, code):
    """Return True if any row contains code in first cell."""
    rows = get_table_rows(page)
    for row in rows:
        if row and row[0].strip() == code:
            return True
    return False


with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=['--ignore-certificate-errors'])
    ctx = browser.new_context(ignore_https_errors=True, viewport={'width': 1920, 'height': 1080})
    page = ctx.new_page()

    # ─── LOGIN ───────────────────────────────────────────────────────────────
    print('=== LOGIN ===')
    page.goto(EC_URL, wait_until='domcontentloaded', timeout=30000)
    page.fill('#username', 'sysadmin')
    page.fill('#password', 'sysadmin')
    page.click('#kc-login')
    page.wait_for_url('**/dashboard**', timeout=60000)
    wait_ajax(page)
    ss(page, 'v3_01_login_ok.png', 'Login OK')
    results['login'] = 'PASS'
    print('  Login OK')

    # ─── NAVIGATE TO BANK ───────────────────────────────────────────────────
    print('\n=== NAVIGATE TO BANK ===')
    si = page.locator("xpath=//input[@id='menu:searchForm:searchTxt']")
    si.wait_for(state='visible', timeout=10000)
    si.clear()
    si.type('Bank', delay=60)
    page.wait_for_load_state('networkidle', timeout=8000)
    page.wait_for_timeout(400)

    bank_link = page.locator(
        "xpath=//*[self::label or self::span][contains(@class,'tv-link') and normalize-space(text())='Bank']"
    )
    bank_link.first.click()
    wait_ajax(page)
    ss(page, 'v3_02_bank_screen.png', 'Bank screen loaded')

    # Confirm screen label
    lbl = page.locator('#screenToolbar\\:form\\:screenLabel').text_content(timeout=5000)
    print(f'  Screen label: {lbl}')
    results['navigate'] = 'PASS' if 'Bank' in lbl else f'FAIL — label={lbl}'

    # ─── VERIFY CLEAN STATE ─────────────────────────────────────────────────
    print('\n=== VERIFY CLEAN STATE ===')
    rows = get_table_rows(page)
    print(f'  Existing rows ({len(rows)}):')
    for r in rows:
        print(f'    {r}')
    autotest_exists = check_row_exists(page, TEST_CODE)
    print(f'  AUTOTEST_BNK_001 exists: {autotest_exists}')
    ss(page, 'v3_03_clean_state.png', f'Rows={len(rows)}, autotest={autotest_exists}')
    results['clean_state'] = 'CLEAN' if not autotest_exists else 'WARNING: pre-exists'

    # ─── INSERT ─────────────────────────────────────────────────────────────
    print('\n=== INSERT ===')
    inserted = click_insert_submenu(page)
    wait_ajax(page)
    page.wait_for_timeout(1500)
    ss(page, 'v3_04_after_insert_click.png', 'After Insert click/trigger')

    # Inspect what fields appeared
    form_fields = find_object_form_fields(page)
    print(f'  Form source: {form_fields.get("source")}')
    visible_inputs = [i for i in form_fields.get('inputs', [])
                      if 'searchTxt' not in i['id'] and 'da_input' not in i['id']]
    print(f'  Visible inputs ({len(visible_inputs)}):')
    for inp in visible_inputs:
        print(f'    id={inp["id"]}  val="{inp["val"]}"  ph="{inp["ph"]}"')

    # Find Bank Code field (mandatory, first editable input that's not date/search)
    bank_code_input = None
    bank_name_input = None
    for inp in visible_inputs:
        iid = inp['id']
        # Skip status area, nav, sidebar, date fields
        if any(x in iid for x in ['statusarea', 'nav:form', 'menu:', 'searchForm', 'hideMenu']):
            continue
        val = inp['val']
        ph  = inp['ph']
        cls = inp['cls']
        if 'da_input' in iid:
            if bank_code_input is None:
                bank_code_input = iid
            elif bank_name_input is None:
                bank_name_input = iid
        elif bank_code_input is None and ('inputtext' in cls.lower() or 'ui-inputfield' in cls.lower()):
            bank_code_input = iid
        elif bank_name_input is None and ('inputtext' in cls.lower() or 'ui-inputfield' in cls.lower()):
            bank_name_input = iid

    # More targeted: objectForm fields
    obj_inputs = [i for i in visible_inputs if 'objectForm' in i['id'] or 'tab:tabPanel' in i['id']]
    if obj_inputs:
        print(f'\n  objectForm/tab inputs ({len(obj_inputs)}):')
        for inp in obj_inputs:
            print(f'    {inp["id"]}  val="{inp["val"]}"  ph="{inp["ph"]}"')
        bank_code_input = obj_inputs[0]['id'] if obj_inputs else bank_code_input
        bank_name_input = obj_inputs[1]['id'] if len(obj_inputs) > 1 else bank_name_input

    print(f'\n  Bank Code field: {bank_code_input}')
    print(f'  Bank Name field: {bank_name_input}')

    # Fill the fields
    fill_success = False
    if bank_code_input:
        try:
            inp_el = page.locator(f'#{bank_code_input.replace(":", "\\:")}')
            inp_el.clear()
            inp_el.type(TEST_CODE, delay=50)
            print(f'  Filled Bank Code: {TEST_CODE}')
            fill_success = True
        except Exception as e:
            print(f'  [ERR] Fill Bank Code failed: {e}')

    if bank_name_input:
        try:
            inp_el = page.locator(f'#{bank_name_input.replace(":", "\\:")}')
            inp_el.clear()
            inp_el.type(TEST_NAME, delay=50)
            print(f'  Filled Bank Name: {TEST_NAME}')
        except Exception as e:
            print(f'  [ERR] Fill Bank Name failed: {e}')

    ss(page, 'v3_05_insert_filled.png', 'Insert fields filled')

    if not fill_success:
        print('\n  [WARN] Could not fill form. Dumping all visible input IDs for diagnosis:')
        all_vis = form_fields.get('inputs', [])
        for inp in all_vis:
            print(f'    {inp["id"]}')
        results['insert'] = 'FAIL — could not fill fields'
    else:
        # Save
        print('  Saving...')
        save_page(page)
        ss(page, 'v3_06_after_insert_save.png', 'After insert save')

        # Verify
        rows_after = get_table_rows(page)
        exists = check_row_exists(page, TEST_CODE)
        print(f'  Rows after insert: {len(rows_after)}, AUTOTEST exists: {exists}')
        if exists:
            print(f'  INSERT PASS — {TEST_CODE} found in table')
            results['insert'] = 'PASS'
        else:
            print(f'  INSERT FAIL — {TEST_CODE} not found. Rows: {rows_after}')
            results['insert'] = 'FAIL — not found after save'

    ss(page, 'v3_07_insert_complete.png', 'Insert phase complete')

    # ─── UPDATE ─────────────────────────────────────────────────────────────
    print('\n=== UPDATE ===')
    if results.get('insert') == 'PASS':
        # Find and click the row for AUTOTEST_BNK_001
        row_locator = page.locator(
            f"xpath=//tbody[@id='manage_object_nav_nav:form:T_data']//tr[td[normalize-space(text())='{TEST_CODE}']]"
        )
        if row_locator.count() > 0:
            row_locator.first.click()
            wait_ajax(page)
            ss(page, 'v3_08_row_selected.png', 'Row selected for update')

            # Find the Bank Name field in objectForm
            upd_fields = find_object_form_fields(page)
            obj_inputs = [i for i in upd_fields.get('inputs', [])
                          if 'objectForm' in i['id'] or 'tab:tabPanel' in i['id']]
            upd_name_field = None
            if len(obj_inputs) > 1:
                upd_name_field = obj_inputs[1]['id']
            elif bank_name_input:
                upd_name_field = bank_name_input

            print(f'  Update name field: {upd_name_field}')
            if upd_name_field:
                try:
                    inp_el = page.locator(f'#{upd_name_field.replace(":", "\\:")}')
                    inp_el.triple_click()
                    inp_el.type(TEST_NAME_UPD, delay=50)
                    ss(page, 'v3_09_update_filled.png', 'Update field filled')
                    save_page(page)
                    ss(page, 'v3_10_after_update_save.png', 'After update save')

                    # Verify update (check name in row)
                    row_after_upd = page.locator(
                        f"xpath=//tbody[@id='manage_object_nav_nav:form:T_data']"
                        f"//tr[td[normalize-space(text())='{TEST_CODE}']]"
                    )
                    if row_after_upd.count() > 0:
                        row_text = row_after_upd.first.text_content()
                        upd_found = TEST_NAME_UPD in row_text
                        print(f'  UPDATE {"PASS" if upd_found else "FAIL"} — row: {row_text[:100]}')
                        results['update'] = 'PASS' if upd_found else f'FAIL — row={row_text[:80]}'
                    else:
                        print(f'  UPDATE FAIL — row not found after update')
                        results['update'] = 'FAIL — row missing'
                except Exception as e:
                    print(f'  [ERR] Update failed: {e}')
                    results['update'] = f'FAIL — {e}'
            else:
                print('  [WARN] Update name field not found')
                results['update'] = 'SKIP — field not found'
        else:
            print(f'  [WARN] Row {TEST_CODE} not found for update')
            results['update'] = 'SKIP — row not in table'
    else:
        print('  Skipping UPDATE (INSERT failed)')
        results['update'] = 'SKIP'

    # ─── DELETE ─────────────────────────────────────────────────────────────
    print('\n=== DELETE ===')
    if results.get('insert') == 'PASS':
        # Select the row
        row_for_del = page.locator(
            f"xpath=//tbody[@id='manage_object_nav_nav:form:T_data']//tr[td[normalize-space(text())='{TEST_CODE}']]"
        )
        if row_for_del.count() > 0:
            row_for_del.first.click()
            wait_ajax(page)
            ss(page, 'v3_11_row_selected_delete.png', 'Row selected for delete')

            # Click Delete toolbar button
            del_btn = page.locator("xpath=//a[@title='Delete [Ctrl+d]' and not(contains(@class,'ui-state-disabled'))]")
            if del_btn.count() == 0:
                del_btn = page.locator("xpath=//a[.//span[contains(@class,'ui-icon-delete')] and not(contains(@class,'ui-state-disabled'))]")
            if del_btn.count() > 0:
                del_btn.first.click()
                wait_ajax(page)
                ss(page, 'v3_12_after_delete_click.png', 'After delete click')

                # Handle confirmation dialog if appears
                confirm_btn = page.locator("xpath=//button[contains(@onclick,'confirm') or @id='confirmationForm:yes'] | xpath=//a[normalize-space(text())='Yes'] | xpath=//button[normalize-space(text())='Yes']")
                if confirm_btn.count() > 0 and confirm_btn.first.is_visible():
                    confirm_btn.first.click()
                    wait_ajax(page)

                # Save
                save_page(page)
                ss(page, 'v3_13_after_delete_save.png', 'After delete save')

                # Verify deleted
                still_exists = check_row_exists(page, TEST_CODE)
                print(f'  DELETE {"PASS" if not still_exists else "FAIL"} — still_exists={still_exists}')
                results['delete'] = 'PASS' if not still_exists else 'FAIL — still in table'
            else:
                print('  [WARN] Delete toolbar button not found/disabled')
                results['delete'] = 'FAIL — delete button not found'
        else:
            print(f'  [WARN] Row {TEST_CODE} not found for delete')
            results['delete'] = 'SKIP — row not found'
    else:
        print('  Skipping DELETE (INSERT failed)')
        results['delete'] = 'SKIP'

    ss(page, 'v3_14_final_state.png', 'Final state')
    ctx.close()
    browser.close()

# ─── SAVE RESULTS ────────────────────────────────────────────────────────────
with open(LOG_PATH, 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2)

print('\n' + '='*60)
print('RESULTS SUMMARY')
print('='*60)
for k, v in results.items():
    print(f'  {k:<15} : {v}')
print(f'\nLog: {LOG_PATH}')
print(f'Screenshots: {SS_DIR}')
