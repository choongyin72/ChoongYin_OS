"""Phase-3 recon (READ-ONLY): how is a single calc RUN? Explore candidate run screens + actions. No save."""
from playwright.sync_api import sync_playwright
import os
EC_URL=os.environ.get('EC_URL','https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/')
def wa(pg,t=15000): pg.wait_for_load_state('networkidle',timeout=t); pg.wait_for_timeout(1000)
def explore(pg, screen):
    si=pg.locator(r'#menu\:searchForm\:searchTxt'); si.wait_for(state='visible',timeout=10000)
    si.clear(); si.type(screen,delay=40); pg.wait_for_load_state('networkidle',timeout=8000); pg.wait_for_timeout(500)
    link=pg.locator(f"xpath=//*[contains(@class,'tv-link') and normalize-space(text())='{screen}']")
    if link.count()==0: print(f"  [{screen}] NOT found"); return
    link.first.click(); wa(pg)
    acts=pg.evaluate("""() => [...document.querySelectorAll("a[title],button[title],button,a.ui-button")].map(e=>(e.getAttribute('title')||e.textContent||'').trim()).filter(t=>t && /run|calc|execut|submit|process|perform|start/i.test(t) && t.length<45)""")
    print(f"  [{screen}] run-ish actions: {sorted(set(acts))[:10]}")
with sync_playwright() as p:
    b=p.chromium.launch(headless=True,args=['--ignore-certificate-errors'])
    pg=b.new_context(ignore_https_errors=True,viewport={'width':1920,'height':1080}).new_page()
    pg.goto(EC_URL,wait_until='domcontentloaded',timeout=30000)
    pg.fill('#username','sysadmin'); pg.fill('#password','sysadmin'); pg.click('#kc-login')
    pg.wait_for_url('**/dashboard**',timeout=60000); wa(pg)
    for s in ("Calculation Group Setup","Calculation Group Context","Period Process Calculations","Daily Financial Item Calculation"):
        try: explore(pg,s)
        except Exception as e: print(f"  [{s}] ERR {str(e)[:40]}")
    print("DONE (read-only).")
    b.close()
