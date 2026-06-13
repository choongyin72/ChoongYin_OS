"""Revert AS2_Onshore Well no 2 ON_STREAM_HRS back to 24 AND validate the cracked gesture:
real-keystroke edit (fires the cell CHANGE behavior -> stages) + menubar Save (execute=@all ->
commits). Captures the change + save POSTs and DB-verifies 22->24. Headless (pure automation)."""
import sys, time, re
sys.path.insert(0, r"c:/Projects/ChoongYin_OS/workstreams/master-plan/ec-automation/libraries")
import DbVerify as d
from playwright.sync_api import sync_playwright
URL="https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"; SCREEN="Daily Production Well Status 1"
OID="96D7FD4CB6490217E053020011AC1940"; TARGET="24"
def dbval(): return d.day_status_value("PWEL_DAY_STATUS", OID, "2003-01-01", "ON_STREAM_HRS")
def dd_opts(fr,g):
    fr.locator(f'[id="nav:form:G:{g}:R:1:C:0:dd_button"]').click(timeout=5000); time.sleep(0.8)
    return fr.evaluate(f"""()=>[...document.querySelectorAll('[id="nav:form:G:{g}:R:1:C:0:dd_panel"] tr[data-item-label]')].map(e=>(e.getAttribute('data-item-label')||'').trim()).filter(t=>t)""")
def dd_pick(fr,g,l): fr.locator(f'[id="nav:form:G:{g}:R:1:C:0:dd_panel"] tr[data-item-label="{l}"]').first.click(timeout=5000); time.sleep(1.2)
posts=[]
with sync_playwright() as p:
    b=p.chromium.launch(headless=True); page=b.new_context(ignore_https_errors=True,viewport={"width":1680,"height":1000}).new_page()
    def on_req(req):
        if req.method=="POST":
            pd=""
            try: pd=req.post_data or ""
            except Exception: pd=""
            s=re.search(r'jakarta\.faces\.source=([^&]+)', pd)
            ev=re.search(r'jakarta\.faces\.behavior\.event=([^&]+)', pd)
            ex=re.search(r'jakarta\.faces\.partial\.execute=([^&]+)', pd)
            posts.append((s.group(1) if s else '?', ev.group(1) if ev else '-', ex.group(1) if ex else '-'))
    page.on("request", on_req)
    page.goto(URL,wait_until="domcontentloaded",timeout=60000)
    page.fill('[id="username"]',"sysadmin"); page.fill('[id="password"]',"sysadmin"); page.click('[id="kc-login"]')
    page.wait_for_selector('[id="menu:searchForm:searchTxt"]',timeout=60000)
    sel=f'xpath=//*[contains(@class,"tv-link") and normalize-space(text())="{SCREEN}"]'; fr=None
    for _ in range(2):
        page.fill('[id="menu:searchForm:searchTxt"]',""); page.locator('[id="menu:searchForm:searchTxt"]').type(SCREEN,delay=40)
        page.wait_for_selector(sel,timeout=15000); time.sleep(0.6); page.locator(sel).first.click()
        page.wait_for_load_state("networkidle",timeout=30000)
        for _ in range(25):
            fr=next((f for f in page.frames if "daily_well_status" in f.url),None)
            if fr: break
            time.sleep(1.0)
        if fr: break
    if not fr: print("no frame"); b.close(); raise SystemExit
    time.sleep(2.0)
    fr.locator('[id="nav:form:G:0:R:1:C:0:da_input"]').fill("2003-01-01"); fr.locator('[id="nav:form:G:0:R:1:C:0:da_input"]').press("Tab"); time.sleep(1.5)
    dd_opts(fr,1); dd_pick(fr,1,"AS2 EC Exploration Norway")
    dd_opts(fr,2); dd_pick(fr,2,"AS2_Onshore Area")
    dd_opts(fr,3); dd_pick(fr,3,"AS2_Production Facility no 1")
    dd_opts(fr,4); dd_pick(fr,4,"AS2_Lift Gas Manifold 1")
    fr.locator('[id="button:form:B"]').click(timeout=6000); page.wait_for_load_state("networkidle",timeout=30000); time.sleep(3.0)

    # find the row whose well-name cell == AS2_Onshore Well no 2
    row = fr.evaluate("""()=>{const tb=document.getElementById('daily_well_status:form:T_data');let idx=-1;
      tb.querySelectorAll('tr').forEach((tr,i)=>{ if((tr.textContent||'').includes('AS2_Onshore Well no 2')) idx=i; }); return idx;}""")
    print("Well no 2 at row index:", row)
    CELL=f"daily_well_status:form:T:{row}:C4_in"
    print("DB before:", dbval(), " cell shows:", fr.locator(f'[id="{CELL}"]').input_value())
    posts.clear()
    # GESTURE: real keystrokes -> Tab (fires change/stage) -> menubar Save (execute=@all)
    el=fr.locator(f'[id="{CELL}"]'); el.click(); el.press("Control+a"); el.press("Delete"); el.type(TARGET, delay=90); el.press("Tab")
    page.wait_for_load_state("networkidle",timeout=12000); time.sleep(1.8)
    sv=page.locator('xpath=//a[starts-with(@title,"Save") and not(contains(@class,"ui-state-disabled"))]')
    print("Save enabled?", sv.count()>0)
    if sv.count()>0:
        sv.first.click(timeout=6000); page.wait_for_load_state("networkidle",timeout=15000); time.sleep(2.5)
    b.close()
print("\nPOSTs during edit+save:")
for s,ev,ex in posts: print(f"  source={s}  event={ev}  execute={ex}")
print("\nDB after:", dbval(), "(target", TARGET+")")
