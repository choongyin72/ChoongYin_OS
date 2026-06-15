"""Targeted PFLW nav crack: find the PU (G2) whose Area (G3) contains 'Onshore area', then cascade
Area -> Facility (G4) -> Flowline (G5), GO, dump the grid id + first rows + cell ids. Deterministic
search (not greedy-first). Read-only."""
import time, json
from playwright.sync_api import sync_playwright

URL = "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"
SCREEN = "Daily Production Flowline, by Flowline"
DATE = "2003-09-20"
WANT_AREA = "Onshore area"   # match on normalized (leading space in stored label)
WANT_FLOWLINE = "PRD_FLUID_ADFAY_54401"


def frame(page):
    for _ in range(20):
        for fr in page.frames:
            try:
                if fr.evaluate("""()=>!!document.querySelector('[id="nav:form:G:0:R:1:C:0:da_input"]')"""):
                    return fr
            except Exception:
                pass
        time.sleep(1.0)
    return page


def opts(fr, g):
    fr.locator(f'[id="nav:form:G:{g}:R:1:C:0:dd_button"]').click(timeout=4000); time.sleep(0.6)
    o = fr.evaluate(f"""()=>[...document.querySelectorAll('[id="nav:form:G:{g}:R:1:C:0:dd_panel"] tr[data-item-label]')].map(e=>(e.getAttribute('data-item-label')||'').trim()).filter(t=>t)""")
    # close panel
    fr.locator(f'[id="nav:form:G:{g}:R:1:C:0:dd_button"]').click(timeout=2000); time.sleep(0.2)
    return o


def pick(fr, g, label):
    fr.locator(f'[id="nav:form:G:{g}:R:1:C:0:dd_button"]').click(timeout=4000); time.sleep(0.5)
    fr.locator(f'xpath=//*[@id="nav:form:G:{g}:R:1:C:0:dd_panel"]//tr[normalize-space(@data-item-label)="{label}"]').first.click(timeout=4000); time.sleep(1.1)


with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    page = b.new_context(ignore_https_errors=True, viewport={"width": 1680, "height": 1000}).new_page()
    page.goto(URL, wait_until="domcontentloaded", timeout=60000)
    page.fill('[id="username"]', "sysadmin"); page.fill('[id="password"]', "sysadmin"); page.click('[id="kc-login"]')
    page.wait_for_selector('[id="menu:searchForm:searchTxt"]', timeout=60000); time.sleep(1.0)
    sel = f'xpath=//*[contains(@class,"tv-link") and normalize-space(text())="{SCREEN}"]'
    page.locator('[id="menu:searchForm:searchTxt"]').type(SCREEN, delay=25)
    page.wait_for_selector(sel, timeout=12000); page.locator(sel).first.click()
    page.wait_for_load_state("networkidle", timeout=30000); time.sleep(3.0)
    fr = frame(page)
    for g in (0, 1):
        di = fr.locator(f'[id="nav:form:G:{g}:R:1:C:0:da_input"]'); di.fill(DATE); di.press("Tab"); time.sleep(0.8)
    pus = opts(fr, 2)
    print(f"PU options ({len(pus)})")
    chosen = None
    for pu in pus:
        pick(fr, 2, pu)
        areas = opts(fr, 3)
        if any(a.strip() == WANT_AREA for a in areas):
            chosen = pu; print(f"  -> PU '{pu}' has area '{WANT_AREA}' (areas={areas})"); break
    if not chosen:
        print("  no PU yields the area; aborting"); b.close(); raise SystemExit(0)
    pick(fr, 3, WANT_AREA)
    facs = opts(fr, 4); print("  G4 facility options:", facs)
    if facs:
        pick(fr, 4, facs[0].strip())
    fls = opts(fr, 5); print("  G5 flowline options:", fls)
    target_fl = next((f for f in fls if f.strip() == WANT_FLOWLINE), fls[0] if fls else None)
    if target_fl:
        pick(fr, 5, target_fl.strip()); print("  picked flowline:", target_fl)
    fr.locator('[id="button:form:B"]').click(timeout=5000); page.wait_for_load_state("networkidle", timeout=30000); time.sleep(2.5)
    grids = fr.evaluate("""()=>[...document.querySelectorAll('[id$=":T_data"]')].map(t=>({id:t.id,rows:t.querySelectorAll('tr').length}))""")
    print("grids:", json.dumps(grids))
    dump = fr.evaluate("""()=>{const t=document.querySelector('[id$=":T_data"]');if(!t)return{};const trs=[...t.querySelectorAll('tr')].slice(0,4).map(tr=>[...tr.querySelectorAll('td')].slice(0,8).map(td=>(td.textContent||'').trim().slice(0,16)));const ins=[...t.querySelectorAll('[id$="_in"]')].slice(0,14).map(e=>e.id);return{firstRows:trs,cellIds:ins};}""")
    print("firstRows:", json.dumps(dump.get("firstRows"))); print("cellIds:", json.dumps(dump.get("cellIds")))
    b.close()
print("DONE")
