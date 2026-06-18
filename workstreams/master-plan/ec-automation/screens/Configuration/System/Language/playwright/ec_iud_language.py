"""EC IUD — Language (Table class / TV). Playwright (Python).
Inline-editable paginated grid, no navigator, PHYSICAL delete (base T_BASIS_LANGUAGE).
Cells: table:form:T:{row}:C0_in (Id, auto) / C1_in (LANGUAGE code) / C2_in (NAME).
Commit cells with real keys + Tab (onchange->PrimeFaces.ab). NEVER touch existing rows.
Env: EC_HEADED, EC_SLOWMO, EC_CODE (default ZZ), EC_NAME, EC_INSERT_ONLY, EC_DELETE_ONLY."""
from playwright.sync_api import sync_playwright
from pathlib import Path
import os

def _repo_root():
    here = Path(__file__).resolve()
    for p in [here, *here.parents]:
        if (p / '.git').exists():
            return p
    return here.parents[3]

EC_URL = os.environ.get('EC_URL', 'https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/')
EC_USER = os.environ.get('EC_USER', 'sysadmin')   # R16: creds from env, never hardcoded
EC_PASS = os.environ.get('EC_PASS', 'sysadmin')
HEADED = os.environ.get('EC_HEADED', '0') == '1'
SLOWMO = int(os.environ.get('EC_SLOWMO', '0')) if HEADED else 0
CODE = os.environ.get('EC_CODE', 'ZZ')
NAME = os.environ.get('EC_NAME', 'Autotest Lang')
LANG_ID = os.environ.get('EC_ID', '999')  # Id/LANGUAGE_ID — required (yellow) field
INSERT_ONLY = os.environ.get('EC_INSERT_ONLY', '0') == '1'
DELETE_ONLY = os.environ.get('EC_DELETE_ONLY', '0') == '1'
SS = _repo_root() / 'docs' / 'EC' / 'screenshots' / 'iud_language'
SS.mkdir(parents=True, exist_ok=True)
GRID = 'table:form:T_data'


def shot(page, n):
    page.screenshot(path=str(SS / f'{n}.png'), full_page=True)


def wait_ajax(page):
    page.wait_for_load_state('networkidle', timeout=15000)


def cell(row, col):
    return f'table:form:T:{row}:C{col}_in'


def get_rows(page):
    """Return [(row_index, code)] from C1 cells on the current page."""
    return page.evaluate("""()=>{const o=[];document.querySelectorAll('input[id^="table:form:T:"][id$=":C1_in"]').forEach(i=>{const m=i.id.match(/:T:(\\d+):C1_in/);if(m)o.push([parseInt(m[1]),(i.value||'').trim()]);});return o;}""")


def find_row(page, code):
    # go to first page
    first = page.locator('.ui-paginator-first:not(.ui-state-disabled)')
    if first.count():
        first.first.click(); wait_ajax(page); page.wait_for_timeout(400)
    for _ in range(12):
        for ri, val in get_rows(page):
            if val == code:
                return ri
        nxt = page.locator('.ui-paginator-next:not(.ui-state-disabled)')
        if not nxt.count():
            return -1
        nxt.first.click(); wait_ajax(page); page.wait_for_timeout(400)
    return -1


def find_blank(page):
    for ri, val in get_rows(page):
        if val == '':
            return ri
    return -1


def type_cell(page, row, col, value):
    sel = f'#{cell(row, col).replace(":", chr(92) + ":")}'
    el = page.locator(f'[id="{cell(row, col)}"]')
    el.click(); el.press('Control+a'); el.press('Delete'); el.type(value, delay=40); el.press('Tab')
    wait_ajax(page); page.wait_for_timeout(500)


def cell_val(page, row, col):
    return page.locator(f'[id="{cell(row, col)}"]').input_value()


def save(page):
    page.locator("xpath=//a[@title='Save [Ctrl+s]']").first.click(); wait_ajax(page); page.wait_for_timeout(800)


def refresh(page):
    page.locator("xpath=//a[@title='Refresh [Ctrl+r]']").first.click(); wait_ajax(page); page.wait_for_timeout(900)


results = {}
with sync_playwright() as p:
    b = p.chromium.launch(headless=not HEADED, slow_mo=SLOWMO, args=['--ignore-certificate-errors'])
    ctx = b.new_context(ignore_https_errors=True, viewport={'width': 1680, 'height': 1050})
    page = ctx.new_page()
    page.goto(EC_URL, wait_until='domcontentloaded', timeout=30000)
    page.fill('#username', EC_USER); page.fill('#password', EC_PASS); page.click('#kc-login')
    page.wait_for_url('**/dashboard**', timeout=60000); wait_ajax(page)
    si = page.locator('#menu\\:searchForm\\:searchTxt'); si.wait_for(state='visible')
    si.clear(); si.type('Language', delay=50); page.wait_for_load_state('networkidle', timeout=8000); page.wait_for_timeout(600)
    page.locator("xpath=//*[self::label or self::span][contains(@class,'tv-link') and normalize-space(text())='Language']").first.click()
    wait_ajax(page); page.wait_for_timeout(1500)
    lbl = page.locator('#screenToolbar\\:form\\:screenLabel').text_content(timeout=5000)
    print(f'=== Screen: {lbl} | code={CODE} ===')
    results['navigate'] = 'PASS'
    shot(page, '01_loaded')

    pre = find_row(page, CODE)
    results['clean'] = 'CLEAN' if pre < 0 else 'PRE-EXISTS'
    print(f'clean state: {results["clean"]}')

    if not DELETE_ONLY:
        print('=== INSERT ===')
        ins = page.locator("xpath=//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'ui-icon-insert')]]")
        ins.first.hover(); page.wait_for_timeout(800)
        page.locator("xpath=(//ul[contains(@class,'ui-menu-child')]//li//a)[1]").first.click()
        wait_ajax(page); page.wait_for_timeout(1000)
        blank = find_blank(page)
        print(f'blank row: {blank}')
        type_cell(page, blank, 0, LANG_ID)   # Id — required (yellow) field
        type_cell(page, blank, 1, CODE)
        type_cell(page, blank, 2, NAME)
        shot(page, '02_insert_filled')
        save(page); refresh(page)
        row = find_row(page, CODE)
        results['insert'] = 'PASS' if row >= 0 else 'FAIL'
        print(f'insert: {results["insert"]} (row {row})')
        shot(page, '03_insert_saved')

    if not INSERT_ONLY and not DELETE_ONLY:
        print('=== UPDATE ===')
        row = find_row(page, CODE)
        type_cell(page, row, 2, NAME + ' UPD')
        save(page); refresh(page)
        row = find_row(page, CODE)
        val = cell_val(page, row, 2)
        results['update'] = 'PASS' if val == NAME + ' UPD' else f'FAIL ({val})'
        print(f'update: {results["update"]}')
        shot(page, '04_update_saved')

    if not INSERT_ONLY:
        print('=== DELETE (physical) ===')
        row = find_row(page, CODE)
        if row >= 0:
            page.locator(f'[id="{cell(row, 1)}"]').click(); page.wait_for_timeout(400)
            active = cell_val(page, row, 1)
            if active != CODE:
                results['delete'] = f'ABORT (active={active})'
            else:
                dele = page.locator("xpath=//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'ui-icon-delete')]]")
                dele.first.hover(); page.wait_for_timeout(800)
                page.locator("xpath=//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'ui-icon-delete')]]//ul[contains(@class,'ui-menu-child')]//a[normalize-space(.)='Language']").first.click()
                wait_ajax(page); page.wait_for_timeout(800)
                save(page); refresh(page)
                gone = find_row(page, CODE) < 0
                results['delete'] = 'PASS' if gone else 'FAIL'
                print(f'delete: {results["delete"]} (gone={gone})')
        else:
            results['delete'] = 'SKIP (not found)'
        shot(page, '05_final')

    ctx.close(); b.close()

print('\n==== RESULTS ====')
for k, v in results.items():
    print(f'  {k:<10}: {v}')
