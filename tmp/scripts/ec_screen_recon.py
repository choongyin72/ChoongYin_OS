"""
Generic READ-ONLY EC screen reconnaissance. Usage: py ec_screen_recon.py "Screen Name"
Dumps: screenlets, navigator, tables (headers/rows/cell-editability), toolbar.
Does NOT set unknown navigator values and NEVER saves. Pure observation.
"""
from playwright.sync_api import sync_playwright
from pathlib import Path
import os, sys


def _repo_root() -> Path:
    here = Path(__file__).resolve()
    for p in [here, *here.parents]:
        if (p / '.git').exists():
            return p
    return here.parents[3]


EC_URL = 'https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/'
SCREEN = sys.argv[1] if len(sys.argv) > 1 else 'Role Maintenance'
slug = SCREEN.lower().replace(' ', '_')
SS_DIR = str(_repo_root() / 'docs' / 'EC' / 'screenshots' / f'recon_{slug}')
os.makedirs(SS_DIR, exist_ok=True)


with sync_playwright() as p:
    b = p.chromium.launch(headless=True, args=['--ignore-certificate-errors'])
    ctx = b.new_context(ignore_https_errors=True, viewport={'width': 1920, 'height': 1080})
    page = ctx.new_page()
    page.goto(EC_URL, wait_until='domcontentloaded', timeout=30000)
    page.fill('#username', 'sysadmin'); page.fill('#password', 'sysadmin'); page.click('#kc-login')
    page.wait_for_url('**/dashboard**', timeout=60000); page.wait_for_load_state('networkidle', timeout=30000)
    si = page.locator('#menu\\:searchForm\\:searchTxt'); si.wait_for(state='visible')
    si.clear(); si.type(SCREEN, delay=50); page.wait_for_load_state('networkidle', timeout=8000); page.wait_for_timeout(600)
    matches = page.evaluate("""()=>{const o=[];document.querySelectorAll('#menu\\\\:searchForm\\\\:searchList .tv-link,#menu\\\\:searchForm\\\\:searchList label').forEach(l=>{if(l.offsetParent)o.push({t:(l.textContent||'').trim(),tip:l.getAttribute('data-tooltip')||''});});return o;}""")
    print(f'Search "{SCREEN}" matches:')
    for m in matches[:10]: print(f'  "{m["t"]}"  [{m["tip"]}]')

    link = page.locator(f"xpath=//*[self::label or self::span][contains(@class,'tv-link') and normalize-space(text())='{SCREEN}']")
    if link.count() == 0:
        print(f'No exact match for "{SCREEN}"'); ctx.close(); b.close(); raise SystemExit
    link.first.click(); page.wait_for_load_state('networkidle', timeout=15000); page.wait_for_timeout(1500)
    try: lbl = page.locator('#screenToolbar\\:form\\:screenLabel').text_content(timeout=5000)
    except Exception: lbl = '(none)'
    print(f'\nScreen label: {lbl}')
    page.screenshot(path=os.path.join(SS_DIR, 'recon_01.png'), full_page=True)

    print('\n=== Screenlets ===')
    for el in page.evaluate("""()=>{const o=[];document.querySelectorAll('[id]').forEach(e=>{if(e.offsetParent!==null&&(e.className||'').match(/screenlet/))o.push({id:e.id,cls:(e.className||'').substring(0,50)});});return o;}"""):
        print(f'  {el["id"]}  [{el["cls"]}]')

    print('\n=== Navigator (nav:form) ===')
    nav = page.evaluate("""()=>{const f=document.getElementById('nav:form');if(!f)return null;const labels=[];f.querySelectorAll('.ECLabelCell,label,legend').forEach(l=>{const t=(l.textContent||'').trim();if(t)labels.push(t.substring(0,28));});const inputs=[];f.querySelectorAll('input:not([type=hidden]),select').forEach(e=>{if(e.id&&e.offsetParent!==null)inputs.push(e.id);});return {labels,inputs};}""")
    print(f'  labels: {nav["labels"] if nav else "(no nav:form)"}')
    if nav:
        for i in nav['inputs']: print(f'    {i}')

    print('\n=== Tables / grids (initial, no filters set) ===')
    for t in page.evaluate("""()=>{const out=[];document.querySelectorAll('.ui-datatable,[class*="tableScreenlet"]').forEach(dt=>{const head=[];dt.querySelectorAll('thead th').forEach(th=>{const x=(th.textContent||'').trim();if(x)head.push(x.substring(0,20));});const body=dt.querySelector('tbody[id$="_data"]');let n=0;const cells=[];if(body){body.querySelectorAll('tr').forEach(tr=>{if((tr.textContent||'').trim())n++;});const r1=body.querySelector('tr');if(r1)r1.querySelectorAll('td').forEach(td=>{const inp=td.querySelector('input,select,textarea');cells.push(inp?'EDIT':'ro');});}out.push({id:dt.id,headers:head.slice(0,12),rows:n,cells:cells.slice(0,10)});});return out;}"""):
        print(f'  id={t["id"]} rows={t["rows"]}')
        if t['headers']: print(f'    headers: {t["headers"]}')
        if t['cells']: print(f'    cell-edit: {t["cells"]}')

    print('\n=== Toolbar ===')
    for it in page.evaluate("""()=>{const o=[];document.querySelectorAll('#screenToolbar\\\\:form\\\\:menuBar a').forEach(a=>{const i=a.querySelector('span[class*="ui-icon-"]');const ic=i?(i.className.match(/ui-icon-[a-z-]+/)||[''])[0]:'';o.push({title:(a.title||(a.textContent||'').trim()).substring(0,20),icon:ic,dis:a.classList.contains('ui-state-disabled')});});return o;}"""):
        print(f'  {it["title"]:<20} {it["icon"]:<18} disabled={it["dis"]}')

    ctx.close(); b.close()
print('\nRead-only recon complete.', SS_DIR)
