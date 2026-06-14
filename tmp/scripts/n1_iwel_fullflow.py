"""Prove the full self-cleaning injection-well flow live + capture the confirm-modal button id:
edit ON_STREAM_HRS null->33, save, DB=33; then CLEAR cell, Save -> handle confirmation modal
(dump its buttons, click confirm), DB=null. Ends clean (DB-restore guard)."""
import time, json, os
import oracledb
from playwright.sync_api import sync_playwright
URL="https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"
SCREEN="Daily Water Injection Well Status"; DATE="2026-02-13"; WELL="AS2_Onshore Well no 5"
SCOPE=[(1,"AS2 EC Exploration Norway"),(2,"AS2_Onshore Area"),(3,"AS2_Production Facility no 1"),(4,"AS2_Water Injection Manifold 1")]
def conn(): return oracledb.connect(user='ECKERNEL_EC',password='energy',dsn=os.environ.get('EC_DB_DSN','localhost:1521/ORCL'),tcp_connect_timeout=15)
def oid():
    c=conn();cur=c.cursor();cur.execute("SELECT OBJECT_ID FROM WELL_VERSION WHERE NAME=:n FETCH FIRST 1 ROWS ONLY",n=WELL);o=cur.fetchone()[0];cur.close();c.close();return o
def db():
    c=conn();cur=c.cursor();cur.execute("SELECT ON_STREAM_HRS FROM IWEL_DAY_STATUS WHERE OBJECT_ID=:o AND TRUNC(DAYTIME)=TO_DATE(:d,'YYYY-MM-DD')",o=oid(),d=DATE);v=cur.fetchone();cur.close();c.close();return v[0] if v else None
def restore():
    c=conn();cur=c.cursor();cur.execute("UPDATE IWEL_DAY_STATUS SET ON_STREAM_HRS=NULL WHERE OBJECT_ID=:o AND TRUNC(DAYTIME)=TO_DATE(:d,'YYYY-MM-DD')",o=oid(),d=DATE);c.commit();cur.close();c.close()
def opts(fr,g):
    fr.locator(f'[id="nav:form:G:{g}:R:1:C:0:dd_button"]').click(timeout=4000); time.sleep(0.7)
    return fr.evaluate(f"""()=>[...document.querySelectorAll('[id="nav:form:G:{g}:R:1:C:0:dd_panel"] tr[data-item-label]')].map(e=>(e.getAttribute('data-item-label')||'').trim()).filter(t=>t)""")
def pick(fr,g,l): fr.locator(f'[id="nav:form:G:{g}:R:1:C:0:dd_panel"] tr[data-item-label="{l}"]').first.click(timeout=4000); time.sleep(1.1)
def ridx(fr): return fr.evaluate(f"""()=>{{const t=document.getElementById('daily_well_status:form:T_data');let i=-1;if(t)t.querySelectorAll('tr').forEach((tr,n)=>{{if((tr.textContent||'').includes('{WELL}'))i=n;}});return i;}}""")
def go(fr,page): fr.locator('[id="button:form:B"]').click(timeout=5000); page.wait_for_load_state("networkidle",timeout=30000); time.sleep(2.2)
def click_save(fr): fr.locator("xpath=//a[@title='Save [Ctrl+s]' and not(contains(@class,'ui-state-disabled'))]").click(timeout=6000)
def settle(page):
    try: page.wait_for_load_state("networkidle",timeout=12000)
    except Exception: pass
    time.sleep(0.8)
def dump_modal(fr):
    return fr.evaluate("""()=>{const m=document.getElementById('confirmationForm:confirmation_modal');
      const vis=m && m.offsetParent!==null;
      const btns=[...document.querySelectorAll('[id^="confirmationForm"] button, [id^="confirmationForm"] a')].map(e=>({id:e.id,t:(e.textContent||'').trim()})).filter(x=>x.t);
      return {visible:!!vis, btns};}""")
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
    go(fr,page)
    # EDIT -> 33
    i=ridx(fr); cid=f"daily_well_status:form:T:{i}:C4_in"
    el=fr.locator(f'[id="{cid}"]'); el.click(); el.fill(""); el.type("33",delay=45); page.keyboard.press("Tab"); settle(page)
    click_save(fr); settle(page)
    md=dump_modal(fr); print("after edit-save modal:", json.dumps(md))
    if md["visible"]:
        # click a confirm/yes/ok button
        for x in md["btns"]:
            if any(k in (x["t"].lower()) for k in ("yes","ok","confirm","save")):
                fr.locator(f'[id="{x["id"]}"]').click(timeout=4000); print("clicked",x); break
        settle(page)
    print("DB after edit->33:", db())
    # CLEAR -> save -> confirm
    go(fr,page); i=ridx(fr); cid=f"daily_well_status:form:T:{i}:C4_in"
    el=fr.locator(f'[id="{cid}"]'); el.click(); el.press("Control+a"); el.press("Delete"); page.keyboard.press("Tab"); settle(page)
    click_save(fr); time.sleep(1.0)
    md=dump_modal(fr); print("after clear-save modal:", json.dumps(md))
    if md["visible"]:
        for x in md["btns"]:
            if any(k in (x["t"].lower()) for k in ("yes","ok","confirm")):
                fr.locator(f'[id="{x["id"]}"]').click(timeout=4000); print("clicked confirm",x); break
        settle(page)
    print("DB after UI-clear+confirm:", db())
    b.close()
final=db()
if final is not None: restore(); print("guard: DB-restored null")
print("final DB:", db()); print("DONE")
