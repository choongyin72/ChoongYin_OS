"""Crack the WR.0001 inline-grid SAVE gesture. Edits C4 (ON_STREAM_HRS) 24->21 via several
candidate save gestures, DB-checks persistence after each, and ALWAYS reverts to 24 at the end.
Self-cleaning + DB-verified. Well AS2_Onshore Well no 2 / 2003-01-01."""
import sys, time
sys.path.insert(0, r"c:/Projects/ChoongYin_OS/workstreams/master-plan/ec-automation/libraries")
import DbVerify as d
from playwright.sync_api import sync_playwright

URL = "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"
SCREEN = "Daily Production Well Status 1"
OID = "96D7FD4CB6490217E053020011AC1940"
CELL = 'daily_well_status:form:T:0:C4_in'

def dbval():
    return d.day_status_value("PWEL_DAY_STATUS", OID, "2003-01-01", "ON_STREAM_HRS")
def dd_opts(fr, g):
    fr.locator(f'[id="nav:form:G:{g}:R:1:C:0:dd_button"]').click(timeout=4000); time.sleep(0.7)
    return fr.evaluate(f"""() => [...document.querySelectorAll('[id="nav:form:G:{g}:R:1:C:0:dd_panel"] tr[data-item-label]')].map(e=>(e.getAttribute('data-item-label')||'').trim()).filter(t=>t)""")
def dd_pick(fr, g, label):
    fr.locator(f'[id="nav:form:G:{g}:R:1:C:0:dd_panel"] tr[data-item-label="{label}"]').first.click(timeout=4000); time.sleep(1.0)
def edit_cell(fr, val):
    fr.locator(f'[id="{CELL}"]').click(timeout=4000)
    fr.locator(f'[id="{CELL}"]').fill(str(val))
    fr.locator(f'[id="{CELL}"]').press("Tab")
    fr.page.wait_for_load_state("networkidle", timeout=12000); time.sleep(1.2)

print("DB before:", dbval())
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_context(ignore_https_errors=True, viewport={"width":1920,"height":1080}).new_page()
    page.goto(URL, wait_until="domcontentloaded", timeout=60000)
    page.fill('[id="username"]',"sysadmin"); page.fill('[id="password"]',"sysadmin"); page.click('[id="kc-login"]')
    page.wait_for_selector('[id="menu:searchForm:searchTxt"]', timeout=60000)
    sel=f'xpath=//*[contains(@class,"tv-link") and normalize-space(text())="{SCREEN}"]'
    fr=None
    for _ in range(2):
        page.fill('[id="menu:searchForm:searchTxt"]',""); page.locator('[id="menu:searchForm:searchTxt"]').type(SCREEN, delay=40)
        page.wait_for_selector(sel, timeout=15000); time.sleep(0.6); page.locator(sel).first.click()
        page.wait_for_load_state("networkidle", timeout=30000)
        for _ in range(25):
            fr=next((f for f in page.frames if "daily_well_status" in f.url), None)
            if fr: break
            time.sleep(1.0)
        if fr: break
    if not fr: print("no frame"); browser.close(); raise SystemExit
    time.sleep(2.0)
    fr.locator('[id="nav:form:G:0:R:1:C:0:da_input"]').fill("2003-01-01"); fr.locator('[id="nav:form:G:0:R:1:C:0:da_input"]').press("Tab"); time.sleep(1.5)
    dd_opts(fr,1); dd_pick(fr,1,"AS2 EC Exploration Norway")
    dd_opts(fr,2); dd_pick(fr,2,"AS2_Onshore Area")
    dd_opts(fr,3); dd_pick(fr,3,"AS2_Production Facility no 1")
    dd_opts(fr,4); dd_pick(fr,4,"AS2_Lift Gas Manifold 1")
    fr.locator('[id="button:form:B"]').click(timeout=5000); page.wait_for_load_state("networkidle", timeout=30000); time.sleep(4.0)
    print("grid C4 on load:", fr.locator(f'[id="{CELL}"]').input_value())

    # Gesture A: edit + Ctrl+s keyboard
    edit_cell(fr, 21)
    print("after edit, C4 =", fr.locator(f'[id="{CELL}"]').input_value())
    fr.locator(f'[id="{CELL}"]').press("Control+s")
    page.wait_for_load_state("networkidle", timeout=15000); time.sleep(2.5)
    print("DB after Ctrl+s:", dbval())

    # Gesture B (if still not 21): look for an ENABLED save anywhere + JS-click it
    if str(dbval()) != "21":
        saves = page.evaluate("""() => [...document.querySelectorAll('a[title^="Save"]')].map((e,i)=>({i, disabled:e.className.includes('ui-state-disabled'), id:e.id, oc:(e.getAttribute('onclick')||'').slice(0,60)}))""")
        print("save anchors (top):", saves)
        savesf = fr.evaluate("""() => [...document.querySelectorAll('a[title^="Save"]')].map((e,i)=>({i, disabled:e.className.includes('ui-state-disabled'), id:e.id, oc:(e.getAttribute('onclick')||'').slice(0,60)}))""")
        print("save anchors (frame):", savesf)

    # ALWAYS revert to 24 + save, then verify DB
    edit_cell(fr, 24)
    fr.locator(f'[id="{CELL}"]').press("Control+s")
    page.wait_for_load_state("networkidle", timeout=15000); time.sleep(2.5)
    browser.close()
print("DB after revert:", dbval())
