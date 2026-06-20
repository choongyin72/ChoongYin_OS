"""
EC IUD Carrier - freestyle Playwright proof. Screen: Configuration > Assets > Cargo Objects > Carrier.
Manage-Object (OV), Bank-family grid (manage_object_nav_nav:form:T_data); NOT gated (nav = optional date).

Field IDs (recon 2026-06-19):
  INSERT objectForm: Code R:0, Name R:1, Start Date R:4 (da_input), Unit R:9 (dd, MANDATORY).
                     (Carrier Group R:2 / Carrier Type R:3 sit between Name and Start Date - both optional.)
  UPDATE updateAttributes: Name R:1.
  DELETE objectdates: End Date R:0:C:3 = Start Date (zero-length window = true delete from ov_carrier).
NEVER TOUCH EXISTING DATA. Test data: AUTOTEST_CARR_* only; the referenced Unit is read-only seed.
Credentials from env (R16): EC_USER/EC_PASS (local sandbox default sysadmin/sysadmin).
  EC_HEADED=1 shows the browser; EC_CODE overrides the test code.
"""
from playwright.sync_api import sync_playwright
from pathlib import Path
import json, os

EC_URL    = os.environ.get('EC_URL', 'https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/')
EC_USER   = os.environ.get('EC_USER', 'sysadmin')   # R16: creds from env, never hardcoded
EC_PASS   = os.environ.get('EC_PASS', 'sysadmin')
SS_DIR    = str(Path(__file__).resolve().parents[1] / 'evidence')
LOG_PATH  = str(Path(__file__).resolve().parents[1] / 'evidence' / 'ec_iud_carrier_result.json')

HEADED    = os.environ.get('EC_HEADED', '0') == '1'
SLOW_MO   = int(os.environ.get('EC_SLOWMO', '600')) if HEADED else 0
_CODE     = os.environ.get('EC_CODE', 'AUTOTEST_CARR_PWDEMO')
TEST_CODE = _CODE
TEST_NAME = f'AUTOTEST Carrier {_CODE}'
TEST_NAME_UPD = f'{TEST_NAME} UPDATED'
START_DATE = '2003-01-01'          # ref-dd screen (Unit) - date must post-date seed reference objects
END_DATE   = '2003-01-01'          # DELETE: End Date = Start Date (zero-length window = true delete)

GRID      = 'manage_object_nav_nav:form:T_data'
INS_CODE  = 'tab:tabPanel:objectForm:form:G:0:R:0:C:1:in'
INS_NAME  = 'tab:tabPanel:objectForm:form:G:0:R:1:C:1:in'
INS_DATE  = 'tab:tabPanel:objectForm:form:G:0:R:4:C:1:da_input'
INS_UNIT  = 'tab:tabPanel:objectForm:form:G:0:R:9:C:1:dd'
UPD_NAME  = 'tab:tabPanel:updateAttributes:form:G:0:R:1:C:1:in'
DEL_END   = 'tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input'

os.makedirs(SS_DIR, exist_ok=True)
results = {}
ss_index = [0]


def ss(page, label):
    ss_index[0] += 1
    name = f'carrier_{ss_index[0]:02d}_{label}.png'
    page.screenshot(path=os.path.join(SS_DIR, name), full_page=False)
    print(f'  [SS] {name}')


def wait_ajax(page, t=20000):
    page.wait_for_load_state('networkidle', timeout=t)
    page.wait_for_timeout(1100)


def esc(fid):
    return '#' + fid.replace(':', '\\:')


def get_rows(page):
    return page.evaluate("""(g) => { const t=document.getElementById(g); if(!t) return [];
        const o=[]; t.querySelectorAll('tr').forEach(tr=>{const c=[];tr.querySelectorAll('td').forEach(td=>c.push(td.textContent.trim()));
            if(c.some(x=>x))o.push(c);}); return o; }""", GRID)


def check_row(page, code):
    return any(r and r[0].strip() == code for r in get_rows(page))


def fill(page, fid, value, date=False):
    el = page.locator(esc(fid))
    if el.count() == 0:
        print(f'  [WARN] field not found: {fid}'); return False
    el.click(); el.fill(value)
    if date:
        page.keyboard.press('Tab'); page.wait_for_timeout(500)
    page.evaluate("""(fid)=>{const e=document.getElementById(fid);if(e){e.dispatchEvent(new Event('change',{bubbles:true}));e.dispatchEvent(new Event('blur',{bubbles:true}));}}""", fid)
    page.wait_for_timeout(350)
    return True


def select_dd_first(page, dd_prefix):
    """Pick the first option of an EC autocomplete dropdown (mandatory ref dd on a throwaway record)."""
    page.locator(esc(dd_prefix + '_button')).first.click()
    item = page.locator(f"xpath=//*[@id='{dd_prefix}_panel']//tr[@data-item-label]").first
    try:
        item.wait_for(state='visible', timeout=8000)
    except Exception:
        page.keyboard.press('Escape'); page.wait_for_timeout(1200)
        page.locator(esc(dd_prefix + '_button')).first.click()
        item.wait_for(state='visible', timeout=10000)
    label = item.get_attribute('data-item-label')
    item.click(); wait_ajax(page, 12000)
    print(f'  Unit (first option): {label}')


def do_save(page):
    save = page.locator("xpath=//a[@title='Save [Ctrl+s]' and not(contains(@class,'ui-state-disabled'))]")
    if save.count() > 0:
        save.first.click(); wait_ajax(page); return 'button'
    page.keyboard.press('Control+s'); wait_ajax(page); return 'ctrl+s'


def click_go(page):
    go = page.locator(esc('button:form:B'))
    if go.count() > 0 and go.first.is_visible():
        go.first.click(); wait_ajax(page)


def select_row(page, code):
    span = page.locator(f"xpath=//tbody[@id='{GRID}']//span[normalize-space(text())='{code}']").first
    try:
        span.wait_for(state='visible', timeout=15000)
    except Exception:
        print(f'  [WARN] row span not found: {code}'); return False
    span.click(); wait_ajax(page); page.wait_for_timeout(800)
    return True


def open_new_object(page):
    page.locator("xpath=//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'ui-icon-insert')]]").first.hover()
    page.wait_for_timeout(900)
    links = page.locator("xpath=//ul[contains(@class,'ui-menu-child')]//li//a")
    for i in range(links.count()):
        if links.nth(i).is_visible() and (links.nth(i).text_content(timeout=800) or '').strip() == 'New Object':
            links.nth(i).click(); break
    wait_ajax(page)


with sync_playwright() as p:
    browser = p.chromium.launch(headless=not HEADED, slow_mo=SLOW_MO, args=['--ignore-certificate-errors'])
    print(f'  [MODE] headed={HEADED}, code={TEST_CODE}')
    page = browser.new_context(ignore_https_errors=True, viewport={'width': 1920, 'height': 1080}).new_page()

    print('=== LOGIN ===')
    page.goto(EC_URL, wait_until='domcontentloaded', timeout=40000)
    page.fill('#username', EC_USER); page.fill('#password', EC_PASS); page.click('#kc-login')
    page.wait_for_url('**/dashboard**', timeout=60000); wait_ajax(page)
    results['login'] = 'PASS'; print('  OK')

    print('\n=== NAVIGATE ===')
    si = page.locator(esc('menu:searchForm:searchTxt')); si.wait_for(state='visible', timeout=10000)
    si.clear(); si.type('Carrier', delay=55); page.wait_for_load_state('networkidle', timeout=8000); page.wait_for_timeout(400)
    page.locator("xpath=//*[self::label or self::span][contains(@class,'tv-link') and normalize-space(text())='Carrier']").first.click()
    wait_ajax(page)
    lbl = page.locator(esc('screenToolbar:form:screenLabel')).text_content(timeout=5000)
    results['navigate'] = 'PASS' if 'Carrier' in (lbl or '') else f'FAIL={lbl}'
    print(f'  Screen: {lbl}')
    ss(page, 'loaded')

    print('\n=== CLEAN STATE ===')
    if check_row(page, TEST_CODE):
        if select_row(page, TEST_CODE):
            fill(page, DEL_END, END_DATE, date=True); do_save(page); click_go(page)
        results['pre_cleanup'] = 'done'
    results['clean'] = 'CLEAN' if not check_row(page, TEST_CODE) else 'PRE-EXISTED+EXPIRED'
    ss(page, 'clean_state')

    print('\n=== INSERT ===')
    open_new_object(page); ss(page, 'new_object')
    fill(page, INS_CODE, TEST_CODE);       print(f'  Code: {TEST_CODE}')
    fill(page, INS_NAME, TEST_NAME);       print(f'  Name: {TEST_NAME}')
    fill(page, INS_DATE, START_DATE, date=True); print(f'  Start: {START_DATE}')
    select_dd_first(page, INS_UNIT)
    ss(page, 'insert_filled')
    do_save(page); click_go(page)
    exists = check_row(page, TEST_CODE) or select_row(page, TEST_CODE)
    results['insert'] = 'PASS' if exists else 'FAIL'
    ss(page, 'insert_result'); print(f'  INSERT: {results["insert"]}')

    print('\n=== UPDATE ===')
    if results['insert'] == 'PASS' and select_row(page, TEST_CODE):
        fill(page, UPD_NAME, TEST_NAME_UPD); do_save(page); click_go(page)
        rows = get_rows(page); row = [r for r in rows if r and r[0] == TEST_CODE]
        results['update'] = 'PASS' if row and TEST_NAME_UPD in str(row) else f'FAIL row={row}'
    else:
        results['update'] = 'SKIP'
    ss(page, 'update_result'); print(f'  UPDATE: {results["update"]}')

    print('\n=== DELETE (End Date = Start Date -> true delete) ===')
    if results['insert'] == 'PASS' and select_row(page, TEST_CODE):
        fill(page, DEL_END, END_DATE, date=True); ss(page, 'delete_end_date_set')
        do_save(page); click_go(page)
        still = check_row(page, TEST_CODE)
        results['delete'] = f'PASS (true delete: EndDate=StartDate={END_DATE})' if not still else 'FAIL - still visible'
    else:
        results['delete'] = 'SKIP'
    ss(page, 'delete_result'); print(f'  DELETE: {results["delete"]}')

    ss(page, 'final_state')
    if HEADED:
        page.wait_for_timeout(5000)
    browser.close()

with open(LOG_PATH, 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2)
print('\n' + '=' * 56)
all_pass = all(str(v).startswith(('PASS', 'CLEAN', 'done', 'PRE-')) for v in results.values())
for k, v in results.items():
    print(f'  {"OK " if str(v).startswith(("PASS","CLEAN","done","PRE-")) else "XX "} {k:<13}: {v}')
print(f'\nOverall: {"ALL PASS" if all_pass else "SOME FAILURES"}\nLog: {LOG_PATH}')
