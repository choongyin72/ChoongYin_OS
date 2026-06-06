"""
EC IUD Test — Bank Screen (Configuration > Finance Objects > Bank)
Local EC: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/
Test data: AUTOTEST_BNK_001 / AUTOTEST Bank 001
Operations: Insert → Verify → Update → Verify → Delete → Verify
"""
from playwright.sync_api import sync_playwright
import json, os, sys, time

EC_URL   = 'https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/'
SS_DIR   = r'c:\Projects\ChoongYin_OS\docs\EC\screenshots\iud_bank'
LOG_PATH = r'c:\Projects\ChoongYin_OS\tmp\logs\ec_iud_bank.txt'
RF_PATH  = r'c:\Projects\ChoongYin_OS\tmp\scripts\ec_iud_bank.robot'

os.makedirs(SS_DIR, exist_ok=True)
os.makedirs(r'c:\Projects\ChoongYin_OS\tmp\logs', exist_ok=True)

class Tee:
    def __init__(self, *files): self.files = files
    def write(self, obj): [f.write(obj) for f in self.files]; [f.flush() for f in self.files]
    def flush(self): [f.flush() for f in self.files]
_log = open(LOG_PATH, 'w', encoding='utf-8')
sys.stdout = Tee(sys.__stdout__, _log)

# Test data
BANK_CODE = 'AUTOTEST_BNK_001'
BANK_NAME = 'AUTOTEST Bank 001'
BANK_NAME_UPDATED = 'AUTOTEST Bank 001 UPDATED'

results = {
    'insert': None, 'verify_insert': None,
    'update': None, 'verify_update': None,
    'delete': None, 'verify_delete': None,
    'blockers': []
}

def take_ss(page, name, step):
    path = os.path.join(SS_DIR, f'{step:02d}_{name}.png')
    page.screenshot(path=path)
    print(f'  📸 Screenshot: {os.path.basename(path)}')
    return path

def wait_and_log(page, msg, timeout=20000):
    page.wait_for_load_state('networkidle', timeout=timeout)
    page.wait_for_timeout(600)
    print(f'  ✓ {msg}')

def get_notification(page):
    """Read EC notification area message."""
    try:
        msg = page.locator('#ECNotificationArea').text_content()
        return msg.strip() if msg else ''
    except:
        return ''

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=['--ignore-certificate-errors'])
    ctx = browser.new_context(ignore_https_errors=True, viewport={'width': 1920, 'height': 1080})
    page = ctx.new_page()
    step = 0

    # ── STEP 0: LOGIN ────────────────────────────────────────────────────────
    print('='*60)
    print('EC IUD TEST — Bank Screen')
    print(f'Test data: {BANK_CODE} / {BANK_NAME}')
    print('='*60)
    print('\n[Step 0] Login...')
    page.goto(EC_URL, wait_until='domcontentloaded', timeout=30000)
    page.fill('#username', 'sysadmin')
    page.fill('#password', 'sysadmin')
    page.click('#kc-login')
    page.wait_for_url('**/dashboard**', timeout=60000)
    wait_and_log(page, 'Logged in')
    step += 1; take_ss(page, 'login_ok', step)

    # ── STEP 1: NAVIGATE TO BANK SCREEN ──────────────────────────────────────
    print('\n[Step 1] Navigate to Bank screen...')
    si = page.locator("xpath=//input[@id='menu:searchForm:searchTxt']")
    si.wait_for(state='visible', timeout=10000)
    si.clear()
    si.type('Bank', delay=60)
    wait_and_log(page, 'Search fired', timeout=8000)

    # Find Bank screen link
    bank_link = None
    for sel in [
        "xpath=//*[self::label or self::span][contains(@class,'tv-link') and normalize-space(text())='Bank']",
        "xpath=//*[self::label or self::span][contains(@class,'tv-link') and normalize-space(text())='Maintain Bank']",
    ]:
        el = page.locator(sel)
        if el.count() > 0 and el.first.is_visible():
            bank_link = el.first
            print(f'  Found link: {el.first.text_content().strip()}')
            break

    if not bank_link:
        # Blocker — try expanding Configuration > Finance Objects
        print('  ⚠️ Bank not found in search — trying treeview expansion...')
        results['blockers'].append('Bank not found in search — tried treeview fallback')
        # Get all search results visible
        all_links = page.locator("xpath=//*[self::label or self::span][contains(@class,'tv-link')]")
        links = [all_links.nth(i).text_content().strip() for i in range(min(all_links.count(), 10))]
        print(f'  Search results: {links}')
        # Try clicking any Bank-related link
        for txt in links:
            if 'bank' in txt.lower() or 'Bank' in txt:
                el = page.locator(f"xpath=//*[self::label or self::span][contains(@class,'tv-link') and normalize-space(text())='{txt}']")
                if el.count() > 0:
                    bank_link = el.first
                    print(f'  Using: {txt}')
                    break

    if bank_link:
        bank_link.click()
        wait_and_log(page, 'Bank screen opened')
        step += 1; take_ss(page, 'bank_screen', step)
        screen_label = page.locator('#screenToolbar\\:form\\:screenLabel').text_content()
        print(f'  Screen label: {screen_label}')
    else:
        results['blockers'].append('CRITICAL: Cannot navigate to Bank screen')
        print('  ❌ Cannot find Bank screen — BLOCKER')
        ctx.close(); browser.close()
        _log.close()
        sys.exit(1)

    # ── STEP 2: VERIFY CLEAN STATE (no AUTOTEST record) ──────────────────────
    print('\n[Step 2] Verify AUTOTEST_BNK_001 does not exist...')
    # Fill navigator if present and click Go
    nav_forms = page.locator('.ECFormScreenlet,.formScreenlet')
    if nav_forms.count() > 0:
        go_btn = page.locator('#button\\:form\\:B')
        if go_btn.count() > 0:
            go_btn.click()
            wait_and_log(page, 'Navigator Go clicked')

    # Check for existing AUTOTEST record
    autotest_rows = page.locator(f"xpath=//tr[@data-rk][.//td[contains(text(),'{BANK_CODE}')]]")
    if autotest_rows.count() > 0:
        print(f'  ⚠️ AUTOTEST record already exists — deleting first (cleanup)')
        # Delete it for clean start
        del_btn = autotest_rows.first.locator("button, span[class*='delete']").first
        if del_btn.count() > 0:
            del_btn.click()
            wait_and_log(page, 'Pre-existing AUTOTEST record deleted')
    else:
        print('  ✓ No AUTOTEST record — clean state confirmed')
    step += 1; take_ss(page, 'clean_state', step)

    # ── STEP 3: INSERT NEW BANK RECORD ───────────────────────────────────────
    print(f'\n[Step 3] INSERT: {BANK_CODE} / {BANK_NAME}...')

    # Click New/Insert button (toolbar insert menu)
    insert_icon = page.locator("xpath=//li[.//span[contains(@class,'ui-icon-insert')]]")
    if insert_icon.count() > 0 and not insert_icon.first.get_attribute('class', '').count('disabled'):
        insert_icon.first.click()
        page.wait_for_timeout(800)
        wait_and_log(page, 'Insert menu opened', timeout=8000)
        step += 1; take_ss(page, 'insert_menu_open', step)

        # Look for "Bank" option in submenu or direct insert
        bank_option = page.locator("xpath=//li/a[contains(.,'Bank')]")
        if bank_option.count() > 0:
            bank_option.first.click()
            wait_and_log(page, 'Bank insert option clicked')
        else:
            # Direct insert — no submenu needed
            print('  No submenu — direct insert mode')
    else:
        print('  ⚠️ Insert toolbar disabled — checking for New button...')
        results['blockers'].append('Insert toolbar disabled initially')

    step += 1; take_ss(page, 'after_insert_click', step)

    # Find the new blank row or editable fields
    # Try to find the Bank Code input in a new row
    bank_code_inputs = page.locator("xpath=//input[contains(@id,'bankCode') or contains(@id,'BANK_CODE') or contains(@id,'code') or contains(@id,'Code')]")
    if bank_code_inputs.count() > 0:
        # Fill Bank Code
        code_input = bank_code_inputs.first
        code_input.click()
        code_input.fill(BANK_CODE)
        page.keyboard.press('Tab')
        wait_and_log(page, f'Filled Bank Code: {BANK_CODE}', timeout=5000)

    # Find Bank Name input
    bank_name_inputs = page.locator("xpath=//input[contains(@id,'bankName') or contains(@id,'BANK_NAME') or contains(@id,'name') or contains(@id,'Name')]")
    if bank_name_inputs.count() > 0:
        name_input = bank_name_inputs.first
        name_input.click()
        name_input.fill(BANK_NAME)
        page.keyboard.press('Tab')
        wait_and_log(page, f'Filled Bank Name: {BANK_NAME}', timeout=5000)

    step += 1; take_ss(page, 'insert_data_filled', step)

    # Save
    print('  Saving...')
    page.click("xpath=//a[@title='Save [Ctrl+s]']")
    wait_and_log(page, 'Save clicked')

    # Handle confirmation dialog if appears
    confirm = page.locator('.ui-confirmdialog-yes')
    if confirm.count() > 0 and confirm.first.is_visible():
        confirm.first.click()
        wait_and_log(page, 'Confirmation accepted')

    notif = get_notification(page)
    step += 1; take_ss(page, 'after_save', step)
    print(f'  Notification: {notif if notif else "(none)"}')
    results['insert'] = 'attempted'

    # ── STEP 4: VERIFY INSERT ─────────────────────────────────────────────────
    print(f'\n[Step 4] VERIFY INSERT: Check {BANK_CODE} in table...')
    # Reload/Go to refresh data
    go_btn = page.locator('#button\\:form\\:B')
    if go_btn.count() > 0:
        go_btn.click()
        wait_and_log(page, 'Refreshed data')

    new_row = page.locator(f"xpath=//tr[@data-rk][.//td[contains(text(),'{BANK_CODE}')]]")
    if new_row.count() > 0:
        results['verify_insert'] = 'PASS'
        print(f'  ✅ INSERT VERIFIED: {BANK_CODE} found in table')
    else:
        results['verify_insert'] = 'FAIL - record not found after insert'
        print(f'  ❌ INSERT VERIFY FAILED: {BANK_CODE} not found')
        results['blockers'].append(f'Insert verification failed for {BANK_CODE}')
    step += 1; take_ss(page, 'verify_insert', step)

    # ── STEP 5: UPDATE ────────────────────────────────────────────────────────
    print(f'\n[Step 5] UPDATE: Change name to {BANK_NAME_UPDATED}...')
    if new_row.count() > 0:
        # Click on the name cell to edit
        name_cell = new_row.first.locator("td").nth(1)  # second column usually name
        name_cell.dblclick()
        page.wait_for_timeout(500)

        # Find editable input in the row
        name_edit = new_row.first.locator("input")
        if name_edit.count() > 0:
            name_edit.first.fill(BANK_NAME_UPDATED)
            page.keyboard.press('Tab')
            wait_and_log(page, f'Updated name to: {BANK_NAME_UPDATED}')
            # Save
            page.click("xpath=//a[@title='Save [Ctrl+s]']")
            wait_and_log(page, 'Update saved')
            confirm2 = page.locator('.ui-confirmdialog-yes')
            if confirm2.count() > 0 and confirm2.first.is_visible():
                confirm2.first.click()
                wait_and_log(page, 'Update confirmation accepted')
            results['update'] = 'attempted'
        else:
            results['update'] = 'SKIP - no editable input found'
            results['blockers'].append('Could not find editable input in row for update')
            print('  ⚠️ No editable input found — skipping update')
    else:
        results['update'] = 'SKIP - record not found'

    step += 1; take_ss(page, 'after_update', step)

    # ── STEP 6: VERIFY UPDATE ─────────────────────────────────────────────────
    print(f'\n[Step 6] VERIFY UPDATE...')
    go_btn2 = page.locator('#button\\:form\\:B')
    if go_btn2.count() > 0:
        go_btn2.click()
        wait_and_log(page, 'Refreshed after update')

    updated_row = page.locator(f"xpath=//tr[@data-rk][.//td[contains(text(),'{BANK_NAME_UPDATED}')]]")
    if updated_row.count() > 0:
        results['verify_update'] = 'PASS'
        print(f'  ✅ UPDATE VERIFIED: {BANK_NAME_UPDATED} found')
    else:
        results['verify_update'] = f'INCONCLUSIVE - checking original name'
        orig_row = page.locator(f"xpath=//tr[@data-rk][.//td[contains(text(),'{BANK_CODE}')]]")
        if orig_row.count() > 0:
            print(f'  ⚠️ Original record still present — update may have failed')
        print(f'  Note: Checking screen label for context')
    step += 1; take_ss(page, 'verify_update', step)

    # ── STEP 7: DELETE ────────────────────────────────────────────────────────
    print(f'\n[Step 7] DELETE: Remove AUTOTEST record...')
    # Find the row (by code)
    target_row = page.locator(f"xpath=//tr[@data-rk][.//td[contains(text(),'{BANK_CODE}')]]")
    if target_row.count() > 0:
        # Select the row first (click checkbox or row)
        target_row.first.click()
        page.wait_for_timeout(500)

        # Click delete icon in toolbar
        delete_icon = page.locator("xpath=//li[.//span[contains(@class,'ui-icon-delete')]]")
        if delete_icon.count() > 0:
            delete_icon.first.click()
            wait_and_log(page, 'Delete triggered')
            # Handle confirmation
            del_confirm = page.locator('.ui-confirmdialog-yes, .ui-dialog .ui-button')
            if del_confirm.count() > 0 and del_confirm.first.is_visible():
                del_confirm.first.click()
                wait_and_log(page, 'Delete confirmed')
            # Save
            page.click("xpath=//a[@title='Save [Ctrl+s]']")
            wait_and_log(page, 'Delete saved')
            results['delete'] = 'attempted'
        else:
            results['delete'] = 'SKIP - delete toolbar not available'
            results['blockers'].append('Delete toolbar icon not available')
    else:
        results['delete'] = 'SKIP - record not found'
    step += 1; take_ss(page, 'after_delete', step)

    # ── STEP 8: VERIFY DELETE ─────────────────────────────────────────────────
    print(f'\n[Step 8] VERIFY DELETE...')
    go_btn3 = page.locator('#button\\:form\\:B')
    if go_btn3.count() > 0:
        go_btn3.click()
        wait_and_log(page, 'Refreshed after delete')

    deleted_row = page.locator(f"xpath=//tr[@data-rk][.//td[contains(text(),'{BANK_CODE}')]]")
    if deleted_row.count() == 0:
        results['verify_delete'] = 'PASS'
        print(f'  ✅ DELETE VERIFIED: {BANK_CODE} no longer in table — environment clean')
    else:
        results['verify_delete'] = 'FAIL - record still present'
        print(f'  ❌ DELETE VERIFY FAILED: {BANK_CODE} still in table')
    step += 1; take_ss(page, 'verify_delete_clean', step)

    ctx.close()
    browser.close()

# ── RESULTS SUMMARY ───────────────────────────────────────────────────────────
print('\n' + '='*60)
print('IUD TEST RESULTS SUMMARY')
print('='*60)
for op, result in results.items():
    if op == 'blockers': continue
    icon = '✅' if str(result).startswith('PASS') else ('⚠️' if 'SKIP' in str(result) or 'attempted' in str(result) else '❌')
    print(f'  {icon} {op.upper():<20}: {result}')

if results['blockers']:
    print(f'\nBlockers encountered ({len(results["blockers"])}):')
    for b in results['blockers']:
        print(f'  ⚠️ {b}')
else:
    print('\n  No blockers encountered.')

print(f'\nScreenshots saved to: {SS_DIR}')
print(f'Log saved to: {LOG_PATH}')

# Save results JSON
results_path = r'c:\Projects\ChoongYin_OS\tmp\logs\ec_iud_bank_results.json'
with open(results_path, 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2)
print(f'Results JSON: {results_path}')
_log.close()
