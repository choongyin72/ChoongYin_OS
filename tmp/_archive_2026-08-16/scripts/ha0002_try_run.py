"""HA.0002 — focused attempt to RUN an allocation for AS2_Onshore (user authorised; local DB
refreshable). Date 2003-01-01 (AS2 has well/stream input then). Complete the cascade, find the
run/calc trigger, attempt it, and DB-check PWEL_DAY_ALLOC before/after to learn definitively whether
the calc runs here or is gated by 'process automation not available'."""
import time, json
import oracledb
from playwright.sync_api import sync_playwright
URL="https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"; SCREEN="Daily Allocation"; DATE="2003-01-01"
def alloc_count():
    c=oracledb.connect(user="ECKERNEL_EC",password="energy",dsn="localhost:1521/ORCL",tcp_connect_timeout=15).cursor()
    c.execute("SELECT COUNT(*) FROM ECKERNEL_EC.PWEL_DAY_ALLOC WHERE TRUNC(DAYTIME)=DATE '2003-01-01'")
    return c.fetchone()[0]
def opts(fr,g):
    try:
        fr.locator(f'[id="nav:form:G:{g}:R:1:C:0:dd_button"]').click(timeout=4000); time.sleep(0.9)
        return fr.evaluate(f"""()=>[...document.querySelectorAll('[id="nav:form:G:{g}:R:1:C:0:dd_panel"] tr[data-item-label]')].map(e=>(e.getAttribute('data-item-label')||'').trim()).filter(t=>t)""")
    except Exception: return []
def pick(fr,g,label):
    try: fr.locator(f'[id="nav:form:G:{g}:R:1:C:0:dd_panel"] tr[data-item-label="{label}"]').first.click(timeout=4000); time.sleep(1.3); return True
    except Exception: return False
print("PWEL_DAY_ALLOC @2003-01-01 BEFORE:", alloc_count())
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
    g2=opts(fr,2); print("G2:", g2[:12])
    pick(fr,2,"AS2_Onshore" if "AS2_Onshore" in g2 else (g2[0] if g2 else ""))
    g3=opts(fr,3); print("G3 (network):", g3[:12])
    if g3: pick(fr,3,g3[0])
    g4=opts(fr,4); print("G4 (calc job):", g4[:12])
    if g4: pick(fr,4,g4[0])
    fr.locator('[id="button:form:B"]').click(timeout=5000); page.wait_for_load_state("networkidle",timeout=30000); time.sleep(3.0); print("GO done")
    # look for a run/calculate trigger anywhere (toolbar menu, context, buttons) and click if found
    ran=fr.evaluate("""()=>{
      const vis=e=>e&&e.offsetParent!==null;
      const cand=[...document.querySelectorAll('a,button')].filter(vis).filter(e=>/calculate|run|execute|allocate|submit/i.test((e.textContent||'')+(e.title||'')));
      return cand.map(e=>({t:(e.textContent||e.title||'').trim().slice(0,30), id:e.id||''}));
    }""")
    print("run/calc candidates:", json.dumps(ran))
    # try clicking the first plausible calc trigger
    for cand in ran:
        if cand["id"]:
            try:
                fr.locator(f'[id="{cand["id"]}"]').first.click(timeout=4000); page.wait_for_load_state("networkidle",timeout=30000); time.sleep(3.0)
                print("clicked:", cand["t"]); break
            except Exception as e: print("click err",cand["t"],str(e)[:40])
    msgs=fr.evaluate("""()=>[...document.querySelectorAll('.ui-growl-item,.ui-messages-error,.ui-messages-info,.ui-message-error-detail,.ui-dialog:not([style*=\"display: none\"])')].map(e=>(e.innerText||'').trim()).filter(Boolean)""")
    print("messages/dialogs:", json.dumps(msgs)[:400])
    page.screenshot(path="c:/Projects/ChoongYin_OS/tmp/ha0002_run_attempt.png", full_page=True)
    b.close()
print("PWEL_DAY_ALLOC @2003-01-01 AFTER:", alloc_count())
