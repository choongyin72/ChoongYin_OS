"""WR.0001 write with REAL KEYSTROKES (not fill) — the framework warns synthetic fill() does not
stage inline-grid values server-side. Edit C4 to a unique sentinel via typed keys + Tab, toolbar
Save, DB-verify; then revert to 24 + Save + DB-verify. Self-cleaning."""
import sys, time
sys.path.insert(0, r"c:/Projects/ChoongYin_OS/workstreams/master-plan/ec-automation/libraries")
import DbVerify as d
from playwright.sync_api import sync_playwright
URL="https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"; SCREEN="Daily Production Well Status 1"
OID="96D7FD4CB6490217E053020011AC1940"; CELL='daily_well_status:form:T:0:C4_in'
def dbval(): return d.day_status_value("PWEL_DAY_STATUS", OID, "2003-01-01", "ON_STREAM_HRS")
def dd_opts(fr,g):
    fr.locator(f'[id="nav:form:G:{g}:R:1:C:0:dd_button"]').click(timeout=4000); time.sleep(0.7)
    return fr.evaluate(f"""()=>[...document.querySelectorAll('[id="nav:form:G:{g}:R:1:C:0:dd_panel"] tr[data-item-label]')].map(e=>(e.getAttribute('data-item-label')||'').trim()).filter(t=>t)""")
def dd_pick(fr,g,l): fr.locator(f'[id="nav:form:G:{g}:R:1:C:0:dd_panel"] tr[data-item-label="{l}"]').first.click(timeout=4000); time.sleep(1.0)

def type_cell(fr, page, val):
    # REAL keystrokes: focus, select-all, type, Tab -> fires EC onchange (PrimeFaces.ab) to stage
    el = fr.locator(f'[id="{CELL}"]'); el.click(timeout=4000)
    el.press("Control+a"); el.press("Delete")
    el.type(str(val), delay=80)
    el.press("Tab")
    page.wait_for_load_state("networkidle", timeout=12000); time.sleep(1.8)

def save(page):
    loc = page.locator('xpath=//a[starts-with(@title,"Save") and not(contains(@class,"ui-state-disabled"))]')
    if loc.count()==0: print("  Save not enabled"); return False
    loc.first.click(timeout=6000); page.wait_for_load_state("networkidle", timeout=15000); time.sleep(2.5)
    print("  Save clicked"); return True

print("DB before:", dbval())
with sync_playwright() as p:
    b=p.chromium.launch(headless=True); page=b.new_context(ignore_https_errors=True,viewport={"width":1920,"height":1080}).new_page()
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
    dd_opts(fr,1); dd_pick(fr,1,"AS2 EC Exploration Norway"); dd_opts(fr,2); dd_pick(fr,2,"AS2_Onshore Area")
    dd_opts(fr,3); dd_pick(fr,3,"AS2_Production Facility no 1"); dd_opts(fr,4); dd_pick(fr,4,"AS2_Lift Gas Manifold 1")
    fr.locator('[id="button:form:B"]').click(timeout=5000); page.wait_for_load_state("networkidle",timeout=30000); time.sleep(4.0)
    cur = fr.locator(f'[id="{CELL}"]').input_value(); print("grid C4 on load:", cur)

    SENTINEL = "22" if cur.strip() not in ("22","22.00") else "20"
    print(f"--- TYPE {SENTINEL} (real keystrokes) ---")
    type_cell(fr, page, SENTINEL)
    print("  cell now:", fr.locator(f'[id="{CELL}"]').input_value())
    save(page)
    after = dbval(); print(f"DB after save {SENTINEL}:", after, "==", SENTINEL, "?", str(after)==SENTINEL)

    print("--- REVERT 24 (real keystrokes) ---")
    type_cell(fr, page, "24")
    save(page)
    b.close()
print("DB after revert:", dbval())
