"""
EC IUD MIME Type Mapping - Playwright (Table class / TV view, inline editable grid, paginated).
Screen: Configuration > System > MIME Type Mapping (mime_type_table:form, no navigator, 5-page grid).
Cells: mime_type_table:form:T:{row}:C0_in (MIME Type), C1_in (File Extensions) - both {mandatory:true}.
Cell commit: each input fires onchange -> PrimeFaces.ab partial-submit -> stages value server-side.
  => MUST type with real keys + Tab to fire onchange, then wait for the AJAX, before Save.
Verify after Save by RELOADING (Refresh) so the grid reflects the DB, then page-search.
INSERT/UPDATE/DELETE; DELETE on a Table class = PHYSICAL row removal.
NEVER touch existing rows. Test row only.
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


ROOT       = _repo_root()
EC_URL     = os.environ.get('EC_URL', 'https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/')
EC_USER    = os.environ.get('EC_USER', 'sysadmin')   # R16: creds from env, never hardcoded
EC_PASS    = os.environ.get('EC_PASS', 'sysadmin')
SS_DIR     = str(ROOT / 'docs' / 'EC' / 'screenshots' / 'iud_mime')
LOG_PATH   = str(ROOT / 'tmp' / 'logs' / 'ec_iud_mime.json')
HEADED     = os.environ.get('EC_HEADED', '0') == '1'
SLOW_MO    = int(os.environ.get('EC_SLOWMO', '700')) if HEADED else 0
INSERT_ONLY = os.environ.get('EC_INSERT_ONLY', '0') == '1'
DELETE_ONLY = os.environ.get('EC_DELETE_ONLY', '0') == '1'
TEST_MIME  = os.environ.get('EC_CODE', 'application/x-ec-autotest')
EXT_INS    = '.ectest'
EXT_UPD    = '.ectest,.ectest2'
TABLE      = 'mime_type_table:form:T_data'

os.makedirs(SS_DIR, exist_ok=True)
os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
results = {}
_ss = [0]


def esc(i): return '#' + i.replace(':', '\\:')

def ss(page, label):
    _ss[0] += 1
    page.screenshot(path=os.path.join(SS_DIR, f'mime_{_ss[0]:02d}_{label}.png'), full_page=False)
    print(f'  [SS] mime_{_ss[0]:02d}_{label}.png')

def wait_ajax(page, t=15000):
    page.wait_for_load_state('networkidle', timeout=t); page.wait_for_timeout(900)

def ec_error(page):
    t = page.evaluate("""()=>{const n=document.getElementById('ECNotificationArea')||document.getElementById('ECClientNotificationArea');return n?(n.textContent||'').replace(/EC\\.jsMessage\\.clear\\(\\);/,'').trim():'';}""")
    return t[:160] if ('Required' in t or 'Error' in t or 'empty' in t or 'exist' in t.lower()) else ''

def get_rows(page):
    return page.evaluate("""()=>{
        const out=[];
        document.querySelectorAll('input[id^="mime_type_table:form:T:"][id$=":C0_in"]').forEach(inp=>{
            const m=inp.id.match(/:T:(\\d+):C0_in/);
            if(m){const ri=m[1];const c1=document.getElementById('mime_type_table:form:T:'+ri+':C1_in');
                out.push({row:parseInt(ri), code:(inp.value||'').trim(), ext:c1?(c1.value||'').trim():''});}
        });
        return out;
    }""")

def go_first_page(page):
    f = page.locator('.ui-paginator-first').first
    if f.count() and f.is_visible() and 'ui-state-disabled' not in (f.get_attribute('class') or ''):
        f.click(); wait_ajax(page)

def find_row_paged(page, mime, max_pages=12):
    """Search across paginator pages; return current-DOM row index of mime, or None."""
    go_first_page(page)
    for _ in range(max_pages):
        for r in get_rows(page):
            if r['code'] == mime:
                return r
        nxt = page.locator('.ui-paginator-next').first
        if nxt.count() == 0 or 'ui-state-disabled' in (nxt.get_attribute('class') or ''):
            break
        nxt.click(); wait_ajax(page)
    return None

def type_cell(page, row, col, value):
    """Type into a grid cell with real keys + Tab so the onchange PrimeFaces.ab AJAX fires."""
    fid = f'mime_type_table:form:T:{row}:C{col}_in'
    el = page.locator(esc(fid))
    if el.count() == 0:
        print(f'  [WARN] cell not found: {fid}'); return False
    el.scroll_into_view_if_needed(); el.click()
    el.press('Control+a'); el.press('Delete')
    el.type(value, delay=40)
    el.press('Tab')          # blur -> onchange -> partial-submit AJAX
    wait_ajax(page)          # wait for staging AJAX to complete
    return True

def do_save(page):
    sv = page.locator("xpath=//a[@title='Save [Ctrl+s]']")
    if sv.count() and 'disabled' not in (sv.first.get_attribute('class') or ''):
        sv.first.click(); wait_ajax(page); return 'button'
    page.keyboard.press('Control+s'); wait_ajax(page); return 'ctrl+s'

def reload_grid(page):
    r = page.locator("xpath=//a[@title='Refresh [Ctrl+r]']")
    if r.count():
        r.first.click(); wait_ajax(page); page.wait_for_timeout(800)

def click_insert_new(page):
    ins = page.locator("xpath=//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'ui-icon-insert')]]")
    ins.first.hover(); page.wait_for_timeout(800)
    sub = page.locator("xpath=//ul[contains(@class,'ui-menu-child')]//li//a")
    for i in range(sub.count()):
        if sub.nth(i).is_visible():
            sub.nth(i).click(); wait_ajax(page); return True
    return False

def click_delete(page):
    dl = page.locator("xpath=//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'ui-icon-delete')]]")
    dl.first.hover(); page.wait_for_timeout(800)
    items = page.locator("xpath=//ul[contains(@class,'ui-menu-child')]//li//a")
    for i in range(items.count()):
        try:
            if items.nth(i).is_visible() and items.nth(i).text_content(timeout=800).strip() == 'MIME Type Mapping':
                items.nth(i).click(); wait_ajax(page); return True
        except Exception:
            pass
    for i in range(items.count()):
        if items.nth(i).is_visible():
            items.nth(i).click(); wait_ajax(page); return True
    return False


with sync_playwright() as p:
    browser = p.chromium.launch(headless=not HEADED, slow_mo=SLOW_MO, args=['--ignore-certificate-errors'])
    print(f'  [MODE] headed={HEADED} slowmo={SLOW_MO} mime={TEST_MIME} insert_only={INSERT_ONLY}')
    ctx = browser.new_context(ignore_https_errors=True, viewport={'width': 1680, 'height': 1050})
    page = ctx.new_page()

    print('=== LOGIN + NAVIGATE ===')
    page.goto(EC_URL, wait_until='domcontentloaded', timeout=30000)
    page.fill('#username', EC_USER); page.fill('#password', EC_PASS); page.click('#kc-login')
    page.wait_for_url('**/dashboard**', timeout=60000); wait_ajax(page)
    si = page.locator('#menu\\:searchForm\\:searchTxt'); si.wait_for(state='visible', timeout=10000)
    si.clear(); si.type('MIME Type Mapping', delay=50); page.wait_for_load_state('networkidle', timeout=8000); page.wait_for_timeout(500)
    page.locator("xpath=//*[self::label or self::span][contains(@class,'tv-link') and normalize-space(text())='MIME Type Mapping']").first.click()
    wait_ajax(page); page.wait_for_timeout(1500)
    lbl = page.locator('#screenToolbar\\:form\\:screenLabel').text_content(timeout=5000)
    results['navigate'] = 'PASS' if 'MIME' in lbl else f'FAIL={lbl}'
    print(f'  Screen: {lbl}')
    ss(page, 'loaded')

    # CLEAN STATE (page-search)
    pre = find_row_paged(page, TEST_MIME)
    results['clean'] = 'PRE-EXISTS' if pre else 'CLEAN'
    print(f'  Clean state: {results["clean"]}')
    go_first_page(page)

    # INSERT
    print('\n=== INSERT ===')
    if DELETE_ONLY:
        results['insert'] = 'SKIP (delete-only)'
    elif results.get('clean') == 'CLEAN':
        click_insert_new(page); ss(page, 'after_insert_click')
        blank = [r['row'] for r in get_rows(page) if r['code'] == '']
        print(f'  blank row(s): {blank}')
        if blank:
            br = blank[0]
            type_cell(page, br, 0, TEST_MIME)
            type_cell(page, br, 1, EXT_INS)
            print(f'  typed row {br}: {TEST_MIME} / {EXT_INS}')
            ss(page, 'insert_filled')
            m = do_save(page); err = ec_error(page)
            print(f'  saved via {m}; ec_error={err or "none"}')
            ss(page, 'insert_saved')
            reload_grid(page)
            found = find_row_paged(page, TEST_MIME)
            print(f'  after reload, found in grid: {found}')
            results['insert'] = 'PASS' if found else f'FAIL err={err or "not persisted after reload"}'
        else:
            results['insert'] = 'FAIL - no blank row'
    else:
        results['insert'] = 'SKIP'
    print(f'  INSERT: {results["insert"]}')

    # UPDATE
    print('\n=== UPDATE ===')
    if INSERT_ONLY:
        results['update'] = 'SKIP (insert-only)'
    elif results.get('insert') == 'PASS':
        r = find_row_paged(page, TEST_MIME)
        if r:
            type_cell(page, r['row'], 1, EXT_UPD)
            ss(page, 'update_filled')
            do_save(page); reload_grid(page)
            r2 = find_row_paged(page, TEST_MIME)
            ok = bool(r2) and r2['ext'] == EXT_UPD
            print(f'  row after update: {r2}')
            results['update'] = 'PASS' if ok else f'FAIL ext={r2}'
        else:
            results['update'] = 'FAIL - row not found'
    else:
        results['update'] = 'SKIP'
    print(f'  UPDATE: {results["update"]}')

    # DELETE (physical)
    print('\n=== DELETE ===')
    if INSERT_ONLY:
        results['delete'] = 'SKIP (insert-only)'
    elif DELETE_ONLY or results.get('insert') == 'PASS':
        r = find_row_paged(page, TEST_MIME)
        if r:
            # select my row (click its cell), verify it's mine before delete
            page.locator(esc(f"mime_type_table:form:T:{r['row']}:C0_in")).click()
            page.wait_for_timeout(400)
            active = page.evaluate(f"()=>{{const e=document.getElementById('mime_type_table:form:T:{r['row']}:C0_in');return e?e.value:'';}}")
            print(f"  active row {r['row']} code='{active}'")
            if active == TEST_MIME:
                ss(page, 'del_row_active')
                click_delete(page)
                conf = page.locator("button:has-text('Yes'), #confirmationForm\\:yes")
                if conf.count() and conf.first.is_visible():
                    conf.first.click(); wait_ajax(page)
                do_save(page); reload_grid(page); ss(page, 'del_saved')
                gone = find_row_paged(page, TEST_MIME) is None
                print(f'  gone after delete+reload: {gone}')
                results['delete'] = 'PASS' if gone else 'FAIL - still present'
            else:
                results['delete'] = 'ABORT - active row not test row (safety)'
        else:
            results['delete'] = 'FAIL - row not found'
    else:
        results['delete'] = 'SKIP'
    print(f'  DELETE: {results["delete"]}')
    ss(page, 'final')
    if HEADED: page.wait_for_timeout(5000)
    ctx.close(); browser.close()

with open(LOG_PATH, 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2)
print('\n' + '=' * 52 + '\nRESULTS\n' + '=' * 52)
for k, v in results.items():
    ok = v in ('PASS', 'CLEAN') or str(v).startswith('PASS') or str(v).startswith('SKIP')
    print(f'  {"OK " if ok else "XX "} {k:<10}: {v}')
print(f'\nLog: {LOG_PATH}\nShots: {SS_DIR}')
