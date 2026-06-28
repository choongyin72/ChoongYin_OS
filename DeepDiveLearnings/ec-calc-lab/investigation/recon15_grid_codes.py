"""Phase-2 recon (READ-ONLY): list the EC_PROD calc grid rows on Create Calculation to pick a copy source. No save."""
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
    d='nav:form:G:0:R:1:C:0:da_input'
    pg.locator(cell(d)).click(); pg.locator(cell(d)).fill('2003-01-01'); pg.keyboard.press('Tab'); pg.wait_for_timeout(800)
    pg.locator(cell('nav:form:G:1:R:1:C:0:dd_button')).click(); pg.wait_for_timeout(1000)
    pg.locator("xpath=//*[@id='nav:form:G:1:R:1:C:0:dd_panel']//tr[normalize-space(@data-item-label)='Production Allocation']").first.click(); wa(pg)
    pg.locator(cell('button:form:B')).click(); wa(pg)
    # dump grid rows: each row's visible cell text
    rows=pg.evaluate("""()=>{const t=document.getElementById('calculation:form:T_data');if(!t)return[];return Array.from(t.querySelectorAll('tr')).map(tr=>Array.from(tr.querySelectorAll('td input, td')).map(td=>(td.value||td.textContent||'').trim()).filter(Boolean).slice(0,4).join(' | ')).filter(Boolean).slice(0,25);}""")
    print(f"EC_PROD calc grid rows ({len(rows)}):")
    for r in rows: print("  ",r[:90])
    print("DONE (read-only).")
    b.close()
