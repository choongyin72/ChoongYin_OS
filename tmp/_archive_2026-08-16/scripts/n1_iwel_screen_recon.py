"""Recon 'Daily Water Injection Well Status' (N1 injection-well candidate, IWEL_DAY_STATUS).
Open, pierce iframe, set date 2026-02-13, dump nav groups + their dd options, walk cascade trying
AS5/AS2 injection scope, GO, dump grid id + first rows + editable cell ids. Read-only."""
import time, json
from playwright.sync_api import sync_playwright
URL="https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"
SCREEN="Daily Water Injection Well Status"; DATE="2026-02-13"

def find_frame(page, key):
    for _ in range(25):
        fr=next((f for f in page.frames if key in (f.url or "")),None)
        if fr: return fr
        time.sleep(1.0)
    return None

with sync_playwright() as p:
    b=p.chromium.launch(headless=True); page=b.new_context(ignore_https_errors=True,viewport={"width":1680,"height":1000}).new_page()
    page.goto(URL,wait_until="domcontentloaded",timeout=60000)
    page.fill('[id="username"]',"sysadmin"); page.fill('[id="password"]',"sysadmin"); page.click('[id="kc-login"]')
    page.wait_for_selector('[id="menu:searchForm:searchTxt"]',timeout=60000); time.sleep(1.0)
    sel=f'xpath=//*[contains(@class,"tv-link") and normalize-space(text())="{SCREEN}"]'
    page.fill('[id="menu:searchForm:searchTxt"]',""); page.locator('[id="menu:searchForm:searchTxt"]').type(SCREEN,delay=35)
    try: page.wait_for_selector(sel,timeout=12000)
    except Exception: print("screen not in treeview"); b.close(); raise SystemExit
    page.locator(sel).first.click(); page.wait_for_load_state("networkidle",timeout=30000); time.sleep=getattr(time,'sleep'); time.sleep(2.0)
    # iframe: injection well likely under wr.screens
    fr=find_frame(page, "wr.screens") or find_frame(page,"inj") or find_frame(page,"daily")
    if not fr:
        # maybe top-level
        fr=page
        print("no iframe matched; using top page. frames:", [f.url[:70] for f in page.frames])
    else:
        print("iframe url:", fr.url[:90])
    time.sleep(1.0)
    # dump nav groups + date field
    nav=fr.evaluate("""()=>{
      const g={}; document.querySelectorAll('[id^="nav:form:G:"]').forEach(e=>{const m=e.id.match(/nav:form:G:(\\d+)/);if(m){g[m[1]]=g[m[1]]||{date:false,dd:false}; if(/da_input/.test(e.id))g[m[1]].date=true; if(/dd_button/.test(e.id))g[m[1]].dd=true;}});
      return g;}""")
    print("nav groups:", json.dumps(nav))
    # set date
    try:
        di=fr.locator('[id="nav:form:G:0:R:1:C:0:da_input"]'); di.fill(DATE); di.press("Tab"); time.sleep(1.0)
        print("date set", DATE)
    except Exception as e: print("date err", str(e)[:80])
    # dump dd options for each non-date group
    for g in sorted(nav.keys()):
        if nav[g].get("dd"):
            try:
                fr.locator(f'[id="nav:form:G:{g}:R:1:C:0:dd_button"]').click(timeout=4000); time.sleep(0.7)
                opts=fr.evaluate(f"""()=>[...document.querySelectorAll('[id="nav:form:G:{g}:R:1:C:0:dd_panel"] tr[data-item-label]')].map(e=>(e.getAttribute('data-item-label')||'').trim()).filter(t=>t).slice(0,15)""")
                print(f"  G:{g} options:", json.dumps(opts))
                # pick an AS-prefixed / first option to cascade
                pick=next((o for o in opts if o.startswith('AS')), opts[0] if opts else None)
                if pick:
                    fr.locator(f'[id="nav:form:G:{g}:R:1:C:0:dd_panel"] tr[data-item-label="{pick}"]').first.click(timeout=4000); time.sleep(1.1)
                    print(f"  G:{g} picked:", pick)
            except Exception as e: print(f"  G:{g} err", str(e)[:70])
    # GO
    try: fr.locator('[id="button:form:B"]').click(timeout=5000); page.wait_for_load_state("networkidle",timeout=30000); time.sleep(2.5); print("GO clicked")
    except Exception as e: print("GO err", str(e)[:80])
    # dump grids + first rows + editable cells
    res=fr.evaluate("""()=>{
      const grids=[...document.querySelectorAll('[id$=":T_data"]')].map(t=>({id:t.id,rows:t.querySelectorAll('tr').length}));
      const main=document.querySelector('[id$=":T_data"]');
      let sample=[]; let cells=[];
      if(main){ const tr=main.querySelector('tr'); if(tr){ sample=[...tr.querySelectorAll('td')].map(td=>(td.textContent||'').trim()).slice(0,10);
        cells=[...main.querySelectorAll('input[id*=":C"]')].map(i=>i.id).slice(0,12);} }
      return {grids, sample, cells};
    }""")
    print("grids:", json.dumps(res["grids"]))
    print("first row cells text:", json.dumps(res["sample"]))
    print("editable input ids:", json.dumps(res["cells"]))
    page.screenshot(path="c:/Projects/ChoongYin_OS/tmp/n1_iwel_recon.png", full_page=True)
    b.close()
print("DONE")
