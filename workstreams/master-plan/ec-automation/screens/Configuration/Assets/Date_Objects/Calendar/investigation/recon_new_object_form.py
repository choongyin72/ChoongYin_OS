"""READ-ONLY recon: Calendar New-Object form -- all controls incl checkboxes. Never saves."""
from playwright.sync_api import sync_playwright
import os
EC_URL=os.environ.get('EC_URL','https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/')
EC_USER=os.environ.get('EC_USER','sysadmin'); EC_PASS=os.environ.get('EC_PASS','sysadmin')
SCREEN='Calendar'
def wa(pg,t=15000): pg.wait_for_load_state('networkidle',timeout=t); pg.wait_for_timeout(900)
with sync_playwright() as p:
    b=p.chromium.launch(headless=True,args=['--ignore-certificate-errors'])
    pg=b.new_context(ignore_https_errors=True,viewport={'width':1920,'height':1080}).new_page()
    pg.goto(EC_URL,wait_until='domcontentloaded',timeout=30000)
    pg.fill('#username',EC_USER); pg.fill('#password',EC_PASS); pg.click('#kc-login')
    pg.wait_for_url('**/dashboard**',timeout=60000); wa(pg)
    si=pg.locator(r'#menu\:searchForm\:searchTxt'); si.wait_for(state='visible',timeout=10000)
    si.clear(); si.type(SCREEN,delay=60); pg.wait_for_load_state('networkidle',timeout=8000); pg.wait_for_timeout(400)
    pg.locator(f"xpath=//*[self::label or self::span][contains(@class,'tv-link') and normalize-space(text())='{SCREEN}']").first.click(); wa(pg)
    print('Screen:',pg.locator(r'#screenToolbar\:form\:screenLabel').text_content(timeout=5000))
    # child-grid check: any second grid on the screen?
    grids=pg.evaluate("""() => Array.from(document.querySelectorAll("tbody[id$='_data'], div[id$='T_data']")).map(e=>e.id).slice(0,8)""")
    print('grids on screen:',grids)
    pg.locator("xpath=//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'ui-icon-insert')]]").first.hover(); pg.wait_for_timeout(1000)
    subs=pg.locator("xpath=//ul[contains(@class,'ui-menu-child')]//li//a")
    for i in range(subs.count()):
        try:
            if subs.nth(i).text_content(timeout=1000).strip()=='New Object' and subs.nth(i).is_visible(): subs.nth(i).click(); break
        except Exception: pass
    wa(pg)
    fields=pg.evaluate("""() => Array.from(document.querySelectorAll("[id*='objectForm:form'][id$=':in'], [id*='objectForm:form'][id$=':da_input'], [id*='objectForm:form'] input[type='checkbox'], [id*='objectForm:form'][id$='_button'], [id*='objectForm:form'] .ui-chkbox-box")).map(e=>({id:e.id||'(chkbox-box)',tag:e.tagName,type:e.type||'',mand:/mandatory:true/i.test(e.className),cls:(e.className||'').slice(0,45)}))""")
    print(f'\nobjectForm controls ({len(fields)}):')
    for f in fields: print(f"   {f['id']}  {f['tag']}/{f['type']} mand={f['mand']} cls='{f['cls']}'")
    print('\nDONE (read-only).')
    b.close()
