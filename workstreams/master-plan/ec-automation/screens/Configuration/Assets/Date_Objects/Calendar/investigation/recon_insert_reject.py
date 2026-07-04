"""READ-ONLY diagnostic: fill Code/Name/Date, attempt Save, capture EC error + flagged cells. May write then we DO NOT GO; if a row persists we expire it."""
from playwright.sync_api import sync_playwright
import os
EC_URL=os.environ.get('EC_URL','https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/')
EC_USER=os.environ.get('EC_USER','sysadmin'); EC_PASS=os.environ.get('EC_PASS','sysadmin')
SCREEN='Calendar'
def wa(pg,t=15000): pg.wait_for_load_state('networkidle',timeout=t); pg.wait_for_timeout(1000)
def f(pg,fid,v):
    pg.locator(f'#{fid.replace(":",chr(92)+":")}').click(); pg.locator(f'#{fid.replace(":",chr(92)+":")}').fill(v)
    pg.evaluate("(i)=>{const e=document.getElementById(i);if(e){e.dispatchEvent(new Event('change',{bubbles:true}));e.dispatchEvent(new Event('blur',{bubbles:true}));}}",fid); pg.wait_for_timeout(300)
with sync_playwright() as p:
    b=p.chromium.launch(headless=True,args=['--ignore-certificate-errors'])
    pg=b.new_context(ignore_https_errors=True,viewport={'width':1920,'height':1080}).new_page()
    pg.goto(EC_URL,wait_until='domcontentloaded',timeout=30000)
    pg.fill('#username',EC_USER); pg.fill('#password',EC_PASS); pg.click('#kc-login')
    pg.wait_for_url('**/dashboard**',timeout=60000); wa(pg)
    si=pg.locator(r'#menu\:searchForm\:searchTxt'); si.wait_for(state='visible',timeout=10000)
    si.clear(); si.type(SCREEN,delay=60); pg.wait_for_load_state('networkidle',timeout=8000); pg.wait_for_timeout(400)
    pg.locator(f"xpath=//*[self::label or self::span][contains(@class,'tv-link') and normalize-space(text())='{SCREEN}']").first.click(); wa(pg)
    pg.locator("xpath=//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'ui-icon-insert')]]").first.hover(); pg.wait_for_timeout(1000)
    subs=pg.locator("xpath=//ul[contains(@class,'ui-menu-child')]//li//a")
    for i in range(subs.count()):
        try:
            if subs.nth(i).text_content(timeout=1000).strip()=='New Object' and subs.nth(i).is_visible(): subs.nth(i).click(); break
        except Exception: pass
    wa(pg)
    f(pg,'tab:tabPanel:objectForm:form:G:0:R:0:C:1:in','AUTOTEST_CAL_DIAG')
    f(pg,'tab:tabPanel:objectForm:form:G:0:R:1:C:1:in','AUTOTEST Calendar DIAG')
    # date with Tab
    d='tab:tabPanel:objectForm:form:G:0:R:2:C:1:da_input'
    pg.locator(f'#{d.replace(":",chr(92)+":")}').click(); pg.locator(f'#{d.replace(":",chr(92)+":")}').fill('2000-01-01'); pg.keyboard.press('Tab'); pg.wait_for_timeout(700)
    # try save
    save=pg.locator("xpath=//a[@title='Save [Ctrl+s]' and not(contains(@class,'ui-state-disabled'))]")
    if save.count()>0: save.first.click(); wa(pg)
    else: pg.keyboard.press('Control+s'); wa(pg)
    err=pg.evaluate("""()=>{const n=document.getElementById('ECNotificationArea')||document.getElementById('ECClientNotificationArea');return n?n.textContent.trim():'(no notification node)';}""")
    print('EC NOTIFICATION:',err[:400])
    # any cells flagged error/required now?
    flagged=pg.evaluate("""()=>Array.from(document.querySelectorAll("[id*='objectForm'] .ui-state-error, [id*='objectForm'].ErrorCellStyle, [id*='objectForm'] [class*='Error']")).map(e=>e.id||e.className).slice(0,12)""")
    print('FLAGGED cells:',flagged)
    # dump all objectForm field current values
    vals=pg.evaluate("""()=>Array.from(document.querySelectorAll("[id*='objectForm:form'][id$=':in'],[id*='objectForm:form'][id$=':da_input'],[id*='objectForm:form'] input[type='checkbox']")).map(e=>({id:e.id.split(':form:')[1],v:e.type==='checkbox'?e.checked:e.value}))""")
    print('FIELD VALUES:',vals)
    print('DONE (no GO issued; if a row persisted it is unconfirmed/expirable).')
    b.close()
