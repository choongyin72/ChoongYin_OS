"""Isolate broken-process vs executor: fire a DIFFERENT HA.0001 status process and watch the DB
(STAT_PROCESS_STATUS) for execution ~70s. If it executes (a row appears) -> the previous process was
the defect; if it also stays WAITING -> the executor isn't draining (escalate). Process via argv[1]."""
import time, json, os, sys
import oracledb
from playwright.sync_api import sync_playwright
URL="https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"; SCREEN="Daily Data Status Processes"; DATE="2003-01-01"
PROCESS = sys.argv[1] if len(sys.argv)>1 else "Verify daily Onshore facility data"
def spc():
    c=oracledb.connect(user='ECKERNEL_EC',password='energy',dsn=os.environ.get('EC_DB_DSN','localhost:1521/ORCL'),tcp_connect_timeout=15);cur=c.cursor()
    cur.execute("SELECT COUNT(*) FROM STAT_PROCESS_STATUS"); n=cur.fetchone()[0]; cur.close();c.close(); return n
def opts(fr,g):
    fr.locator(f'[id="nav:form:G:{g}:R:1:C:0:dd_button"]').click(timeout=4000); time.sleep(0.8)
    return fr.evaluate(f"""()=>[...document.querySelectorAll('[id="nav:form:G:{g}:R:1:C:0:dd_panel"] tr[data-item-label]')].map(e=>(e.getAttribute('data-item-label')||'').trim()).filter(t=>t)""")
def pick(fr,g,l): fr.locator(f'[id="nav:form:G:{g}:R:1:C:0:dd_panel"] tr[data-item-label="{l}"]').first.click(timeout=4000); time.sleep(1.2)
print("process:",PROCESS,"| STAT_PROCESS_STATUS before:",spc())
with sync_playwright() as p:
    b=p.chromium.launch(headless=True); page=b.new_context(ignore_https_errors=True,viewport={"width":1680,"height":1000}).new_page()
    page.goto(URL,wait_until="domcontentloaded",timeout=60000)
    page.fill('[id="username"]',"sysadmin"); page.fill('[id="password"]',"sysadmin"); page.click('[id="kc-login"]')
    page.wait_for_selector('[id="menu:searchForm:searchTxt"]',timeout=60000); time.sleep(1.0)
    sel=f'xpath=//*[contains(@class,"tv-link") and normalize-space(text())="{SCREEN}"]'
    page.fill('[id="menu:searchForm:searchTxt"]',""); page.locator('[id="menu:searchForm:searchTxt"]').type(SCREEN,delay=35)
    page.wait_for_selector(sel,timeout=12000); page.locator(sel).first.click(); page.wait_for_load_state("networkidle",timeout=30000); time.sleep(2.0)
    fr=next((f for f in page.frames if "dashboard.jsf" in (f.url or "") and "top=false" in (f.url or "")),None) or page
    for g in (0,1):
        di=fr.locator(f'[id="nav:form:G:{g}:R:1:C:0:da_input"]'); di.fill(DATE); di.press("Tab"); time.sleep(0.9)
    g2=opts(fr,2)
    if PROCESS not in g2: print("PROCESS not in G2 list:", json.dumps(g2))
    pick(fr,2,PROCESS); print("picked", PROCESS)
    # (HA.0001 nav has only G:2 process dd)
    fr.locator('[id="button:form:B"]').click(timeout=5000); page.wait_for_load_state("networkidle",timeout=30000); time.sleep(2.0)
    fr.locator('[id="RunProcessButton:form:B"]').click(timeout=6000); print("RUN clicked")
    rj=fr.evaluate("""()=>{const t=document.getElementById('RunningJobs:form:T_data');return t?(t.innerText||'').replace(/\\s+/g,' ').slice(0,80):'';}""")
    print("RunningJobs:", rj)
    b.close()
# poll DB ~70s
for i in range(7):
    time.sleep(10); n=spc()
    print(f"  t+{(i+1)*10}s STAT_PROCESS_STATUS={n}")
    if n>0: print(">>> EXECUTED (a status-process run row appeared)"); break
print("DONE")
