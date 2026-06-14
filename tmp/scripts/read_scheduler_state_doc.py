"""Extract the EC_SCHEDULER_STARTUPSTATE + EC_SCHEDULER_THREADCOUNT definitions (states/meaning) from
ec-ec-app.html, and any 'Runtime resource settings'/'replicas'/horizontal-scaling text. Authenticated."""
import time, json
from playwright.sync_api import sync_playwright
URL="https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"
DOC="https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/containers/ec-ec-app.html"
with sync_playwright() as p:
    b=p.chromium.launch(headless=True); page=b.new_context(ignore_https_errors=True,viewport={"width":1400,"height":1000}).new_page()
    page.goto(URL,wait_until="domcontentloaded",timeout=60000)
    try:
        page.wait_for_selector('[id="username"]',timeout=15000); page.fill('[id="username"]',"sysadmin"); page.fill('[id="password"]',"sysadmin"); page.click('[id="kc-login"]'); page.wait_for_load_state("networkidle",timeout=30000)
    except Exception: pass
    time.sleep(1.0)
    page.goto(DOC,wait_until="domcontentloaded",timeout=60000); page.wait_for_load_state("networkidle",timeout=30000); time.sleep(1.5)
    # Grab text windows around the key tokens
    for tok in ["SCHEDULER_STARTUPSTATE","SCHEDULER_THREADCOUNT","SERVER_STATE","Runtime resource"]:
        txt=page.evaluate(f"""()=>{{const full=document.body.innerText||''; const i=full.indexOf('{tok}'); if(i<0)return ''; return full.slice(Math.max(0,i-260), i+360);}}""")
        print(f"=== around '{tok}' ==="); print(txt.strip()[:620]); print("----")
    b.close()
print("DONE")
