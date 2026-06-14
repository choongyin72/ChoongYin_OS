"""Read the EC tech-doc 'BPM settings' section of ec-ec-app.html via an AUTHENTICATED browser
(same Keycloak login used all session). Dumps the section text + every env var / setting it lists."""
import time, json
from playwright.sync_api import sync_playwright
URL="https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"
DOC="https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/containers/ec-ec-app.html"

with sync_playwright() as p:
    b=p.chromium.launch(headless=True); page=b.new_context(ignore_https_errors=True,viewport={"width":1400,"height":1000}).new_page()
    page.goto(URL,wait_until="domcontentloaded",timeout=60000)
    # login if presented
    try:
        page.wait_for_selector('[id="username"]',timeout=15000)
        page.fill('[id="username"]',"sysadmin"); page.fill('[id="password"]',"sysadmin"); page.click('[id="kc-login"]')
        page.wait_for_load_state("networkidle",timeout=30000)
    except Exception:
        pass
    time.sleep(1.0)
    page.goto(DOC, wait_until="domcontentloaded", timeout=60000)
    page.wait_for_load_state("networkidle", timeout=30000); time.sleep(1.5)
    title = page.title()
    print("PAGE TITLE:", title)
    # full text + the BPM settings section specifically
    res = page.evaluate("""()=>{
      const full=(document.body.innerText||'');
      // find a heading containing 'BPM' and capture text until the next heading of same/higher level
      const heads=[...document.querySelectorAll('h1,h2,h3,h4,h5')];
      let out=[];
      heads.forEach((h,i)=>{
        if(/bpm/i.test(h.textContent||'')){
          let txt=h.textContent.trim()+"\\n";
          let n=h.nextElementSibling;
          let guard=0;
          while(n && !/^H[1-5]$/.test(n.tagName) && guard<60){ txt+=(n.innerText||n.textContent||'')+"\\n"; n=n.nextElementSibling; guard++; }
          out.push(txt);
        }
      });
      // also list all env-var-looking tokens in the page
      const envs=[...new Set((full.match(/[A-Z][A-Z0-9_]{4,}/g)||[]).filter(x=>/BPM|SCHEDULER|WORKER|CLIENT_SECRET|EC_URL|KIE|JBPM/.test(x)))];
      return {sections: out, envTokens: envs, allHeadings: heads.map(h=>h.textContent.trim()).slice(0,60)};
    }""")
    print("\n=== HEADINGS ON PAGE ===")
    print(json.dumps(res["allHeadings"], indent=1))
    print("\n=== BPM-RELATED SECTION(S) ===")
    for s in res["sections"]:
        print(s[:2500]); print("----")
    print("\n=== BPM/scheduler/worker env tokens found ===")
    print(json.dumps(res["envTokens"]))
    b.close()
print("DONE")
