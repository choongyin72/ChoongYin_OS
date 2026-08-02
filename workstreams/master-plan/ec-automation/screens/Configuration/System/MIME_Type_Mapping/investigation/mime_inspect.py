"""
Phase scan - DOM deep-dive of MIME Type Mapping (READ-ONLY, never saves).
Captures: grid structure + existing rows, cell input IDs, toolbar, Insert submenu,
and the new-row cell IDs after clicking Insert (no Save, so no data change).
"""
from playwright.sync_api import sync_playwright
from pathlib import Path
import os


def _repo_root() -> Path:
    here = Path(__file__).resolve()
    for p in [here, *here.parents]:
        if (p / '.git').exists():
            return p
    return here.parents[5]


EC_URL = os.environ.get('EC_URL', 'https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/')
SS_DIR = str(_repo_root() / 'docs' / 'EC' / 'screenshots' / 'iud_mime')
os.makedirs(SS_DIR, exist_ok=True)
TABLE = 'mime_type_table:form:T_data'


def esc(i): return '#' + i.replace(':', '\\:')


with sync_playwright() as p:
    b = p.chromium.launch(headless=True, args=['--ignore-certificate-errors'])
    ctx = b.new_context(ignore_https_errors=True, viewport={'width': 1680, 'height': 1050})
    page = ctx.new_page()
    page.goto(EC_URL, wait_until='domcontentloaded', timeout=30000)
    page.fill('#username', os.environ.get("EC_USER", "sysadmin")); page.fill('#password', os.environ.get("EC_PASS", "sysadmin")); page.click('#kc-login')
    page.wait_for_url('**/dashboard**', timeout=60000); page.wait_for_load_state('networkidle', timeout=30000)
    si = page.locator('#menu\\:searchForm\\:searchTxt'); si.wait_for(state='visible')
    si.clear(); si.type('MIME Type Mapping', delay=50); page.wait_for_load_state('networkidle', timeout=8000); page.wait_for_timeout(600)
    page.locator("xpath=//*[self::label or self::span][contains(@class,'tv-link') and normalize-space(text())='MIME Type Mapping']").first.click()
    page.wait_for_load_state('networkidle', timeout=15000); page.wait_for_timeout(2000)
    lbl = page.locator('#screenToolbar\\:form\\:screenLabel').text_content(timeout=5000)
    print(f'Screen: {lbl}')
    page.screenshot(path=os.path.join(SS_DIR, 'scan_01_loaded.png'), full_page=True)

    # existing rows + cell structure
    grid = page.evaluate(f"""()=>{{
        const tb=document.getElementById('{TABLE}'); if(!tb) return {{found:false}};
        const rows=[]; const cellIds=[];
        tb.querySelectorAll('tr').forEach((tr,ri)=>{{
            const cells=[]; tr.querySelectorAll('td').forEach(td=>{{
                const inp=td.querySelector('input,select,textarea');
                cells.push({{txt:(td.textContent||'').trim().substring(0,30), inpId:(inp&&inp.id)||'', type:inp?(inp.type||inp.tagName):'ro'}});
            }});
            if(cells.length) rows.push(cells);
        }});
        return {{found:true, rowCount:rows.length, rows:rows.slice(0,8)}};
    }}""")
    print(f'\n=== EXISTING GRID ({TABLE}) ===')
    print(f'  found={grid.get("found")} rowCount={grid.get("rowCount")}')
    for r in grid.get('rows', []):
        print(f'    {r}')

    # toolbar
    print('\n=== TOOLBAR ===')
    for it in page.evaluate("""()=>{const o=[];document.querySelectorAll('#screenToolbar\\\\:form\\\\:menuBar a').forEach(a=>{const i=a.querySelector('span[class*="ui-icon-"]');const ic=i?(i.className.match(/ui-icon-[a-z-]+/)||[''])[0]:'';o.push({title:(a.title||(a.textContent||'').trim()).substring(0,24),icon:ic,dis:a.classList.contains('ui-state-disabled'),li:a.closest('li')?a.closest('li').className.substring(0,40):''});});return o;}"""):
        print(f'  {it["title"]:<24} {it["icon"]:<16} disabled={it["dis"]}  li={it["li"]}')

    # hover Insert, capture submenu
    print('\n=== INSERT submenu ===')
    ins = page.locator("xpath=//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'ui-icon-insert')]]")
    if ins.count() > 0:
        ins.first.hover(); page.wait_for_timeout(900)
        items = page.evaluate("""()=>{const o=[];document.querySelectorAll('.ui-menu-child a').forEach(a=>{if(a.offsetParent)o.push((a.textContent||'').trim());});return o;}""")
        print(f'  submenu items: {items}')
        # click first visible submenu item (New row) - NO SAVE
        sub = page.locator("xpath=//ul[contains(@class,'ui-menu-child')]//li//a")
        for i in range(sub.count()):
            if sub.nth(i).is_visible():
                sub.nth(i).click(); print(f'  clicked: "{sub.nth(i).text_content().strip()}"'); break
        page.wait_for_load_state('networkidle', timeout=12000); page.wait_for_timeout(1200)
        page.screenshot(path=os.path.join(SS_DIR, 'scan_02_after_insert.png'), full_page=True)

        # capture the new row cell input IDs
        newrow = page.evaluate(f"""()=>{{
            const tb=document.getElementById('{TABLE}'); if(!tb) return {{}};
            const out=[];
            tb.querySelectorAll('tr').forEach(tr=>{{
                tr.querySelectorAll('td').forEach(td=>{{
                    const inp=td.querySelector('input:not([type=hidden]),select,textarea');
                    if(inp&&inp.id) out.push({{id:inp.id, type:inp.type||inp.tagName, val:inp.value||''}});
                }});
            }});
            return {{inputs: out}};
        }}""")
        print('\n  New-row editable inputs (after Insert):')
        for inp in newrow.get('inputs', []):
            print(f'    {inp["id"]}  [{inp["type"]}] val="{inp["val"]}"')

    ctx.close(); b.close()
print('\nScan complete (READ-ONLY, no save).', SS_DIR)
