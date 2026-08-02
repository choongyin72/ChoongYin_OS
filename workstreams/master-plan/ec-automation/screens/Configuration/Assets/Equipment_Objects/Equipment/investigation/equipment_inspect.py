"""
Phase 0 - Deep-dive DOM scan of the EC Equipment screen (READ-ONLY).
Captures: navigator (5 filter dropdowns) IDs + current values, Go/arrow button,
toolbar (incl. the - button), the equipment table, and the objectForm /
updateAttributes / objectdates field IDs. NEVER saves - observation only.
"""
import os
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
    return here.parents[5]


EC_URL = os.environ.get('EC_URL', 'https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/')
SS_DIR = str(_repo_root() / 'docs' / 'EC' / 'screenshots' / 'iud_equipment')
os.makedirs(SS_DIR, exist_ok=True)


def dump_form(page, form_id):
    """Return labels + inputs/selects inside a form/container, with current values."""
    return page.evaluate("""(formId) => {
        const el = document.getElementById(formId) || document.querySelector('[id^="'+formId+'"]');
        if (!el) return {found:false};
        const fields = [];
        el.querySelectorAll('input,select,textarea,.ui-selectonemenu,.ui-autocomplete').forEach(e => {
            if (!e.id) return;
            const vis = e.offsetParent !== null;
            fields.push({
                id: e.id, tag: e.tagName, type: e.type||'', val: (e.value||'').substring(0,40),
                cls: (e.className||'').substring(0,50), visible: vis
            });
        });
        // labels for context
        const labels = [];
        el.querySelectorAll('label,.ECLabelCell,legend').forEach(l => {
            const t = (l.textContent||'').trim();
            if (t) labels.push(t.substring(0,40));
        });
        return {found:true, html: el.outerHTML.substring(0,400), fields, labels};
    }""", form_id)


with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=['--ignore-certificate-errors'])
    ctx = browser.new_context(ignore_https_errors=True, viewport={'width': 1920, 'height': 1080})
    page = ctx.new_page()

    # -- LOGIN --
    page.goto(EC_URL, wait_until='domcontentloaded', timeout=30000)
    page.fill('#username', os.environ.get("EC_USER", "sysadmin")); page.fill('#password', os.environ.get("EC_PASS", "sysadmin"))
    page.click('#kc-login')
    page.wait_for_url('**/dashboard**', timeout=60000)
    page.wait_for_load_state('networkidle', timeout=30000)
    print('LOGIN OK')

    # -- NAVIGATE TO EQUIPMENT --
    si = page.locator('#menu\\:searchForm\\:searchTxt')
    si.wait_for(state='visible', timeout=10000)
    si.clear(); si.type('Equipment', delay=60)
    page.wait_for_load_state('networkidle', timeout=8000)
    page.wait_for_timeout(500)
    # capture what the search returned
    results = page.evaluate("""() => {
        const out = [];
        document.querySelectorAll('#menu\\\\:searchForm\\\\:searchList .tv-link, #menu\\\\:searchForm\\\\:searchList label').forEach(l => {
            if (l.offsetParent) out.push({text:(l.textContent||'').trim(), id:l.id||'', tip:l.getAttribute('data-tooltip')||''});
        });
        return out;
    }""")
    print('\n=== SEARCH RESULTS for "Equipment" ===')
    for r in results:
        print(f'  "{r["text"]}"  id={r["id"]}  tip={r["tip"]}')

    # Click the Equipment tree link (prefer exact match, first visible)
    eq = page.locator("xpath=//*[self::label or self::span][contains(@class,'tv-link') and normalize-space(text())='Equipment']")
    print(f'\nEquipment links matched: {eq.count()}')
    eq.first.click()
    page.wait_for_load_state('networkidle', timeout=15000)
    page.wait_for_timeout(1500)
    try:
        lbl = page.locator('#screenToolbar\\:form\\:screenLabel').text_content(timeout=5000)
    except Exception:
        lbl = '(no label)'
    print(f'Screen label: {lbl}')
    page.screenshot(path=os.path.join(SS_DIR, 'scan_01_equipment_loaded.png'), full_page=True)

    # -- ALL VISIBLE IDs --
    ids = page.evaluate("""() => {
        const out = [];
        document.querySelectorAll('[id]').forEach(el => {
            if (el.offsetParent !== null && el.id)
                out.push({id:el.id, tag:el.tagName, cls:(el.className||'').substring(0,40)});
        });
        return out;
    }""")
    print(f'\n=== VISIBLE IDs ({len(ids)}) - screenlets/forms/buttons ===')
    for el in ids:
        if any(k in el['id'] for k in ['nav:form', 'button:form', 'manage_object', 'screenToolbar', 'tab:tabPanel']) \
           and not el['id'].count(':') > 6:
            print(f'  {el["id"]} ({el["tag"]}) {el["cls"][:35]}')

    # -- NAVIGATOR (nav:form) --
    print('\n=== NAVIGATOR nav:form ===')
    nav = dump_form(page, 'nav:form')
    if nav.get('found'):
        print(f'  labels: {nav["labels"]}')
        for f in nav['fields']:
            if f['visible']:
                print(f'  {f["id"]}  <{f["tag"]}/{f["type"]}> val="{f["val"]}" cls={f["cls"][:30]}')

    # -- TOOLBAR (find + and - buttons) --
    print('\n=== TOOLBAR (menuBar) ===')
    tb = page.evaluate("""() => {
        const items = [];
        document.querySelectorAll('#screenToolbar\\\\:form\\\\:menuBar a').forEach(a => {
            const icon = a.querySelector('span[class*="ui-icon-"]');
            const iconcls = icon ? (icon.className.match(/ui-icon-[a-z-]+/)||[''])[0] : '';
            items.push({
                title: a.title || (a.textContent||'').trim().substring(0,20),
                icon: iconcls,
                disabled: a.classList.contains('ui-state-disabled'),
                parent_li_cls: a.closest('li') ? a.closest('li').className.substring(0,60) : ''
            });
        });
        return items;
    }""")
    for it in tb:
        print(f'  {it["title"][:22]:<22} icon={it["icon"]:<18} disabled={it["disabled"]}')

    # -- GO / ARROW button --
    print('\n=== GO / ARROW button candidates ===')
    go = page.evaluate("""() => {
        const out = [];
        document.querySelectorAll('#button\\\\:form button, #button\\\\:form a, [id^="button:form"]').forEach(b => {
            if (b.id) out.push({id:b.id, tag:b.tagName, title:b.title||'', cls:(b.className||'').substring(0,40), vis:b.offsetParent!==null});
        });
        return out;
    }""")
    for g in go:
        print(f'  {g["id"]} <{g["tag"]}> title="{g["title"]}" vis={g["vis"]} cls={g["cls"][:30]}')

    # -- CLICK GO (>) to load the equipment list --
    print('\n=== CLICK GO (load list) ===')
    clicked_go = False
    for sel in ['#button\\:form\\:B', '#button\\:form button', "xpath=//div[contains(@class,'goButtonScreenlet')]//button"]:
        loc = page.locator(sel)
        if loc.count() > 0 and loc.first.is_visible():
            loc.first.click()
            clicked_go = True
            print(f'  Clicked Go via: {sel}')
            break
    page.wait_for_load_state('networkidle', timeout=15000)
    page.wait_for_timeout(1500)
    page.screenshot(path=os.path.join(SS_DIR, 'scan_02_after_go.png'), full_page=True)

    # -- EQUIPMENT TABLE --
    print('\n=== EQUIPMENT TABLE (manage_object_nav_nav:form:T_data) ===')
    rows = page.evaluate("""() => {
        const tbody = document.getElementById('manage_object_nav_nav:form:T_data');
        if (!tbody) return {found:false};
        const out = [];
        tbody.querySelectorAll('tr').forEach(tr => {
            const cells = [];
            tr.querySelectorAll('td').forEach(td => cells.push((td.textContent||'').trim()));
            if (cells.some(c=>c)) out.push(cells);
        });
        return {found:true, rows: out};
    }""")
    if rows.get('found'):
        print(f'  Rows ({len(rows["rows"])}):')
        for r in rows['rows']:
            print(f'    {r}')
    else:
        print('  Table not found (filters may need setting).')

    # -- ROW SELECT (existing row, READ-ONLY) to capture updateAttributes/objectdates --
    print('\n=== ROW SELECT (read-only, first existing row) ===')
    first_span = page.locator("css=#manage_object_nav_nav\\:form\\:T_data span").first
    if first_span.count() > 0:
        try:
            first_span.click()
            page.wait_for_load_state('networkidle', timeout=15000)
            page.wait_for_timeout(1500)
            page.screenshot(path=os.path.join(SS_DIR, 'scan_03_row_selected.png'), full_page=True)
            for fid in ['tab:tabPanel:updateAttributes:form', 'tab:tabPanel:objectdates:form']:
                d = dump_form(page, fid)
                print(f'\n  --- {fid} ---')
                if d.get('found'):
                    for f in d['fields']:
                        if f['visible'] and 'statusarea' not in f['id']:
                            print(f'    {f["id"]}  val="{f["val"]}"')
            # toolbar state AFTER row select (is - button now enabled?)
            del_state = page.evaluate("""() => {
                const items = [];
                document.querySelectorAll('#screenToolbar\\\\:form\\\\:menuBar a').forEach(a => {
                    const icon = a.querySelector('span[class*="ui-icon-"]');
                    const iconcls = icon ? (icon.className.match(/ui-icon-[a-z-]+/)||[''])[0] : '';
                    if (iconcls.includes('delete') || iconcls.includes('minus') || iconcls.includes('trash'))
                        items.push({icon:iconcls, disabled:a.classList.contains('ui-state-disabled'),
                                    li:a.closest('li')?a.closest('li').className.substring(0,60):''});
                });
                return items;
            }""")
            print(f'\n  Delete/- button after row select: {del_state}')
        except Exception as e:
            print(f'  Row select error: {e}')
    else:
        print('  No rows to select.')

    # -- INSERT -> NEW OBJECT (capture objectForm, READ-ONLY, no save) --
    print('\n=== INSERT -> NEW OBJECT (capture objectForm fields, no save) ===')
    try:
        insert_li = page.locator("xpath=//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'ui-icon-insert')]]")
        if insert_li.count() > 0:
            insert_li.first.hover()
            page.wait_for_timeout(900)
            sub = page.locator("xpath=//ul[contains(@class,'ui-menu-child')]//li//a")
            # print submenu labels
            labels = []
            for i in range(sub.count()):
                try:
                    if sub.nth(i).is_visible():
                        labels.append(sub.nth(i).text_content(timeout=800).strip())
                except Exception:
                    pass
            print(f'  Insert submenu items: {labels}')
            # click first (New Object)
            for i in range(sub.count()):
                if sub.nth(i).is_visible():
                    sub.nth(i).click(); break
            page.wait_for_load_state('networkidle', timeout=15000)
            page.wait_for_timeout(1500)
            page.screenshot(path=os.path.join(SS_DIR, 'scan_04_new_object.png'), full_page=True)
            d = dump_form(page, 'tab:tabPanel:objectForm:form')
            print('  --- objectForm fields ---')
            if d.get('found'):
                for f in d['fields']:
                    if f['visible'] and 'statusarea' not in f['id']:
                        print(f'    {f["id"]}  <{f["type"]}> val="{f["val"]}"')
        else:
            print('  Insert button not found.')
    except Exception as e:
        print(f'  Insert scan error: {e}')

    ctx.close()
    browser.close()

print('\nScan complete. Screenshots:', SS_DIR)
