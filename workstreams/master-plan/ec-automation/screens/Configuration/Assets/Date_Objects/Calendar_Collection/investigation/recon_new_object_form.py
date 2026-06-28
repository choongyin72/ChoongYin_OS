"""READ-ONLY recon: Calendar Collection grid id + GO presence + New-Object form fields. Never saves."""
from playwright.sync_api import sync_playwright
import os
EC_URL=os.environ.get('EC_URL','https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/')
EC_USER=os.environ.get('EC_USER','sysadmin'); EC_PASS=os.environ.get('EC_PASS','sysadmin')
SCREEN='Calendar Collection'
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
    grids=pg.evaluate("""()=>Array.from(document.querySelectorAll("tbody[id$='_data']")).map(e=>e.id).slice(0,10)""")
    print('grids:',grids)
    go=pg.locator('#button\:form\:B'); print('GO present:',go.count(),'visible:',go.count()>0 and go.first.is_visible())
    pg.locator("xpath=//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'ui-icon-insert')]]").first.hover(); pg.wait_for_timeout(1000)
    subs=pg.locator("xpath=//ul[contains(@class,'ui-menu-child')]//li//a")
    for i in range(subs.count()):
        try:
            if subs.nth(i).text_content(timeout=1000).strip()=='New Object' and subs.nth(i).is_visible(): subs.nth(i).click(); break
        except Exception: pass
    wa(pg)
    fields=pg.evaluate("""()=>Array.from(document.querySelectorAll("[id*='objectForm:form'][id$=':in'],[id*='objectForm:form'][id$=':da_input'],[id*='objectForm:form'][id$='_button'],[id*='objectForm:form'] input[type='checkbox']")).map(e=>({id:e.id,mand:/mandatory:true/i.test(e.className)}))""")
    print(f'objectForm fields ({len(fields)}):')
    for f in fields: print(f"   {f['id']} mand={f['mand']}")
    print('DONE (read-only).')
    b.close()
