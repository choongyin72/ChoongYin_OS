"""
Deep DOM inspection of Bank screen to understand exact insert pattern.
"""
from playwright.sync_api import sync_playwright
import json, os, sys

EC_URL = 'https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/'
SS_DIR = r'c:\Projects\ChoongYin_OS\docs\EC\screenshots\iud_bank'
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
    si = page.locator("xpath=//input[@id='menu:searchForm:searchTxt']")
    si.wait_for(state='visible', timeout=10000)
    si.clear(); si.type('Bank', delay=60)
    page.wait_for_load_state('networkidle', timeout=8000)
    page.wait_for_timeout(400)

    bank_link = page.locator("xpath=//*[self::label or self::span][contains(@class,'tv-link') and normalize-space(text())='Bank']")
    bank_link.first.click()
    page.wait_for_load_state('networkidle', timeout=15000)
    page.wait_for_timeout(1500)

    # Full page screenshot
    page.screenshot(path=os.path.join(SS_DIR, 'inspect_01_bank_full.png'), full_page=True)
    print('Full page screenshot taken')

    # Deep DOM inspection
    dom = page.evaluate("""() => {
        const r = {};

        // ALL visible IDs
        const ids = [];
        document.querySelectorAll('[id]').forEach(el => {
            if (el.offsetParent !== null && el.id)
                ids.push({id:el.id, tag:el.tagName, cls:el.className.substring(0,50)});
        });
        r.all_ids = ids;

        // Toolbar HTML (to see what buttons exist)
        const tb = document.getElementById('screenToolbar:form:menuBar');
        r.toolbar_html = tb ? tb.outerHTML.substring(0,3000) : 'not found';

        // manage_object_nav structure
        const mon = document.getElementById('manage_object_nav_nav:form');
        r.manage_obj_nav = mon ? {
            html: mon.outerHTML.substring(0, 2000),
            inner_ids: []
        } : null;
        if (mon) {
            mon.querySelectorAll('[id]').forEach(el => {
                r.manage_obj_nav.inner_ids.push({id:el.id, tag:el.tagName, cls:el.className.substring(0,40)});
            });
        }

        // Tab panel structure
        const tab = document.getElementById('tab:tabPanel');
        r.tab_panel = tab ? {
            html_sample: tab.outerHTML.substring(0,500),
            tabs: []
        } : null;
        if (tab) {
            tab.querySelectorAll('.ui-tabs-nav li').forEach(li => {
                r.tab_panel.tabs.push({id:li.id, text:li.textContent.trim()});
            });
        }

        // nav:form structure
        const nav = document.getElementById('nav:form');
        r.nav_form = nav ? {
            html: nav.outerHTML.substring(0,1500),
            inputs: []
        } : null;
        if (nav) {
            nav.querySelectorAll('input,select,button').forEach(el => {
                if(el.id) r.nav_form.inputs.push({id:el.id, type:el.type||el.tagName,
                                                   ph:el.placeholder||'', val:el.value||''});
            });
        }

        return r;
    }""")

    print('\n=== ALL VISIBLE IDs ===')
    for el in dom['all_ids']:
        print(f'  {el["id"]} ({el["tag"]}) {el["cls"][:40]}')

    print('\n=== TOOLBAR HTML ===')
    print(dom['toolbar_html'][:2000])

    print('\n=== MANAGE OBJECT NAV ===')
    if dom['manage_obj_nav']:
        print(f'HTML: {dom["manage_obj_nav"]["html"][:800]}')
        print('Inner IDs:')
        for el in dom['manage_obj_nav']['inner_ids']:
            print(f'  {el["id"]} ({el["tag"]})')
    else:
        print('Not found')

    print('\n=== NAV FORM ===')
    if dom['nav_form']:
        print(f'HTML: {dom["nav_form"]["html"][:800]}')
        print('Inputs:')
        for inp in dom['nav_form']['inputs']:
            print(f'  {inp["id"]} ({inp["type"]}) ph="{inp["ph"]}" val="{inp["val"]}"')

    print('\n=== TAB PANEL ===')
    if dom['tab_panel']:
        print(f'Sample: {dom["tab_panel"]["html_sample"][:300]}')
        print(f'Tabs: {dom["tab_panel"]["tabs"]}')

    # Now click Insert and inspect what appears
    print('\n=== CLICKING INSERT ===')
    insert_li = page.locator("xpath=//li[.//span[contains(@class,'ui-icon-insert')]]")
    print(f'Insert LI found: {insert_li.count()}')
    if insert_li.count() > 0:
        cls = insert_li.first.get_attribute('class') or ''
        print(f'Insert LI class: {cls}')
        print(f'Insert enabled: {"disabled" not in cls}')
        insert_li.first.click()
        page.wait_for_timeout(1000)
        page.screenshot(path=os.path.join(SS_DIR, 'inspect_02_after_insert_click.png'))
        print('Screenshot after insert click taken')

        # Check for submenu
        submenu_items = page.evaluate("""() => {
            const items = [];
            document.querySelectorAll('.ui-menu-child li a, .ui-submenu li a').forEach(a => {
                if(a.offsetParent) items.push({text:a.textContent.trim(), id:a.id||''});
            });
            return items;
        }""")
        print(f'Submenu items: {submenu_items}')

    ctx.close()
    browser.close()

print('\nInspection complete. Check screenshots in:', SS_DIR)
