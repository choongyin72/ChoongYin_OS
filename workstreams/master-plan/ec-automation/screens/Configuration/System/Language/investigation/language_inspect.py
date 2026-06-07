"""READ-ONLY recon of the Language screen (Table class). No save. Dumps grid id,
cell input ids, toolbar, insert/delete submenu labels, and the search breadcrumb."""
from playwright.sync_api import sync_playwright

EC_URL = 'https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/'

with sync_playwright() as p:
    b = p.chromium.launch(headless=True, args=['--ignore-certificate-errors'])
    ctx = b.new_context(ignore_https_errors=True, viewport={'width': 1680, 'height': 1050})
    page = ctx.new_page()
    page.goto(EC_URL, wait_until='domcontentloaded', timeout=30000)
    page.fill('#username', 'sysadmin'); page.fill('#password', 'sysadmin'); page.click('#kc-login')
    page.wait_for_url('**/dashboard**', timeout=60000); page.wait_for_load_state('networkidle', timeout=30000)
    si = page.locator('#menu\\:searchForm\\:searchTxt'); si.wait_for(state='visible')
    si.clear(); si.type('Language', delay=60); page.wait_for_load_state('networkidle', timeout=8000); page.wait_for_timeout(800)

    # breadcrumb tooltip on the search result link
    bc = page.evaluate("""()=>{
        const out=[];
        document.querySelectorAll('.tv-link, [class*="tv-link"]').forEach(a=>{
            const t=(a.textContent||'').trim();
            if(t==='Language') out.push({text:t, title:a.getAttribute('title')||a.getAttribute('data-original-title')||'', parentTitle:(a.closest('[title]')?a.closest('[title]').getAttribute('title'):'')});
        });
        return out;
    }""")
    print('=== search result(s) for "Language" ===')
    for r in bc: print('  ', r)

    page.locator("xpath=//*[self::label or self::span][contains(@class,'tv-link') and normalize-space(text())='Language']").first.click()
    page.wait_for_load_state('networkidle', timeout=15000); page.wait_for_timeout(1800)
    try:
        lbl = page.locator('#screenToolbar\\:form\\:screenLabel').text_content(timeout=5000)
    except Exception:
        lbl = '(no screenLabel)'
    print(f'\nScreen label: {lbl}')

    # find the grid table(s) and cell input ids
    grid = page.evaluate("""()=>{
        const out={tables:[]};
        document.querySelectorAll('tbody[id$="_data"]').forEach(tb=>{
            const info={id:tb.id, rows:tb.querySelectorAll('tr').length, cellInputs:[]};
            tb.querySelectorAll('tr')[0]?.querySelectorAll('td').forEach(td=>{
                const inp=td.querySelector('input,select,textarea');
                info.cellInputs.push({id:(inp&&inp.id)||'', type:inp?(inp.type||inp.tagName):'ro', txt:(td.textContent||'').trim().substring(0,20)});
            });
            out.tables.push(info);
        });
        return out;
    }""")
    print('\n=== grid tables (tbody[id$=_data]) ===')
    for t in grid['tables']:
        print(f"  table id: {t['id']}  rows={t['rows']}")
        for c in t['cellInputs']:
            print(f"      cell: id='{c['id']}'  type={c['type']}  txt='{c['txt']}'")

    # toolbar + insert submenu + delete submenu labels
    print('\n=== INSERT submenu ===')
    ins = page.locator("xpath=//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'ui-icon-insert')]]")
    if ins.count() > 0:
        ins.first.hover(); page.wait_for_timeout(800)
        items = page.evaluate("""()=>{const o=[];document.querySelectorAll('li.ui-menu-parent .ui-menu-child a').forEach(a=>{if(a.offsetParent)o.push((a.textContent||'').trim());});return o;}""")
        print('  insert submenu items:', items)
    print('\n=== DELETE submenu ===')
    dele = page.locator("xpath=//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'ui-icon-delete')]]")
    if dele.count() > 0:
        dele.first.hover(); page.wait_for_timeout(800)
        items = page.evaluate("""()=>{const o=[];document.querySelectorAll('li.ui-menu-parent .ui-menu-child a').forEach(a=>{if(a.offsetParent)o.push((a.textContent||'').trim());});return o;}""")
        print('  delete submenu items:', items)

    ctx.close(); b.close()
print('\nrecon done (READ-ONLY, no save).')
