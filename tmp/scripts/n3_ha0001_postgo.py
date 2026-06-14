"""N3 make-or-break: on HA.0001, set From/To date, GO, then dump the statusProcess:form (process
selector + RUN button), dateStartJob (Simulate?), and any log/running grids. NO run fired (read-only
structure dump). Resolves: synchronous RUN (buildable now) vs BPM dispatch (executor stall risk)."""
import time, json
from playwright.sync_api import sync_playwright
URL="https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"; SCREEN="Daily Data Status Processes"
DATE="2003-01-01"

with sync_playwright() as p:
    b=p.chromium.launch(headless=True); page=b.new_context(ignore_https_errors=True,viewport={"width":1680,"height":1000}).new_page()
    page.goto(URL,wait_until="domcontentloaded",timeout=60000)
    page.fill('[id="username"]',"sysadmin"); page.fill('[id="password"]',"sysadmin"); page.click('[id="kc-login"]')
    page.wait_for_selector('[id="menu:searchForm:searchTxt"]',timeout=60000)
    sel=f'xpath=//*[contains(@class,"tv-link") and normalize-space(text())="{SCREEN}"]'; fr=None
    for _ in range(3):
        page.fill('[id="menu:searchForm:searchTxt"]',""); page.locator('[id="menu:searchForm:searchTxt"]').type(SCREEN,delay=40)
        try: page.wait_for_selector(sel,timeout=12000)
        except Exception: pass
        time.sleep(0.6)
        try: page.locator(sel).first.click()
        except Exception: continue
        page.wait_for_load_state("networkidle",timeout=30000)
        for _ in range(20):
            fr=next((f for f in page.frames if "dashboard.jsf" in f.url and "top=false" in f.url),None)
            if fr: break
            time.sleep(1.0)
        if fr: break
    if not fr: print("NOT LOADED"); b.close(); raise SystemExit
    time.sleep(2.0)
    # set both dates + GO
    for g in (0,1):
        di=fr.locator(f'[id="nav:form:G:{g}:R:1:C:0:da_input"]')
        try: di.fill(DATE); di.press("Tab"); time.sleep(0.8)
        except Exception as e: print(f"date G{g} err:", str(e)[:80])
    try:
        fr.locator('[id="button:form:B"]').click(timeout=6000); page.wait_for_load_state("networkidle",timeout=30000); time.sleep(2.5)
        print("GO clicked")
    except Exception as e: print("GO err:", str(e)[:100])

    dump=fr.evaluate("""()=>{
      const pick=(pred)=>[...document.querySelectorAll('[id]')].filter(pred).map(e=>({id:e.id,tag:e.tagName,cls:(e.className||'').slice(0,40),t:(e.textContent||'').trim().slice(0,30)}));
      const sp = pick(e=>e.id.startsWith('statusProcess:form')).slice(0,40);
      const dj = pick(e=>e.id.startsWith('dateStartJob:form')).slice(0,30);
      const grids = [...document.querySelectorAll('[id$=":T_data"]')].map(e=>({id:e.id, rows:e.querySelectorAll('tr').length}));
      // dropdown panels / option rows in statusProcess
      const ddopts = [...document.querySelectorAll('[id^="statusProcess:form"] tr[data-item-label]')].map(e=>e.getAttribute('data-item-label')).slice(0,20);
      // any button whose text looks like a run trigger
      const runbtns = [...document.querySelectorAll('a,button')].map(e=>({id:e.id,t:(e.textContent||'').trim()})).filter(x=>/run|verif|approv|execut|process|start/i.test(x.t) && x.t.length<40).slice(0,20);
      const simchk = [...document.querySelectorAll('input[type=checkbox],[id*=imulate]')].map(e=>({id:e.id,checked:e.checked})).slice(0,10);
      return {sp, dj, grids, ddopts, runbtns, simchk};
    }""")
    print("\nstatusProcess:form elements:")
    for x in dump["sp"]: print("   ", json.dumps(x))
    print("\nstatusProcess dropdown options:", json.dumps(dump["ddopts"]))
    print("\ndateStartJob:form elements:")
    for x in dump["dj"]: print("   ", json.dumps(x))
    print("\ncheckboxes / simulate:", json.dumps(dump["simchk"]))
    print("\ngrids (T_data + rows):", json.dumps(dump["grids"]))
    print("\nrun-trigger buttons:", json.dumps(dump["runbtns"]))
    page.screenshot(path="c:/Projects/ChoongYin_OS/tmp/n3_ha0001_postgo.png", full_page=True)
    b.close()
print("DONE")
