"""Deep scan of the MIME grid cell-edit + commit mechanism. READ-ONLY (no save)."""
from playwright.sync_api import sync_playwright
import os
EC_URL = 'https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/'

with sync_playwright() as p:
    b = p.chromium.launch(headless=True, args=['--ignore-certificate-errors'])
    ctx = b.new_context(ignore_https_errors=True, viewport={'width':1680,'height':1050}); page = ctx.new_page()
    page.goto(EC_URL, wait_until='domcontentloaded', timeout=30000)
    page.fill('#username', os.environ.get("EC_USER", "sysadmin")); page.fill('#password', os.environ.get("EC_PASS", "sysadmin")); page.click('#kc-login')
    page.wait_for_url('**/dashboard**', timeout=60000); page.wait_for_load_state('networkidle', timeout=30000)
    si=page.locator('#menu\\:searchForm\\:searchTxt'); si.wait_for(state='visible')
    si.clear(); si.type('MIME Type Mapping', delay=50); page.wait_for_load_state('networkidle', timeout=8000); page.wait_for_timeout(600)
    page.locator("xpath=//*[self::label or self::span][contains(@class,'tv-link') and normalize-space(text())='MIME Type Mapping']").first.click()
    page.wait_for_load_state('networkidle', timeout=15000); page.wait_for_timeout(1500)

    # datatable widget + paginator + editable mode
    info = page.evaluate("""()=>{
        const dt=document.querySelector('#mime_type_table\\\\:form\\\\:T') || document.querySelector('[id="mime_type_table:form:T"]');
        const out={};
        if(dt){ out.dt_class=dt.className.substring(0,120);
            out.has_paginator=!!dt.querySelector('.ui-paginator');
            out.rows_in_dom=dt.querySelectorAll('tbody[id$="_data"] tr').length;
            out.editors=dt.querySelectorAll('.ui-cell-editor').length;
            out.row_editors=dt.querySelectorAll('.ui-row-editor').length; }
        // a sample cell input outerHTML
        const inp=document.getElementById('mime_type_table:form:T:0:C0_in');
        out.cell_html = inp ? inp.outerHTML.substring(0,700) : 'no C0_in';
        // forms on page (which form holds the table)
        out.table_form = document.querySelector('[id="mime_type_table:form"]') ? 'mime_type_table:form exists' : 'no';
        return out;
    }""")
    print('=== datatable / cell info ===')
    for k,v in info.items(): print(f'  {k}: {v}')

    # Click Insert -> capture the NEW row input outerHTML + how add works
    ins = page.locator("xpath=//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'ui-icon-insert')]]")
    ins.first.hover(); page.wait_for_timeout(800)
    sub = page.locator("xpath=//ul[contains(@class,'ui-menu-child')]//li//a")
    for i in range(sub.count()):
        if sub.nth(i).is_visible(): sub.nth(i).click(); break
    page.wait_for_load_state('networkidle', timeout=12000); page.wait_for_timeout(1200)

    newinfo = page.evaluate("""()=>{
        // find blank C0 row
        let blank=null;
        document.querySelectorAll('input[id^="mime_type_table:form:T:"][id$=":C0_in"]').forEach(inp=>{
            if((inp.value||'')==='' && blank===null) blank=inp.id;
        });
        const el = blank?document.getElementById(blank):null;
        const c1id = blank? blank.replace(':C0_in',':C1_in'):null;
        const c1 = c1id?document.getElementById(c1id):null;
        return {blank_id:blank, blank_html: el?el.outerHTML.substring(0,900):'none',
                c1_html: c1?c1.outerHTML.substring(0,500):'none',
                tr_html: el? el.closest('tr').outerHTML.substring(0,600):'none'};
    }""")
    print('\n=== NEW blank row after Insert ===')
    for k,v in newinfo.items(): print(f'  {k}: {v}\n')

    ctx.close(); b.close()
print('done')
