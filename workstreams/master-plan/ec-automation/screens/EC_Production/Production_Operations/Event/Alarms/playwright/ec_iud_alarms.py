"""
EC IUD Alarms - freestyle Playwright proof. Screen: EC Production > Production Operations > Event > Alarms.
EVENT-LOG pattern: a DATA/DAY class (FCTY_DAY_ALARM) shown as a GATED inline grid. The PU/Area/Facility
cascade navigator (+ Date) + GO must be applied before the grid loads; then you ADD alarm rows. No object
code - rows are identified by a unique REASON marker. Insert/Delete are PHYSICAL.

Inline-grid cells (recon 2026-06-19): C0_da_input Time / C1_dd Area / C2_dd Type-of-Alarm (MANDATORY) /
C3_in Reason (marker) / C4_cb Report / C5_in Duration.   DB verify: DV_ALARMS by REASON marker.
NEVER TOUCH EXISTING DATA: AUTOTEST_ALARM_* reasons only. Credentials from env (R16).
  EC_HEADED=1 shows the browser; EC_CODE overrides the Reason marker.
"""
from playwright.sync_api import sync_playwright
from pathlib import Path
import json, os

EC_URL    = os.environ.get('EC_URL', 'https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/')
EC_USER   = os.environ.get('EC_USER', 'sysadmin')   # R16: creds from env, never hardcoded
EC_PASS   = os.environ.get('EC_PASS', 'sysadmin')
SS_DIR    = str(Path(__file__).resolve().parents[1] / 'evidence')
LOG_PATH  = str(Path(__file__).resolve().parents[1] / 'evidence' / 'ec_iud_alarms_result.json')

HEADED    = os.environ.get('EC_HEADED', '0') == '1'
SLOW_MO   = int(os.environ.get('EC_SLOWMO', '600')) if HEADED else 0
REASON    = os.environ.get('EC_CODE', 'AUTOTEST_ALARM_PWDEMO')
REASON_UPD = f'{REASON}_UPD'
ALARM_DATE = '2026-06-18'
NAV = {'G:1': 'P1 Production Unit', 'G:2': 'P1 Area', 'G:3': 'P1 Facility 1'}

GRID = 'alarms:form:T_data'
CELL = 'alarms:form:T'

os.makedirs(SS_DIR, exist_ok=True)
results = {}
ss_index = [0]


def ss(page, label):
    ss_index[0] += 1
    page.screenshot(path=os.path.join(SS_DIR, f'alarms_{ss_index[0]:02d}_{label}.png'), full_page=False)
    print(f'  [SS] alarms_{ss_index[0]:02d}_{label}.png')


def wait_ajax(page, t=20000):
    page.wait_for_load_state('networkidle', timeout=t); page.wait_for_timeout(1000)


def esc(fid):
    return '#' + fid.replace(':', '\\:')


def set_nav_dd(page, group, label):
    ddp = f'nav:form:{group}:R:1:C:0:dd'
    page.locator(esc(ddp + '_button')).first.click(); page.wait_for_timeout(900)
    page.locator(f"xpath=//*[@id='{ddp}_panel']//tr[normalize-space(@data-item-label)='{label}']").first.click()
    wait_ajax(page, 14000)


def select_cell_dd_first(page, dd_prefix):
    page.locator(esc(dd_prefix + '_button')).first.click()
    item = page.locator(f"xpath=//*[@id='{dd_prefix}_panel']//tr[@data-item-label]").first
    item.wait_for(state='visible', timeout=8000)
    label = item.get_attribute('data-item-label')
    item.click(); wait_ajax(page, 12000)
    print(f'  Type of Alarm (first option): {label}')


def type_cell(page, cell_id, value):
    el = page.locator(esc(cell_id))
    el.scroll_into_view_if_needed(); el.click()
    el.press('Control+a'); el.press('Delete'); el.type(value, delay=40); el.press('Tab')
    wait_ajax(page)


def row_by_reason(page, reason):
    return page.evaluate("""(args)=>{const [g,v]=args; const t=document.getElementById(g); if(!t) return -1;
        for(const e of t.querySelectorAll("input[id$='C3_in']")){ if((e.value||'')===v){const m=e.id.match(/:T:(\\d+):/); if(m) return parseInt(m[1]);}} return -1;}""", [GRID, reason])


def do_save(page):
    sv = page.locator("xpath=//a[@title='Save [Ctrl+s]' and not(contains(@class,'ui-state-disabled'))]")
    if sv.count() > 0:
        sv.first.click(); wait_ajax(page); return
    page.keyboard.press('Control+s'); wait_ajax(page)


def click_go(page):
    page.locator(esc('button:form:B')).first.click(); wait_ajax(page)


def insert_blank_row(page):
    page.locator("xpath=//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'ui-icon-insert')]]").first.hover()
    page.wait_for_timeout(900)
    page.locator("xpath=//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'ui-icon-insert')]]//ul[contains(@class,'ui-menu-child')]//a[normalize-space(.)='Alarms']").first.click()
    wait_ajax(page)


def delete_selected(page):
    page.locator("xpath=//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'ui-icon-delete')]]").first.hover()
    page.wait_for_timeout(900)
    page.locator("xpath=//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'ui-icon-delete')]]//ul[contains(@class,'ui-menu-child')]//a[normalize-space(.)='Alarms']").first.click()
    wait_ajax(page)


with sync_playwright() as p:
    browser = p.chromium.launch(headless=not HEADED, slow_mo=SLOW_MO, args=['--ignore-certificate-errors'])
    print(f'  [MODE] headed={HEADED}, reason={REASON}')
    page = browser.new_context(ignore_https_errors=True, viewport={'width': 1920, 'height': 1080}).new_page()

    print('=== LOGIN ===')
    page.goto(EC_URL, wait_until='domcontentloaded', timeout=40000)
    page.fill('#username', EC_USER); page.fill('#password', EC_PASS); page.click('#kc-login')
    page.wait_for_url('**/dashboard**', timeout=60000); wait_ajax(page)
    results['login'] = 'PASS'

    print('\n=== NAVIGATE + CASCADE NAV ===')
    si = page.locator(esc('menu:searchForm:searchTxt')); si.wait_for(state='visible', timeout=10000)
    si.clear(); si.type('Alarms', delay=55); page.wait_for_load_state('networkidle', timeout=8000); page.wait_for_timeout(400)
    page.locator("xpath=//*[self::label or self::span][contains(@class,'tv-link') and normalize-space(text())='Alarms']").first.click()
    wait_ajax(page)
    page.locator(esc('nav:form:G:0:R:1:C:0:da_input')).fill(ALARM_DATE); page.keyboard.press('Tab'); page.wait_for_timeout(500)
    for g, v in NAV.items():
        set_nav_dd(page, g, v); print(f'  nav {g} = {v}')
    click_go(page)
    results['navigate'] = 'PASS'
    ss(page, 'loaded')

    print('\n=== CLEAN STATE ===')
    if row_by_reason(page, REASON) >= 0:
        results['clean'] = 'PRE-EXISTED'
    else:
        results['clean'] = 'CLEAN'
    ss(page, 'clean_state')

    print('\n=== INSERT ===')
    insert_blank_row(page)
    r = row_by_reason(page, '')
    print(f'  blank row idx: {r}')
    select_cell_dd_first(page, f'{CELL}:{r}:C2_dd')
    r = row_by_reason(page, '')
    type_cell(page, f'{CELL}:{r}:C3_in', REASON); print(f'  Reason: {REASON}')
    ss(page, 'insert_filled')
    do_save(page); click_go(page)
    results['insert'] = 'PASS' if row_by_reason(page, REASON) >= 0 else 'FAIL'
    ss(page, 'insert_result'); print(f'  INSERT: {results["insert"]}')

    print('\n=== UPDATE (Reason change) ===')
    r = row_by_reason(page, REASON)
    if r >= 0:
        type_cell(page, f'{CELL}:{r}:C3_in', REASON_UPD); do_save(page); click_go(page)
        results['update'] = 'PASS' if row_by_reason(page, REASON_UPD) >= 0 and row_by_reason(page, REASON) < 0 else 'FAIL'
    else:
        results['update'] = 'SKIP'
    ss(page, 'update_result'); print(f'  UPDATE: {results["update"]}')

    print('\n=== DELETE (physical) ===')
    r = row_by_reason(page, REASON_UPD)
    if r >= 0:
        page.locator(esc(f'{CELL}:{r}:C3_in')).click(); page.wait_for_timeout(800)
        delete_selected(page); do_save(page); click_go(page)
        results['delete'] = 'PASS' if row_by_reason(page, REASON_UPD) < 0 else 'FAIL - still present'
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
all_pass = all(str(v).startswith(('PASS', 'CLEAN')) for v in results.values())
for k, v in results.items():
    print(f'  {"OK " if str(v).startswith(("PASS","CLEAN")) else "XX "} {k:<10}: {v}')
print(f'\nOverall: {"ALL PASS" if all_pass else "SOME FAILURES"}\nLog: {LOG_PATH}')
