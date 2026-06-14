"""N3 crack: set From/To date, open G:2 scope dd (dump options), pick one, GO, then dump the populated
statusProcess grid (process rows + how to select) + RUN button + Simulate + log/running grids.
Read-only EXCEPT it does NOT click RUN (structure only). Tries dates 2003-01-01 (113 P wells) and
2021-10-01 fallback."""
import time, json
from playwright.sync_api import sync_playwright
URL="https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"; SCREEN="Daily Data Status Processes"

def opts(fr,g):
    try:
        fr.locator(f'[id="nav:form:G:{g}:R:1:C:0:dd_button"]').click(timeout=4000); time.sleep(0.9)
        labs=fr.evaluate(f"""()=>[...document.querySelectorAll('[id="nav:form:G:{g}:R:1:C:0:dd_panel"] tr[data-item-label]')].map(e=>(e.getAttribute('data-item-label')||'')).filter(t=>t.trim())""")
        return labs
    except Exception as e: return [f"ERR {e}"]

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
    DATE="2003-01-01"
    for g in (0,1):
        di=fr.locator(f'[id="nav:form:G:{g}:R:1:C:0:da_input"]'); di.fill(DATE); di.press("Tab"); time.sleep(0.8)
    g2=opts(fr,2)
    print("G:2 options:", json.dumps(g2[:25]))
    if g2 and not str(g2[0]).startswith("ERR"):
        target=g2[0]
        try:
            fr.locator(f'[id="nav:form:G:2:R:1:C:0:dd_panel"] tr[data-item-label="{target}"]').first.click(timeout=4000); time.sleep(1.2)
            print("picked G:2 =", repr(target))
        except Exception as e: print("pick G2 err:", str(e)[:80])
    try:
        fr.locator('[id="button:form:B"]').click(timeout=6000); page.wait_for_load_state("networkidle",timeout=30000); time.sleep(3.0)
        print("GO clicked")
    except Exception as e: print("GO err:", str(e)[:80])

    res=fr.evaluate("""()=>{
      const grid=[...document.querySelectorAll('[id^="statusProcess:form:T"] tr, [id^="statusProcess:form"] table tr')]
        .map(tr=>({id:tr.id||'', cells:[...tr.querySelectorAll('td,th')].map(td=>(td.textContent||'').trim()).filter(Boolean).slice(0,7)}))
        .filter(r=>r.cells.length).slice(0,30);
      const body=(document.body.innerText||'').replace(/\\s+/g,' ');
      const procHits=['P3_VERIFY_FCTY','Verify P3','VER_ONS_FCTY','Verify daily Onshore','P1_FwdUpd','P1FctyAlloc','Verify','Approve','Reverse'].filter(n=>body.includes(n));
      const runbtns=[...document.querySelectorAll('a[id],button[id]')].map(e=>({id:e.id,title:e.getAttribute('title')||'',t:(e.textContent||'').trim().slice(0,26)}))
        .filter(x=>/run|verif|approv|execut|start|process|play|status/i.test(x.title+' '+x.t) && !/searchForm|treeView|tabPanel/.test(x.id)).slice(0,25);
      const tdata=[...document.querySelectorAll('[id$="_data"]')].map(e=>({id:e.id,rows:e.querySelectorAll('tr').length}));
      const sims=[...document.querySelectorAll('input[type=checkbox]')].map(e=>({id:e.id,checked:e.checked,name:(e.closest('[id]')||{}).id||''})).slice(0,12);
      return {grid, procHits, runbtns, tdata, sims};
    }""")
    print("\nstatusProcess grid rows:")
    for r in res["grid"]: print("   ", json.dumps(r))
    print("\nprocess-name hits in body:", json.dumps(res["procHits"]))
    print("\n*_data containers+rows:", json.dumps(res["tdata"]))
    print("\ncheckboxes:", json.dumps(res["sims"]))
    print("\nrun-ish buttons:")
    for x in res["runbtns"]: print("   ", json.dumps(x))
    page.screenshot(path="c:/Projects/ChoongYin_OS/tmp/n3_crack.png", full_page=True)
    b.close()
print("DONE")
