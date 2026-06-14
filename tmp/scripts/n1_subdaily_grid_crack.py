"""Live-crack the sub-daily '- by Well' grid. Cascade: date 2024-10-01 -> G1=FRMW PU -> greedily
pick each next dd (prefer an option containing 'FRMW', else first) through G5 (the well leaf) ->
GO -> dump the grid id, first rows, and cell ids. Goal: confirm rows = intraday time intervals and
read the cell layout (so the T3 can map row-index -> DAYTIME hour + cell -> measured column).
Read-only (no Save)."""
import time, json, os
from playwright.sync_api import sync_playwright

URL = "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"
SCREEN = "Sub Daily Production Well Status 1 - by Well"
DATE = "2024-10-01"


def dd_opts(fr, g):
    fr.locator(f'[id="nav:form:G:{g}:R:1:C:0:dd_button"]').click(timeout=4000)
    time.sleep(0.7)
    return fr.evaluate(f"""()=>[...document.querySelectorAll('[id="nav:form:G:{g}:R:1:C:0:dd_panel"] tr[data-item-label]')].map(e=>(e.getAttribute('data-item-label')||'').trim()).filter(t=>t)""")


def dd_pick(fr, g, label):
    fr.locator(f'[id="nav:form:G:{g}:R:1:C:0:dd_panel"] tr[data-item-label="{label}"]').first.click(timeout=4000)
    time.sleep(1.1)


with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    page = b.new_context(ignore_https_errors=True, viewport={"width": 1680, "height": 1000}).new_page()
    page.goto(URL, wait_until="domcontentloaded", timeout=60000)
    page.fill('[id="username"]', "sysadmin"); page.fill('[id="password"]', "sysadmin"); page.click('[id="kc-login"]')
    page.wait_for_selector('[id="menu:searchForm:searchTxt"]', timeout=60000); time.sleep(1.0)
    sel = f'xpath=//*[contains(@class,"tv-link") and normalize-space(text())="{SCREEN}"]'
    page.locator('[id="menu:searchForm:searchTxt"]').type(SCREEN, delay=30)
    page.wait_for_selector(sel, timeout=12000); page.locator(sel).first.click()
    page.wait_for_load_state("networkidle", timeout=30000); time.sleep(2.5)
    fr = next((f for f in page.frames if "dashboard.jsf" in (f.url or "") and "top=false" in (f.url or "")), None) or page

    di = fr.locator('[id="nav:form:G:0:R:1:C:0:da_input"]'); di.fill(DATE); di.press("Tab"); time.sleep(1.0)
    print("date:", DATE)
    chain = {1: "FRMW PU"}
    dd_opts(fr, 1); dd_pick(fr, 1, "FRMW PU"); print("G1 <- FRMW PU")
    for g in (2, 3, 4, 5):
        opts = dd_opts(fr, g)
        if not opts:
            print(f"G{g}: (no options — cascade leaf reached or not required)")
            # close panel
            fr.locator(f'[id="nav:form:G:{g}:R:1:C:0:dd_button"]').click(timeout=2000); time.sleep(0.3)
            continue
        pick = next((o for o in opts if "FRMW" in o.upper()), opts[0])
        print(f"G{g} options({len(opts)}): {opts[:8]}  -> picking {pick!r}")
        dd_pick(fr, g, pick); chain[g] = pick
    # GO
    fr.locator('[id="button:form:B"]').click(timeout=5000); page.wait_for_load_state("networkidle", timeout=30000); time.sleep(2.5)
    print("\nnav chain:", json.dumps(chain))

    grids = fr.evaluate("""()=>[...document.querySelectorAll('[id$=":T_data"]')].map(t=>({id:t.id, rows:t.querySelectorAll('tr').length}))""")
    print("grids:", json.dumps(grids))
    # dump the first grid's first rows + cell ids
    dump = fr.evaluate("""()=>{const t=document.querySelector('[id$=":T_data"]'); if(!t) return {};
      const trs=[...t.querySelectorAll('tr')].slice(0,4).map(tr=>[...tr.querySelectorAll('td')].slice(0,8).map(td=>(td.textContent||'').trim().slice(0,18)));
      const ins=[...t.querySelectorAll('input,[id*=":C"]')].slice(0,12).map(e=>e.id).filter(Boolean);
      return {firstRows:trs, sampleCellIds:ins};}""")
    print("firstRows:", json.dumps(dump.get("firstRows"))); print("sampleCellIds:", json.dumps(dump.get("sampleCellIds")))
    page.screenshot(path="tmp/n1_subdaily_grid.png")
    b.close()
print("DONE")
