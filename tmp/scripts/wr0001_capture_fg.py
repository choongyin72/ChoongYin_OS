"""FOREGROUND headed capture: open WR.0001 @ AS2 scope, hold ~150s for the user to edit On-Stream
Hrs (row0) + Save in THIS window, capture all POSTs, then DB-verify ON_STREAM_HRS and print the
save request(s). Foreground so the window reliably surfaces (background launch didn't)."""
import sys, time, re
sys.path.insert(0, r"c:/Projects/ChoongYin_OS/workstreams/master-plan/ec-automation/libraries")
import DbVerify as d
from playwright.sync_api import sync_playwright
URL="https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"; SCREEN="Daily Production Well Status 1"
OID="96D7FD4CB6490217E053020011AC1940"
def dbval(): return d.day_status_value("PWEL_DAY_STATUS", OID, "2003-01-01", "ON_STREAM_HRS")
def dd_opts(fr,g):
    fr.locator(f'[id="nav:form:G:{g}:R:1:C:0:dd_button"]').click(timeout=5000); time.sleep(0.8)
    return fr.evaluate(f"""()=>[...document.querySelectorAll('[id="nav:form:G:{g}:R:1:C:0:dd_panel"] tr[data-item-label]')].map(e=>(e.getAttribute('data-item-label')||'').trim()).filter(t=>t)""")
def dd_pick(fr,g,l): fr.locator(f'[id="nav:form:G:{g}:R:1:C:0:dd_panel"] tr[data-item-label="{l}"]').first.click(timeout=5000); time.sleep(1.2)

posts=[]; t0=time.time(); ready_t=[None]
with sync_playwright() as p:
    b=p.chromium.launch(headless=False); page=b.new_context(ignore_https_errors=True, viewport={"width":1680,"height":1000}).new_page()
    def on_req(req):
        if req.method=="POST":
            pd=""
            try: pd=req.post_data or ""
            except Exception: pd=""
            src=re.search(r'jakarta\.faces\.source=([^&]+)', pd) or re.search(r'javax\.faces\.source=([^&]+)', pd)
            posts.append((time.time()-t0, src.group(1) if src else '?', pd[:260]))
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
    if not fr: print("ERROR no frame"); b.close(); raise SystemExit
    time.sleep(2.0)
    fr.locator('[id="nav:form:G:0:R:1:C:0:da_input"]').fill("2003-01-01"); fr.locator('[id="nav:form:G:0:R:1:C:0:da_input"]').press("Tab"); time.sleep(1.5)
    dd_opts(fr,1); dd_pick(fr,1,"AS2 EC Exploration Norway")
    dd_opts(fr,2); dd_pick(fr,2,"AS2_Onshore Area")
    dd_opts(fr,3); dd_pick(fr,3,"AS2_Production Facility no 1")
    dd_opts(fr,4); dd_pick(fr,4,"AS2_Lift Gas Manifold 1")
    fr.locator('[id="button:form:B"]').click(timeout=6000); page.wait_for_load_state("networkidle",timeout=30000); time.sleep(3.0)
    # Refresh to clear any phantom uncommitted values -> grid shows TRUE DB values
    try:
        page.locator('xpath=//a[@title="Refresh [Ctrl+r]"]').first.click(timeout=6000)
        page.wait_for_load_state("networkidle",timeout=20000); time.sleep(3.0)
    except Exception as e:
        print("refresh skipped:", str(e)[:60])
    try: pre = fr.locator('[id="daily_well_status:form:T:0:C4_in"]').input_value()
    except Exception: pre="?"
    ready_t[0]=time.time()-t0
    print(f">>> READY at {ready_t[0]:.0f}s — cell C4 shows {pre}, DB={dbval()} — YOUR TURN <<<", flush=True)
    time.sleep(210)  # user acts here
    try: cellv = fr.locator('[id="daily_well_status:form:T:0:C4_in"]').input_value()
    except Exception: cellv="?"
    b.close()

print("\n=== POSTs AFTER ready (your actions) ===")
rt=ready_t[0] or 0
acted=[x for x in posts if x[0] > rt + 0.5]
for ts,src,pd in acted:
    print(f"[{ts:6.1f}s] SOURCE={src}\n    {pd}")
if not acted: print("(no POSTs captured after ready — save happened in another window again?)")
print("\ncell C4 at end:", cellv)
print("DB ON_STREAM_HRS at end:", dbval())
