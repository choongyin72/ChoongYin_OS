from playwright.sync_api import sync_playwright
import os, oracledb
def say(m): print(m, flush=True)
with sync_playwright() as p:
    b=p.chromium.connect_over_cdp("http://localhost:9222")
    pg=b.contexts[0].pages[0]
    sv=pg.locator("xpath=//a[@title='Save [Ctrl+s]' and not(contains(@class,'ui-state-disabled'))]")
    if sv.count()>0 and sv.first.is_visible(): sv.first.click(); say("clicked Save")
    else: pg.keyboard.press('Control+s'); say("Ctrl+s")
    pg.wait_for_load_state('networkidle',timeout=20000); pg.wait_for_timeout(2500)
    pg.screenshot(path="C:/tmp/step_save.png", full_page=True); say("SHOT step_save")
con=oracledb.connect(user=os.environ.get('EC_DB_USER','ECKERNEL_EC'),password=os.environ.get('EC_DB_PASS','energy'),dsn=os.environ.get('EC_DB_DSN','localhost:1521/ORCL'))
cur=con.cursor()
cur.execute("select ecdp_objects.GetObjCode(job_id), to_char(nvl(last_updated_date,created_date),'YYYY-MM-DD HH24:MI:SS') from tv_alloc_network_job_conn where ecdp_objects.GetObjCode(alloc_network_id)='P1_DAY_ALLOC' order by 2 desc")
rows=cur.fetchall()
say("P1_DAY_ALLOC jobs in DB now:")
for r in rows: say("  "+str(r))
jobs=[r[0] for r in rows]
say("=> AUTOTEST connected: "+("YES" if 'AUTOTEST_CALC_TEST' in jobs else "NO")+" | DWV kept: "+("YES" if 'EC_DAILY_VOLUME' in jobs else "NO")+" | CALC_TEST kept: "+("YES" if 'CALC_TEST' in jobs else "NO"))
cur.close(); con.close()
