"""Submit EC_DAILY_VOLUME via RUN CALCULATIONS and POLL the RunningJobs grid (WAITING->Running->
Completed?) + DB, to learn if the job executor runs the queued allocation. ProdAllocButton:form:B.
P1 Dashboard + Daily Well Volume @ 2021-10-01."""
import time, json
import oracledb
from playwright.sync_api import sync_playwright
URL="https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"; SCREEN="Daily Allocation"; DATE="2021-10-01"
def db():
    c=oracledb.connect(user="ECKERNEL_EC",password="energy",dsn="localhost:1521/ORCL",tcp_connect_timeout=15).cursor()
    c.execute("SELECT COUNT(*), TO_CHAR(MAX(LAST_UPDATED_DATE),'HH24:MI:SS'), ROUND(SUM(ALLOC_GAS_VOL),1) FROM ECKERNEL_EC.PWEL_DAY_ALLOC WHERE TRUNC(DAYTIME)=DATE '2021-10-01'")
    return c.fetchone()
def opts(fr,g):
    try:
        fr.locator(f'[id="nav:form:G:{g}:R:1:C:0:dd_button"]').click(timeout=4000); time.sleep(0.9)
        return fr.evaluate(f"""()=>[...document.querySelectorAll('[id="nav:form:G:{g}:R:1:C:0:dd_panel"] tr[data-item-label]')].map(e=>(e.getAttribute('data-item-label')||'').trim()).filter(t=>t)""")
    except Exception: return []
def pick(fr,g,label):
    try: fr.locator(f'[id="nav:form:G:{g}:R:1:C:0:dd_panel"] tr[data-item-label="{label}"]').first.click(timeout=4000); time.sleep(1.3)
    except Exception: pass
print("BEFORE:", db())
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
    fr.locator('[id="ProdAllocButton:form:B"]').click(timeout=6000); print("clicked Run Calculations"); time.sleep(3.0)
    # poll RunningJobs grid + refresh
    for i in range(8):
        try: fr.locator('xpath=//a[@title="Refresh [Ctrl+r]"]').first.click(timeout=4000)
        except Exception: pass
        time.sleep(10.0)
        rj=fr.evaluate("""()=>{const t=document.getElementById('RunningJobs:form:T_data'); const l=document.getElementById('log_list:form:T_data'); return {run:(t?(t.innerText||'').replace(/\\s+/g,' ').slice(0,160):''), log:(l?(l.innerText||'').replace(/\\s+/g,' ').slice(0,160):'')};}""")
        print(f"  t+{(i+1)*10}s  RunningJobs: {rj['run']!r}  log: {rj['log']!r}  DB:", db())
    b.close()
print("FINAL:", db())
