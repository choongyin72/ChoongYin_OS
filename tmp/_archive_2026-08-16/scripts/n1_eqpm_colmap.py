"""Map a cell <-> EQPM_DAY_STATUS column via edit->save->diff, then RESTORE NULL via DB.
Scope: P1 Production Unit / P1 Area / P1 Facility 1 @2024-02-06, equipment 'P1 Chiller 002'.
Tries C4_in -> 22. Self-cleaning."""
import time, json, os
import oracledb
from playwright.sync_api import sync_playwright
URL="https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"; SCREEN="Daily Equipment Status"; DATE="2024-02-06"
EQP="P1 Chiller 002"; CELLCOL="C4"
SCOPE=[(1,"P1 Production Unit"),(2,"P1 Area"),(3,"P1 Facility 1")]
NUMCOLS=["ON_STREAM_HRS","ON_STREAM_SECS","AVG_RPM","AVG_SPM","AVG_INTAKE_PRESS","AVG_PRESS","AVG_TEMP","AVG_TORQUE","POWER_CONSUMPTION","POWER_GENERATED"]
def conn(): return oracledb.connect(user='ECKERNEL_EC',password='energy',dsn=os.environ.get('EC_DB_DSN','localhost:1521/ORCL'),tcp_connect_timeout=15)
def oid():
    c=conn();cur=c.cursor();cur.execute("SELECT OBJECT_ID FROM OV_EQPM WHERE NAME=:n FETCH FIRST 1 ROWS ONLY",n=EQP);r=cur.fetchone();cur.close();c.close();return r[0] if r else None
def db_row():
    o=oid()
    if not o: return None
    c=conn();cur=c.cursor()
    cur.execute(f"SELECT {','.join(NUMCOLS)} FROM EQPM_DAY_STATUS WHERE OBJECT_ID=:o AND TRUNC(DAYTIME)=TO_DATE(:d,'YYYY-MM-DD')",o=o,d=DATE)
    r=cur.fetchone();cur.close();c.close();return dict(zip(NUMCOLS,r)) if r else None
def restore(cols):
    o=oid();c=conn();cur=c.cursor();sets=", ".join(f"{x}=NULL" for x in cols)
    cur.execute(f"UPDATE EQPM_DAY_STATUS SET {sets} WHERE OBJECT_ID=:o AND TRUNC(DAYTIME)=TO_DATE(:d,'YYYY-MM-DD')",o=o,d=DATE);c.commit();n=cur.rowcount;cur.close();c.close();return n
def opts(fr,g):
    fr.locator(f'[id="nav:form:G:{g}:R:1:C:0:dd_button"]').click(timeout=4000); time.sleep(0.7)
    return fr.evaluate(f"""()=>[...document.querySelectorAll('[id="nav:form:G:{g}:R:1:C:0:dd_panel"] tr[data-item-label]')].map(e=>(e.getAttribute('data-item-label')||'').trim()).filter(t=>t)""")
def pick(fr,g,l): fr.locator(f'[id="nav:form:G:{g}:R:1:C:0:dd_panel"] tr[data-item-label="{l}"]').first.click(timeout=4000); time.sleep(1.1)
def ridx(fr): return fr.evaluate(f"""()=>{{const t=document.getElementById('equipment_status:form:T_data');let i=-1;if(t)t.querySelectorAll('tr').forEach((tr,n)=>{{if((tr.textContent||'').includes('{EQP}'))i=n;}});return i;}}""")
print("OID:",oid(),"BEFORE:",json.dumps(db_row()))
with sync_playwright() as p:
    b=p.chromium.launch(headless=True); page=b.new_context(ignore_https_errors=True,viewport={"width":1680,"height":1000}).new_page()
    page.goto(URL,wait_until="domcontentloaded",timeout=60000)
    page.fill('[id="username"]',"sysadmin"); page.fill('[id="password"]',"sysadmin"); page.click('[id="kc-login"]')
    page.wait_for_selector('[id="menu:searchForm:searchTxt"]',timeout=60000); time.sleep(1.0)
    sel=f'xpath=//*[contains(@class,"tv-link") and normalize-space(text())="{SCREEN}"]'
    page.fill('[id="menu:searchForm:searchTxt"]',""); page.locator('[id="menu:searchForm:searchTxt"]').type(SCREEN,delay=35)
    page.wait_for_selector(sel,timeout=12000); page.locator(sel).first.click(); page.wait_for_load_state("networkidle",timeout=30000); time.sleep(2.0)
    fr=next((f for f in page.frames if "dashboard.jsf" in (f.url or "") and "top=false" in (f.url or "")),None) or page
    fr.locator('[id="nav:form:G:0:R:1:C:0:da_input"]').fill(DATE); fr.locator('[id="nav:form:G:0:R:1:C:0:da_input"]').press("Tab"); time.sleep(1.0)
    for g,l in SCOPE: opts(fr,g); pick(fr,g,l)
    fr.locator('[id="button:form:B"]').click(timeout=5000); page.wait_for_load_state("networkidle",timeout=30000); time.sleep(2.5)
    i=ridx(fr); print("row idx",i)
    cid=f"equipment_status:form:T:{i}:{CELLCOL}_in"
    fr.locator(f'[id="{cid}"]').click(timeout=5000); fr.locator(f'[id="{cid}"]').fill(""); fr.locator(f'[id="{cid}"]').type("22",delay=45); page.keyboard.press("Tab")
    try: page.wait_for_load_state("networkidle",timeout=12000)
    except Exception: pass
    time.sleep(0.8)
    fr.locator("xpath=//a[@title='Save [Ctrl+s]' and not(contains(@class,'ui-state-disabled'))]").click(timeout=6000)
    try: page.wait_for_load_state("networkidle",timeout=15000)
    except Exception: pass
    time.sleep(1.5); b.close()
after=db_row(); print("AFTER C4->22:",json.dumps(after))
before={k:None for k in NUMCOLS}
changed=[k for k in NUMCOLS if (after or {}).get(k) not in (None,)]
print(">>> C4 maps to:",changed)
if changed: restore(changed); print("restored; now:",json.dumps(db_row()))
print("DONE")
