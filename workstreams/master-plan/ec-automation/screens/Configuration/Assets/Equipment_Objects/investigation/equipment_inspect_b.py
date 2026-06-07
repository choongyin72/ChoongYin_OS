"""
Phase 0b — drive the Equipment cascading navigator, then capture LABELED field maps.
READ-ONLY (no save). Learns: how to set the 5 autocomplete filters, the labeled
objectForm / updateAttributes / objectdates fields, and the - delete button behaviour.
"""
from playwright.sync_api import sync_playwright
from pathlib import Path
import os


def _repo_root() -> Path:
    env = os.environ.get('REPO_ROOT')
    if env:
        return Path(env)
    here = Path(__file__).resolve()
    for parent in [here, *here.parents]:
        if (parent / '.git').exists():
            return parent
    return here.parents[5]


EC_URL = os.environ.get('EC_URL', 'https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/')
SS_DIR = str(_repo_root() / 'docs' / 'EC' / 'screenshots' / 'iud_equipment')
os.makedirs(SS_DIR, exist_ok=True)

# Navigator filter values (per screenshot)
NAV = [
    ('G:1', 'Production Unit'),
    ('G:2', 'Offshore area'),
    ('G:3', 'Offshore facility'),
    ('G:4', 'Compressor'),
]


def labeled_fields(page, form_id):
    """Map each visible field to its EC label (label cell is C:0:la, field is C:1)."""
    return page.evaluate("""(formId) => {
        const root = document.getElementById(formId) || document.querySelector('[id^="'+formId+'"]');
        if (!root) return {found:false};
        const out = [];
        root.querySelectorAll('input:not([type=hidden]),textarea,select').forEach(e => {
            if (!e.id || e.offsetParent === null) return;
            if (e.id.includes('statusarea')) return;
            // label: replace :C:1:... segment with :C:0:la
            let labelId = e.id.replace(/:C:1:[a-z_]+$/, ':C:0:la');
            const labelEl = document.getElementById(labelId);
            const label = labelEl ? (labelEl.textContent||'').trim() : '';
            out.push({
                id: e.id, type: e.type||e.tagName, label: label.substring(0,40),
                readonly: e.readOnly, val: (e.value||'').substring(0,30),
                mandatory: (e.closest('[class*="mandatory:true"]')!==null) ||
                           (labelEl && /mandatory:true/.test(labelEl.className))
            });
        });
        return {found:true, fields: out};
    }""", form_id)


def set_autocomplete(page, group, value):
    """Set an EC autocomplete-dd navigator field. Try dropdown-button, else type+pick."""
    base = f'nav:form:{group}:R:1:C:0:dd'
    inp = f'{base}_input'
    sel_input = f'#{inp.replace(":", "\\:")}'
    # Strategy 1: click the dropdown trigger button to open full list
    btn = page.locator(f'#{base.replace(":", "\\:")}_btn, [id="{base}_btn"]')
    el = page.locator(sel_input)
    if el.count() == 0:
        print(f'    {group}: input not found ({inp})'); return False
    el.scroll_into_view_if_needed()
    el.click()
    el.fill('')
    el.type(value, delay=60)
    page.wait_for_timeout(1200)
    # pick matching suggestion from any visible autocomplete panel
    item = page.locator("xpath=//ul[contains(@class,'ui-autocomplete-items')]//li[normalize-space(.)="
                        f"'{value}']")
    if item.count() == 0:
        item = page.locator("xpath=//li[contains(@class,'ui-autocomplete-item') and normalize-space(.)="
                            f"'{value}']")
    if item.count() > 0 and item.first.is_visible():
        item.first.click()
        page.wait_for_load_state('networkidle', timeout=10000)
        page.wait_for_timeout(800)
        print(f'    {group} = "{value}"  (picked suggestion)')
        return True
    # fallback: press Enter/Down+Enter
    el.press('ArrowDown'); page.wait_for_timeout(400); el.press('Enter')
    page.wait_for_load_state('networkidle', timeout=10000)
    page.wait_for_timeout(800)
    got = page.evaluate(f"() => {{const e=document.getElementById('{inp}'); return e? e.value : '';}}")
    print(f'    {group} target "{value}" -> field now "{got}"')
    return value.lower() in (got or '').lower()


with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=['--ignore-certificate-errors'])
    ctx = browser.new_context(ignore_https_errors=True, viewport={'width': 1920, 'height': 1080})
    page = ctx.new_page()

    # login + navigate
    page.goto(EC_URL, wait_until='domcontentloaded', timeout=30000)
    page.fill('#username', 'sysadmin'); page.fill('#password', 'sysadmin')
    page.click('#kc-login')
    page.wait_for_url('**/dashboard**', timeout=60000)
    page.wait_for_load_state('networkidle', timeout=30000)
    si = page.locator('#menu\\:searchForm\\:searchTxt')
    si.wait_for(state='visible'); si.clear(); si.type('Equipment', delay=60)
    page.wait_for_load_state('networkidle', timeout=8000); page.wait_for_timeout(500)
    page.locator("xpath=//*[self::label or self::span][contains(@class,'tv-link') and normalize-space(text())='Equipment']").first.click()
    page.wait_for_load_state('networkidle', timeout=15000); page.wait_for_timeout(1500)
    print('Equipment loaded')

    # capture one autocomplete's HTML to learn structure
    ac_html = page.evaluate("""() => {
        const dd = document.getElementById('nav:form:G:1:R:1:C:0:dd');
        return dd ? dd.outerHTML.substring(0,600) : 'not found';
    }""")
    print(f'\n=== Autocomplete G:1 HTML ===\n{ac_html}\n')

    # set the 4 cascading filters in order
    print('=== SET NAVIGATOR (cascading) ===')
    for group, value in NAV:
        set_autocomplete(page, group, value)
    page.screenshot(path=os.path.join(SS_DIR, 'scanb_01_filters_set.png'), full_page=True)

    # Go
    print('\n=== GO ===')
    page.locator('#button\\:form\\:B').first.click()
    page.wait_for_load_state('networkidle', timeout=15000); page.wait_for_timeout(1500)
    page.screenshot(path=os.path.join(SS_DIR, 'scanb_02_after_go.png'), full_page=True)

    # table
    rows = page.evaluate("""() => {
        const tb = document.getElementById('manage_object_nav_nav:form:T_data');
        if(!tb) return {found:false};
        const out=[]; tb.querySelectorAll('tr').forEach(tr=>{const c=[];tr.querySelectorAll('td').forEach(td=>c.push((td.textContent||'').trim()));if(c.some(x=>x))out.push(c);});
        return {found:true, rows:out};
    }""")
    print(f'\n=== TABLE ===\n  found={rows.get("found")}, rows={rows.get("rows")}')

    # row select (existing, read-only) → updateAttributes + objectdates labeled
    if rows.get('found') and rows.get('rows'):
        first_span = page.locator("css=#manage_object_nav_nav\\:form\\:T_data span").first
        first_span.click()
        page.wait_for_load_state('networkidle', timeout=15000); page.wait_for_timeout(1500)
        page.screenshot(path=os.path.join(SS_DIR, 'scanb_03_row_selected.png'), full_page=True)
        for fid in ['tab:tabPanel:updateAttributes:form', 'tab:tabPanel:objectdates:form']:
            d = labeled_fields(page, fid)
            print(f'\n=== {fid} (labeled) ===')
            if d.get('found'):
                for f in d['fields']:
                    print(f'  {f["label"]:<28} -> {f["id"]}  [{f["type"]}] ro={f["readonly"]} val="{f["val"]}"')
        # delete button state after selection
        delbtn = page.evaluate("""() => {
            const out=[];
            document.querySelectorAll('#screenToolbar\\\\:form\\\\:menuBar a').forEach(a=>{
                const i=a.querySelector('span[class*="ui-icon-"]');
                const ic=i?(i.className.match(/ui-icon-[a-z-]+/)||[''])[0]:'';
                if(ic.includes('delete')||ic.includes('trash'))
                    out.push({icon:ic, disabled:a.classList.contains('ui-state-disabled'),
                              li:a.closest('li')?a.closest('li').className:'', onclick:(a.getAttribute('onclick')||'').substring(0,120)});
            });
            return out;
        }""")
        print(f'\n=== DELETE BUTTON after row-select ===\n  {delbtn}')

    # Insert → New Object → objectForm labeled
    print('\n=== INSERT → New Object → objectForm (labeled) ===')
    insert_li = page.locator("xpath=//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'ui-icon-insert')]]")
    insert_li.first.hover(); page.wait_for_timeout(900)
    sub = page.locator("xpath=//ul[contains(@class,'ui-menu-child')]//li//a")
    for i in range(sub.count()):
        if sub.nth(i).is_visible():
            sub.nth(i).click(); break
    page.wait_for_load_state('networkidle', timeout=15000); page.wait_for_timeout(1500)
    page.screenshot(path=os.path.join(SS_DIR, 'scanb_04_new_object.png'), full_page=True)
    d = labeled_fields(page, 'tab:tabPanel:objectForm:form')
    if d.get('found'):
        for f in d['fields']:
            print(f'  {f["label"]:<28} -> {f["id"]}  [{f["type"]}] ro={f["readonly"]} val="{f["val"]}"')

    ctx.close(); browser.close()
print('\nPhase 0b complete. Screenshots:', SS_DIR)
