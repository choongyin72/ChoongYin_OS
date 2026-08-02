"""
Phase 0e - robust cascading-navigator setter with per-field verify + diagnostics.
Type -> wait for suggestions -> click exact suggestion -> wait cascade -> verify stuck.
Then Go and locate the result table. READ-ONLY.
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


def field_val(page, group):
    inp = f'nav:form:{group}:R:1:C:0:dd_input'
    return page.evaluate(f"()=>{{const e=document.getElementById('{inp}');return e?e.value:'';}}")


def list_suggestions(page):
    return page.evaluate("""() => {
        const out=[];
        document.querySelectorAll('.ui-autocomplete-panel').forEach(p=>{
            if(p.offsetParent===null) return;
            p.querySelectorAll('li.ui-autocomplete-item').forEach(li=>out.push((li.textContent||'').trim()));
        });
        return out;
    }""")


def set_field(page, group, want, retries=2):
    inp = f'nav:form:{group}:R:1:C:0:dd_input'
    sel = f'#{inp.replace(":", "\\:")}'
    for attempt in range(1, retries + 1):
        el = page.locator(sel)
        el.scroll_into_view_if_needed()
        el.click()
        el.fill('')
        # type a prefix to trigger suggestions (use first word to be safe)
        el.type(want, delay=70)
        page.wait_for_timeout(1800)
        sugg = list_suggestions(page)
        print(f'  {group} attempt{attempt} typed "{want}" -> suggestions: {sugg[:10]}')
        if sugg:
            item = page.locator("xpath=//div[contains(@class,'ui-autocomplete-panel')]//li[contains(@class,'ui-autocomplete-item') and normalize-space(.)="
                                f"'{want}']")
            if item.count() == 0:
                item = page.locator("xpath=//div[contains(@class,'ui-autocomplete-panel')]//li[contains(@class,'ui-autocomplete-item')][1]")
            if item.count() > 0 and item.first.is_visible():
                item.first.click()
                page.wait_for_load_state('networkidle', timeout=12000)
                page.wait_for_timeout(1000)
                got = field_val(page, group)
                print(f'  {group} -> committed "{got}"')
                if got.strip():
                    return got
        else:
            # no suggestions yet (cascade not ready) - wait and retry
            page.keyboard.press('Escape')
            page.wait_for_timeout(1200)
    print(f'  {group} FAILED to set "{want}"')
    return ''


with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=['--ignore-certificate-errors'])
    ctx = browser.new_context(ignore_https_errors=True, viewport={'width': 1920, 'height': 1080})
    page = ctx.new_page()
    page.goto(EC_URL, wait_until='domcontentloaded', timeout=30000)
    page.fill('#username', os.environ.get("EC_USER", "sysadmin")); page.fill('#password', os.environ.get("EC_PASS", "sysadmin")); page.click('#kc-login')
    page.wait_for_url('**/dashboard**', timeout=60000); page.wait_for_load_state('networkidle', timeout=30000)
    si = page.locator('#menu\\:searchForm\\:searchTxt'); si.wait_for(state='visible')
    si.clear(); si.type('Equipment', delay=60); page.wait_for_load_state('networkidle', timeout=8000); page.wait_for_timeout(500)
    page.locator("xpath=//*[self::label or self::span][contains(@class,'tv-link') and normalize-space(text())='Equipment']").first.click()
    page.wait_for_load_state('networkidle', timeout=15000); page.wait_for_timeout(1500)
    print('Equipment loaded\n=== SET NAVIGATOR (robust, in cascade order) ===')

    set_field(page, 'G:1', 'Production Unit 1')
    set_field(page, 'G:2', 'Offshore area')
    set_field(page, 'G:3', 'Offshore facility')
    set_field(page, 'G:4', 'Compressor')

    # re-read ALL after setting (did any get cleared by cascade?)
    print('\n=== FINAL navigator values ===')
    for g, name in [('G:1','Production Unit'),('G:2','Area'),('G:3','Facility Class 1'),('G:4','Equipment Type')]:
        print(f'  {name:<18} = "{field_val(page, g)}"')
    page.screenshot(path=os.path.join(SS_DIR, 'robust_01_filters.png'), full_page=True)

    print('\n=== GO ===')
    page.locator('#button\\:form\\:B').first.click()
    page.wait_for_load_state('networkidle', timeout=15000); page.wait_for_timeout(2000)
    page.screenshot(path=os.path.join(SS_DIR, 'robust_02_after_go.png'), full_page=True)
    msg = page.evaluate("""()=>{const n=document.getElementById('ECNotificationArea');return n?(n.textContent||'').replace(/EC\\.jsMessage\\.clear\\(\\);/,'').trim().substring(0,160):'';}""")
    print(f'Message: {msg or "(none)"}')

    info = page.evaluate("""() => {
        const tables=[];
        document.querySelectorAll('.ui-datatable').forEach(dt=>{
            const body=dt.querySelector('tbody[id$="_data"]'); let n=0,first='';
            if(body){const trs=body.querySelectorAll('tr');trs.forEach(tr=>{if((tr.textContent||'').trim())n++;});first=trs.length?(trs[0].textContent||'').trim().substring(0,70):'';}
            tables.push({id:dt.id, body:body?body.id:'', rows:n, first});
        });
        const hits=[];
        document.querySelectorAll('span,td').forEach(e=>{const t=(e.textContent||'').trim();
            if(t.startsWith('OFF_')&&e.children.length===0) hits.push({txt:t.substring(0,28), tbody:e.closest('tbody')?e.closest('tbody').id:''});});
        return {tables, hits:hits.slice(0,5)};
    }""")
    print('\n=== DataTables after Go ===')
    for t in info['tables']:
        print(f'  id={t["id"]}  body={t["body"]}  rows={t["rows"]}  first="{t["first"]}"')
    print(f'Equipment-row hits: {info["hits"]}')

    ctx.close(); browser.close()
print('\nDone.', SS_DIR)
