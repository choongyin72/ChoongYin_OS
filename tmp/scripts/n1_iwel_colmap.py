"""Map cell C4 <-> IWEL_DAY_STATUS column via edit->save->diff, then RESTORE NULL via DB (clean
cleanup; UI null-revert is unreliable for empty-original cells). Scope: AS2 water injection manifold
@2026-02-13, well 'AS2_Onshore Well no 5'. Completes the injection-well N1 recon."""
import time, json, os
import oracledb
from playwright.sync_api import sync_playwright
URL="https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"
SCREEN="Daily Water Injection Well Status"; DATE="2026-02-13"; WELL="AS2_Onshore Well no 5"; CELLCOL="C4"
SCOPE=[(1,"AS2 EC Exploration Norway"),(2,"AS2_Onshore Area"),(3,"AS2_Production Facility no 1"),(4,"AS2_Water Injection Manifold 1")]
NUMCOLS=["INJ_VOL","INJ_MASS","INJ_RATE","ON_STREAM_HRS","AVG_ANNULUS_PRESS","AVG_TUBING_PRESS","AVG_CHOKE_SIZE","AVG_GAS_DENSITY"]

def conn(): return oracledb.connect(user='ECKERNEL_EC',password='energy',dsn=os.environ.get('EC_DB_DSN','localhost:1521/ORCL'),tcp_connect_timeout=15)
def oid_of():
    c=conn();cur=c.cursor();cur.execute("SELECT OBJECT_ID FROM WELL_VERSION WHERE NAME=:n FETCH FIRST 1 ROWS ONLY",n=WELL);o=cur.fetchone()[0];cur.close();c.close();return o
def db_row():
    c=conn();cur=c.cursor()
    cur.execute(f"SELECT {','.join(NUMCOLS)} FROM IWEL_DAY_STATUS WHERE OBJECT_ID=:o AND TRUNC(DAYTIME)=TO_DATE(:d,'YYYY-MM-DD')",o=oid_of(),d=DATE)
    r=cur.fetchone();cur.close();c.close();return dict(zip(NUMCOLS,r)) if r else None
def restore_nulls(changed_cols):
    c=conn();cur=c.cursor()
    sets=", ".join(f"{col}=NULL" for col in changed_cols)
    cur.execute(f"UPDATE IWEL_DAY_STATUS SET {sets} WHERE OBJECT_ID=:o AND TRUNC(DAYTIME)=TO_DATE(:d,'YYYY-MM-DD')",o=oid_of(),d=DATE)
    c.commit(); n=cur.rowcount; cur.close();c.close(); return n
def opts(fr,g):
    fr.locator(f'[id="nav:form:G:{g}:R:1:C:0:dd_button"]').click(timeout=4000); time.sleep(0.7)
    return fr.evaluate(f"""()=>[...document.querySelectorAll('[id="nav:form:G:{g}:R:1:C:0:dd_panel"] tr[data-item-label]')].map(e=>(e.getAttribute('data-item-label')||'').trim()).filter(t=>t)""")
def pick(fr,g,label):
    fr.locator(f'[id="nav:form:G:{g}:R:1:C:0:dd_panel"] tr[data-item-label="{label}"]').first.click(timeout=4000); time.sleep(1.1)
def row_index(fr,name):
    return fr.evaluate(f"""()=>{{const t=document.getElementById('daily_well_status:form:T_data');let i=-1;if(t)t.querySelectorAll('tr').forEach((tr,n)=>{{if((tr.textContent||'').includes('{name}'))i=n;}});return i;}}""")

before=db_row(); print("BEFORE:", json.dumps(before))
with sync_playwright() as p:
    b=p.chromium.launch(headless=True); page=b.new_context(ignore_https_errors=True,viewport={"width":1680,"height":1000}).new_page()
    page.goto(URL,wait_until="domcontentloaded",timeout=60000)
    page.fill('[id="username"]',"sysadmin"); page.fill('[id="password"]',"sysadmin"); page.click('[id="kc-login"]')
    page.wait_for_selector('[id="menu:searchForm:searchTxt"]',timeout=60000); time.sleep(1.0)
    sel=f'xpath=//*[contains(@class,"tv-link") and normalize-space(text())="{SCREEN}"]'
    page.fill('[id="menu:searchForm:searchTxt"]',""); page.locator('[id="menu:searchForm:searchTxt"]').type(SCREEN,delay=35)
    page.wait_for_selector(sel,timeout=12000); page.locator(sel).first.click(); page.wait_for_load_state("networkidle",timeout=30000); time.sleep(2.0)
    fr=next((f for f in page.frames if "dashboard.jsf" in (f.url or "") and "top=false" in (f.url or "")),None) or page
    di=fr.locator('[id="nav:form:G:0:R:1:C:0:da_input"]'); di.fill(DATE); di.press("Tab"); time.sleep(1.0)
    for g,label in SCOPE: opts(fr,g); pick(fr,g,label)
    fr.locator('[id="button:form:B"]').click(timeout=5000); page.wait_for_load_state("networkidle",timeout=30000); time.sleep(2.5)
    idx=row_index(fr,WELL); print("row idx",idx)
    cid=f"daily_well_status:form:T:{idx}:{CELLCOL}_in"
    fr.locator(f'[id="{cid}"]').click(timeout=5000); fr.locator(f'[id="{cid}"]').fill(""); fr.locator(f'[id="{cid}"]').type("22",delay=45)
    page.keyboard.press("Tab");
    try: page.wait_for_load_state("networkidle",timeout=12000)
    except Exception: pass
    time.sleep(0.8)
    fr.locator("xpath=//a[@title='Save [Ctrl+s]' and not(contains(@class,'ui-state-disabled'))]").click(timeout=6000)
    try: page.wait_for_load_state("networkidle",timeout=15000)
    except Exception: pass
    time.sleep(1.5)
    b.close()
after=db_row(); print("AFTER EDIT C4->22:", json.dumps(after))
changed=[c for c in NUMCOLS if (before or {}).get(c)!=(after or {}).get(c)]
print(">>> C4 maps to IWEL column(s):", changed, "(value now =", {c:after[c] for c in changed}, ")")
if changed:
    n=restore_nulls(changed); print("RESTORED NULL on",changed,"rows updated=",n)
    print("AFTER RESTORE:", json.dumps(db_row()))
print("DONE")
