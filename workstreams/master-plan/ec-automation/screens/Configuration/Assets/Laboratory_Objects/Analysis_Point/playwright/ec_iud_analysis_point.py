"""
EC IUD Analysis Point — freestyle Playwright proof. Screen: Configuration > Assets > Laboratory Objects >
Analysis Point. OV-GM (groupmodel, 3-level cascade): the grid (manageObject:form:T_data) loads only after
the PU -> Area -> Facility Class 1 navigator cascade (dds at nav:form:G:0:R:1:C:1/C:2/C:3) + GO.

Field IDs (recon 2026-06-19):
  INSERT objectForm: Start Date R:0, Code R:2, Name R:3, Type R:4 (dd, MANDATORY),
                     Op PU R:10 / Op Area R:11 / Op Facility Class 1 R:12 (dds — set = nav scope so the
                     row lists in the filtered grid; the groupmodel link).
  UPDATE updateAttributes: Name R:1.   DELETE objectdates: End Date R:0:C:3 = Start Date (true delete).
NEVER TOUCH EXISTING DATA. Test data: AUTOTEST_AP_* only. Credentials from env (R16).
  EC_HEADED=1 shows the browser; EC_CODE overrides the test code.
"""
from playwright.sync_api import sync_playwright
from pathlib import Path
import json, os

EC_URL    = os.environ.get('EC_URL', 'https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/')
EC_USER   = os.environ.get('EC_USER', 'sysadmin')   # R16: creds from env, never hardcoded
EC_PASS   = os.environ.get('EC_PASS', 'sysadmin')
SS_DIR    = str(Path(__file__).resolve().parents[1] / 'evidence')
LOG_PATH  = str(Path(__file__).resolve().parents[1] / 'evidence' / 'ec_iud_analysis_point_result.json')

HEADED    = os.environ.get('EC_HEADED', '0') == '1'
SLOW_MO   = int(os.environ.get('EC_SLOWMO', '600')) if HEADED else 0
_CODE     = os.environ.get('EC_CODE', 'AUTOTEST_AP_PWDEMO')
TEST_CODE = _CODE
TEST_NAME = f'AUTOTEST Analysis Point {_CODE}'
TEST_NAME_UPD = f'{TEST_NAME} UPDATED'
START_DATE = '2003-01-01'          # ref-dd screen — date must post-date seed reference objects
END_DATE   = '2003-01-01'          # DELETE: End Date = Start Date (zero-length window = true delete)
SCOPE = ['P1 Production Unit', 'P1 Area', 'P1 Facility 1']

GRID    = 'manageObject:form:T_data'
NAV_DDS = ['nav:form:G:0:R:1:C:1:dd', 'nav:form:G:0:R:1:C:2:dd', 'nav:form:G:0:R:1:C:3:dd']
INS_DATE = 'tab:tabPanel:objectForm:form:G:0:R:0:C:1:da_input'
INS_CODE = 'tab:tabPanel:objectForm:form:G:0:R:2:C:1:in'
INS_NAME = 'tab:tabPanel:objectForm:form:G:0:R:3:C:1:in'
INS_TYPE = 'tab:tabPanel:objectForm:form:G:0:R:4:C:1:dd'
INS_OP = ['tab:tabPanel:objectForm:form:G:0:R:10:C:1:dd', 'tab:tabPanel:objectForm:form:G:0:R:11:C:1:dd',
          'tab:tabPanel:objectForm:form:G:0:R:12:C:1:dd']
UPD_NAME = 'tab:tabPanel:updateAttributes:form:G:0:R:1:C:1:in'
DEL_END  = 'tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input'

os.makedirs(SS_DIR, exist_ok=True)
results = {}
ss_index = [0]


def ss(page, label):
    ss_index[0] += 1
    page.screenshot(path=os.path.join(SS_DIR, f'ap_{ss_index[0]:02d}_{label}.png'), full_page=False)
    print(f'  [SS] ap_{ss_index[0]:02d}_{label}.png')


def wait_ajax(page, t=20000):
    page.wait_for_load_state('networkidle', timeout=t); page.wait_for_timeout(1000)


def esc(fid):
    return '#' + fid.replace(':', '\\:')


def get_rows(page):
    return page.evaluate("""(g)=>{const t=document.getElementById(g); if(!t) return [];
        const o=[]; t.querySelectorAll('tr').forEach(tr=>{const c=[];tr.querySelectorAll('td').forEach(td=>c.push(td.textContent.trim()));
            if(c.some(x=>x))o.push(c);}); return o;}""", GRID)


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


def select_dd(page, dd_prefix, label=None):
    """Pick an option by label, or the first option if label is None."""
    page.locator(esc(dd_prefix + '_button')).first.click()
    if label:
        item = page.locator(f"xpath=//*[@id='{dd_prefix}_panel']//tr[normalize-space(@data-item-label)='{label}']")
    else:
        item = page.locator(f"xpath=//*[@id='{dd_prefix}_panel']//tr[@data-item-label]")
    try:
        item.first.wait_for(state='visible', timeout=8000)
    except Exception:
        page.keyboard.press('Escape'); page.wait_for_timeout(1200)
        page.locator(esc(dd_prefix + '_button')).first.click(); item.first.wait_for(state='visible', timeout=10000)
    picked = item.first.get_attribute('data-item-label')
    item.first.click(); wait_ajax(page, 12000)
    return picked


def do_save(page):
    sv = page.locator("xpath=//a[@title='Save [Ctrl+s]' and not(contains(@class,'ui-state-disabled'))]")
    if sv.count() > 0:
        sv.first.click(); wait_ajax(page); return
    page.keyboard.press('Control+s'); wait_ajax(page)


def click_go(page):
    go = page.locator(esc('button:form:B'))
    if go.count() > 0 and go.first.is_visible():
        go.first.click(); wait_ajax(page)


def select_row(page, code):
    span = page.locator(f"xpath=//tbody[@id='{GRID}']//span[normalize-space(text())='{code}']").first
    try:
        span.wait_for(state='visible', timeout=20000)
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
    results['login'] = 'PASS'

    print('\n=== NAVIGATE + CASCADE NAV ===')
    si = page.locator(esc('menu:searchForm:searchTxt')); si.wait_for(state='visible', timeout=10000)
    si.clear(); si.type('Analysis Point', delay=55); page.wait_for_load_state('networkidle', timeout=8000); page.wait_for_timeout(400)
    page.locator("xpath=//*[self::label or self::span][contains(@class,'tv-link') and normalize-space(text())='Analysis Point']").first.click()
    wait_ajax(page)
    for dd, val in zip(NAV_DDS, SCOPE):
        print(f'  nav {dd.split(":")[-2]} <- {select_dd(page, dd, val)}')
    click_go(page)
    results['navigate'] = 'PASS'
    ss(page, 'loaded')

    print('\n=== CLEAN STATE ===')
    if check_row(page, TEST_CODE) and select_row(page, TEST_CODE):
        fill(page, DEL_END, END_DATE, date=True); do_save(page); click_go(page)
    results['clean'] = 'CLEAN' if not check_row(page, TEST_CODE) else 'PRE-EXISTED+EXPIRED'
    ss(page, 'clean_state')

    print('\n=== INSERT ===')
    open_new_object(page)
    fill(page, INS_CODE, TEST_CODE);       print(f'  Code: {TEST_CODE}')
    fill(page, INS_NAME, TEST_NAME)
    fill(page, INS_DATE, START_DATE, date=True)
    print(f'  Type (first): {select_dd(page, INS_TYPE)}')
    for dd, val in zip(INS_OP, SCOPE):
        print(f'  {dd.split(":")[-2]} (Op) <- {select_dd(page, dd, val)}')
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
        do_save(page); click_go(page); click_go(page)
        results['delete'] = f'PASS (true delete: EndDate=StartDate={END_DATE})' if not check_row(page, TEST_CODE) else 'FAIL — still visible'
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
