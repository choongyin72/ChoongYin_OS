"""READ-ONLY locator recon of the 'Monthly Data Status Processes' screen (N3 monthly). Confirm nav
structure (date fields + Process dropdown options), GO button, Run button — so the T3 is built on the
REAL screen model, not a guess. NO run, NO write (stops before any Run click)."""
import time
import json
from playwright.sync_api import sync_playwright

# NOTE: this is the LOCAL SANDBOX host (ap-f0a7g341jn6d...), NOT the canonical app URL — this is a
# read-only recon throwaway, so the sandbox host is intentional. The RF suite resolves its URL from
# environment.py (EC_URL) per the repo convention; do not treat this literal as the app URL.
URL = "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"
SCREEN = "Monthly Data Status Processes"

with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    page = b.new_context(ignore_https_errors=True, viewport={"width": 1680, "height": 1000}).new_page()
    page.goto(URL, wait_until="domcontentloaded", timeout=60000)
    page.fill('[id="username"]', "sysadmin")
    page.fill('[id="password"]', "sysadmin")
    page.click('[id="kc-login"]')
    page.wait_for_selector('[id="menu:searchForm:searchTxt"]', timeout=60000)
    time.sleep(1.0)
    page.locator('[id="menu:searchForm:searchTxt"]').type(SCREEN, delay=25)
    time.sleep(1.5)
    hits = page.evaluate("""()=>[...document.querySelectorAll('.tv-link')].map(e=>e.textContent.trim()).filter(Boolean)""")
    print("search hits:", json.dumps(hits[:12]))
    sel = f'xpath=//*[contains(@class,"tv-link") and normalize-space(text())="{SCREEN}"]'
    if page.locator(sel).count() == 0:
        print("SCREEN NOT FOUND by exact name — candidates above.")
        b.close(); raise SystemExit(0)
    page.locator(sel).first.click()
    page.wait_for_load_state("networkidle", timeout=30000)
    time.sleep(2.5)
    # non-iframed family (com.ec.prod.ha) — use page directly
    fr = page
    nav = fr.evaluate(r"""()=>{
      const all=[...document.querySelectorAll('[id*="nav:form"]')];
      const labels=all.filter(e=>/:la$/.test(e.id)).map(e=>({id:e.id,t:(e.textContent||'').trim().slice(0,24)}));
      const dates=all.filter(e=>/da_input$/.test(e.id)).map(e=>e.id);
      const dds=all.filter(e=>/:dd$/.test(e.id)).map(e=>e.id);
      const btns=[...document.querySelectorAll('button,[id*="Button"],a[title]')]
        .map(e=>({id:e.id,t:(e.textContent||e.title||'').trim().slice(0,18)}))
        .filter(x=>x.id && /go|run|button|process/i.test(x.id+' '+x.t)).slice(0,12);
      return {labels,dates,dds,btns};
    }""")
    print("\nLABELS:", json.dumps(nav["labels"]))
    print("DATE FIELDS:", json.dumps(nav["dates"]))
    print("PROCESS DDs:", json.dumps(nav["dds"]))
    print("BUTTONS:", json.dumps(nav["btns"]))
    # open the process dd (likely G:2) and dump options to confirm P1_FwdUpdPar1 selectable
    for dd in nav["dds"]:
        try:
            fr.click(f'[id="{dd}_button"]', timeout=4000); time.sleep(0.7)
            opts = fr.evaluate("""(pid)=>{const p=document.getElementById(pid);if(!p)return null;
              return [...p.querySelectorAll('li,tr')].map(r=>r.getAttribute('data-item-label')).filter(Boolean).slice(0,60);}""", dd+"_panel")
            print(f"\nDD {dd} options:", json.dumps(opts))
        except Exception as e:
            print(f"\nDD {dd} err:", str(e)[:70])
    b.close()
print("DONE")
