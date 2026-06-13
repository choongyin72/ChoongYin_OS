"""PO.0002 validate + map (post-restart, clean slate). Open Daily Gas Stream Status @ AS2 scope,
edit measured:form row0 C7 to a UNIQUE sentinel via the proven gesture (real keystrokes + Tab ->
change/stage; menubar Save -> commit @all), then scan STRM_DAY_STREAM on 2003-01-01 for the
sentinel to find (OBJECT_ID, column) = the cell<->DB-column map + persistence proof. Reverts."""
import time, re
import oracledb
from playwright.sync_api import sync_playwright
URL="https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"; SCREEN="Daily Gas Stream Status"
CELL='measured:form:T:0:C7_in'; SENT="1234.5"
def db():
    return oracledb.connect(user="ECKERNEL_EC",password="energy",dsn="localhost:1521/ORCL",tcp_connect_timeout=15)
def scan_for(val):
    c=db().cursor()
    c.execute("SELECT * FROM ECKERNEL_EC.STRM_DAY_STREAM WHERE TRUNC(DAYTIME)=DATE '2003-01-01'")
    names=[d[0] for d in c.description]
    hits=[]
    for r in c.fetchall():
        for n,v in zip(names,r):
            if v is not None and str(v).replace('.0','')==str(val).replace('.0',''):
                hits.append((r[names.index('OBJECT_ID')], n, str(v)))
    return hits
def dd_opts(fr,g):
    fr.locator(f'[id="nav:form:G:{g}:R:1:C:0:dd_button"]').click(timeout=5000); time.sleep(0.8)
    return fr.evaluate(f"""()=>[...document.querySelectorAll('[id="nav:form:G:{g}:R:1:C:0:dd_panel"] tr[data-item-label]')].map(e=>(e.getAttribute('data-item-label')||'').trim()).filter(t=>t)""")
def dd_pick(fr,g,l): fr.locator(f'[id="nav:form:G:{g}:R:1:C:0:dd_panel"] tr[data-item-label="{l}"]').first.click(timeout=5000); time.sleep(1.2)
def save(page):
    sv=page.locator('xpath=//a[starts-with(@title,"Save") and not(contains(@class,"ui-state-disabled"))]')
    print("  save enabled?", sv.count()>0)
    if sv.count()>0: sv.first.click(timeout=6000); page.wait_for_load_state("networkidle",timeout=15000); time.sleep(2.5)

with sync_playwright() as p:
    b=p.chromium.launch(headless=True); page=b.new_context(ignore_https_errors=True,viewport={"width":1680,"height":1000}).new_page()
    page.goto(URL,wait_until="domcontentloaded",timeout=60000)
    page.fill('[id="username"]',"sysadmin"); page.fill('[id="password"]',"sysadmin"); page.click('[id="kc-login"]')
    page.wait_for_selector('[id="menu:searchForm:searchTxt"]',timeout=60000)
    sel='xpath=//*[contains(@class,"tv-link") and normalize-space(text())="Daily Gas Stream Status"]'; fr=None
    for _ in range(3):
        page.fill('[id="menu:searchForm:searchTxt"]',""); page.locator('[id="menu:searchForm:searchTxt"]').type(SCREEN,delay=40)
        page.wait_for_selector(sel,timeout=15000); time.sleep(0.6); page.locator(sel).first.click()
        page.wait_for_load_state("networkidle",timeout=30000)
        for _ in range(25):
            fr=next((f for f in page.frames if ".screens/" in f.url and "dashboard" not in f.url),None)
            if fr: break
            time.sleep(1.0)
        if fr: break
    if not fr: print("NOT LOADED (app up?)"); b.close(); raise SystemExit
    time.sleep(2.0)
    fr.locator('[id="nav:form:G:0:R:1:C:0:da_input"]').fill("2003-01-01"); fr.locator('[id="nav:form:G:0:R:1:C:0:da_input"]').press("Tab"); time.sleep(1.5)
    dd_opts(fr,1); dd_pick(fr,1,"AS2 EC Exploration Norway")
    dd_opts(fr,2); dd_pick(fr,2,"AS2_Onshore Area")
    dd_opts(fr,3); dd_pick(fr,3,"AS2_Production Facility no 1")
    fr.locator('[id="button:form:B"]').click(timeout=6000); page.wait_for_load_state("networkidle",timeout=30000); time.sleep(3.5)
    orig=fr.locator(f'[id="{CELL}"]').input_value(); print("row0 C7 original:", orig)
    print("pre-existing sentinel rows (should be none):", scan_for(SENT))
    # EDIT to sentinel (real keystrokes + Tab) -> SAVE
    el=fr.locator(f'[id="{CELL}"]'); el.click(); el.press("Control+a"); el.press("Delete"); el.type(SENT, delay=90); el.press("Tab")
    page.wait_for_load_state("networkidle",timeout=12000); time.sleep(1.8)
    print("cell after type:", el.input_value()); save(page)
    hits=scan_for(SENT)
    print("\n>>> DB rows == sentinel after save:", hits, "<<<")
    # revert
    orig_num=re.sub(r'[^0-9.]','',orig) or "0"
    el=fr.locator(f'[id="{CELL}"]'); el.click(); el.press("Control+a"); el.press("Delete"); el.type(orig_num, delay=90); el.press("Tab")
    page.wait_for_load_state("networkidle",timeout=12000); time.sleep(1.5); save(page)
    print("after revert, sentinel rows (should be none):", scan_for(SENT))
    b.close()
print("DONE")
