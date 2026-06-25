"""
Phase 0c - find the real Equipment result-table element id + the working filter combo.
READ-ONLY.
"""
from playwright.sync_api import sync_playwright
from pathlib import Path
import os


def _repo_root() -> Path:
    here = Path(__file__).resolve()
    for parent in [here, *here.parents]:
        if (parent / '.git').exists():
            return parent
    return here.parents[5]


EC_URL = os.environ.get('EC_URL', 'https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/')
SS_DIR = str(_repo_root() / 'docs' / 'EC' / 'screenshots' / 'iud_equipment')
os.makedirs(SS_DIR, exist_ok=True)


def set_ac(page, group, value):
    inp = f'nav:form:{group}:R:1:C:0:dd_input'
    el = page.locator(f'#{inp.replace(":", "\\:")}')
    if el.count() == 0:
        return
    el.scroll_into_view_if_needed(); el.click(); el.fill(''); el.type(value, delay=60)
    page.wait_for_timeout(1000)
    item = page.locator("xpath=//li[contains(@class,'ui-autocomplete-item') and normalize-space(.)="
                        f"'{value}']")
    if item.count() > 0 and item.first.is_visible():
        item.first.click()
    else:
        el.press('ArrowDown'); page.wait_for_timeout(300); el.press('Enter')
    page.wait_for_load_state('networkidle', timeout=10000); page.wait_for_timeout(700)
    got = page.evaluate(f"()=>{{const e=document.getElementById('{inp}');return e?e.value:'';}}")
    print(f'    {group} target "{value}" -> "{got}"')


def dump_tables(page, tag):
    info = page.evaluate("""() => {
        const out = [];
        document.querySelectorAll('.ui-datatable').forEach(dt => {
            const body = dt.querySelector('tbody[id$="_data"]');
            let nrows = 0, first = '';
            if (body) {
                const trs = body.querySelectorAll('tr');
                trs.forEach(tr => { if ((tr.textContent||'').trim()) nrows++; });
                first = trs.length ? (trs[0].textContent||'').trim().substring(0,60) : '';
            }
            out.push({id: dt.id, bodyId: body?body.id:'(none)', nrows, first});
        });
        // also: locate any element containing the known existing equipment code
        const hit = [];
        document.querySelectorAll('span,td,div').forEach(e => {
            if ((e.textContent||'').trim().startsWith('OFF_FLASH_GAS') && e.children.length===0)
                hit.push({id:e.id||'(no id)', tag:e.tagName, closestTbody: e.closest('tbody')?e.closest('tbody').id:''});
        });
        return {tables: out, offHits: hit.slice(0,3)};
    }""")
    print(f'\n  [{tag}] DataTables:')
    for t in info['tables']:
        print(f'    id={t["id"]}  body={t["bodyId"]}  rows={t["nrows"]}  first="{t["first"]}"')
    print(f'  [{tag}] OFF_FLASH_GAS hits: {info["offHits"]}')
    return info


with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=['--ignore-certificate-errors'])
    ctx = browser.new_context(ignore_https_errors=True, viewport={'width': 1920, 'height': 1080})
    page = ctx.new_page()
    page.goto(EC_URL, wait_until='domcontentloaded', timeout=30000)
    page.fill('#username', 'sysadmin'); page.fill('#password', 'sysadmin'); page.click('#kc-login')
    page.wait_for_url('**/dashboard**', timeout=60000); page.wait_for_load_state('networkidle', timeout=30000)
    si = page.locator('#menu\\:searchForm\\:searchTxt'); si.wait_for(state='visible')
    si.clear(); si.type('Equipment', delay=60); page.wait_for_load_state('networkidle', timeout=8000); page.wait_for_timeout(500)
    page.locator("xpath=//*[self::label or self::span][contains(@class,'tv-link') and normalize-space(text())='Equipment']").first.click()
    page.wait_for_load_state('networkidle', timeout=15000); page.wait_for_timeout(1500)
    print('Equipment loaded')

    # List Production Unit options (open its dropdown panel)
    print('\n=== Production Unit (G:1) options ===')
    pu = page.locator('#nav\\:form\\:G\\:1\\:R\\:1\\:C\\:0\\:dd_input')
    pu.click(); pu.press('ArrowDown'); page.wait_for_timeout(1000)
    opts = page.evaluate("""() => {
        const out=[]; document.querySelectorAll('.ui-autocomplete-panel:not([style*="display: none"]) li.ui-autocomplete-item').forEach(li=>{
            if(li.offsetParent) out.push((li.textContent||'').trim());
        });
        return out;
    }""")
    print(f'  options: {opts}')
    page.keyboard.press('Escape')

    # ATTEMPT 1: only Area + Facility Class 1 + Equipment Type (leave Production Unit unset)
    print('\n=== ATTEMPT 1: Area + Facility Class 1 + Equipment Type (no PU) ===')
    set_ac(page, 'G:2', 'Offshore area')
    set_ac(page, 'G:3', 'Offshore facility')
    set_ac(page, 'G:4', 'Compressor')
    page.locator('#button\\:form\\:B').first.click()
    page.wait_for_load_state('networkidle', timeout=15000); page.wait_for_timeout(1500)
    page.screenshot(path=os.path.join(SS_DIR, 'find_01_no_pu.png'), full_page=True)
    info1 = dump_tables(page, 'no-PU')

    # ATTEMPT 2: also set Production Unit (first option) then Go
    print('\n=== ATTEMPT 2: + Production Unit (first option) ===')
    if opts:
        set_ac(page, 'G:1', opts[0])
        set_ac(page, 'G:2', 'Offshore area')
        set_ac(page, 'G:3', 'Offshore facility')
        set_ac(page, 'G:4', 'Compressor')
        page.locator('#button\\:form\\:B').first.click()
        page.wait_for_load_state('networkidle', timeout=15000); page.wait_for_timeout(1500)
        page.screenshot(path=os.path.join(SS_DIR, 'find_02_with_pu.png'), full_page=True)
        dump_tables(page, 'with-PU')

    ctx.close(); browser.close()
print('\nDone.', SS_DIR)
