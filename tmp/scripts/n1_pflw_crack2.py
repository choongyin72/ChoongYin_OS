"""PFLW crack v2 — robust frame acquisition (poll until the nav date field is present), then enumerate
the nav groups (date vs dd), set From/To date = 2003-09-20, cascade the dd groups greedily, GO, and
dump the grid id + first rows + cell ids. Read-only."""
import time, json
from playwright.sync_api import sync_playwright

URL = "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"
SCREEN = "Daily Production Flowline, by Flowline"
DATE = "2003-09-20"


def get_frame(page):
    # poll for the frame that actually has the nav date input
    for _ in range(20):
        for fr in page.frames:
            try:
                if fr.evaluate("""()=>!!document.querySelector('[id="nav:form:G:0:R:1:C:0:da_input"]')"""):
                    return fr
            except Exception:
                pass
        time.sleep(1.0)
    return page


def dd_opts(fr, g):
    try:
        fr.locator(f'[id="nav:form:G:{g}:R:1:C:0:dd_button"]').click(timeout=4000); time.sleep(0.7)
        return fr.evaluate(f"""()=>[...document.querySelectorAll('[id="nav:form:G:{g}:R:1:C:0:dd_panel"] tr[data-item-label]')].map(e=>(e.getAttribute('data-item-label')||'').trim()).filter(t=>t)""")
    except Exception as e:
        return [f"ERR{str(e)[:30]}"]


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
    page.wait_for_load_state("networkidle", timeout=30000); time.sleep(3.0)
    fr = get_frame(page)
    # enumerate distinct nav groups
    groups = fr.evaluate("""()=>{const g={};document.querySelectorAll('[id^="nav:form:G:"]').forEach(e=>{const m=e.id.match(/nav:form:G:(\\d+):/);if(m){const i=m[1];g[i]=g[i]||{date:false,dd:false};if(/da_input/.test(e.id))g[i].date=true;if(/dd_button/.test(e.id))g[i].dd=true;}});return g;}""")
    print("nav groups:", json.dumps(groups))
    # set date(s) on every date group
    for gi, info in groups.items():
        if info.get("date"):
            di = fr.locator(f'[id="nav:form:G:{gi}:R:1:C:0:da_input"]')
            if di.count():
                di.fill(DATE); di.press("Tab"); time.sleep(0.9); print(f"  set date G{gi}={DATE}")
    # cascade dd groups in order
    chain = {}
    for gi in sorted((int(k) for k in groups), key=int):
        if groups[str(gi)].get("dd"):
            opts = dd_opts(fr, gi)
            if opts and not str(opts[0]).startswith("ERR") and len(opts) > 0:
                pick = opts[0]
                print(f"  G{gi} dd opts({len(opts)}): {opts[:6]} -> {pick!r}")
                dd_pick(fr, gi, pick); chain[gi] = pick
            else:
                print(f"  G{gi} dd: {opts}")
    fr.locator('[id="button:form:B"]').click(timeout=5000); page.wait_for_load_state("networkidle", timeout=30000); time.sleep(2.5)
    print("chain:", json.dumps(chain))
    grids = fr.evaluate("""()=>[...document.querySelectorAll('[id$=":T_data"]')].map(t=>({id:t.id,rows:t.querySelectorAll('tr').length}))""")
    print("grids:", json.dumps(grids))
    dump = fr.evaluate("""()=>{const t=document.querySelector('[id$=":T_data"]');if(!t)return{};const trs=[...t.querySelectorAll('tr')].slice(0,4).map(tr=>[...tr.querySelectorAll('td')].slice(0,7).map(td=>(td.textContent||'').trim().slice(0,16)));const ins=[...t.querySelectorAll('[id$="_in"]')].slice(0,12).map(e=>e.id);return{firstRows:trs,cellIds:ins};}""")
    print("firstRows:", json.dumps(dump.get("firstRows"))); print("cellIds:", json.dumps(dump.get("cellIds")))
    b.close()
print("DONE")
