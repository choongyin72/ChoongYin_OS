"""Deeper sub-daily N1 recon (2026-06-14). The N1 DB-verify keys on (OBJECT_ID, TRUNC(DAYTIME)) — but
PWEL_SUB_DAY_STATUS has MULTIPLE intraday rows per well/day, so the key must include the TIME.
Establish: (1) the exact PK (does DAYTIME carry the time-of-day, or is there a separate interval col?);
(2) for one well on the richest P day, the actual intraday DAYTIME values (the grain); (3) numeric
measured cols; (4) the '- by Well' screen variant nav + grid + whether cells carry the time.
Read-only."""
import time, json, os
import oracledb
from playwright.sync_api import sync_playwright

URL = "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"
SCREEN = "Sub Daily Production Well Status 1 - by Well"
c = oracledb.connect(user='ECKERNEL_EC', password='energy',
                     dsn=os.environ.get('EC_DB_DSN', 'localhost:1521/ORCL'), tcp_connect_timeout=15)
cur = c.cursor()


def show(t, sql, n=12):
    print(f"\n=== {t} ===")
    try:
        cur.execute(sql)
        cols = [d[0] for d in cur.description]
        print("  " + " | ".join(cols))
        for r in cur.fetchall()[:n]:
            print("  " + " | ".join("" if v is None else str(v)[:30] for v in r))
    except Exception as e:
        print("  ERR", str(e)[:160])


# (1) PK / unique constraint columns
show("PWEL_SUB_DAY_STATUS PK columns",
     "SELECT cc.column_name, cc.position FROM all_constraints ac "
     "JOIN all_cons_columns cc ON ac.constraint_name=cc.constraint_name AND ac.owner=cc.owner "
     "WHERE ac.table_name='PWEL_SUB_DAY_STATUS' AND ac.constraint_type='P' ORDER BY cc.position")
# does DAYTIME carry time-of-day?
show("DAYTIME data type + sample with HH24:MI:SS",
     "SELECT TO_CHAR(DAYTIME,'YYYY-MM-DD HH24:MI:SS') dt, OBJECT_ID, RECORD_STATUS "
     "FROM PWEL_SUB_DAY_STATUS WHERE RECORD_STATUS='P' "
     "ORDER BY DAYTIME FETCH FIRST 8 ROWS ONLY")
# (2) richest P day + one well's intraday rows on it
show("richest P day",
     "SELECT TO_CHAR(TRUNC(DAYTIME),'YYYY-MM-DD') d, COUNT(*) n, COUNT(DISTINCT OBJECT_ID) wells "
     "FROM PWEL_SUB_DAY_STATUS WHERE RECORD_STATUS='P' GROUP BY TRUNC(DAYTIME) ORDER BY n DESC FETCH FIRST 4 ROWS ONLY")
show("intraday rows for ONE well on its richest day (the time grain)",
     "SELECT OBJECT_ID, TO_CHAR(DAYTIME,'YYYY-MM-DD HH24:MI:SS') dt FROM PWEL_SUB_DAY_STATUS "
     "WHERE RECORD_STATUS='P' AND OBJECT_ID=(SELECT OBJECT_ID FROM PWEL_SUB_DAY_STATUS WHERE RECORD_STATUS='P' "
     "GROUP BY OBJECT_ID ORDER BY COUNT(*) DESC FETCH FIRST 1 ROWS ONLY) ORDER BY DAYTIME FETCH FIRST 15 ROWS ONLY")
# (3) numeric measured cols
show("numeric measured cols",
     "SELECT column_name FROM all_tab_columns WHERE table_name='PWEL_SUB_DAY_STATUS' "
     "AND data_type='NUMBER' AND column_name NOT IN ('OBJECT_ID') ORDER BY column_id", n=20)

cur.close(); c.close()

# (4) UI recon of the '- by Well' variant
with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    page = b.new_context(ignore_https_errors=True, viewport={"width": 1680, "height": 1000}).new_page()
    page.goto(URL, wait_until="domcontentloaded", timeout=60000)
    page.fill('[id="username"]', "sysadmin"); page.fill('[id="password"]', "sysadmin"); page.click('[id="kc-login"]')
    page.wait_for_selector('[id="menu:searchForm:searchTxt"]', timeout=60000); time.sleep(1.0)
    sel = f'xpath=//*[contains(@class,"tv-link") and normalize-space(text())="{SCREEN}"]'
    page.fill('[id="menu:searchForm:searchTxt"]', ""); page.locator('[id="menu:searchForm:searchTxt"]').type(SCREEN, delay=30)
    try:
        page.wait_for_selector(sel, timeout=10000); page.locator(sel).first.click()
        page.wait_for_load_state("networkidle", timeout=30000); time.sleep(2.5)
        print("\n=== opened screen:", SCREEN)
    except Exception as e:
        print("\nopen err", str(e)[:90])
        # list what tv-links DO contain 'Sub Daily'
        links = page.evaluate("""()=>[...document.querySelectorAll('.tv-link')].map(e=>e.textContent.trim()).filter(t=>/Sub Daily/i.test(t))""")
        print("Sub Daily screens available:", json.dumps(links))
    fr = next((f for f in page.frames if "dashboard.jsf" in (f.url or "") and "top=false" in (f.url or "")), None) or page
    info = fr.evaluate("""()=>{const nav={};document.querySelectorAll('[id^="nav:form:G:"]').forEach(e=>{const m=e.id.match(/nav:form:G:(\\d+)/);if(m){nav[m[1]]=nav[m[1]]||{};if(/da_input/.test(e.id))nav[m[1]].date=true;if(/dd_button/.test(e.id))nav[m[1]].dd=true;}});
      const grids=[...document.querySelectorAll('[id$=":T_data"]')].map(t=>t.id);
      return {nav,grids};}""")
    print("nav:", json.dumps(info["nav"])); print("grids:", json.dumps(info["grids"]))
    b.close()
print("DONE")
