"""N2: try to get a SUCCESS allocation exit (Simulate ON = no DB write). Network 'Testing allocation
RUN_NO' + calc 'RUN_NO_TEST' (effective 2003-01-01). Read log_list exit status + any log/error.
ProdAllocButton:form:B."""
import time, json
from playwright.sync_api import sync_playwright
URL="https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"; SCREEN="Daily Allocation"; DATE="2003-01-01"
def opts(fr,g):
    try:
        fr.locator(f'[id="nav:form:G:{g}:R:1:C:0:dd_button"]').click(timeout=4000); time.sleep(0.9)
        return fr.evaluate(f"""()=>[...document.querySelectorAll('[id="nav:form:G:{g}:R:1:C:0:dd_panel"] tr[data-item-label]')].map(e=>(e.getAttribute('data-item-label')||'').trim()).filter(t=>t)""")
    except Exception: return []
def pick(fr,g,label):
    try: fr.locator(f'[id="nav:form:G:{g}:R:1:C:0:dd_panel"] tr[data-item-label="{label}"]').first.click(timeout=4000); time.sleep(1.3); return True
    except Exception: return False
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
    for g in (0,1):
        di=fr.locator(f'[id="nav:form:G:{g}:R:1:C:0:da_input"]'); di.fill(DATE); di.press("Tab"); time.sleep(1.0)
    g2=opts(fr,2); print("networks:", [x for x in g2 if "RUN_NO" in x or "Testing" in x] or g2[:6])
    net=next((x for x in g2 if "RUN_NO" in x or "Testing alloc" in x), None)
    if not net: print("test network not in list:", g2);
    pick(fr,2, net or (g2[0] if g2 else ""))
    opts(fr,3); g4=opts(fr,4); print("calc jobs:", g4)
    pick(fr,4, next((x for x in g4 if "RUN_NO" in x.upper() or "TEST" in x.upper()), (g4[0] if g4 else "")))
    fr.locator('[id="button:form:B"]').click(timeout=5000); page.wait_for_load_state("networkidle",timeout=30000); time.sleep(2.0)
    # Simulate ON
    chk=fr.evaluate("""()=>{const lbl=[...document.querySelectorAll('*')].find(e=>e.children.length===0&&(e.textContent||'').trim()==='Simulate'); if(!lbl)return 'no-label'; let s=lbl.closest('td,div,span')||lbl.parentElement; for(let i=0;i<4&&s;i++){const box=s.querySelector('.ui-chkbox-box,input[type=checkbox]'); if(box){box.click();return 'checked';} s=s.parentElement;} return 'no-box';}""")
    print("Simulate:", chk); time.sleep(0.8)
    fr.locator('[id="ProdAllocButton:form:B"]').click(timeout=6000); print("RUN clicked")
    page.wait_for_load_state("networkidle",timeout=90000); time.sleep(8.0)
    res=fr.evaluate("""()=>{const l=document.getElementById('log_list:form:T_data'); const r=document.getElementById('RunningJobs:form:T_data');
      const body=(document.body.innerText||''); const st=(body.match(/(Success|Failure|Completed|Error|Waiting)[^\\n]{0,30}/gi)||[]).slice(0,6);
      return {log:(l?(l.innerText||'').replace(/\\s+/g,' ').slice(0,260):''), running:(r?(r.innerText||'').replace(/\\s+/g,' ').slice(0,120):''), st};}""")
    print("log_list:", res["log"]); print("RunningJobs:", res["running"]); print("status:", json.dumps(res["st"]))
    page.screenshot(path="c:/Projects/ChoongYin_OS/tmp/alloc_runno_sim.png", full_page=True)
    b.close()
print("DONE")
