"""Crack 'Daily Production Flowline, by Flowline': set date 2003-09-20, dump nav dd groups + options,
greedily cascade (prefer options that lead to data), GO, dump the grid id + first rows + cell ids.
Confirm it mirrors the N1 daily well-grid pattern. Read-only."""
import time, json, os
from playwright.sync_api import sync_playwright

URL = "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"
SCREEN = "Daily Production Flowline, by Flowline"
DATE = "2003-09-20"


def dd_opts(fr, g):
    try:
        fr.locator(f'[id="nav:form:G:{g}:R:1:C:0:dd_button"]').click(timeout=4000); time.sleep(0.7)
        opts = fr.evaluate(f"""()=>[...document.querySelectorAll('[id="nav:form:G:{g}:R:1:C:0:dd_panel"] tr[data-item-label]')].map(e=>(e.getAttribute('data-item-label')||'').trim()).filter(t=>t)""")
        return opts
    except Exception as e:
        return [f"ERR {str(e)[:40]}"]


def dd_pick(fr, g, label):
    fr.locator(f'[id="nav:form:G:{g}:R:1:C:0:dd_panel"] tr[data-item-label="{label}"]').first.click(timeout=4000); time.sleep(1.1)


with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    page = b.new_context(ignore_https_errors=True, viewport={"width": 1680, "height": 1000}).new_page()
    page.goto(URL, wait_until="domcontentloaded", timeout=60000)
    page.fill('[id="username"]', "sysadmin"); page.fill('[id="password"]', "sysadmin"); page.click('[id="kc-login"]')
    page.wait_for_selector('[id="menu:searchForm:searchTxt"]', timeout=60000); time.sleep(1.0)
    sel = f'xpath=//*[contains(@class,"tv-link") and normalize-space(text())="{SCREEN}"]'
    page.locator('[id="menu:searchForm:searchTxt"]').type(SCREEN, delay=25)
    page.wait_for_selector(sel, timeout=12000); page.locator(sel).first.click()
    page.wait_for_load_state("networkidle", timeout=30000); time.sleep(2.5)
    fr = next((f for f in page.frames if "dashboard.jsf" in (f.url or "") and "top=false" in (f.url or "")), None) or page
    # nav structure
    nav = fr.evaluate("""()=>{const o={};document.querySelectorAll('[id^="nav:form:G:"]').forEach(e=>{const m=e.id.match(/nav:form:G:(\\d+)/);if(m){o[m[1]]=o[m[1]]||{};if(/da_input/.test(e.id))o[m[1]].date=true;if(/dd_button/.test(e.id))o[m[1]].dd=true;}});return o;}""")
    print("nav groups:", json.dumps(nav))
    # set date (assume G0)
    di = fr.locator('[id="nav:form:G:0:R:1:C:0:da_input"]')
    if di.count():
        di.fill(DATE); di.press("Tab"); time.sleep(1.0); print("date set", DATE)
    # greedy cascade through dd groups (skip G0 if it's the date)
    chain = {}
    for g in sorted(int(k) for k in nav):
        if nav[str(g)].get("dd"):
            opts = dd_opts(fr, g)
            if opts and not opts[0].startswith("ERR"):
                pick = opts[0]
                print(f"G{g} options({len(opts)}): {opts[:6]} -> pick {pick!r}")
                dd_pick(fr, g, pick); chain[g] = pick
            else:
                print(f"G{g}: {opts}")
    fr.locator('[id="button:form:B"]').click(timeout=5000); page.wait_for_load_state("networkidle", timeout=30000); time.sleep(2.5)
    print("chain:", json.dumps(chain))
    grids = fr.evaluate("""()=>[...document.querySelectorAll('[id$=":T_data"]')].map(t=>({id:t.id,rows:t.querySelectorAll('tr').length}))""")
    print("grids:", json.dumps(grids))
    dump = fr.evaluate("""()=>{const t=document.querySelector('[id$=":T_data"]');if(!t)return{};const trs=[...t.querySelectorAll('tr')].slice(0,3).map(tr=>[...tr.querySelectorAll('td')].slice(0,6).map(td=>(td.textContent||'').trim().slice(0,16)));const ins=[...t.querySelectorAll('[id$="_in"]')].slice(0,10).map(e=>e.id);return{firstRows:trs,cellIds:ins};}""")
    print("firstRows:", json.dumps(dump.get("firstRows"))); print("cellIds:", json.dumps(dump.get("cellIds")))
    b.close()
print("DONE")
