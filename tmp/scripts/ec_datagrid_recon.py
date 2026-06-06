"""
READ-ONLY reconnaissance of a data-grid ("TV") screen: Daily Equipment Status.
Goal: learn the data-grid pattern (navigator, grid structure, inline-edit cells, columns)
WITHOUT entering or saving any data. Pure observation. NEVER touches data.
"""
from playwright.sync_api import sync_playwright
from pathlib import Path
import os


def _repo_root() -> Path:
    here = Path(__file__).resolve()
    for p in [here, *here.parents]:
        if (p / '.git').exists():
            return p
    return here.parents[3]


EC_URL = 'https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/'
SS_DIR = str(_repo_root() / 'docs' / 'EC' / 'screenshots' / 'recon_datagrid')
os.makedirs(SS_DIR, exist_ok=True)
SCREEN = 'Daily Equipment Status'


with sync_playwright() as p:
    b = p.chromium.launch(headless=True, args=['--ignore-certificate-errors'])
    ctx = b.new_context(ignore_https_errors=True, viewport={'width': 1920, 'height': 1080})
    page = ctx.new_page()
    page.goto(EC_URL, wait_until='domcontentloaded', timeout=30000)
    page.fill('#username', 'sysadmin'); page.fill('#password', 'sysadmin'); page.click('#kc-login')
    page.wait_for_url('**/dashboard**', timeout=60000); page.wait_for_load_state('networkidle', timeout=30000)
    si = page.locator('#menu\\:searchForm\\:searchTxt'); si.wait_for(state='visible')
    si.clear(); si.type(SCREEN, delay=50); page.wait_for_load_state('networkidle', timeout=8000); page.wait_for_timeout(600)
    # open exact match
    link = page.locator(f"xpath=//*[self::label or self::span][contains(@class,'tv-link') and normalize-space(text())='{SCREEN}']")
    print(f'Search matches for "{SCREEN}": {link.count()}')
    link.first.click()
    page.wait_for_load_state('networkidle', timeout=15000); page.wait_for_timeout(1500)
    try:
        lbl = page.locator('#screenToolbar\\:form\\:screenLabel').text_content(timeout=5000)
    except Exception:
        lbl = '(none)'
    print(f'Screen label: {lbl}')
    page.screenshot(path=os.path.join(SS_DIR, 'dg_01_loaded.png'), full_page=True)

    # screenlets / top-level forms
    print('\n=== Screenlets / forms / buttons ===')
    ids = page.evaluate("""()=>{const o=[];document.querySelectorAll('[id]').forEach(e=>{
        if(e.offsetParent!==null && (e.className||'').match(/screenlet|goButton|ECMenuBar/)) o.push({id:e.id,cls:(e.className||'').substring(0,45)});});return o;}""")
    for el in ids: print(f'  {el["id"]}  [{el["cls"]}]')

    # navigator structure
    print('\n=== Navigator (nav:form) ===')
    nav = page.evaluate("""()=>{const f=document.getElementById('nav:form');if(!f)return null;
        const labels=[];f.querySelectorAll('.ECLabelCell,label,legend').forEach(l=>{const t=(l.textContent||'').trim();if(t)labels.push(t.substring(0,30));});
        const inputs=[];f.querySelectorAll('input:not([type=hidden]),select').forEach(e=>{if(e.id&&e.offsetParent!==null)inputs.push({id:e.id,type:e.type||e.tagName,val:(e.value||'').substring(0,20)});});
        return {labels,inputs};}""")
    if nav:
        print(f'  labels: {nav["labels"]}')
        for i in nav['inputs']: print(f'    {i["id"]} [{i["type"]}] val="{i["val"]}"')
    else:
        print('  no nav:form')

    # set cascading navigator (read-only: loading data does not modify it)
    def set_nav(group, want):
        btn = f'nav:form:{group}:R:1:C:0:dd_button'
        panel = f'nav:form:{group}:R:1:C:0:dd_panel'
        t = page.locator('#' + btn.replace(':', '\\:'))
        if t.count() == 0:
            print(f'  {group}: no dropdown'); return
        t.first.click(); page.wait_for_timeout(900)
        opt = page.locator('#' + panel.replace(':', '\\:')).get_by_text(want, exact=True)
        if opt.count() == 0:
            opt = page.locator('#' + panel.replace(':', '\\:')).get_by_text(want)
        if opt.count() > 0:
            opt.first.click(); page.wait_for_load_state('networkidle', timeout=12000); page.wait_for_timeout(800)
            print(f'  nav {group} = "{want}"')

    print('\n  Setting navigator (Production Unit / Offshore area / Offshore facility) ...')
    set_nav('G:1', 'Production Unit'); set_nav('G:2', 'Offshore area'); set_nav('G:3', 'Offshore facility')
    go = page.locator('#button\\:form\\:B')
    if go.count() > 0 and go.first.is_visible():
        print('  Go -> load grid (read-only)')
        go.first.click(); page.wait_for_load_state('networkidle', timeout=15000); page.wait_for_timeout(1800)
        page.screenshot(path=os.path.join(SS_DIR, 'dg_02_after_go.png'), full_page=True)

    # the grid: equipment_status:form table (capture headers, rows, cell editability)
    print('\n=== GRID (equipment_status:form) ===')
    grid = page.evaluate("""()=>{
        const root=document.getElementById('equipment_status:form');if(!root)return null;
        // headers
        const head=[];root.querySelectorAll('thead th').forEach(th=>{const t=(th.textContent||'').trim();if(t)head.push(t.substring(0,24));});
        // body rows
        const body=root.querySelector('tbody[id$="_data"]');
        let nrows=0; const sampleCells=[];
        if(body){const trs=body.querySelectorAll('tr');trs.forEach(tr=>{if((tr.textContent||'').trim())nrows++;});
            const r1=trs[0];
            if(r1)r1.querySelectorAll('td').forEach(td=>{const inp=td.querySelector('input,select,textarea');
                sampleCells.push({id:(inp&&inp.id)||td.id||'', edit:inp?('EDIT:'+(inp.type||inp.tagName)):'readonly', val:(td.textContent||'').trim().substring(0,16)});});}
        return {bodyId:body?body.id:'', headers:head, rows:nrows, sampleCells:sampleCells.slice(0,14)};
    }""")
    if grid:
        print(f'  body id: {grid["bodyId"]}')
        print(f'  headers ({len(grid["headers"])}): {grid["headers"]}')
        print(f'  rows: {grid["rows"]}')
        print(f'  row-1 cells (edit type / id / value):')
        for c in grid['sampleCells']:
            print(f'    {c["edit"]:<14} {c["id"]:<45} "{c["val"]}"')
    else:
        print('  equipment_status:form not found')

    # toolbar buttons
    print('\n=== Toolbar ===')
    tb = page.evaluate("""()=>{const o=[];document.querySelectorAll('#screenToolbar\\\\:form\\\\:menuBar a').forEach(a=>{const i=a.querySelector('span[class*="ui-icon-"]');const ic=i?(i.className.match(/ui-icon-[a-z-]+/)||[''])[0]:'';o.push({title:(a.title||(a.textContent||'').trim()).substring(0,22),icon:ic,disabled:a.classList.contains('ui-state-disabled')});});return o;}""")
    for it in tb: print(f'  {it["title"]:<22} {it["icon"]:<18} disabled={it["disabled"]}')

    ctx.close(); b.close()
print('\nRecon complete (READ-ONLY — no data touched).', SS_DIR)
