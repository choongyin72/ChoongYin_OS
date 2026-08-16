"""STRM sub-daily recon: DB scope (which PU/Area/Facility the 2011-01-01 streams sit under, via
OV_STREAM) + UI screen search for the 'Sub Daily ... Stream' screen. Read-only."""
import time, json, os
import oracledb
from playwright.sync_api import sync_playwright
URL = "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"

c = oracledb.connect(user='ECKERNEL_EC', password='energy', dsn=os.environ.get('EC_DB_DSN', 'localhost:1521/ORCL'), tcp_connect_timeout=15)
cur = c.cursor()
cur.execute("SELECT column_name FROM all_tab_columns WHERE table_name='OV_STREAM' AND (column_name LIKE '%FCTY%' OR column_name LIKE '%AREA%' OR column_name LIKE '%PROD_UNIT%' OR column_name='NAME' OR column_name LIKE '%PHASE%' OR column_name LIKE '%CLASS%') ORDER BY column_id")
print("OV_STREAM scope cols:", [r[0] for r in cur.fetchall()])
cur.execute("""SELECT ov.NAME, ov.OP_AREA_CODE, ov.OP_FCTY_1_CODE
  FROM OV_STREAM ov WHERE ov.OBJECT_ID IN (SELECT DISTINCT OBJECT_ID FROM STRM_SUB_DAY_STATUS WHERE RECORD_STATUS='P' AND TRUNC(DAYTIME)=TO_DATE('2011-01-01','YYYY-MM-DD')) ORDER BY ov.NAME""")
print("streams on 2011-01-01 (NAME | area | fcty1):")
for r in cur.fetchall():
    print("  ", r[0], "|", r[1], "|", r[2])
cur.close(); c.close()

with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    page = b.new_context(ignore_https_errors=True, viewport={"width": 1680, "height": 1000}).new_page()
    page.goto(URL, wait_until="domcontentloaded", timeout=60000)
    page.fill('[id="username"]', "sysadmin"); page.fill('[id="password"]', "sysadmin"); page.click('[id="kc-login"]')
    page.wait_for_selector('[id="menu:searchForm:searchTxt"]', timeout=60000); time.sleep(1.0)
    page.locator('[id="menu:searchForm:searchTxt"]').type("Sub Daily", delay=25); time.sleep(1.5)
    screens = page.evaluate("""()=>[...document.querySelectorAll('.tv-link')].map(e=>e.textContent.trim()).filter(t=>/Sub Daily/i.test(t))""")
    print("\nSub Daily screens:", json.dumps(screens))
    b.close()
print("DONE")
