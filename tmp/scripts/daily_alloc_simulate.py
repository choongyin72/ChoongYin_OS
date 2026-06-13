"""Try SIMULATE mode on HA.0002 (likely the synchronous run path — no executor). Check the Simulate
box, set Log Level to a detailed level, RUN CALCULATIONS, and read the result/log in-session (NO
refresh, to keep context). P1 Dashboard + Daily Well Volume @ 2021-10-01."""
import time, json
from playwright.sync_api import sync_playwright
URL="https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"; SCREEN="Daily Allocation"; DATE="2021-10-01"
def opts(fr,g):
    try:
        fr.locator(f'[id="nav:form:G:{g}:R:1:C:0:dd_button"]').click(timeout=4000); time.sleep(0.9)
        return fr.evaluate(f"""()=>[...document.querySelectorAll('[id="nav:form:G:{g}:R:1:C:0:dd_panel"] tr[data-item-label]')].map(e=>(e.getAttribute('data-item-label')||'').trim()).filter(t=>t)""")
    except Exception: return []
def pick(fr,g,label):
    try: fr.locator(f'[id="nav:form:G:{g}:R:1:C:0:dd_panel"] tr[data-item-label="{label}"]').first.click(timeout=4000); time.sleep(1.3)
    except Exception: pass
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
    g2=opts(fr,2); pick(fr,2,"P1 Dashboard" if "P1 Dashboard" in g2 else (g2[0] if g2 else ""))
    opts(fr,3); g4=opts(fr,4); pick(fr,4, next((x for x in g4 if "Volume" in x), g4[0] if g4 else ""))
    fr.locator('[id="button:form:B"]').click(timeout=5000); page.wait_for_load_state("networkidle",timeout=30000); time.sleep(2.0)
    # find + check the Simulate checkbox (PrimeFaces ui-chkbox near the 'Simulate' label)
    chk=fr.evaluate("""()=>{
      const lbl=[...document.querySelectorAll('*')].find(e=>e.children.length===0 && (e.textContent||'').trim()==='Simulate');
      if(!lbl) return null;
      // search siblings/ancestor for a ui-chkbox-box or input checkbox
      let scope=lbl.closest('td,div,span')||lbl.parentElement;
      for(let up=0; up<4 && scope; up++){ const box=scope.querySelector('.ui-chkbox-box, input[type=checkbox]'); if(box){ box.click(); return {clicked:true, cls:box.className||box.type}; } scope=scope.parentElement; }
      return {clicked:false};
    }""")
    print("Simulate checkbox:", json.dumps(chk)); time.sleep(1.0)
    # RUN
    fr.locator('[id="ProdAllocButton:form:B"]').click(timeout=6000); print("Run Calculations clicked (simulate)")
    page.wait_for_load_state("networkidle",timeout=90000); time.sleep(8.0)
    res=fr.evaluate("""()=>{
      const g=id=>{const t=document.getElementById(id);return t?(t.innerText||'').replace(/\\s+/g,' ').slice(0,220):null;};
      const msgs=[...document.querySelectorAll('.ui-growl-item,.ui-messages-error,.ui-messages-info,.ui-dialog:not([style*=\"display: none\"])')].map(e=>(e.innerText||'').trim()).filter(Boolean);
      const body=(document.body.innerText||''); const st=(body.match(/(Completed|Success|Failed|Error|Running|Waiting|Simulat)[^\\n]{0,30}/gi)||[]).slice(0,8);
      return {running:g('RunningJobs:form:T_data'), log:g('log_list:form:T_data'), msgs, statusHits:st};
    }""")
    print("RunningJobs:", res["running"]); print("log_list:", res["log"]); print("status hits:", json.dumps(res["statusHits"])); print("msgs:", json.dumps(res["msgs"])[:300])
    page.screenshot(path="c:/Projects/ChoongYin_OS/tmp/ha0002_simulate.png", full_page=True)
    b.close()
print("DONE")
