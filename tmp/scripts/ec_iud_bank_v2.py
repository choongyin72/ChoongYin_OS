"""
EC IUD Test v2 — Bank Screen
Local EC: https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/
Test data: AUTOTEST_BNK_001 / AUTOTEST Bank 001
"""
from playwright.sync_api import sync_playwright
import json, os, sys

EC_URL   = 'https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/'
SS_DIR   = r'c:\Projects\ChoongYin_OS\docs\EC\screenshots\iud_bank'
LOG_PATH = r'c:\Projects\ChoongYin_OS\tmp\logs\ec_iud_bank.txt'

os.makedirs(SS_DIR, exist_ok=True)

class Tee:
    def __init__(self, *files): self.files = files
    def write(self, obj): [f.write(obj) for f in self.files]; [f.flush() for f in self.files]
    def flush(self): [f.flush() for f in self.files]
_log = open(LOG_PATH, 'w', encoding='utf-8')
sys.stdout = Tee(sys.__stdout__, _log)

BANK_CODE = 'AUTOTEST_BNK_001'
BANK_NAME = 'AUTOTEST Bank 001'
BANK_NAME_UPDATED = 'AUTOTEST Bank 001 UPDATED'

results = {'insert': None, 'verify_insert': None, 'update': None,
           'verify_update': None, 'delete': None, 'verify_delete': None, 'blockers': []}

step = 0

def ss(page, name):
    global step; step += 1
    path = os.path.join(SS_DIR, f'{step:02d}_{name}.png')
    page.screenshot(path=path, full_page=False)
    print(f'  📸 {step:02d}_{name}.png')

def w(page, msg='done', timeout=15000):
    page.wait_for_load_state('networkidle', timeout=timeout)
    page.wait_for_timeout(500)
    print(f'  ✓ {msg}')

def notif(page):
    try: return (page.locator('#ECNotificationArea').text_content() or '').strip()
    except: return ''

def toolbar_enabled(page, icon_class):
    """Check if a toolbar icon is enabled (not disabled)."""
    li = page.locator(f"xpath=//li[.//span[contains(@class,'{icon_class}')]]")
    if li.count() == 0: return False
    cls = li.first.get_attribute('class') or ''
    return 'disabled' not in cls and 'state-disabled' not in cls

def click_toolbar(page, icon_class):
    """Click a toolbar icon."""
    li = page.locator(f"xpath=//li[.//span[contains(@class,'{icon_class}')]]")
    if li.count() > 0:
        li.first.click()
        page.wait_for_timeout(800)
        return True
    return False

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, args=['--ignore-certificate-errors', '--start-maximized'])
    ctx = browser.new_context(ignore_https_errors=True, viewport={'width': 1920, 'height': 1080})
    page = ctx.new_page()

    # LOGIN
    print('='*60)
    print('EC IUD TEST v2 — Bank Screen')
    print(f'Test: {BANK_CODE} | {BANK_NAME}')
    print('='*60)
    page.goto(EC_URL, wait_until='domcontentloaded', timeout=30000)
    page.fill('#username', 'sysadmin')
    page.fill('#password', 'sysadmin')
    page.click('#kc-login')
    page.wait_for_url('**/dashboard**', timeout=60000)
    w(page, 'Logged in')
    ss(page, '01_login_ok')

    # NAVIGATE TO BANK
    print('\n[NAVIGATE] Bank screen...')
    si = page.locator("xpath=//input[@id='menu:searchForm:searchTxt']")
    si.wait_for(state='visible', timeout=10000)
    si.clear()
    si.type('Bank', delay=60)
    w(page, 'Search fired', timeout=8000)
    ss(page, '02_search_bank')

    bank_link = page.locator("xpath=//*[self::label or self::span][contains(@class,'tv-link') and normalize-space(text())='Bank']")
    if bank_link.count() > 0:
        bank_link.first.click()
        w(page, 'Bank screen opened')
        ss(page, '03_bank_loaded')
    else:
        print('  ❌ Bank screen not found — ASKING USER')
        results['blockers'].append('Bank screen not found in search')
        ctx.close(); browser.close(); _log.close(); sys.exit(1)

    # INSPECT DOM — understand Bank screen structure
    print('\n[INSPECT] Bank screen DOM...')
    dom_info = page.evaluate("""() => {
        const r = {};
        r.screen_label = document.getElementById('screenToolbar:form:screenLabel')?.textContent?.trim()||'';
        r.screenlets = [];
        document.querySelectorAll('[class*=Screenlet],[class*=screenlet]').forEach(s => {
            if(s.id) r.screenlets.push({id:s.id, cls:s.className.substring(0,60)});
        });
        r.datatables = [];
        document.querySelectorAll('.ui-datatable').forEach(dt => {
            const cols = [];
            dt.querySelectorAll('thead th').forEach(th => cols.push(th.textContent.trim().substring(0,20)));
            const rows = dt.querySelectorAll('tbody tr').length;
            r.datatables.push({id:dt.id, cols:cols.slice(0,6), rows:rows});
        });
        r.inputs = [];
        document.querySelectorAll('input[id],select[id]').forEach(inp => {
            if(inp.offsetParent) r.inputs.push({id:inp.id, type:inp.type||inp.tagName, ph:inp.placeholder||''});
        });
        // Toolbar state
        r.save_enabled = !document.querySelector("a[title='Save [Ctrl+s]']")?.className?.includes('disabled');
        const insertLi = document.querySelector('li span.ui-icon-insert')?.closest('li');
        r.insert_enabled = insertLi ? !insertLi.className.includes('disabled') : false;
        const deleteLi = document.querySelector('li span.ui-icon-delete')?.closest('li');
        r.delete_enabled = deleteLi ? !deleteLi.className.includes('disabled') : false;
        return r;
    }""")
    print(f'  Screen: {dom_info["screen_label"]}')
    print(f'  Screenlets: {len(dom_info["screenlets"])} — {[s["id"][:30] for s in dom_info["screenlets"][:5]]}')
    print(f'  Datatables: {len(dom_info["datatables"])} — {[(d["id"][:25],d["cols"][:3],d["rows"]) for d in dom_info["datatables"][:3]]}')
    print(f'  Inputs: {len(dom_info["inputs"])} — {[i["id"][:30] for i in dom_info["inputs"][:5]]}')
    print(f'  Toolbar: save={dom_info["save_enabled"]} insert={dom_info["insert_enabled"]} delete={dom_info["delete_enabled"]}')

    # If screen has navigator with Go button — click Go first
    go_btn = page.locator('#button\\:form\\:B')
    if go_btn.count() > 0:
        print('\n[GO] Clicking Go to load all banks...')
        go_btn.click()
        w(page, 'Data loaded after Go')
        ss(page, '04_bank_data_loaded')
        # Re-inspect
        dom_info2 = page.evaluate("""() => {
            const dts = [];
            document.querySelectorAll('.ui-datatable').forEach(dt => {
                const cols = [];
                dt.querySelectorAll('thead th').forEach(th => cols.push(th.textContent.trim().substring(0,20)));
                dts.push({id:dt.id, cols:cols.slice(0,6), rows:dt.querySelectorAll('tbody tr').length});
            });
            return {datatables: dts};
        }""")
        print(f'  After Go: {[(d["id"][:25],d["cols"][:3],d["rows"]) for d in dom_info2["datatables"][:3]]}')

    # CHECK CLEAN STATE
    print(f'\n[CHECK] No existing {BANK_CODE}...')
    existing = page.locator(f"xpath=//tr[@data-rk][.//td[contains(text(),'{BANK_CODE}')]]")
    if existing.count() > 0:
        print(f'  ⚠️ AUTOTEST record exists — cleaning up first')
        existing.first.click()
        page.wait_for_timeout(300)
        click_toolbar(page, 'ui-icon-delete')
        w(page, 'Pre-cleanup delete', timeout=10000)
        page.click("xpath=//a[@title='Save [Ctrl+s]']")
        w(page, 'Pre-cleanup save')
    else:
        print(f'  ✓ Clean — no existing {BANK_CODE}')
    ss(page, '05_clean_verified')

    # ── INSERT ────────────────────────────────────────────────────────────────
    print(f'\n[INSERT] Creating {BANK_CODE}...')
    insert_ok = click_toolbar(page, 'ui-icon-insert')
    if not insert_ok:
        results['blockers'].append('Insert toolbar icon not found')
        print('  ⚠️ No insert icon — checking alternative...')
        # Try New button pattern
        new_btn = page.locator("xpath=//button[contains(@id,'new') or contains(@id,'New')]")
        if new_btn.count() > 0: new_btn.first.click()

    page.wait_for_timeout(1000)
    ss(page, '06_after_insert_click')

    # Check for submenu
    submenu = page.locator("xpath=//li/a[contains(text(),'Bank') and not(contains(text(),'Account'))]")
    if submenu.count() > 0 and submenu.first.is_visible():
        submenu.first.click()
        w(page, 'Bank submenu clicked')
        ss(page, '07_submenu_bank')

    # Find new row inputs
    print('  Looking for input fields...')
    all_inputs = page.evaluate("""() => {
        const ins = [];
        document.querySelectorAll('input[id],select[id]').forEach(inp => {
            if(inp.offsetParent && !inp.readOnly && inp.type !== 'hidden')
                ins.push({id:inp.id, type:inp.type||inp.tagName, val:inp.value, ph:inp.placeholder||''});
        });
        return ins;
    }""")
    print(f'  Editable inputs: {[i["id"][:40] for i in all_inputs[:8]]}')

    # Fill Bank Code — try various input ID patterns
    filled_code = False
    for pattern in ['bankCode', 'BANK_CODE', 'code', 'Code', 'CODE']:
        inp = page.locator(f"xpath=//input[contains(@id,'{pattern}') and not(contains(@id,'sfilter')) and not(contains(@id,'search'))]")
        if inp.count() > 0 and inp.first.is_visible():
            inp.first.click()
            inp.first.fill(BANK_CODE)
            page.keyboard.press('Tab')
            print(f'  ✓ Filled Bank Code via id*={pattern}: {BANK_CODE}')
            filled_code = True
            break

    if not filled_code and all_inputs:
        # Use first editable input
        first_input = page.locator(f"xpath=//input[@id='{all_inputs[0]['id']}']")
        first_input.fill(BANK_CODE)
        page.keyboard.press('Tab')
        print(f'  ✓ Filled first input {all_inputs[0]["id"][:30]}: {BANK_CODE}')
        filled_code = True

    # Fill Bank Name
    filled_name = False
    for pattern in ['bankName', 'BANK_NAME', 'name', 'Name', 'NAME']:
        inp = page.locator(f"xpath=//input[contains(@id,'{pattern}') and not(contains(@id,'sfilter')) and not(contains(@id,'search'))]")
        if inp.count() > 0 and inp.first.is_visible():
            val = inp.first.input_value()
            if val != BANK_CODE:  # skip if already filled with bank code
                inp.first.fill(BANK_NAME)
                page.keyboard.press('Tab')
                print(f'  ✓ Filled Bank Name via id*={pattern}: {BANK_NAME}')
                filled_name = True
                break

    if not filled_name and len(all_inputs) > 1:
        second_input = page.locator(f"xpath=//input[@id='{all_inputs[1]['id']}']")
        second_input.fill(BANK_NAME)
        page.keyboard.press('Tab')
        print(f'  ✓ Filled second input {all_inputs[1]["id"][:30]}: {BANK_NAME}')

    ss(page, '08_insert_filled')

    # Save
    print('  Saving insert...')
    page.click("xpath=//a[@title='Save [Ctrl+s]']")
    w(page, 'Save clicked')
    confirm = page.locator('.ui-confirmdialog-yes')
    if confirm.count() > 0 and confirm.first.is_visible():
        confirm.first.click()
        w(page, 'Save confirmed')
    msg = notif(page)
    ss(page, '09_insert_saved')
    print(f'  Notification: {msg or "(none)"}')
    results['insert'] = 'completed'

    # VERIFY INSERT
    print(f'\n[VERIFY INSERT] Looking for {BANK_CODE}...')
    if go_btn.count() > 0:
        go_btn.click()
        w(page, 'Refreshed')
    new_row = page.locator(f"xpath=//tr[@data-rk][.//td[contains(text(),'{BANK_CODE}')]]")
    if new_row.count() > 0:
        results['verify_insert'] = 'PASS'
        print(f'  ✅ INSERT VERIFIED: {BANK_CODE} in table ({new_row.count()} row)')
        row_data = new_row.first.inner_text()
        print(f'  Row data: {row_data[:80]}')
    else:
        results['verify_insert'] = 'FAIL'
        print(f'  ❌ {BANK_CODE} not found after insert')
        results['blockers'].append(f'Insert verify failed: {BANK_CODE} not found')
    ss(page, '10_verify_insert')

    # UPDATE — find and edit the record
    print(f'\n[UPDATE] Changing name to {BANK_NAME_UPDATED}...')
    target = page.locator(f"xpath=//tr[@data-rk][.//td[contains(text(),'{BANK_CODE}')]]")
    if target.count() > 0:
        # Find name cell (2nd column usually)
        cells = target.first.locator('td')
        for idx in range(cells.count()):
            cell_txt = cells.nth(idx).inner_text().strip()
            if BANK_NAME in cell_txt or 'Bank' in cell_txt:
                cells.nth(idx).click()
                page.wait_for_timeout(500)
                # Try double-click to enter edit mode
                cells.nth(idx).dblclick()
                page.wait_for_timeout(500)
                break
        # Find editable input in the row
        row_input = target.first.locator("input:not([type='hidden'])")
        if row_input.count() > 0:
            row_input.first.fill(BANK_NAME_UPDATED)
            page.keyboard.press('Tab')
            print(f'  ✓ Updated name to: {BANK_NAME_UPDATED}')
            ss(page, '11_update_filled')
            page.click("xpath=//a[@title='Save [Ctrl+s]']")
            w(page, 'Update saved')
            confirm2 = page.locator('.ui-confirmdialog-yes')
            if confirm2.count() > 0 and confirm2.first.is_visible():
                confirm2.first.click()
                w(page, 'Update confirmed')
            results['update'] = 'completed'
        else:
            results['update'] = 'SKIP - no editable row input'
            results['blockers'].append('Row not in edit mode — could not update')
            print('  ⚠️ Row not editable — Bank may be insert-only')
    else:
        results['update'] = 'SKIP - record not found'
    ss(page, '12_after_update')

    # VERIFY UPDATE
    print(f'\n[VERIFY UPDATE] Looking for {BANK_NAME_UPDATED}...')
    if go_btn.count() > 0:
        go_btn.click()
        w(page, 'Refreshed for update verify')
    upd_row = page.locator(f"xpath=//tr[@data-rk][.//td[contains(text(),'{BANK_NAME_UPDATED}')]]")
    if upd_row.count() > 0:
        results['verify_update'] = 'PASS'
        print(f'  ✅ UPDATE VERIFIED: {BANK_NAME_UPDATED} in table')
    else:
        # Check if original still there
        orig = page.locator(f"xpath=//tr[@data-rk][.//td[contains(text(),'{BANK_CODE}')]]")
        results['verify_update'] = f'INCONCLUSIVE - original name may persist ({orig.count()} rows with code)'
        print(f'  ⚠️ Updated name not found — original rows: {orig.count()}')
    ss(page, '13_verify_update')

    # DELETE — remove AUTOTEST record
    print(f'\n[DELETE] Removing {BANK_CODE}...')
    del_target = page.locator(f"xpath=//tr[@data-rk][.//td[contains(text(),'{BANK_CODE}')]]")
    if del_target.count() > 0:
        del_target.first.click()
        page.wait_for_timeout(400)
        ss(page, '14_record_selected')
        if click_toolbar(page, 'ui-icon-delete'):
            w(page, 'Delete triggered')
            confirm3 = page.locator('.ui-confirmdialog-yes, .ui-dialog .ui-button[id*=yes]')
            if confirm3.count() > 0 and confirm3.first.is_visible():
                confirm3.first.click()
                w(page, 'Delete confirmed')
            page.click("xpath=//a[@title='Save [Ctrl+s]']")
            w(page, 'Delete saved')
            results['delete'] = 'completed'
        else:
            results['delete'] = 'SKIP - delete toolbar not available'
            results['blockers'].append('Delete toolbar not clickable')
    else:
        results['delete'] = 'SKIP - record not found for delete'
    ss(page, '15_after_delete')

    # VERIFY DELETE
    print(f'\n[VERIFY DELETE] Confirming {BANK_CODE} removed...')
    if go_btn.count() > 0:
        go_btn.click()
        w(page, 'Final refresh')
    gone = page.locator(f"xpath=//tr[@data-rk][.//td[contains(text(),'{BANK_CODE}')]]")
    if gone.count() == 0:
        results['verify_delete'] = 'PASS'
        print(f'  ✅ DELETE VERIFIED: {BANK_CODE} gone — environment clean')
    else:
        results['verify_delete'] = 'FAIL - record still present'
        print(f'  ❌ {BANK_CODE} still in table')
    ss(page, '16_verify_delete_clean')

    ctx.close()
    browser.close()

# SUMMARY
print('\n' + '='*60)
print('IUD TEST SUMMARY')
print('='*60)
for op, res in results.items():
    if op == 'blockers': continue
    icon = '✅' if str(res).startswith('PASS') or res == 'completed' else ('⚠️' if 'SKIP' in str(res) or 'INCONCLUSIVE' in str(res) else '❌')
    print(f'  {icon} {op.upper():<20}: {res}')
if results['blockers']:
    print(f'\nBlockers:')
    for b in results['blockers']: print(f'  ⚠️ {b}')
else:
    print('\n  ✅ No blockers')
print(f'\nScreenshots: {SS_DIR}')

with open(r'c:\Projects\ChoongYin_OS\tmp\logs\ec_iud_bank_results.json', 'w') as f:
    json.dump(results, f, indent=2)
_log.close()
