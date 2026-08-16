"""Deep-dive EC docs on ec-worker / background service / scheduler. Authenticated browser.
(1) ec-ec-app.html: extract Scheduler-related sections (EC_SCHEDULER_STARTUPSTATE/THREADCOUNT) + any
worker/background/standby/RUNNING text. (2) scan the doc nav/index for pages about worker/scheduler/
scaling/background/high-availability and print their links."""
import time, json
from playwright.sync_api import sync_playwright
URL="https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"
DOC="https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/frmw/containers/ec-ec-app.html"
IDX="https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/doc/Energy-Components/current/technical-documentation/"
with sync_playwright() as p:
    b=p.chromium.launch(headless=True); page=b.new_context(ignore_https_errors=True,viewport={"width":1400,"height":1000}).new_page()
    page.goto(URL,wait_until="domcontentloaded",timeout=60000)
    try:
        page.wait_for_selector('[id="username"]',timeout=15000)
        page.fill('[id="username"]',"sysadmin"); page.fill('[id="password"]',"sysadmin"); page.click('[id="kc-login"]'); page.wait_for_load_state("networkidle",timeout=30000)
    except Exception: pass
    time.sleep(1.0)
    page.goto(DOC,wait_until="domcontentloaded",timeout=60000); page.wait_for_load_state("networkidle",timeout=30000); time.sleep(1.5)
    res=page.evaluate(r"""()=>{
      const heads=[...document.querySelectorAll('h1,h2,h3,h4,h5')];
      let out=[];
      heads.forEach(h=>{ if(/scheduler|worker|background|standby|cluster|node/i.test(h.textContent||'')){
        let txt=h.textContent.trim()+"\n"; let n=h.nextElementSibling,g=0;
        while(n && !/^H[1-5]$/.test(n.tagName) && g<40){ txt+=(n.innerText||n.textContent||'')+"\n"; n=n.nextElementSibling; g++; }
        out.push(txt.slice(0,1400)); } });
      const full=(document.body.innerText||'');
      const m=(full.match(/[A-Z][A-Z0-9_]{5,}/g)||[]).filter(x=>/SCHEDULER|WORKER|STARTUPSTATE|THREAD/.test(x));
      return {sections:out, tokens:[...new Set(m)]};
    }""")
    print("=== ec-ec-app.html scheduler/worker sections ===")
    for s in res["sections"]: print(s); print("----")
    print("scheduler/worker env tokens:", json.dumps(res["tokens"]))
    # scan doc index for worker/scheduler/scaling pages
    try:
        page.goto(IDX,wait_until="domcontentloaded",timeout=60000); page.wait_for_load_state("networkidle",timeout=20000); time.sleep(1.0)
        links=page.evaluate(r"""()=>[...document.querySelectorAll('a')].map(a=>({t:(a.textContent||'').trim(),h:a.getAttribute('href')||''})).filter(x=>/worker|scheduler|scal|background|high.?availab|cluster|deploy|operat/i.test(x.t+' '+x.h)).slice(0,40)""")
        print("\n=== doc links re worker/scheduler/scaling/ops ===")
        for l in links: print("  ", json.dumps(l))
    except Exception as e: print("idx err",str(e)[:80])
    b.close()
print("DONE")
