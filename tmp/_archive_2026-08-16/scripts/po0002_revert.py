"""Revert STRM_DAY_STREAM.GRS_VOL for AS2_Flare Gas 001 back to 2949.9 (fresh session avoids the
edit->save->edit chaining issue). DB-verify after."""
import time
import oracledb
from playwright.sync_api import sync_playwright
URL="https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"; SCREEN="Daily Gas Stream Status"
OID="96D7FD4CB6770217E053020011AC1940"; CELL='measured:form:T:0:C7_in'; TARGET="2949.9"
def grsvol():
    c=oracledb.connect(user="ECKERNEL_EC",password="energy",dsn="localhost:1521/ORCL",tcp_connect_timeout=15).cursor()
    c.execute("SELECT GRS_VOL FROM ECKERNEL_EC.STRM_DAY_STREAM WHERE OBJECT_ID=:o AND TRUNC(DAYTIME)=DATE '2003-01-01'", o=OID)
    r=c.fetchone(); return r[0] if r else None
def dd_opts(fr,g):
    fr.locator(f'[id="nav:form:G:{g}:R:1:C:0:dd_button"]').click(timeout=5000); time.sleep(0.8)
    return fr.evaluate(f"""()=>[...document.querySelectorAll('[id="nav:form:G:{g}:R:1:C:0:dd_panel"] tr[data-item-label]')].map(e=>(e.getAttribute('data-item-label')||'').trim()).filter(t=>t)""")
def dd_pick(fr,g,l): fr.locator(f'[id="nav:form:G:{g}:R:1:C:0:dd_panel"] tr[data-item-label="{l}"]').first.click(timeout=5000); time.sleep(1.2)
print("GRS_VOL before:", grsvol())
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
    if not fr: print("NOT LOADED"); b.close(); raise SystemExit
    time.sleep(2.0)
    fr.locator('[id="nav:form:G:0:R:1:C:0:da_input"]').fill("2003-01-01"); fr.locator('[id="nav:form:G:0:R:1:C:0:da_input"]').press("Tab"); time.sleep(1.5)
    dd_opts(fr,1); dd_pick(fr,1,"AS2 EC Exploration Norway")
    dd_opts(fr,2); dd_pick(fr,2,"AS2_Onshore Area")
    dd_opts(fr,3); dd_pick(fr,3,"AS2_Production Facility no 1")
    fr.locator('[id="button:form:B"]').click(timeout=6000); page.wait_for_load_state("networkidle",timeout=30000); time.sleep(3.5)
    print("cell shows:", fr.locator(f'[id="{CELL}"]').input_value())
    el=fr.locator(f'[id="{CELL}"]'); el.click(); el.press("Control+a"); el.press("Delete"); el.type(TARGET, delay=90); el.press("Tab")
    page.wait_for_load_state("networkidle",timeout=12000); time.sleep(1.8)
    sv=page.locator('xpath=//a[starts-with(@title,"Save") and not(contains(@class,"ui-state-disabled"))]')
    print("save enabled?", sv.count()>0)
    if sv.count()>0: sv.first.click(timeout=6000); page.wait_for_load_state("networkidle",timeout=15000); time.sleep(2.5)
    b.close()
print("GRS_VOL after:", grsvol())
