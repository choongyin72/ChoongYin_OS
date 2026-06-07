"""
Phase 0d — crack the cascading navigator by driving each field as a DROPDOWN
(click chevron trigger -> pick from populated panel) with cascade waits.
Lists real option values at each step, then Go and find the result table id. READ-ONLY.
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


def open_and_pick(page, group, want):
    """Click the autocomplete dropdown trigger for nav group, list options, pick `want`."""
    dd = f'nav:form:{group}:R:1:C:0:dd'
    esc = dd.replace(':', '\\:')
    # the dropdown trigger button lives inside the dd span
    trigger = page.locator(f'#{esc} button, #{esc} .ui-autocomplete-dropdown')
    if trigger.count() == 0:
        print(f'  {group}: no dropdown trigger found'); return False
    trigger.first.click()
    page.wait_for_timeout(1200)
    # list visible panel options
    opts = page.evaluate("""() => {
        const out=[];
        document.querySelectorAll('.ui-autocomplete-panel').forEach(panel=>{
            if (panel.offsetParent === null) return;
            panel.querySelectorAll('li.ui-autocomplete-item').forEach(li=>{
                out.push((li.textContent||'').trim());
            });
        });
        return out;
    }""")
    print(f'  {group} options ({len(opts)}): {opts[:12]}')
    # pick exact match else contains
    item = page.locator("xpath=//div[contains(@class,'ui-autocomplete-panel')]//li[contains(@class,'ui-autocomplete-item') and normalize-space(.)="
                        f"'{want}']")
    if item.count() == 0:
        item = page.locator("xpath=//div[contains(@class,'ui-autocomplete-panel')]//li[contains(@class,'ui-autocomplete-item') and contains(normalize-space(.),"
                            f"'{want}')]")
    if item.count() > 0 and item.first.is_visible():
        picked = item.first.text_content().strip()
        item.first.click()
        page.wait_for_load_state('networkidle', timeout=12000); page.wait_for_timeout(900)
        got = page.evaluate(f"()=>{{const e=document.getElementById('{dd}_input');return e?e.value:'';}}")
        print(f'  {group} picked "{picked}" -> field="{got}"')
        return True
    print(f'  {group} "{want}" NOT in options')
    page.keyboard.press('Escape')
    return False


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
    print('Equipment loaded\n=== CASCADING NAVIGATOR (dropdown picks) ===')

    open_and_pick(page, 'G:1', 'Production Unit 1')
    open_and_pick(page, 'G:2', 'Offshore area')
    open_and_pick(page, 'G:3', 'Offshore facility')
    open_and_pick(page, 'G:4', 'Compressor')

    page.screenshot(path=os.path.join(SS_DIR, 'crack_01_filters.png'), full_page=True)
    print('\n=== GO ===')
    page.locator('#button\\:form\\:B').first.click()
    page.wait_for_load_state('networkidle', timeout=15000); page.wait_for_timeout(2000)
    page.screenshot(path=os.path.join(SS_DIR, 'crack_02_after_go.png'), full_page=True)

    # any error message?
    msg = page.evaluate("""()=>{const n=document.getElementById('ECNotificationArea');return n?(n.textContent||'').trim().substring(0,160):'';}""")
    print(f'Message: {msg or "(none)"}')

    # find ALL datatables + locate equipment rows
    info = page.evaluate("""() => {
        const tables=[];
        document.querySelectorAll('.ui-datatable').forEach(dt=>{
            const body=dt.querySelector('tbody[id$="_data"]');
            let n=0, first='';
            if(body){const trs=body.querySelectorAll('tr');trs.forEach(tr=>{if((tr.textContent||'').trim())n++;});first=trs.length?(trs[0].textContent||'').trim().substring(0,70):'';}
            tables.push({id:dt.id, body:body?body.id:'', rows:n, first});
        });
        const hits=[];
        document.querySelectorAll('span,td').forEach(e=>{
            const t=(e.textContent||'').trim();
            if((t.startsWith('OFF_')) && e.children.length===0)
                hits.push({txt:t.substring(0,30), tbody:e.closest('tbody')?e.closest('tbody').id:'', td_id:e.id||''});
        });
        return {tables, hits:hits.slice(0,5)};
    }""")
    print('\n=== DataTables after Go ===')
    for t in info['tables']:
        print(f'  id={t["id"]}  body={t["body"]}  rows={t["rows"]}  first="{t["first"]}"')
    print(f'\nEquipment-row hits: {info["hits"]}')

    ctx.close(); browser.close()
print('\nDone.', SS_DIR)
