from playwright.sync_api import sync_playwright
import os, oracledb
def say(m): print(m, flush=True)
def cell(s): return '#'+s.replace(':',r'\:')
with sync_playwright() as p:
    b=p.chromium.connect_over_cdp("http://localhost:9222")
    pg=b.contexts[0].pages[0]
    pg.locator(cell('deletebutton:form:B')).click(); say("clicked DELETE CALCULATION"); pg.wait_for_timeout(1200)
    yn=pg.get_by_role("button", name="Yes")
    if yn.count()>0 and yn.first.is_visible(): yn.first.click(); say("confirmed Yes")
    else: say("no Yes dialog")
    pg.wait_for_load_state('networkidle',timeout=20000); pg.wait_for_timeout(2500)
    pg.screenshot(path="C:/tmp/calc_deleted.png", full_page=True); say("SHOT calc_deleted")
con=oracledb.connect(user=os.environ.get('EC_DB_USER','ECKERNEL_EC'),password=os.environ.get('EC_DB_PASS','energy'),dsn=os.environ.get('EC_DB_DSN','localhost:1521/ORCL'))
cur=con.cursor()
cur.execute("select count(*) from calculation where object_code='AUTOTEST_CALC_TEST'")
say("CALCULATION rows AUTOTEST_CALC_TEST: "+str(cur.fetchone()[0]))
cur.execute("select count(*) from calculation where object_code in ('RUN_NO_TEST','CALC_TEST')")
say("control calcs RUN_NO_TEST+CALC_TEST still present (expect 2): "+str(cur.fetchone()[0]))
cur.execute("select count(*) from tv_alloc_network_job_conn where ecdp_objects.GetObjCode(job_id)='AUTOTEST_CALC_TEST'")
say("job connections for AUTOTEST_CALC_TEST (expect 0): "+str(cur.fetchone()[0]))
cur.close(); con.close()
