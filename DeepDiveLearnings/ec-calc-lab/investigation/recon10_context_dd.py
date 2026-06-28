"""Phase-2 recon (READ-ONLY): Create Calculation context dd options + post-GO panels. Never saves."""
from playwright.sync_api import sync_playwright
import os
EC_URL='https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/'
def wa(pg,t=15000): pg.wait_for_load_state('networkidle',timeout=t); pg.wait_for_timeout(1200)
with sync_playwright() as p:
    b=p.chromium.launch(headless=True,args=['--ignore-certificate-errors'])
    pg=b.new_context(ignore_https_errors=True,viewport={'width':1920,'height':1080}).new_page()
    pg.goto(EC_URL,wait_until='domcontentloaded',timeout=30000)
    pg.fill('#username','sysadmin'); pg.fill('#password','sysadmin'); pg.click('#kc-login')
    pg.wait_for_url('**/dashboard**',timeout=60000); wa(pg)
    si=pg.locator(r'#menu\:searchForm\:searchTxt'); si.wait_for(state='visible',timeout=10000)
    si.clear(); si.type('Create Calculation',delay=50); pg.wait_for_load_state('networkidle',timeout=8000); pg.wait_for_timeout(700)
    pg.locator("xpath=//*[contains(@class,'tv-link') and normalize-space(text())='Create Calculation']").first.click(); wa(pg)
    # open the G:1 context dd
    btn='nav:form:G:1:R:1:C:0:dd_button'
    pg.locator(f'#{btn.replace(":",chr(92)+":")}').click(); pg.wait_for_timeout(1200)
    opts=pg.evaluate("""() => Array.from(document.querySelectorAll("[id$=':dd_panel'] tr")).map(tr=>tr.getAttribute('data-item-label')).filter(Boolean)""")
    print("context dd options:",opts)
    print("\nDONE (read-only; nothing saved).")
    b.close()
