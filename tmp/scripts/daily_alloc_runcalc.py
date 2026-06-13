"""RUN an allocation via HA.0002 'RUN CALCULATIONS' (synchronous, NOT BPM). P1 Dashboard +
Daily Well Volume (EC_DAILY_VOLUME) @ 2021-10-01. Read the result grid (exit status) + DB-verify
PWEL_DAY_ALLOC (count, recompute timestamp, conservation no-neg). User-authorised; DB refreshable."""
import time, json
import oracledb
from playwright.sync_api import sync_playwright
URL="https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"; SCREEN="Daily Allocation"; DATE="2021-10-01"
def db():
    c=oracledb.connect(user="ECKERNEL_EC",password="energy",dsn="localhost:1521/ORCL",tcp_connect_timeout=15).cursor()
    c.execute("""SELECT COUNT(*), TO_CHAR(MAX(LAST_UPDATED_DATE),'YYYY-MM-DD HH24:MI:SS'),
                  SUM(CASE WHEN ALLOC_GAS_VOL<0 OR ALLOC_NET_OIL_VOL<0 OR ALLOC_WATER_VOL<0 THEN 1 ELSE 0 END),
                  ROUND(SUM(ALLOC_GAS_VOL),1), ROUND(SUM(ALLOC_NET_OIL_VOL),1)
                 FROM ECKERNEL_EC.PWEL_DAY_ALLOC WHERE TRUNC(DAYTIME)=DATE '2021-10-01'""")
    return c.fetchone()
def opts(fr,g):
    try:
        fr.locator(f'[id="nav:form:G:{g}:R:1:C:0:dd_button"]').click(timeout=4000); time.sleep(0.9)
        return fr.evaluate(f"""()=>[...document.querySelectorAll('[id="nav:form:G:{g}:R:1:C:0:dd_panel"] tr[data-item-label]')].map(e=>(e.getAttribute('data-item-label')||'').trim()).filter(t=>t)""")
    except Exception: return []
def pick(fr,g,label):
    try: fr.locator(f'[id="nav:form:G:{g}:R:1:C:0:dd_panel"] tr[data-item-label="{label}"]').first.click(timeout=4000); time.sleep(1.3); return True
    except Exception: return False
print("BEFORE (cnt, lastUpd, negs, sumGas, sumOil):", db())
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
    opts(fr,3)
    g4=opts(fr,4); print("calc jobs:", g4); pick(fr,4, next((x for x in g4 if "Volume" in x), g4[0] if g4 else ""))
    fr.locator('[id="button:form:B"]').click(timeout=5000); page.wait_for_load_state("networkidle",timeout=30000); time.sleep(2.5)
    # click RUN CALCULATIONS (by visible text)
    try:
        fr.locator('text="RUN CALCULATIONS"').first.click(timeout=6000)
        print("clicked RUN CALCULATIONS"); page.wait_for_load_state("networkidle",timeout=60000); time.sleep(6.0)
    except Exception as e:
        print("RUN click err:", str(e)[:100])
    # read the result grid (exit status / status text)
    res=fr.evaluate("""()=>{
      const txt=(document.body.innerText||'');
      const grids=[...document.querySelectorAll('[id$="T_data"]')].filter(e=>e.offsetParent).map(t=>({id:t.id,rows:t.querySelectorAll('tr').length, sample:(t.innerText||'').slice(0,160)}));
      const msgs=[...document.querySelectorAll('.ui-growl-item,.ui-messages-error,.ui-messages-info')].map(e=>(e.innerText||'').trim()).filter(Boolean);
      const status=/(Completed|Success|Failed|Error|Running|Exit)[^\\n]{0,40}/gi; const st=txt.match(status)||[];
      return {grids, msgs, statusHits: st.slice(0,8)};
    }""")
    print("result grids:", json.dumps(res["grids"])[:500])
    print("status hits:", json.dumps(res["statusHits"]))
    print("messages:", json.dumps(res["msgs"])[:300])
    page.screenshot(path="c:/Projects/ChoongYin_OS/tmp/ha0002_runcalc.png", full_page=True)
    b.close()
print("AFTER  (cnt, lastUpd, negs, sumGas, sumOil):", db())
