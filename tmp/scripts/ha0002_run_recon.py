"""HA.0002 run-mechanism recon (READ-ONLY): set From/To date to a date with allocation history,
populate the Network Group/Network/Calc-Job dds, select them, GO, and observe what appears (a Run/
Calculate control? a results grid? a 'process automation' dependency?). Does NOT commit a calc run
beyond clicking GO (which on this screen loads/views; the actual calc trigger is what we're mapping)."""
import time, json
from playwright.sync_api import sync_playwright
URL="https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"; SCREEN="Daily Allocation"
DATE="2021-10-01"
def opts(fr,g):
    try:
        fr.locator(f'[id="nav:form:G:{g}:R:1:C:0:dd_button"]').click(timeout=4000); time.sleep(0.9)
        o=fr.evaluate(f"""()=>[...document.querySelectorAll('[id="nav:form:G:{g}:R:1:C:0:dd_panel"] tr[data-item-label]')].map(e=>(e.getAttribute('data-item-label')||'').trim()).filter(t=>t)""")
        return o
    except Exception as e: return [f"ERR{str(e)[:30]}"]
def pick(fr,g,label):
    fr.locator(f'[id="nav:form:G:{g}:R:1:C:0:dd_panel"] tr[data-item-label="{label}"]').first.click(timeout=4000); time.sleep(1.2)
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
    # set From + To date
    for g in (0,1):
        try:
            di=fr.locator(f'[id="nav:form:G:{g}:R:1:C:0:da_input"]'); di.fill(DATE); di.press("Tab"); time.sleep(1.0)
        except Exception as e: print(f"date G{g} err",str(e)[:40])
    print("after dates set:")
    g2=opts(fr,2); print(" G2 Network Group/Network:", g2[:12])
    if g2 and not g2[0].startswith("ERR"): pick(fr,2,g2[0])
    g3=opts(fr,3); print(" G3 Allocation Network:", g3[:12])
    if g3 and not g3[0].startswith("ERR"): pick(fr,3,g3[0])
    g4=opts(fr,4); print(" G4 Calculation Job:", g4[:12])
    if g4 and not g4[0].startswith("ERR"): pick(fr,4,g4[0])
    # GO
    try:
        fr.locator('[id="button:form:B"]').click(timeout=5000); page.wait_for_load_state("networkidle",timeout=30000); time.sleep(3.5); print("GO clicked")
    except Exception as e: print("GO err",str(e)[:50])
    # observe: any run/calculate control, grids, messages, the process-automation state
    obs=fr.evaluate("""()=>{
      const vis=e=>e&&e.offsetParent!==null;
      const acts=[...document.querySelectorAll('a[title],button[title],a.ui-button,button.ui-button,a.ui-menuitem-link')].filter(vis)
        .map(e=>(e.textContent||e.title||'').trim()).filter(t=>t && /run|calc|execut|start|process|submit|allocat/i.test(t));
      const grids=[...document.querySelectorAll('[id$="T_data"]')].filter(vis).map(t=>({id:t.id,rows:t.querySelectorAll('tr').length}));
      const msgs=[...document.querySelectorAll('.ui-growl-item,.ui-messages-error,.ui-messages-info,.ui-message-error-detail')].map(e=>(e.innerText||'').trim()).filter(Boolean);
      return {actions:[...new Set(acts)], grids, msgs};
    }""")
    print("RUN/CALC actions visible:", json.dumps(obs["actions"]))
    print("grids:", json.dumps(obs["grids"]))
    print("messages:", json.dumps(obs["msgs"]))
    page.screenshot(path="c:/Projects/ChoongYin_OS/tmp/ha0002_after_go.png", full_page=True)
    b.close()
print("DONE")
