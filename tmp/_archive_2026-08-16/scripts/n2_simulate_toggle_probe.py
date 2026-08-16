"""N2 final probe: reliably toggle Simulate ON, then run POSITIVE (RUN_NO) and NEGATIVE (P1) with
Simulate, polling log_list for the NEW row + its Exit Status (cell 7) + time to appear. De-risks the
RF build (toggle gesture, completion detection, exact statuses). Simulate = no DB write."""
import time, json
from playwright.sync_api import sync_playwright
URL="https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"; SCREEN="Daily Allocation"
SIM_INPUT="dateStartJob:form:G:0:R:1:C:2:cb"; SIM_CELL="dateStartJob:form:G:0:R:1:C:2"

def opts(fr,g):
    fr.locator(f'[id="nav:form:G:{g}:R:1:C:0:dd_button"]').click(timeout=4000); time.sleep(0.9)
    return fr.evaluate(f"""()=>[...document.querySelectorAll('[id="nav:form:G:{g}:R:1:C:0:dd_panel"] tr[data-item-label]')].map(e=>(e.getAttribute('data-item-label')||'')).filter(t=>t.trim())""")
def pick(fr,g,label):
    fr.locator(f'[id="nav:form:G:{g}:R:1:C:0:dd_panel"] tr[data-item-label="{label}"]').first.click(timeout=4000); time.sleep(1.3)
def sim_state(fr):
    return fr.evaluate(f"""()=>{{const i=document.getElementById('{SIM_INPUT}'); return i?i.checked:null;}}""")
def cell_html(fr):
    return fr.evaluate(f"""()=>{{const c=document.getElementById('{SIM_CELL}'); return c?c.outerHTML.slice(0,400):'NO CELL';}}""")

def run_scope(fr, page, date, net, label):
    for g in (0,1):
        di=fr.locator(f'[id="nav:form:G:{g}:R:1:C:0:da_input"]'); di.fill(date); di.press("Tab"); time.sleep(1.0)
    opts(fr,2); pick(fr,2,net)
    opts(fr,3); g4=opts(fr,4)
    print(f"  [{label}] calc jobs:", g4)
    pick(fr,4,g4[0])
    fr.locator('[id="button:form:B"]').click(timeout=5000); page.wait_for_load_state("networkidle",timeout=30000); time.sleep(2.0)
    print(f"  [{label}] Simulate before:", sim_state(fr))
    # toggle ON by clicking the visible cell box (try cell, then label span)
    for clicker in (SIM_CELL, SIM_CELL+":box"):
        try:
            fr.locator(f'[id="{clicker}"]').click(timeout=2500); time.sleep(0.6)
            if sim_state(fr): break
        except Exception: pass
    if not sim_state(fr):
        # fallback: click the .ECCheckboxCell wrapper near the input
        fr.evaluate(f"""()=>{{const i=document.getElementById('{SIM_INPUT}'); const cell=i.closest('.ECCheckboxCell,td,div'); const box=cell?cell.querySelector('div,span'):null; (box||i).click();}}""")
        time.sleep(0.6)
    print(f"  [{label}] Simulate after:", sim_state(fr))
    if sim_state(fr) is None or sim_state(fr) is False:
        print(f"  [{label}] CELL HTML:", cell_html(fr))
    before=fr.evaluate("""()=>{const t=document.getElementById('log_list:form:T_data'); return t?t.querySelectorAll('tr').length:0;}""")
    fr.locator('[id="ProdAllocButton:form:B"]').click(timeout=6000)
    status=None; appeared=None
    for i in range(12):
        time.sleep(2.0)
        try: page.wait_for_load_state("networkidle",timeout=6000)
        except Exception: pass
        top=fr.evaluate("""()=>{const t=document.getElementById('log_list:form:T_data'); if(!t)return null; const tr=t.querySelector('tr'); return tr?[...tr.querySelectorAll('td')].map(td=>(td.textContent||'').trim()):null;}""")
        n=fr.evaluate("""()=>{const t=document.getElementById('log_list:form:T_data'); return t?t.querySelectorAll('tr').length:0;}""")
        if top and (n>before or (top[7] if len(top)>7 else '')):
            status = top[7] if len(top)>7 else None
            appeared=(i+1)*2
            # accept once we see a terminal status word
            if status and any(k in status for k in ("Success","Failure","Error")):
                print(f"  [{label}] t+{appeared}s rows {before}->{n} EXIT STATUS='{status}' top={json.dumps(top)}")
                break
    else:
        print(f"  [{label}] NO terminal status within poll; last top status='{status}'")
    return status

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
    print("== POSITIVE ==")
    run_scope(fr, page, "2003-01-01", "Testing allocation RUN_NO", "POS")
    # reload screen state for a clean negative scope (re-pick networks)
    print("== NEGATIVE ==")
    run_scope(fr, page, "2021-10-01", "P1 Dashboard", "NEG")
    b.close()
print("DONE")
