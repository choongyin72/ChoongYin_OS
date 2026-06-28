"""Phase-1 (READ-ONLY UI): find the calc RUN trigger. Open Calculation Set + Calculation Equation
screens, dump toolbar actions / buttons (looking for Run/Calculate/Submit). Never saves."""
from playwright.sync_api import sync_playwright
import os
EC_URL=os.environ.get('EC_URL','https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/')
EC_USER=os.environ.get('EC_USER','sysadmin'); EC_PASS=os.environ.get('EC_PASS','sysadmin')
def wa(pg,t=15000): pg.wait_for_load_state('networkidle',timeout=t); pg.wait_for_timeout(1000)
def explore(pg, screen):
    si=pg.locator(r'#menu\:searchForm\:searchTxt'); si.wait_for(state='visible',timeout=10000)
    si.clear(); si.type(screen,delay=50); pg.wait_for_load_state('networkidle',timeout=8000); pg.wait_for_timeout(500)
    link=pg.locator(f"xpath=//*[self::label or self::span][contains(@class,'tv-link') and normalize-space(text())='{screen}']")
    if link.count()==0: print(f"  [{screen}] tv-link NOT found"); return
    link.first.click(); wa(pg)
    lbl=pg.locator(r'#screenToolbar\:form\:screenLabel').text_content(timeout=5000)
    # dump toolbar action titles + any button text containing run/calc/submit/process
    acts=pg.evaluate("""() => {
       const out=[];
       document.querySelectorAll("a[title], button[title], a.ui-button, button").forEach(e=>{
         const t=(e.getAttribute('title')||e.textContent||'').trim();
         if(t && /run|calc|submit|process|execute|perform|schedul/i.test(t)) out.push(t.slice(0,40));
       });
       return [...new Set(out)].slice(0,20);
    }""")
    print(f"  [{lbl}] run-ish actions: {acts}")
with sync_playwright() as p:
    b=p.chromium.launch(headless=True,args=['--ignore-certificate-errors'])
    pg=b.new_context(ignore_https_errors=True,viewport={'width':1920,'height':1080}).new_page()
    pg.goto(EC_URL,wait_until='domcontentloaded',timeout=30000)
    pg.fill('#username',EC_USER); pg.fill('#password',EC_PASS); pg.click('#kc-login')
    pg.wait_for_url('**/dashboard**',timeout=60000); wa(pg)
    for s in ("Calculation Set","Calculation Sets (All)","Merged Calculation Jobs"):
        try: explore(pg,s)
        except Exception as e: print(f"  [{s}] ERR {str(e)[:50]}")
    print("DONE (read-only).")
    b.close()
