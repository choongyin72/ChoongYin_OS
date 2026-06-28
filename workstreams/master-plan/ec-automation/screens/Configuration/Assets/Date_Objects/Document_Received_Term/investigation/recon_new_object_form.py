"""
READ-ONLY recon: open Document Received Term, click Insert -> New Object, dump every
objectForm field (id, label, mandatory/yellow, control type). Never saves.
Confirms the OV New-Object mandatory set for CD.0108 before building the IUD flow.
"""
from playwright.sync_api import sync_playwright
import os

EC_URL  = os.environ.get('EC_URL', 'https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/')
EC_USER = os.environ.get('EC_USER', 'sysadmin')
EC_PASS = os.environ.get('EC_PASS', 'sysadmin')
SCREEN  = 'Document Received Term'

def wait_ajax(page, t=15000):
    page.wait_for_load_state('networkidle', timeout=t); page.wait_for_timeout(1000)

with sync_playwright() as p:
    b = p.chromium.launch(headless=True, args=['--ignore-certificate-errors'])
    pg = b.new_context(ignore_https_errors=True, viewport={'width':1920,'height':1080}).new_page()
    pg.goto(EC_URL, wait_until='domcontentloaded', timeout=30000)
    pg.fill('#username', EC_USER); pg.fill('#password', EC_PASS); pg.click('#kc-login')
    pg.wait_for_url('**/dashboard**', timeout=60000); wait_ajax(pg)
    si = pg.locator(r'#menu\:searchForm\:searchTxt'); si.wait_for(state='visible', timeout=10000)
    si.clear(); si.type(SCREEN, delay=60); pg.wait_for_load_state('networkidle', timeout=8000); pg.wait_for_timeout(400)
    pg.locator(f"xpath=//*[self::label or self::span][contains(@class,'tv-link') and normalize-space(text())='{SCREEN}']").first.click()
    wait_ajax(pg)
    lbl = pg.locator(r'#screenToolbar\:form\:screenLabel').text_content(timeout=5000)
    print(f'Screen: {lbl}')

    insert_li = pg.locator("xpath=//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'ui-icon-insert')]]")
    insert_li.first.hover(); pg.wait_for_timeout(1000)
    subs = pg.locator("xpath=//ul[contains(@class,'ui-menu-child')]//li//a")
    for i in range(subs.count()):
        try:
            if subs.nth(i).text_content(timeout=1000).strip() == 'New Object' and subs.nth(i).is_visible():
                subs.nth(i).click(); print('  clicked New Object'); break
        except Exception: pass
    wait_ajax(pg)

    fields = pg.evaluate("""() => {
        const out = [];
        document.querySelectorAll("[id*='objectForm:form'][id$=':in'], [id*='objectForm:form'][id$=':da_input'], [id*='objectForm:form'][id$='_button']").forEach(e => {
            const cls = e.className || '';
            // label: nearest preceding label cell text in same row
            let lab = '';
            const tr = e.closest('tr');
            if (tr) { const l = tr.querySelector("label, td"); lab = l ? l.textContent.trim().slice(0,40) : ''; }
            out.push({id: e.id, tag: e.tagName, type: e.type||'', yellow: /mandatory|required|ec-required/i.test(cls) || (getComputedStyle(e).backgroundColor||'').includes('255, 255'), cls: cls.slice(0,60), label: lab});
        });
        return out;
    }""")
    print(f'\nobjectForm fields ({len(fields)}):')
    for f in fields:
        print(f"   {f['id']}")
        print(f"        tag={f['tag']} type={f['type']} label='{f['label']}' cls='{f['cls']}'")
    # also dump any visible *_panel dropdown ids
    dds = pg.evaluate("""() => Array.from(document.querySelectorAll("[id*='objectForm'][id$='_button']")).map(e=>e.id)""")
    print(f'\ndropdown buttons: {dds}')
    print('\nDONE (read-only; nothing saved).')
    b.close()
