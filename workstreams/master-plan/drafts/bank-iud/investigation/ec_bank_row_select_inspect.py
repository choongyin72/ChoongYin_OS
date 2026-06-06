"""
Inspect Bank screen after clicking AUTOTEST_BNK_001 row.
Determines: what changes in toolbar + objectForm after row selection.
Answers: how to trigger delete for Manage Object screen.
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


EC_URL   = os.environ.get('EC_URL', 'https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/')
SS_DIR   = str(_repo_root() / 'docs' / 'EC' / 'screenshots' / 'iud_bank')
TEST_CODE = 'AUTOTEST_BNK_001'
os.makedirs(SS_DIR, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=['--ignore-certificate-errors'])
    ctx = browser.new_context(ignore_https_errors=True, viewport={'width': 1920, 'height': 1080})
    page = ctx.new_page()

    # Login
    page.goto(EC_URL, wait_until='domcontentloaded', timeout=30000)
    page.fill('#username', 'sysadmin'); page.fill('#password', 'sysadmin')
    page.click('#kc-login')
    page.wait_for_url('**/dashboard**', timeout=60000)
    page.wait_for_load_state('networkidle', timeout=30000)

    # Navigate to Bank
    si = page.locator('#menu\\:searchForm\\:searchTxt')
    si.wait_for(state='visible', timeout=10000)
    si.clear(); si.type('Bank', delay=60)
    page.wait_for_load_state('networkidle', timeout=8000)
    page.wait_for_timeout(400)
    page.locator(
        "xpath=//*[self::label or self::span][contains(@class,'tv-link') and normalize-space(text())='Bank']"
    ).first.click()
    page.wait_for_load_state('networkidle', timeout=15000)
    page.wait_for_timeout(1500)
    page.screenshot(path=os.path.join(SS_DIR, 'rsinspect_01_bank.png'))
    print('Bank screen loaded')

    # Check table
    rows = page.evaluate("""() => {
        const tbody = document.getElementById('manage_object_nav_nav:form:T_data');
        if (!tbody) return [];
        const out = [];
        tbody.querySelectorAll('tr').forEach(tr => {
            const cells = [];
            tr.querySelectorAll('td').forEach(td => cells.push(td.textContent.trim()));
            if (cells.some(c => c)) out.push({cells, id: tr.id||''});
        });
        return out;
    }""")
    print(f'\nTable rows: {len(rows)}')
    autotest_row = None
    for r in rows:
        print(f'  {r["cells"]}, tr_id={r["id"]}')
        if r["cells"] and r["cells"][0] == TEST_CODE:
            autotest_row = r

    if not autotest_row:
        print(f'\n{TEST_CODE} not found in table — abort')
        ctx.close(); browser.close()
        exit(1)

    print(f'\nFound AUTOTEST row: {autotest_row}')

    # Check toolbar BEFORE row click
    toolbar_before = page.evaluate("""() => {
        const items = [];
        document.querySelectorAll('#screenToolbar\\\\:form\\\\:menuBar li a').forEach(a => {
            items.push({
                title: a.title || a.textContent.trim(),
                disabled: a.classList.contains('ui-state-disabled'),
                cls: a.className.substring(0, 80),
                onclick_snippet: (a.onclick ? a.onclick.toString() : a.getAttribute('onclick') || '').substring(0,100)
            });
        });
        return items;
    }""")
    print('\n=== TOOLBAR BEFORE ROW CLICK ===')
    for item in toolbar_before:
        print(f'  {item["title"][:30]:<30} disabled={item["disabled"]}')

    # Click the AUTOTEST row using JS (click on the first span in the row)
    print(f'\n=== CLICKING AUTOTEST ROW ===')
    page.evaluate(f"""() => {{
        const tbody = document.getElementById('manage_object_nav_nav:form:T_data');
        const trs = tbody.querySelectorAll('tr');
        for (const tr of trs) {{
            const first_td = tr.querySelector('td');
            if (first_td && first_td.textContent.trim() === '{TEST_CODE}') {{
                console.log('Clicking tr for AUTOTEST_BNK_001');
                tr.click();
                // Also try the first span inside
                const span = first_td.querySelector('span');
                if (span) span.click();
                break;
            }}
        }}
    }}""")
    page.wait_for_timeout(500)
    page.wait_for_load_state('networkidle', timeout=15000)
    page.wait_for_timeout(2000)  # Extra wait for objectForm to load
    page.screenshot(path=os.path.join(SS_DIR, 'rsinspect_02_after_row_click.png'))

    # Check toolbar AFTER row click
    toolbar_after = page.evaluate("""() => {
        const items = [];
        document.querySelectorAll('#screenToolbar\\\\:form\\\\:menuBar li a, #screenToolbar\\\\:form\\\\:menuBar li').forEach(el => {
            if (el.tagName === 'A') {
                items.push({
                    type: 'a',
                    title: el.title || el.textContent.trim().substring(0,30),
                    disabled: el.classList.contains('ui-state-disabled'),
                    onclick_80: (el.getAttribute('onclick') || '').substring(0,120)
                });
            }
        });
        return items;
    }""")
    print('\n=== TOOLBAR AFTER ROW CLICK ===')
    for item in toolbar_after:
        print(f'  {item["title"][:30]:<30} disabled={item["disabled"]}')
        if 'delete' in item['title'].lower() or 'Delete' in item['title']:
            print(f'    DELETE onclick: {item["onclick_80"]}')

    # Check objectForm
    obj_form = page.evaluate("""() => {
        const forms = ['tab:tabPanel:objectForm:form', 'objectForm:form', 'tab:tabPanel'];
        for (const fid of forms) {
            const el = document.getElementById(fid);
            if (el) {
                const inputs = [];
                el.querySelectorAll('input:not([type=hidden])').forEach(e => {
                    if (e.id && e.offsetParent !== null)
                        inputs.push({id:e.id, val:e.value, ro:e.readOnly});
                });
                return {id: fid, inputs: inputs};
            }
        }
        return {id: 'not found', inputs: []};
    }""")
    print(f'\n=== OBJECT FORM (source={obj_form["id"]}) ===')
    for inp in obj_form['inputs']:
        if 'statusarea' not in inp['id']:
            print(f'  {inp["id"]}  val="{inp["val"]}"  ro={inp["ro"]}')

    # Get ALL toolbar HTML
    toolbar_html = page.evaluate("""() => {
        const t = document.getElementById('screenToolbar:form:menuBar');
        return t ? t.outerHTML.substring(0, 5000) : 'not found';
    }""")
    print('\n=== FULL TOOLBAR HTML (first 5000 chars) ===')
    print(toolbar_html)

    # Check row selection state
    sel_state = page.evaluate(f"""() => {{
        const tbody = document.getElementById('manage_object_nav_nav:form:T_data');
        const sel_input = document.getElementById('manage_object_nav_nav:form:T_selection');
        const selected_trs = tbody ? Array.from(tbody.querySelectorAll('tr.ui-state-highlight, tr.ui-row-editing, tr[aria-selected="true"]')) : [];
        return {{
            selection_input: sel_input ? sel_input.value : null,
            selected_rows: selected_trs.map(tr => tr.textContent.trim().substring(0,50)),
            highlight_rows: tbody ? tbody.querySelectorAll('tr.ui-state-highlight').length : 0
        }};
    }}""")
    print(f'\n=== ROW SELECTION STATE ===')
    print(sel_state)

    ctx.close()
    browser.close()

print('\nInspection complete')
print(f'Screenshots: {SS_DIR}')
