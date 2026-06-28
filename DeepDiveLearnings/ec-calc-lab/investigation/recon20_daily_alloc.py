"""Recon (READ-ONLY) the Daily Allocation screen: nav field ids + Log Level dd + Simulate checkbox + RUN button.
Opens + captures; does NOT click RUN."""
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
    si.clear(); si.type('Daily Allocation',delay=50); pg.wait_for_load_state('networkidle',timeout=8000); pg.wait_for_timeout(700)
    link=pg.locator("xpath=//*[contains(@class,'tv-link') and normalize-space(text())='Daily Allocation']")
    print("Daily Allocation tv-link:",link.count())
    link.first.click(); wa(pg)
    # capture all nav inputs/dds + labels, the Log Level + Simulate + RUN button
    info=pg.evaluate("""()=>{
      const ins=[...document.querySelectorAll("input[id^='nav:form'], [id^='nav:form'][id$='dd_button'], [id^='nav:form'] select")].map(e=>({id:e.id,type:e.type||e.tagName}));
      const cb=[...document.querySelectorAll("input[type='checkbox'], .ui-chkbox-box")].map(e=>e.id||e.className).slice(0,8);
      const btns=[...document.querySelectorAll('button,a.ui-button,a[title]')].map(e=>({id:e.id,t:(e.textContent||e.getAttribute('title')||'').trim().slice(0,28)})).filter(x=>x.t && /run|go|ok|view|download|simulate/i.test(x.t)).slice(0,12);
      const dds=[...document.querySelectorAll("[id^='nav:form'][id$='dd_button']")].map(e=>e.id);
      return {inputs:ins.slice(0,20), checkboxes:cb, buttons:btns, dds};
    }""")
    print("nav inputs:",info['inputs'])
    print("dd buttons:",info['dds'])
    print("checkboxes:",info['checkboxes'])
    print("buttons:",info['buttons'])
    b.close()
