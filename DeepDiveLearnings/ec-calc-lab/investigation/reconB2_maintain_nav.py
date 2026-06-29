"""SCAN (READ-ONLY): Maintain Calculation nav fields - identify the 'Calculation' selector to pick AUTOTEST_CALC_TEST."""
from playwright.sync_api import sync_playwright
import os
EC_URL=os.environ.get('EC_URL','https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/')
def wa(pg,t=20000): pg.wait_for_load_state('networkidle',timeout=t); pg.wait_for_timeout(1200)
with sync_playwright() as p:
    b=p.chromium.launch(headless=True,args=['--ignore-certificate-errors'])
    pg=b.new_context(ignore_https_errors=True,viewport={'width':1920,'height':1080}).new_page()
    pg.goto(EC_URL,wait_until='domcontentloaded',timeout=30000)
    pg.fill('#username','sysadmin'); pg.fill('#password','sysadmin'); pg.click('#kc-login')
    pg.wait_for_url('**/dashboard**',timeout=60000); wa(pg)
    si=pg.locator(r'#menu\:searchForm\:searchTxt'); si.wait_for(state='visible',timeout=10000)
    si.clear(); si.type('Maintain Calculation',delay=50); pg.wait_for_load_state('networkidle',timeout=8000); pg.wait_for_timeout(700)
    pg.locator("xpath=//*[contains(@class,'tv-link') and normalize-space(text())='Maintain Calculation']").first.click(); wa(pg)
    nav=pg.evaluate("""()=>{
      const labs=[...document.querySelectorAll('label,th,span')].map(e=>e.textContent.trim()).filter(t=>t&&t.length<30&&/date|context|calculation/i.test(t)).slice(0,8);
      const fields=[...document.querySelectorAll("[id^='nav:form'] input, [id^='nav:form'][id$='dd_button'], [id^='nav:form'][id$='_button']")].map(e=>({id:e.id,type:e.type||e.tagName,ph:e.placeholder||''}));
      return {labs:[...new Set(labs)], fields};
    }""")
    print("nav labels:",nav['labs'])
    print("nav fields:")
    for f in nav['fields']: print("   ",f)
    b.close()
