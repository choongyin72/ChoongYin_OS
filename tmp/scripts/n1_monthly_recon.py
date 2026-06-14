"""Recon Monthly Production Well Status (novel monthly cadence). DB: find the monthly well-status
table + a month with editable (P) data + numeric cols. UI: open the screen, dump nav groups (is the
period a month vs a date?) + grid id. Read-only."""
import time, json, os
import oracledb
from playwright.sync_api import sync_playwright
URL="https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"; SCREEN="Monthly Production Well Status"
c=oracledb.connect(user='ECKERNEL_EC',password='energy',dsn=os.environ.get('EC_DB_DSN','localhost:1521/ORCL'),tcp_connect_timeout=15);cur=c.cursor()
def show(t,sql):
    print(f"=== {t} ===")
    try:
        cur.execute(sql);cols=[d[0] for d in cur.description];print(" | ".join(cols))
        for r in cur.fetchall()[:10]: print("  "+" | ".join("" if v is None else str(v)[:36] for v in r))
    except Exception as e: print("  ERR",str(e)[:140])
show("candidate monthly well-status tables",
    "SELECT table_name FROM all_tables WHERE owner='ECKERNEL_EC' AND table_name LIKE 'PWEL%MTH%' AND table_name NOT LIKE '%\\_JN' ESCAPE '\\' ORDER BY table_name")
show("PWEL_MTH_STATUS row/status (if exists)",
    "SELECT RECORD_STATUS, COUNT(*) n, TO_CHAR(MAX(TRUNC(DAYTIME)),'YYYY-MM-DD') maxd FROM PWEL_MTH_STATUS GROUP BY RECORD_STATUS")
show("PWEL_MTH_STATUS top month with P data",
    "SELECT TO_CHAR(TRUNC(DAYTIME),'YYYY-MM-DD') d, COUNT(*) n FROM PWEL_MTH_STATUS WHERE RECORD_STATUS='P' GROUP BY TRUNC(DAYTIME) ORDER BY n DESC FETCH FIRST 4 ROWS ONLY")
cur.close();c.close()
with sync_playwright() as p:
    b=p.chromium.launch(headless=True); page=b.new_context(ignore_https_errors=True,viewport={"width":1600,"height":1000}).new_page()
    page.goto(URL,wait_until="domcontentloaded",timeout=60000)
    page.fill('[id="username"]',"sysadmin"); page.fill('[id="password"]',"sysadmin"); page.click('[id="kc-login"]')
    page.wait_for_selector('[id="menu:searchForm:searchTxt"]',timeout=60000); time.sleep(1.0)
    sel=f'xpath=//*[contains(@class,"tv-link") and normalize-space(text())="{SCREEN}"]'
    page.fill('[id="menu:searchForm:searchTxt"]',""); page.locator('[id="menu:searchForm:searchTxt"]').type(SCREEN,delay=35)
    try: page.wait_for_selector(sel,timeout=10000); page.locator(sel).first.click(); page.wait_for_load_state("networkidle",timeout=30000); time.sleep(2.5)
    except Exception as e: print("open err",str(e)[:70])
    fr=next((f for f in page.frames if "dashboard.jsf" in (f.url or "") and "top=false" in (f.url or "")),None) or page
    info=fr.evaluate("""()=>{const nav={};document.querySelectorAll('[id^="nav:form:G:"]').forEach(e=>{const m=e.id.match(/nav:form:G:(\\d+)/);if(m){nav[m[1]]=nav[m[1]]||{};if(/da_input/.test(e.id))nav[m[1]].date=true;if(/mo_input|month/i.test(e.id))nav[m[1]].month=true;if(/dd_button/.test(e.id))nav[m[1]].dd=true;}});
      const periodInputs=[...document.querySelectorAll('[id^="nav:form:G:0"]')].map(e=>e.id).slice(0,8);
      const grids=[...document.querySelectorAll('[id$=":T_data"]')].map(t=>t.id);
      return {nav, periodInputs, grids};}""")
    print("=== UI nav ==="); print("nav groups:", json.dumps(info["nav"])); print("G:0 period inputs:", json.dumps(info["periodInputs"])); print("grids:", json.dumps(info["grids"]))
    b.close()
print("DONE")
