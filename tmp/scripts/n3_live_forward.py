"""N3 FIRST LIVE RUN (forward): HA.0001, date 2003-01-01, process 'P1 Forward Status Update' (has a
reverse pair for self-clean). Set dates + pick process(G:2) + GO + click RunProcessButton:form:B.
Poll statusProcess:form:T_data for the result row (Process Name / New Status / # Rows Updated) and
RunningJobs (sync vs BPM stall). Reports the on-screen outcome; DB-verify done separately next."""
import time, json
from playwright.sync_api import sync_playwright
URL="https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"; SCREEN="Daily Data Status Processes"
DATE="2003-01-01"; PROCESS="P1 Forward Status Update"

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
    for g in (0,1):
        di=fr.locator(f'[id="nav:form:G:{g}:R:1:C:0:da_input"]'); di.fill(DATE); di.press("Tab"); time.sleep(0.8)
    # pick process in G:2
    fr.locator('[id="nav:form:G:2:R:1:C:0:dd_button"]').click(timeout=4000); time.sleep(0.9)
    fr.locator(f'[id="nav:form:G:2:R:1:C:0:dd_panel"] tr[data-item-label="{PROCESS}"]').first.click(timeout=4000); time.sleep(1.2)
    print("picked process:", PROCESS)
    fr.locator('[id="button:form:B"]').click(timeout=6000); page.wait_for_load_state("networkidle",timeout=30000); time.sleep(2.5)
    print("GO clicked")
    def loggrid():
        return fr.evaluate("""()=>{const t=document.getElementById('statusProcess:form:T_data'); if(!t)return [];
          return [...t.querySelectorAll('tr')].map(tr=>[...tr.querySelectorAll('td')].map(td=>(td.textContent||'').trim())).filter(r=>r.some(x=>x));}""")
    def running():
        return fr.evaluate("""()=>{const t=document.getElementById('RunningJobs:form:T_data'); if(!t)return '';
          return [...t.querySelectorAll('tr')].map(tr=>(tr.textContent||'').replace(/\\s+/g,' ').trim()).filter(x=>x).join(' || ').slice(0,160);}""")
    print("log BEFORE run:", json.dumps(loggrid()))
    # RUN
    fr.locator('[id="RunProcessButton:form:B"]').click(timeout=6000); print("RUN PROCESS clicked")
    for i in range(12):
        time.sleep(2.0)
        try: page.wait_for_load_state("networkidle",timeout=6000)
        except Exception: pass
        lg=loggrid(); rj=running()
        print(f"  t+{(i+1)*2:>2}s running='{rj}' log_rows={len(lg)}")
        if any(any('Rows' in str(c) or 'V' == str(c) or 'Verif' in str(c) for c in row) for row in lg) or len(lg)>1:
            break
    print("\nLOG AFTER run:")
    for row in loggrid(): print("   ", json.dumps(row))
    page.screenshot(path="c:/Projects/ChoongYin_OS/tmp/n3_live_forward.png", full_page=True)
    b.close()
print("DONE")
