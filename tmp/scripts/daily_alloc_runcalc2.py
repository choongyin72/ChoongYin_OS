"""Run allocation via HA.0002 'RUN CALCULATIONS' — robustly locate the button by DOM text, click it,
wait for the RunningJobs/log result, DB-verify PWEL_DAY_ALLOC. P1 Dashboard + Daily Well Volume @
2021-10-01. User-authorised; DB refreshable."""
import time, json
import oracledb
from playwright.sync_api import sync_playwright
URL="https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"; SCREEN="Daily Allocation"; DATE="2021-10-01"
def db():
    c=oracledb.connect(user="ECKERNEL_EC",password="energy",dsn="localhost:1521/ORCL",tcp_connect_timeout=15).cursor()
    c.execute("""SELECT COUNT(*), TO_CHAR(MAX(LAST_UPDATED_DATE),'YYYY-MM-DD HH24:MI:SS'),
                  SUM(CASE WHEN ALLOC_GAS_VOL<0 OR ALLOC_NET_OIL_VOL<0 OR ALLOC_WATER_VOL<0 THEN 1 ELSE 0 END),
                  ROUND(SUM(ALLOC_GAS_VOL),1)
                 FROM ECKERNEL_EC.PWEL_DAY_ALLOC WHERE TRUNC(DAYTIME)=DATE '2021-10-01'""")
    return c.fetchone()
def opts(fr,g):
    try:
        fr.locator(f'[id="nav:form:G:{g}:R:1:C:0:dd_button"]').click(timeout=4000); time.sleep(0.9)
        return fr.evaluate(f"""()=>[...document.querySelectorAll('[id="nav:form:G:{g}:R:1:C:0:dd_panel"] tr[data-item-label]')].map(e=>(e.getAttribute('data-item-label')||'').trim()).filter(t=>t)""")
    except Exception: return []
def pick(fr,g,label):
    try: fr.locator(f'[id="nav:form:G:{g}:R:1:C:0:dd_panel"] tr[data-item-label="{label}"]').first.click(timeout=4000); time.sleep(1.3)
    except Exception: pass
print("BEFORE (cnt,lastUpd,negs,sumGas):", db())
with sync_playwright() as p:
    b=p.chromium.launch(headless=True); page=b.new_context(ignore_https_errors=True,viewport={"width":1680,"height":1000}).new_page()
    page.goto(URL,wait_until="domcontentloaded",timeout=60000)
    page.fill('[id="username"]',"sysadmin"); page.fill('[id="password"]',"sysadmin"); page.click('[id="kc-login"]')
    page.wait_for_selector('[id="menu:searchForm:searchTxt"]',timeout=60000)
    sel='xpath=//*[contains(@class,"tv-link") and normalize-space(text())="Daily Allocation"]'; fr=None
    for _ in range(3):
        page.fill('[id="menu:searchForm:searchTxt"]',""); page.locator('[id="menu:searchForm:searchTxt"]').type(SCREEN,delay=40)
        try: page.wait_for_selector(sel,timeout=12000)
        except Exception: pass
        time.sleep(0.6)
        try: page.locator(sel).first.click()
        except Exception: continue
        page.wait_for_load_state("networkidle",timeout=30000)
        for _ in range(25):
            fr=next((f for f in page.frames if "edit_daily_alloc" in f.url),None)
            if fr: break
            time.sleep(1.0)
        if fr: break
    if not fr: print("NOT LOADED"); b.close(); raise SystemExit
    time.sleep(2.0)
    for g in (0,1):
        di=fr.locator(f'[id="nav:form:G:{g}:R:1:C:0:da_input"]'); di.fill(DATE); di.press("Tab"); time.sleep(1.0)
    g2=opts(fr,2); pick(fr,2, next((x for x in g2 if x=="P1 Dashboard"), g2[0] if g2 else ""))
    opts(fr,3); g4=opts(fr,4); pick(fr,4, next((x for x in g4 if "Volume" in x), g4[0] if g4 else ""))
    fr.locator('[id="button:form:B"]').click(timeout=5000); page.wait_for_load_state("networkidle",timeout=30000); time.sleep(2.5)
    # find the LEAF 'RUN CALCULATIONS' element, then its clickable ancestor (a/button/.ui-button)
    runinfo=fr.evaluate("""()=>{
      const leaf=[...document.querySelectorAll('*')].find(e=>e.offsetParent && e.children.length===0 &&
        (e.textContent||'').trim().toUpperCase()==='RUN CALCULATIONS');
      let el = leaf;
      if (leaf) el = leaf.closest('a,button,[onclick],.ui-button,.ui-commandlink') || leaf;
      // also try input[value]
      if (!el || !el.id){ const inp=[...document.querySelectorAll('input[type=submit],input[type=button]')].find(i=>i.offsetParent && (i.value||'').toUpperCase().includes('RUN CALCULATION')); if(inp) el=inp; }
      return el?{id:el.id, tag:el.tagName, txt:(el.textContent||el.value||'').trim().slice(0,30), onclick:(el.getAttribute('onclick')||'').slice(0,80)}:null;
    }""")
    print("RUN button:", json.dumps(runinfo))
    if runinfo and runinfo.get("id"):
        try:
            fr.locator(f'[id="{runinfo["id"]}"]').first.click(timeout=6000)
        except Exception:
            fr.evaluate(f"""()=>{{const e=document.getElementById('{runinfo["id"]}'); if(e)e.click();}}""")
        print("clicked RUN"); page.wait_for_load_state("networkidle",timeout=90000); time.sleep(8.0)
    else:
        # fallback JS click by text
        fr.evaluate("""()=>{const e=[...document.querySelectorAll('a,button,span,div')].find(x=>x.offsetParent&&(x.textContent||'').trim().toUpperCase().includes('RUN CALCULATION')); if(e)e.click();}""")
        print("JS-clicked RUN by text"); page.wait_for_load_state("networkidle",timeout=90000); time.sleep(8.0)
    # results
    res=fr.evaluate("""()=>{
      const g=id=>{const t=document.getElementById(id); return t?(t.innerText||'').replace(/\\s+/g,' ').slice(0,220):null;};
      return {running:g('RunningJobs:form:T_data'), log:g('log_list:form:T_data')};
    }""")
    print("RunningJobs grid:", res["running"]); print("log_list grid:", res["log"])
    msgs=fr.evaluate("""()=>[...document.querySelectorAll('.ui-growl-item,.ui-messages-error,.ui-messages-info,.ui-dialog:not([style*=\"display: none\"])')].map(e=>(e.innerText||'').trim()).filter(Boolean)""")
    print("messages:", json.dumps(msgs)[:300])
    page.screenshot(path="c:/Projects/ChoongYin_OS/tmp/ha0002_runcalc2.png", full_page=True)
    b.close()
print("AFTER  (cnt,lastUpd,negs,sumGas):", db())
