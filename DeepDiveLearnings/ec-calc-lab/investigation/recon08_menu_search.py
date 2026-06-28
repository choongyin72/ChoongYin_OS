"""Phase-1 (READ-ONLY): dump every menu tv-link matching 'Calculation' to get real runnable screen labels."""
from playwright.sync_api import sync_playwright
import os
EC_URL=os.environ.get('EC_URL','https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/')
def wa(pg,t=15000): pg.wait_for_load_state('networkidle',timeout=t); pg.wait_for_timeout(1200)
with sync_playwright() as p:
    b=p.chromium.launch(headless=True,args=['--ignore-certificate-errors'])
    pg=b.new_context(ignore_https_errors=True,viewport={'width':1920,'height':1080}).new_page()
    pg.goto(EC_URL,wait_until='domcontentloaded',timeout=30000)
    pg.fill('#username','sysadmin'); pg.fill('#password','sysadmin'); pg.click('#kc-login')
    pg.wait_for_url('**/dashboard**',timeout=60000); wa(pg)
    for term in ("Calculation","Calc","Maintain Calc"):
        si=pg.locator(r'#menu\:searchForm\:searchTxt'); si.wait_for(state='visible',timeout=10000)
        si.clear(); si.type(term,delay=50); pg.wait_for_load_state('networkidle',timeout=8000); pg.wait_for_timeout(800)
        links=pg.evaluate("""() => Array.from(document.querySelectorAll(".tv-link")).map(e=>e.textContent.trim()).filter(Boolean)""")
        print(f"[search '{term}'] {len(links)} tv-links:")
        for l in sorted(set(links))[:30]: print("   ",l)
        print()
    b.close()
