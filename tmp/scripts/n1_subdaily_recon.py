"""Recon 'Sub Daily Production Well Status 1' (new pattern: intraday intervals). DB: PWEL_SUB_DAY_STATUS
key cols (is there a time/interval beyond DAYTIME?) + a data day + numeric cols. UI: open screen, dump
nav groups + grid id + sample rows/cells. Read-only."""
import time, json, os
import oracledb
from playwright.sync_api import sync_playwright
URL="https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"; SCREEN="Sub Daily Production Well Status 1"
c=oracledb.connect(user='ECKERNEL_EC',password='energy',dsn=os.environ.get('EC_DB_DSN','localhost:1521/ORCL'),tcp_connect_timeout=15);cur=c.cursor()
def show(t,sql):
    print(f"=== {t} ===")
    try:
        cur.execute(sql);cols=[d[0] for d in cur.description];print(" | ".join(cols))
        for r in cur.fetchall()[:8]: print("  "+" | ".join("" if v is None else str(v)[:34] for v in r))
    except Exception as e: print("  ERR",str(e)[:140])
show("PWEL_SUB_DAY_STATUS key-ish cols",
    "SELECT column_name,data_type FROM all_tab_columns WHERE table_name='PWEL_SUB_DAY_STATUS' AND (column_name IN ('OBJECT_ID','DAYTIME','RECORD_STATUS') OR column_name LIKE '%TIME%' OR column_name LIKE '%INTERVAL%' OR column_name LIKE '%SEQ%' OR column_name LIKE '%FROM%' OR column_name LIKE '%TO%') ORDER BY column_id")
show("PWEL_SUB_DAY_STATUS top P day",
    "SELECT TO_CHAR(TRUNC(DAYTIME),'YYYY-MM-DD') d, COUNT(*) n, COUNT(DISTINCT OBJECT_ID) wells FROM PWEL_SUB_DAY_STATUS WHERE RECORD_STATUS='P' GROUP BY TRUNC(DAYTIME) ORDER BY n DESC FETCH FIRST 4 ROWS ONLY")
show("PWEL_SUB_DAY_STATUS numeric cols",
    "SELECT column_name FROM all_tab_columns WHERE table_name='PWEL_SUB_DAY_STATUS' AND data_type='NUMBER' AND column_name<>'OBJECT_ID' ORDER BY column_id FETCH FIRST 12 ROWS ONLY")
cur.close();c.close()
with sync_playwright() as p:
    b=p.chromium.launch(headless=True); page=b.new_context(ignore_https_errors=True,viewport={"width":1680,"height":1000}).new_page()
    page.goto(URL,wait_until="domcontentloaded",timeout=60000)
    page.fill('[id="username"]',"sysadmin"); page.fill('[id="password"]',"sysadmin"); page.click('[id="kc-login"]')
    page.wait_for_selector('[id="menu:searchForm:searchTxt"]',timeout=60000); time.sleep(1.0)
    sel=f'xpath=//*[contains(@class,"tv-link") and normalize-space(text())="{SCREEN}"]'
    page.fill('[id="menu:searchForm:searchTxt"]',""); page.locator('[id="menu:searchForm:searchTxt"]').type(SCREEN,delay=30)
    try: page.wait_for_selector(sel,timeout=10000); page.locator(sel).first.click(); page.wait_for_load_state("networkidle",timeout=30000); time.sleep(2.5)
    except Exception as e: print("open err",str(e)[:70])
    fr=next((f for f in page.frames if "dashboard.jsf" in (f.url or "") and "top=false" in (f.url or "")),None) or page
    info=fr.evaluate("""()=>{const nav={};document.querySelectorAll('[id^="nav:form:G:"]').forEach(e=>{const m=e.id.match(/nav:form:G:(\\d+)/);if(m){nav[m[1]]=nav[m[1]]||{};if(/da_input/.test(e.id))nav[m[1]].date=true;if(/dd_button/.test(e.id))nav[m[1]].dd=true;}});
      const grids=[...document.querySelectorAll('[id$=":T_data"]')].map(t=>t.id);
      return {nav,grids};}""")
    print("=== UI nav ==="); print("nav:", json.dumps(info["nav"])); print("grids:", json.dumps(info["grids"]))
    b.close()
print("DONE")
