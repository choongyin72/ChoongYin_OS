"""HA.0002 — run EC_DAILY_VOLUME over a P1 network for 2021-10-01 (a date that already has 22
allocated wells), now that I know AS2_Onshore had no job. Complete the cascade (Group->Network->
Calc Job), GO, then locate + click the direct run/calculate trigger (NOT BPM). DB before/after
PWEL_DAY_ALLOC @2021-10-01. User-authorised; local DB refreshable."""
import time, json
import oracledb
from playwright.sync_api import sync_playwright
URL="https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"; SCREEN="Daily Allocation"; DATE="2021-10-01"
def alloc_count():
    c=oracledb.connect(user="ECKERNEL_EC",password="energy",dsn="localhost:1521/ORCL",tcp_connect_timeout=15).cursor()
    c.execute("SELECT COUNT(*), TO_CHAR(MAX(LAST_UPDATED_DATE),'HH24:MI:SS'), TO_CHAR(MAX(CREATED_DATE),'YYYY-MM-DD HH24:MI') FROM ECKERNEL_EC.PWEL_DAY_ALLOC WHERE TRUNC(DAYTIME)=DATE '2021-10-01'")
    return c.fetchone()
def opts(fr,g):
    try:
        fr.locator(f'[id="nav:form:G:{g}:R:1:C:0:dd_button"]').click(timeout=4000); time.sleep(0.9)
        return fr.evaluate(f"""()=>[...document.querySelectorAll('[id="nav:form:G:{g}:R:1:C:0:dd_panel"] tr[data-item-label]')].map(e=>(e.getAttribute('data-item-label')||'').trim()).filter(t=>t)""")
    except Exception: return []
def pick(fr,g,label):
    try: fr.locator(f'[id="nav:form:G:{g}:R:1:C:0:dd_panel"] tr[data-item-label="{label}"]').first.click(timeout=4000); time.sleep(1.3); return True
    except Exception as e: print("  pick err",label,str(e)[:40]); return False
print("PWEL_DAY_ALLOC @2021-10-01 BEFORE (count, lastUpd, created):", alloc_count())
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
    g2=opts(fr,2); print("G2 options:", g2[:14])
    # prefer a P1 daily network
    g2pick=next((x for x in g2 if "P1 Day" in x or "P1 Dashboard" in x), None) or next((x for x in g2 if x.startswith("P1")), None)
    print("G2 pick:", g2pick); pick(fr,2,g2pick)
    g3=opts(fr,3); print("G3 options:", g3[:14])
    if g3: pick(fr,3,g3[0])
    g4=opts(fr,4); print("G4 (calc job) options:", g4[:14])
    g4pick=next((x for x in g4 if "DAILY_VOLUME" in x), None) or (g4[0] if g4 else None)
    print("G4 pick:", g4pick)
    if g4pick: pick(fr,4,g4pick)
    fr.locator('[id="button:form:B"]').click(timeout=5000); page.wait_for_load_state("networkidle",timeout=30000); time.sleep(3.0); print("GO done")
    # enumerate ALL toolbar/menu items + any run/calculate action now visible (incl overflow menus)
    actions=page.evaluate("""()=>{
      const vis=e=>e&&e.offsetParent!==null;
      return [...document.querySelectorAll('a[title],button[title],a.ui-menuitem-link,button.ui-button,a.ui-button')].filter(vis)
        .map(e=>({t:(e.textContent||'').trim().slice(0,28), title:(e.title||'').slice(0,28), id:e.id||''}))
        .filter(x=>x.t||x.title);
    }""")
    print("visible actions:", json.dumps(actions)[:900])
    page.screenshot(path="c:/Projects/ChoongYin_OS/tmp/ha0002_p1_after_go.png", full_page=True)
    b.close()
print("PWEL_DAY_ALLOC @2021-10-01 AFTER:", alloc_count())
