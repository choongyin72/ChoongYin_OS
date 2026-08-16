"""Recon HA.0002 Daily Allocation (READ-ONLY): find the screen, dump URL/CLASS_NAME, navigator
(date/scope), the RUN/Calculate trigger button(s), and any result grids. Does NOT run a calc."""
import time, json
from playwright.sync_api import sync_playwright
URL="https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"
TERMS=["Daily Allocation","Daily Production Allocation"]
with sync_playwright() as p:
    b=p.chromium.launch(headless=True); page=b.new_context(ignore_https_errors=True,viewport={"width":1680,"height":1000}).new_page()
    page.goto(URL,wait_until="domcontentloaded",timeout=60000)
    page.fill('[id="username"]',"sysadmin"); page.fill('[id="password"]',"sysadmin"); page.click('[id="kc-login"]')
    page.wait_for_selector('[id="menu:searchForm:searchTxt"]',timeout=60000)
    # list what the search finds for each term
    chosen=None
    for term in TERMS:
        page.fill('[id="menu:searchForm:searchTxt"]',""); page.locator('[id="menu:searchForm:searchTxt"]').type(term,delay=40); time.sleep(1.5)
        res=page.evaluate("""()=>[...document.querySelectorAll('.tv-link')].filter(e=>e.offsetParent).map(e=>(e.textContent||'').trim()).filter(t=>t)""")
        print(f"[{term}] ->", res[:12])
        if not chosen:
            chosen=next((r for r in res if "alloc" in r.lower() and "daily" in r.lower()), None)
    print("\nchosen screen:", chosen)
    if not chosen: b.close(); raise SystemExit
    sel=f'xpath=//*[contains(@class,"tv-link") and normalize-space(text())="{chosen}"]'; fr=None
    for _ in range(3):
        page.fill('[id="menu:searchForm:searchTxt"]',""); page.locator('[id="menu:searchForm:searchTxt"]').type(chosen[:20],delay=40)
        try: page.wait_for_selector(sel,timeout=10000)
        except Exception: pass
        time.sleep(0.6)
        try: page.locator(sel).first.click()
        except Exception: continue
        page.wait_for_load_state("networkidle",timeout=30000)
        for _ in range(25):
            fr=next((f for f in page.frames if ".screens/" in f.url and "dashboard" not in f.url),None)
            if fr: break
            time.sleep(1.0)
        if fr: break
    if not fr: print("NOT LOADED"); b.close(); raise SystemExit
    time.sleep(2.0)
    print("SCREEN URL:", fr.url)
    info=fr.evaluate("""()=>{
      const lab=id=>{const e=document.getElementById(id);return e?(e.textContent||'').trim():null;};
      const groups=[]; for(let i=0;i<10;i++){const l=lab(`nav:form:G:${i}:R:0:C:0:la`); if(!l)continue;
        const dd=document.getElementById(`nav:form:G:${i}:R:1:C:0:dd_input`); const da=document.getElementById(`nav:form:G:${i}:R:1:C:0:da_input`);
        groups.push({g:i,label:l,type:dd?'dd':(da?'date':'?')});}
      const vis=e=>e&&e.offsetParent!==null;
      const buttons=[...document.querySelectorAll('a[title],button[title],a.ui-button,button.ui-button')].filter(vis)
        .map(e=>({id:e.id||'',title:e.title||'',txt:(e.textContent||'').trim().slice(0,24)}))
        .filter(x=>/run|calc|execute|start|go|process|allocat/i.test(x.id+x.title+x.txt));
      const grids=[...document.querySelectorAll('[id$="T_data"]')].filter(vis).map(t=>t.id);
      return {groups,buttons,grids};
    }""")
    print("NAV:", json.dumps(info["groups"]))
    print("RUN-ish buttons:", json.dumps(info["buttons"], indent=1))
    print("grids:", info["grids"])
    b.close()
print("DONE")
