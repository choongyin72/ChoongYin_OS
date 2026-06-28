"""Phase-2 recon (READ-ONLY): Create Calculation -> date+context+GO -> map the calc-header create gesture.
Never saves (no calc created)."""
from playwright.sync_api import sync_playwright
import os
EC_URL=os.environ.get('EC_URL','https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/')
def wa(pg,t=20000): pg.wait_for_load_state('networkidle',timeout=t); pg.wait_for_timeout(1200)
def cell(s): return '#'+s.replace(':',r'\:')
with sync_playwright() as p:
    b=p.chromium.launch(headless=True,args=['--ignore-certificate-errors'])
    pg=b.new_context(ignore_https_errors=True,viewport={'width':1920,'height':1080}).new_page()
    pg.goto(EC_URL,wait_until='domcontentloaded',timeout=30000)
    pg.fill('#username','sysadmin'); pg.fill('#password','sysadmin'); pg.click('#kc-login')
    pg.wait_for_url('**/dashboard**',timeout=60000); wa(pg)
    si=pg.locator(r'#menu\:searchForm\:searchTxt'); si.wait_for(state='visible',timeout=10000)
    si.clear(); si.type('Create Calculation',delay=50); pg.wait_for_load_state('networkidle',timeout=8000); pg.wait_for_timeout(700)
    pg.locator("xpath=//*[contains(@class,'tv-link') and normalize-space(text())='Create Calculation']").first.click(); wa(pg)
    # set date
    d='nav:form:G:0:R:1:C:0:da_input'
    pg.locator(cell(d)).click(); pg.locator(cell(d)).fill('2003-01-01'); pg.keyboard.press('Tab'); pg.wait_for_timeout(800)
    # set context = Production Allocation
    pg.locator(cell('nav:form:G:1:R:1:C:0:dd_button')).click(); pg.wait_for_timeout(1000)
    pg.locator("xpath=//*[@id='nav:form:G:1:R:1:C:0:dd_panel']//tr[normalize-space(@data-item-label)='Production Allocation']").first.click(); wa(pg)
    # GO
    pg.locator(cell('button:form:B')).click(); wa(pg)
    print("after GO. calculation panel + toolbar actions:")
    # toolbar New/Insert actions
    acts=pg.evaluate("""() => Array.from(document.querySelectorAll("a[title],button[title]")).map(e=>e.getAttribute('title')).filter(t=>t && /new|insert|create|add|delete|save/i.test(t)).slice(0,15)""")
    print("  toolbar:",sorted(set(acts)))
    # calculation:form grid + any editable header fields
    grids=pg.evaluate("""()=>Array.from(document.querySelectorAll("tbody[id$='_data'], div[id*='calculation:form']")).map(e=>e.id).slice(0,10)""")
    print("  calc panels:",grids)
    flds=pg.evaluate("""()=>Array.from(document.querySelectorAll("[id*='calculation:form'] input, [id*='calculation:form'] select, [id*='calculation:form'][id$='dd_button']")).map(e=>e.id).slice(0,20)""")
    print("  calculation:form field ids:",flds)
    print("DONE (read-only; no calc created).")
    b.close()
