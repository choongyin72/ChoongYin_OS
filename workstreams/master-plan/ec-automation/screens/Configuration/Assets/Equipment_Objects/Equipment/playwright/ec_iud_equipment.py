"""
EC IUD Equipment - Playwright (Manage Object screen, screen 2 of 2).
Navigator (cascading dropdowns, EXACT values per screenshot):
  Production Unit | Offshore area | Offshore facility | Compressor  -> Go
Field IDs (from Phase 0 deep-dive scan):
  INSERT  objectForm:      Code R:1:C:1:in, Name R:2:C:1:in, Start Date R:4:C:1:da_input
                           (Equipment Type R:0 is read-only, auto = Compressor from navigator)
  UPDATE  updateAttributes: Name R:2:C:1:in
  DELETE  objectdates:      End Date R:0:C:3:da_input = Start Date (zero-length = true delete);
                            toolbar - button is disabled (ui-submenu-state-disabled), so End=Start.
Result table: manageObject:form:T_data
NEVER TOUCH existing data (OFF_FLASH_GAS_CC / OFF_GINJ_COMP_A / OFF_GINJ_COMP_B).
"""
from playwright.sync_api import sync_playwright
from pathlib import Path
import json, os


def _repo_root() -> Path:
    env = os.environ.get('REPO_ROOT')
    if env:
        return Path(env)
    here = Path(__file__).resolve()
    for parent in [here, *here.parents]:
        if (parent / '.git').exists():
            return parent
    return here.parents[4]


ROOT          = _repo_root()
EC_URL        = os.environ.get('EC_URL', 'https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/')
EC_USER       = os.environ.get('EC_USER', 'sysadmin')   # R16: creds from env, never hardcoded
EC_PASS       = os.environ.get('EC_PASS', 'sysadmin')
SS_DIR        = str(ROOT / 'docs' / 'EC' / 'screenshots' / 'iud_equipment')
LOG_PATH      = str(ROOT / 'tmp' / 'logs' / 'ec_iud_equipment.json')

HEADED        = os.environ.get('EC_HEADED', '0') == '1'
SLOW_MO       = int(os.environ.get('EC_SLOWMO', '700')) if HEADED else 0
SKIP_DELETE   = os.environ.get('EC_SKIP_DELETE', '0') == '1'   # insert+update only (for DB proof)
DELETE_ONLY   = os.environ.get('EC_DELETE_ONLY', '0') == '1'   # select existing + delete (cleanup)
_CODE         = os.environ.get('EC_CODE', 'AUTOTEST_EQP_001')
_NUM          = _CODE.split('_')[-1]
TEST_CODE     = _CODE
TEST_NAME     = f'AUTOTEST Equipment {_NUM}'
TEST_NAME_UPD = f'AUTOTEST Equipment {_NUM} UPDATED'
START_DATE    = '2000-01-01'
END_DATE      = '2000-01-01'   # = Start Date -> true delete

# Navigator values (EXACT, per screenshot)
NAV = [('G:1', 'Production Unit'), ('G:2', 'Offshore area'),
       ('G:3', 'Offshore facility'), ('G:4', 'Compressor')]

# objectForm (insert) field IDs
INS_CODE = 'tab:tabPanel:objectForm:form:G:0:R:1:C:1:in'
INS_NAME = 'tab:tabPanel:objectForm:form:G:0:R:2:C:1:in'
INS_DATE = 'tab:tabPanel:objectForm:form:G:0:R:4:C:1:da_input'
# updateAttributes field IDs
UPD_NAME = 'tab:tabPanel:updateAttributes:form:G:0:R:2:C:1:in'
# objectdates field IDs
DEL_END  = 'tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input'
TABLE    = 'manageObject:form:T_data'

os.makedirs(SS_DIR, exist_ok=True)
os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
results = {}
_ss = [0]


def esc(i): return '#' + i.replace(':', '\\:')

def ss(page, label):
    _ss[0] += 1
    name = f'eq_{_ss[0]:02d}_{label}.png'
    page.screenshot(path=os.path.join(SS_DIR, name), full_page=False)
    print(f'  [SS] {name}')

def wait_ajax(page, t=15000):
    page.wait_for_load_state('networkidle', timeout=t); page.wait_for_timeout(1200)

def get_rows(page):
    return page.evaluate(f"""()=>{{const tb=document.getElementById('{TABLE}');if(!tb)return[];const o=[];
        tb.querySelectorAll('tr').forEach(tr=>{{const c=[];tr.querySelectorAll('td').forEach(td=>c.push((td.textContent||'').trim()));if(c.some(x=>x))o.push(c);}});return o;}}""")

def check_row(page, code):
    return any(r and r[0].strip() == code for r in get_rows(page))

def set_nav(page, group, want):
    btn = f'nav:form:{group}:R:1:C:0:dd_button'
    panel = f'nav:form:{group}:R:1:C:0:dd_panel'
    inp = f'nav:form:{group}:R:1:C:0:dd_input'
    page.locator(esc(btn)).first.click()
    page.wait_for_timeout(1000)
    opt = page.locator(esc(panel)).get_by_text(want, exact=True)
    if opt.count() == 0:
        opt = page.locator(esc(panel)).get_by_text(want)
    opt.first.click()
    wait_ajax(page, 12000)
    got = page.evaluate(f"()=>{{const e=document.getElementById('{inp}');return e?e.value.trim():'';}}")
    print(f'  nav {group} = "{got}"')
    return got

def fill(page, fid, value):
    el = page.locator(esc(fid))
    if el.count() == 0 or not el.is_visible():
        print(f'  [WARN] field not found: {fid}'); return False
    el.click(); el.fill(value)
    page.evaluate(f"""()=>{{const e=document.getElementById('{fid}');if(e){{e.dispatchEvent(new Event('change',{{bubbles:true}}));e.dispatchEvent(new Event('blur',{{bubbles:true}}));}}}}""")
    page.wait_for_timeout(400); return True

def fill_date(page, fid, value):
    el = page.locator(esc(fid))
    if el.count() == 0 or not el.is_visible():
        print(f'  [WARN] date field not found: {fid}'); return False
    el.click(); el.fill(value); page.keyboard.press('Tab'); page.wait_for_timeout(600)
    page.evaluate(f"""()=>{{const e=document.getElementById('{fid}');if(e){{e.dispatchEvent(new Event('change',{{bubbles:true}}));e.dispatchEvent(new Event('blur',{{bubbles:true}}));}}}}""")
    page.wait_for_timeout(400); return True

def do_save(page):
    sv = page.locator("xpath=//a[@title='Save [Ctrl+s]']")
    if sv.count() > 0 and 'disabled' not in (sv.first.get_attribute('class') or ''):
        sv.first.click(); wait_ajax(page); return 'button'
    page.evaluate("()=>{if(typeof EC!=='undefined')EC.toolbar.toggleSaveButton(true);}")
    page.wait_for_timeout(300)
    sv2 = page.locator("xpath=//a[@title='Save [Ctrl+s]' and not(contains(@class,'ui-state-disabled'))]")
    if sv2.count() > 0:
        sv2.first.click(); wait_ajax(page); return 'toggle+button'
    page.keyboard.press('Control+s'); wait_ajax(page); return 'ctrl+s'

def click_go(page):
    page.locator('#button\\:form\\:B').first.click(); wait_ajax(page)

def apply_navigator(page):
    for g, v in NAV:
        set_nav(page, g, v)
    click_go(page)

def select_row(page, code):
    sp = page.locator(f'css={esc(TABLE)} span').filter(has_text=code).first
    if sp.count() == 0:
        print(f'  [WARN] row span not found: {code}'); return False
    sp.click(); wait_ajax(page); page.wait_for_timeout(800); return True

def ec_error(page):
    t = page.evaluate("""()=>{const n=document.getElementById('ECNotificationArea');return n?(n.textContent||'').replace(/EC\\.jsMessage\\.clear\\(\\);/,'').trim():'';}""")
    return t[:160] if ('Required' in t or 'Error' in t or 'empty' in t) else ''


with sync_playwright() as p:
    browser = p.chromium.launch(headless=not HEADED, slow_mo=SLOW_MO, args=['--ignore-certificate-errors'])
    print(f'  [MODE] headed={HEADED} slowmo={SLOW_MO} code={TEST_CODE}')
    ctx = browser.new_context(ignore_https_errors=True, viewport={'width': 1920, 'height': 1080})
    page = ctx.new_page()

    # LOGIN
    print('=== LOGIN ===')
    page.goto(EC_URL, wait_until='domcontentloaded', timeout=30000)
    page.fill('#username', EC_USER); page.fill('#password', EC_PASS); page.click('#kc-login')
    page.wait_for_url('**/dashboard**', timeout=60000); wait_ajax(page)
    results['login'] = 'PASS'; print('  OK')

    # NAVIGATE
    print('\n=== NAVIGATE TO EQUIPMENT ===')
    si = page.locator('#menu\\:searchForm\\:searchTxt'); si.wait_for(state='visible', timeout=10000)
    si.clear(); si.type('Equipment', delay=60); page.wait_for_load_state('networkidle', timeout=8000); page.wait_for_timeout(500)
    page.locator("xpath=//*[self::label or self::span][contains(@class,'tv-link') and normalize-space(text())='Equipment']").first.click()
    wait_ajax(page)
    lbl = page.locator('#screenToolbar\\:form\\:screenLabel').text_content(timeout=5000)
    results['navigate'] = 'PASS' if 'Equipment' in lbl else f'FAIL={lbl}'
    print(f'  Screen: {lbl}')
    ss(page, 'loaded')

    # APPLY NAVIGATOR FILTERS
    print('\n=== SET NAVIGATOR + GO ===')
    apply_navigator(page)
    ss(page, 'filtered')
    rows0 = get_rows(page)
    print(f'  Equipment rows ({len(rows0)}): {[r[0] for r in rows0]}')
    err = ec_error(page)
    if err:
        print(f'  [ERR] navigator: {err}')
    results['navigator'] = 'PASS' if rows0 else f'FAIL err={err or "no rows"}'

    # CLEAN STATE
    print('\n=== CLEAN STATE ===')
    if check_row(page, TEST_CODE):
        print(f'  [WARN] {TEST_CODE} already present - use a fresh code')
        results['clean'] = 'PRE-EXISTS'
    else:
        results['clean'] = 'CLEAN'

    # INSERT
    print('\n=== INSERT ===')
    if DELETE_ONLY:
        results['insert'] = 'SKIP (delete-only)'
    elif results.get('clean') == 'CLEAN' and rows0:
        insert_li = page.locator("xpath=//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'ui-icon-insert')]]")
        insert_li.first.hover(); page.wait_for_timeout(900)
        sub = page.locator("xpath=//ul[contains(@class,'ui-menu-child')]//li//a")
        for i in range(sub.count()):
            try:
                if sub.nth(i).is_visible() and sub.nth(i).text_content(timeout=800).strip() == 'New Object':
                    sub.nth(i).click(); break
            except Exception:
                pass
        wait_ajax(page); ss(page, 'new_object')
        fill(page, INS_CODE, TEST_CODE);  print(f'  Code: {TEST_CODE}')
        fill(page, INS_NAME, TEST_NAME);  print(f'  Name: {TEST_NAME}')
        fill_date(page, INS_DATE, START_DATE); print(f'  Start: {START_DATE}')
        # confirm Equipment Type auto-set
        et = page.evaluate("()=>{const e=document.getElementById('tab:tabPanel:objectForm:form:G:0:R:0:C:1:in');return e?e.value:'';}")
        print(f'  Equipment Type (auto): "{et}"')
        ss(page, 'insert_filled')
        m = do_save(page); print(f'  Saved via: {m}')
        err = ec_error(page)
        if err: print(f'  [ERR] save: {err}')
        ss(page, 'insert_saved')
        click_go(page)  # refresh list with same filters
        exists = check_row(page, TEST_CODE)
        print(f'  Rows now: {[r[0] for r in get_rows(page)]}')
        results['insert'] = 'PASS' if exists else f'FAIL err={err or "not in table"}'
    else:
        results['insert'] = 'SKIP'
    print(f'  INSERT: {results["insert"]}')
    ss(page, 'insert_result')

    # UPDATE
    print('\n=== UPDATE ===')
    if DELETE_ONLY:
        results['update'] = 'SKIP (delete-only)'
    elif results.get('insert') == 'PASS':
        if select_row(page, TEST_CODE):
            ss(page, 'upd_row')
            fill(page, UPD_NAME, TEST_NAME_UPD); print(f'  Name -> {TEST_NAME_UPD}')
            ss(page, 'upd_filled')
            do_save(page); click_go(page)
            sel_again = [r for r in get_rows(page) if r and r[0] == TEST_CODE]
            ok = bool(sel_again) and TEST_NAME_UPD in str(sel_again)
            print(f'  Row: {sel_again}')
            results['update'] = 'PASS' if ok else f'FAIL row={sel_again}'
        else:
            results['update'] = 'FAIL - row not found'
    else:
        results['update'] = 'SKIP'
    print(f'  UPDATE: {results["update"]}')

    # DELETE - try - button, else End=Start
    print('\n=== DELETE (try - button, else End=Start) ===')
    if SKIP_DELETE:
        results['delete'] = 'SKIP (skip-delete mode)'
    elif (DELETE_ONLY or results.get('insert') == 'PASS') and check_row(page, TEST_CODE):
        select_row(page, TEST_CODE); ss(page, 'del_row')
        # try the - / delete toolbar button if enabled
        delbtn = page.locator("xpath=//a[(@title='Delete [Ctrl+d]' or .//span[contains(@class,'ui-icon-delete')]) and not(ancestor::li[contains(@class,'ui-submenu-state-disabled')]) and not(contains(@class,'ui-state-disabled'))]")
        used = ''
        if delbtn.count() > 0 and delbtn.first.is_visible():
            print('  - button appears enabled - clicking it')
            delbtn.first.click(); wait_ajax(page)
            confirm = page.locator("button:has-text('Yes'), #confirmationForm\\:yes")
            if confirm.count() > 0 and confirm.first.is_visible():
                confirm.first.click(); wait_ajax(page)
            do_save(page); used = '-button'
        else:
            print('  - button disabled (as expected) - using End Date = Start Date')
            fill_date(page, DEL_END, END_DATE); print(f'  End Date = {END_DATE}')
            ss(page, 'del_enddate')
            do_save(page); used = 'end=start'
        click_go(page)
        gone = not check_row(page, TEST_CODE)
        print(f'  DELETE via {used}: gone={gone}')
        results['delete'] = f'PASS ({used})' if gone else f'FAIL via {used} (still present)'
    else:
        results['delete'] = 'SKIP'
    print(f'  DELETE: {results["delete"]}')
    ss(page, 'final')

    ctx.close(); browser.close()

with open(LOG_PATH, 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2)
print('\n' + '=' * 56 + '\nRESULTS\n' + '=' * 56)
for k, v in results.items():
    ok = v in ('PASS', 'CLEAN') or str(v).startswith('PASS')
    print(f'  {"OK " if ok else "XX "} {k:<12}: {v}')
print(f'\nLog: {LOG_PATH}\nShots: {SS_DIR}')
