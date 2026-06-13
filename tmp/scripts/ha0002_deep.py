"""HA.0002 Daily Allocation — deeper READ-ONLY recon: dump the nav dropdown options (Allocation
Network Group/Network, Allocation Network, Calculation Job) and, after selecting a network + a
recent date + GO, observe what appears (a Run/Calculate action? a results grid? toolbar actions).
Does NOT run a calc yet — just maps the run mechanism + finds real network/job names."""
import time, json
from playwright.sync_api import sync_playwright
URL="https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"; SCREEN="Daily Allocation"
def dd_opts(fr,g):
    try:
        fr.locator(f'[id="nav:form:G:{g}:R:1:C:0:dd_button"]').click(timeout=4000); time.sleep(0.8)
        o=fr.evaluate(f"""()=>[...document.querySelectorAll('[id="nav:form:G:{g}:R:1:C:0:dd_panel"] tr[data-item-label]')].map(e=>(e.getAttribute('data-item-label')||'').trim()).filter(t=>t)""")
        fr.locator(f'[id="nav:form:G:{g}:R:1:C:0:dd_button"]').click(timeout=2000); time.sleep(0.2)
        return o
    except Exception as e:
        return [f"ERR {str(e)[:40]}"]
with sync_playwright() as p:
    b=p.chromium.launch(headless=True); page=b.new_context(ignore_https_errors=True,viewport={"width":1680,"height":1000}).new_page()
    page.goto(URL,wait_until="domcontentloaded",timeout=60000)
    page.fill('[id="username"]',"sysadmin"); page.fill('[id="password"]',"sysadmin"); page.click('[id="kc-login"]')
    page.wait_for_selector('[id="menu:searchForm:searchTxt"]',timeout=60000)
    sel='xpath=//*[contains(@class,"tv-link") and normalize-space(text())="Daily Allocation"]'; fr=None
    for _ in range(3):
        page.fill('[id="menu:searchForm:searchTxt"]',""); page.locator('[id="menu:searchForm:searchTxt"]').type(SCREEN,delay=40)
        try: page.wait_for_selector(sel,timeout=12000)
        except Exception: pass
        time.sleep(0.6)
        try: page.locator(sel).first.click()
        except Exception: continue
        page.wait_for_load_state("networkidle",timeout=30000)
        for _ in range(25):
            fr=next((f for f in page.frames if "edit_daily_alloc" in f.url),None)
            if fr: break
            time.sleep(1.0)
        if fr: break
    if not fr: print("NOT LOADED"); b.close(); raise SystemExit
    time.sleep(2.0)
    print("URL:", fr.url)
    print("G2 (Network Group/Network):", dd_opts(fr,2)[:15])
    print("G3 (Allocation Network):", dd_opts(fr,3)[:15])
    print("G4 (Calculation Job):", dd_opts(fr,4)[:15])
    # toolbar actions available (run/calculate live in the toolbar menu typically)
    tb=page.evaluate("""()=>[...document.querySelectorAll('a[title],button[title]')].filter(e=>e.offsetParent)
        .map(e=>({title:e.title})).filter(x=>x.title && !/logout/i.test(x.title))""")
    print("toolbar titles:", json.dumps([t["title"] for t in tb]))
    b.close()
print("DONE")
