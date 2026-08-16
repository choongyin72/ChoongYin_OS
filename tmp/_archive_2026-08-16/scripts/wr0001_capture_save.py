"""Headed capture session: open WR.0001, load the AS2 scope, then HOLD the browser open and log
every POST request (the JSF AJAX) to a file so we can see exactly what a real user's Save sends.
The user performs the edit + Save manually in the visible browser. READ + capture only."""
import time
from pathlib import Path
from playwright.sync_api import sync_playwright
URL="https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"; SCREEN="Daily Production Well Status 1"
OUT=Path(r"c:/Projects/ChoongYin_OS/tmp/wr0001_capture"); OUT.mkdir(parents=True, exist_ok=True)
LOG=OUT/"network.log"; READY=OUT/"READY.txt"; DONE=OUT/"DONE.txt"
LOG.write_text("", encoding="utf-8")
for f in (READY, DONE):
    if f.exists(): f.unlink()
t0=time.time()
def log(line):
    with open(LOG,"a",encoding="utf-8") as f: f.write(f"[{time.time()-t0:6.1f}s] {line}\n")
def dd_opts(fr,g):
    fr.locator(f'[id="nav:form:G:{g}:R:1:C:0:dd_button"]').click(timeout=5000); time.sleep(0.8)
    return fr.evaluate(f"""()=>[...document.querySelectorAll('[id="nav:form:G:{g}:R:1:C:0:dd_panel"] tr[data-item-label]')].map(e=>(e.getAttribute('data-item-label')||'').trim()).filter(t=>t)""")
def dd_pick(fr,g,l): fr.locator(f'[id="nav:form:G:{g}:R:1:C:0:dd_panel"] tr[data-item-label="{l}"]').first.click(timeout=5000); time.sleep(1.2)

with sync_playwright() as p:
    b=p.chromium.launch(headless=False); ctx=b.new_context(ignore_https_errors=True, viewport={"width":1680,"height":1000}); page=ctx.new_page()
    def on_req(req):
        if req.method=="POST":
            pd=""
            try: pd=req.post_data or ""
            except Exception: pd=""
            # surface the JSF source/behaviour params that reveal which action fired
            import re
            src=re.search(r'javax\.faces\.source=([^&]+)', pd); beh=re.search(r'javax\.faces\.behavior\.event=([^&]+)', pd)
            tag=f" SOURCE={src.group(1) if src else '?'} EVENT={beh.group(1) if beh else '-'}"
            log(f"POST {req.url.split('/')[-1][:50]}{tag} :: {pd[:220]}")
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
    if not fr: log("ERROR no frame"); b.close(); raise SystemExit
    time.sleep(2.0)
    fr.locator('[id="nav:form:G:0:R:1:C:0:da_input"]').fill("2003-01-01"); fr.locator('[id="nav:form:G:0:R:1:C:0:da_input"]').press("Tab"); time.sleep(1.5)
    dd_opts(fr,1); dd_pick(fr,1,"AS2 EC Exploration Norway")
    dd_opts(fr,2); dd_pick(fr,2,"AS2_Onshore Area")
    dd_opts(fr,3); dd_pick(fr,3,"AS2_Production Facility no 1")
    dd_opts(fr,4); dd_pick(fr,4,"AS2_Lift Gas Manifold 1")
    fr.locator('[id="button:form:B"]').click(timeout=6000); page.wait_for_load_state("networkidle",timeout=30000); time.sleep(3.0)
    log("=== READY: grid loaded @ AS2 scope, 2003-01-01. Row 0 = AS2_Onshore Well no 2. USER'S TURN. ===")
    READY.write_text("ready", encoding="utf-8")
    # hold open up to 8 min OR until a DONE.txt marker appears, capturing all POSTs
    for _ in range(480):
        if DONE.exists(): log("DONE marker seen — closing soon"); break
        time.sleep(1.0)
    time.sleep(1.0)
    b.close()
log("session closed")
