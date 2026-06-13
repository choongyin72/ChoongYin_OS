"""Commit the WR.0001 inline edit properly: real change 24->23, inspect ALL Save anchors
(visible/onclick), click the VISIBLE enabled one, handle any confirm dialog, DB-verify; revert."""
import sys, time, json
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

def dump_saves(page):
    return page.evaluate("""()=>[...document.querySelectorAll('a[title^="Save"]')].map(e=>({
        vis: e.offsetParent!==null, disabled:e.className.includes('ui-state-disabled'),
        id:e.id||'', oc:(e.getAttribute('onclick')||'').slice(0,70), cls:e.className.slice(0,45)}))""")

def commit_save(page):
    saves = dump_saves(page)
    print("  Save anchors:", json.dumps(saves))
    # click the visible, enabled one via Playwright (actionable)
    clicked=False
    loc = page.locator('xpath=//a[starts-with(@title,"Save") and not(contains(@class,"ui-state-disabled"))]')
    n = loc.count()
    for i in range(n):
        el = loc.nth(i)
        try:
            if el.is_visible():
                el.click(timeout=6000); clicked=True; print(f"  clicked visible Save #{i}"); break
        except Exception as ex:
            print(f"  click #{i} err:", str(ex)[:60])
    if not clicked and n>0:
        loc.first.click(timeout=6000, force=True); clicked=True; print("  force-clicked Save #0")
    page.wait_for_load_state("networkidle", timeout=15000); time.sleep=getattr(time,'sleep'); time.sleep(2.0)
    # handle any confirm dialog (Yes/OK/Save)
    dlg = page.locator('xpath=//div[contains(@class,"ui-dialog") and not(contains(@style,"display: none"))]//button[.//span[contains(.,"Yes") or contains(.,"OK") or contains(.,"Save")]] | //button[.//span[contains(.,"Yes")]]')
    if dlg.count()>0:
        try:
            dlg.first.click(timeout=5000); print("  confirm dialog -> clicked Yes/OK")
            page.wait_for_load_state("networkidle", timeout=15000); time.sleep(2.0)
        except Exception as ex: print("  dialog err:", str(ex)[:60])
    else:
        print("  (no confirm dialog)")

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
    print("grid C4 on load:", fr.locator(f'[id="{CELL}"]').input_value())

    print("--- EDIT 24 -> 23 ---")
    fr.locator(f'[id="{CELL}"]').click(timeout=4000); fr.locator(f'[id="{CELL}"]').fill("23"); fr.locator(f'[id="{CELL}"]').press("Tab")
    page.wait_for_load_state("networkidle",timeout=12000); time.sleep(1.5)
    print("  cell now:", fr.locator(f'[id="{CELL}"]').input_value())
    commit_save(page)
    print("DB after commit:", dbval())

    print("--- REVERT -> 24 ---")
    fr.locator(f'[id="{CELL}"]').click(timeout=4000); fr.locator(f'[id="{CELL}"]').fill("24"); fr.locator(f'[id="{CELL}"]').press("Tab")
    page.wait_for_load_state("networkidle",timeout=12000); time.sleep(1.5)
    commit_save(page)
    b.close()
print("DB after revert:", dbval())
