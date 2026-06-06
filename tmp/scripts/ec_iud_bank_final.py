"""
EC IUD Bank — FINAL.
Correct field IDs from deep DOM inspection:
  INSERT  : objectForm:form G:0:R:0=Code, R:1=Name, R:2:da_input=StartDate
  UPDATE  : updateAttributes:form G:0:R:1=Name  (Code is read-only after creation)
  DELETE  : objectdates:form G:0:R:0:C:3:da_input = EndDate (EC restricts hard-delete for banks;
            soft-delete by setting End Date = makes bank inactive/expired)
NEVER TOUCH EXISTING DATA. Test data: AUTOTEST_BNK_001 only.
"""
from playwright.sync_api import sync_playwright
import json, os

EC_URL        = 'https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/'
SS_DIR        = r'c:\Projects\ChoongYin_OS\docs\EC\screenshots\iud_bank'
LOG_PATH      = r'c:\Projects\ChoongYin_OS\tmp\logs\ec_iud_bank_final.json'
TEST_CODE     = 'AUTOTEST_BNK_003'
TEST_NAME     = 'AUTOTEST Bank 003'
TEST_NAME_UPD = 'AUTOTEST Bank 003 UPDATED'
START_DATE    = '2000-01-01'
END_DATE      = '2000-01-02'   # Soft-delete: expire next day

# Field IDs (from DOM deep dive)
INS_CODE_ID   = 'tab:tabPanel:objectForm:form:G:0:R:0:C:1:in'
INS_NAME_ID   = 'tab:tabPanel:objectForm:form:G:0:R:1:C:1:in'
INS_DATE_ID   = 'tab:tabPanel:objectForm:form:G:0:R:2:C:1:da_input'
UPD_CODE_ID   = 'tab:tabPanel:updateAttributes:form:G:0:R:0:C:1:in'
UPD_NAME_ID   = 'tab:tabPanel:updateAttributes:form:G:0:R:1:C:1:in'
DEL_ENDDATE_ID= 'tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input'

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
    # Enable then click
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
    """Click the row span for a given bank code."""
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
    ss(page, 'bank_loaded')

    # ── CLEAN STATE / PRE-CLEANUP ────────────────────────────────────────────
    print('\n=== CLEAN STATE ===')
    rows0 = get_table_rows(page)
    print(f'  Banks: {[r[0] for r in rows0]}')

    if check_row(page, TEST_CODE):
        print(f'  Pre-existing AUTOTEST found — expiring to clean up')
        ok = select_row(page, TEST_CODE)
        if ok:
            fill_date(page, DEL_ENDDATE_ID, END_DATE)
            ss(page, 'pre_cleanup_end_date_set')
            do_save(page)
            click_go(page)
            print(f'  Cleanup: still_in_table={check_row(page, TEST_CODE)}')
        results['pre_cleanup'] = 'done'

    rows0 = get_table_rows(page)
    print(f'  Banks now: {[r[0] for r in rows0]}')
    results['clean'] = 'CLEAN' if not check_row(page, TEST_CODE) else 'PRE-EXISTED+EXPIRED'
    ss(page, 'clean_state')

    # Reset screen only if pre-cleanup was done (screen state changed)
    if results.get('pre_cleanup') == 'done':
        si2 = page.locator('#menu\\:searchForm\\:searchTxt')
        si2.clear(); si2.type('Bank', delay=60)
        page.wait_for_load_state('networkidle', timeout=8000)
        page.wait_for_timeout(400)
        page.locator(
            "xpath=//*[self::label or self::span][contains(@class,'tv-link') and normalize-space(text())='Bank']"
        ).first.click()
        wait_ajax(page)
        print('  Screen refreshed after pre-cleanup')

    # ── INSERT ───────────────────────────────────────────────────────────────
    print('\n=== INSERT ===')

    # Click "New Object" via JS eval of onclick — bypasses hover state issues in headless mode
    # Hover Insert → click "New Object"
    # XPath uses normalize-space(.) to match descendant text (text is in child <span>)
    insert_li = page.locator(
        "xpath=//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'ui-icon-insert')]]"
    )
    insert_li.first.hover()
    page.wait_for_timeout(1000)
    # All submenu links — click the one whose descendant text = "New Object"
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
        # Click first visible submenu link
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

    # Fill the 3 mandatory fields
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

    # ── UPDATE ───────────────────────────────────────────────────────────────
    print('\n=== UPDATE ===')
    if results.get('insert') == 'PASS':
        ok = select_row(page, TEST_CODE)
        if ok:
            ss(page, 'update_row_selected')
            # Verify the updateAttributes loaded
            code_val = get_field_val(page, UPD_CODE_ID)
            name_val = get_field_val(page, UPD_NAME_ID)
            print(f'  updateAttributes loaded: code={code_val}, name={name_val}')

            # Update the Bank Name
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
            results['update'] = 'FAIL — row not found'
    else:
        results['update'] = 'SKIP'
    ss(page, 'update_result')

    # ── DELETE (soft-delete via End Date) ────────────────────────────────────
    print('\n=== DELETE (soft-delete via End Date) ===')
    print('  NOTE: EC Bank toolbar Delete is disabled by design (banks are permanent master data).')
    print(f'  Soft-delete: set End Date={END_DATE} on AUTOTEST bank to expire it.')
    if results.get('insert') == 'PASS':
        ok = select_row(page, TEST_CODE)
        if ok:
            ss(page, 'delete_row_selected')
            # Verify objectdates tab loaded
            start = get_field_val(page, DEL_ENDDATE_ID.replace('C:3', 'C:1'))
            enddate_val = get_field_val(page, DEL_ENDDATE_ID)
            print(f'  objectdates: StartDate={start}, EndDate={enddate_val}')

            # Set End Date = one day after Start Date (expires the bank)
            ok_end = fill_date(page, DEL_ENDDATE_ID, END_DATE)
            print(f'  EndDate set: {END_DATE} (ok={ok_end})')
            ss(page, 'delete_end_date_set')

            method_d = do_save(page)
            err_d = get_ec_error(page)
            print(f'  Saved via: {method_d}')
            ss(page, 'delete_saved')

            click_go(page)

            # Verify: after expiry, bank should NOT appear in table at current nav date
            # (End Date < current nav date = bank is expired/inactive = soft-delete success)
            still_visible = check_row(page, TEST_CODE)
            print(f'  Bank still in table after expiry: {still_visible}')
            if not still_visible:
                print(f'  DELETE PASS: bank expired (EndDate={END_DATE}), no longer visible at current date')
                results['delete'] = f'PASS (soft-delete: EndDate={END_DATE}, bank expired)'
            else:
                print(f'  DELETE FAIL: bank still visible after End Date set')
                results['delete'] = f'FAIL — still visible err={err_d or "none"}'
        else:
            results['delete'] = 'FAIL — row not found'
    else:
        results['delete'] = 'SKIP'
    ss(page, 'delete_result')
    print(f'  DELETE: {results["delete"]}')

    ss(page, 'final_state')
    ctx.close()
    browser.close()

# Save results
with open(LOG_PATH, 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2)

print('\n' + '='*60)
print('FINAL RESULTS')
print('='*60)
all_pass = True
for k, v in results.items():
    ok = v in ('PASS', 'CLEAN', 'done') or v.startswith('PASS') or v.startswith('PRE-')
    sym = '✓' if ok else '✗'
    if not ok and k not in ('pre_cleanup', 'clean'): all_pass = False
    print(f'  {sym} {k:<15} : {v}')
print(f'\nOverall: {"ALL PASS" if all_pass else "SOME FAILURES"}')
print(f'Log:     {LOG_PATH}')
print(f'Shots:   {SS_DIR}')
