"""Targeted crack of 'Sub Daily Gas Stream Status - by Stream' to the P1 gas stream. Nav: Date(G0) +
PU(G1)=P1 Production Unit -> Area(G2)=P1 Area -> Facility(G3)=P1 Facility 1 -> Stream(G4)=P1 S059 M GAS
PO.0028. GO, dump grid id + headers + row0 cells (find C for ON_STREAM_HRS + the Daytime cell). Dumps
options at each level as fallback. Read-only."""
import time, json
from playwright.sync_api import sync_playwright

URL = "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"
SCREEN = "Sub Daily Gas Stream Status - by Stream"
DATE = "2011-01-01"
TARGETS = {1: "P1 Production Unit", 2: "P1 Area", 3: "P1 Facility 1", 4: "P1 S059 M GAS PO.0028"}


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
    page.locator('[id="menu:searchForm:searchTxt"]').type(SCREEN, delay=22)
    page.wait_for_selector(sel, timeout=12000); page.locator(sel).first.click()
    page.wait_for_load_state("networkidle", timeout=30000); time.sleep(3.0)
    fr = frame(page)
    di = fr.locator('[id="nav:form:G:0:R:1:C:0:da_input"]'); di.fill(DATE); di.press("Tab"); time.sleep(0.8)
    for g in (1, 2, 3, 4):
        o = opts(fr, g)
        want = TARGETS[g]
        target = next((x for x in o if x.strip() == want), None)
        print(f"  G{g}({len(o)}): {o[:6]}{' ...' if len(o)>6 else ''} -> {target or '(target not found; first='+repr(o[0] if o else None)+')'}")
        pick(fr, g, (target or o[0]).strip())
    fr.locator('[id="button:form:B"]').click(timeout=5000); page.wait_for_load_state("networkidle", timeout=30000); time.sleep(2.5)
    grids = fr.evaluate("""()=>[...document.querySelectorAll('[id$=":T_data"]')].map(t=>({id:t.id,rows:t.querySelectorAll('tr').length}))""")
    print("grids:", json.dumps(grids))
    info = fr.evaluate("""()=>{const t=document.querySelector('[id$=":T_data"]');if(!t)return{};
      const grid=t.id.replace(':T_data','');
      const heads=[...document.querySelectorAll('[id^="'+grid+'"] th')].map(th=>(th.textContent||'').trim()).filter(Boolean).slice(0,32);
      const row0=[...t.querySelectorAll('tr')][0];
      const cells=row0?[...row0.querySelectorAll('[id*=":C"]')].slice(0,14).map(e=>({c:(e.id.split(':T:0:')[1]||e.id.split(':T:')[1]||e.id),val:(e.value!==undefined?e.value:(e.textContent||'').trim()).slice(0,14)})):[];
      return {grid, headers:heads, cells};}""")
    print("grid:", info.get("grid")); print("HEADERS:", json.dumps(info.get("headers"))); print("ROW0:", json.dumps(info.get("cells")))
    b.close()
print("DONE")
