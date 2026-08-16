"""PFLW (Production Flowline) N1 clone recon (read-only). DB: find the flowline NAME source + a scope
date's objects. UI: find the 'Daily Production Flowline Status' screen, open it, dump nav groups +
grid id (to confirm it mirrors the proven well-grid N1 pattern)."""
import time, json, os
import oracledb
from playwright.sync_api import sync_playwright

URL = "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"

# --- DB: flowline name source ---
c = oracledb.connect(user='ECKERNEL_EC', password='energy', dsn=os.environ.get('EC_DB_DSN', 'localhost:1521/ORCL'), tcp_connect_timeout=15)
cur = c.cursor()
for src in ("OV_PRODUCTIONFLOWLINE", "OV_FLOWLINE", "OV_PROD_FLOWLINE", "FLOWLINE_VERSION", "OV_PFLW", "PROD_FLOWLINE_VERSION"):
    try:
        cur.execute(f"SELECT COUNT(*) FROM {src}")
        n = cur.fetchone()[0]
        print(f"name-source candidate {src}: EXISTS ({n} rows)")
    except Exception:
        pass
# names of the 7 flowlines with P data on 2003-09-20 (resolve via any source that has their OBJECT_IDs)
cur.execute("SELECT DISTINCT OBJECT_ID FROM PFLW_DAY_STATUS WHERE RECORD_STATUS='P' AND TRUNC(DAYTIME)=TO_DATE('2003-09-20','YYYY-MM-DD')")
oids = [r[0] for r in cur.fetchall()]
print("flowline OBJECT_IDs on 2003-09-20:", oids[:3], "...total", len(oids))
cur.close(); c.close()

# --- UI: find flowline status screens ---
with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    page = b.new_context(ignore_https_errors=True, viewport={"width": 1680, "height": 1000}).new_page()
    page.goto(URL, wait_until="domcontentloaded", timeout=60000)
    page.fill('[id="username"]', "sysadmin"); page.fill('[id="password"]', "sysadmin"); page.click('[id="kc-login"]')
    page.wait_for_selector('[id="menu:searchForm:searchTxt"]', timeout=60000); time.sleep(1.0)
    page.locator('[id="menu:searchForm:searchTxt"]').type("Flowline", delay=30); time.sleep(1.5)
    screens = page.evaluate("""()=>[...document.querySelectorAll('.tv-link')].map(e=>e.textContent.trim()).filter(t=>/Flowline/i.test(t))""")
    print("\nFlowline screens in treeview:", json.dumps(screens))
    b.close()
print("DONE")
