"""WR.0001 'Daily Production Well Status 1' — frame-targeted GO probe (READ-ONLY).
Captures nav-group labels, the dd option lists, then clicks the iframe GO (button:form:B)
with the default date to reveal the status grid id + headers + editable cells. No Save."""
import os, time, json
from pathlib import Path
from playwright.sync_api import sync_playwright

URL = "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"
SCREEN = "Daily Production Well Status 1"
OUT = Path(r"c:/Projects/ChoongYin_OS/tmp/wr0001_recon")
OUT.mkdir(parents=True, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_context(ignore_https_errors=True, viewport={"width": 1920, "height": 1080}).new_page()
    page.goto(URL, wait_until="domcontentloaded", timeout=60000)
    page.fill('[id="username"]', "sysadmin"); page.fill('[id="password"]', "sysadmin")
    page.click('[id="kc-login"]')
    page.wait_for_selector('[id="menu:searchForm:searchTxt"]', timeout=60000)
    sel = f'xpath=//*[contains(@class,"tv-link") and normalize-space(text())="{SCREEN}"]'
    fr = None
    for attempt in range(2):
        page.fill('[id="menu:searchForm:searchTxt"]', "")
        page.locator('[id="menu:searchForm:searchTxt"]').type(SCREEN, delay=40)
        page.wait_for_selector(sel, timeout=15000)
        time.sleep(0.6)
        page.locator(sel).first.click()
        page.wait_for_load_state("networkidle", timeout=30000)
        for _ in range(25):
            fr = next((f for f in page.frames if "daily_well_status" in f.url), None)
            if fr:
                break
            time.sleep(1.0)
        if fr:
            break
        print(f"attempt {attempt+1}: frame not loaded, retrying")
    if not fr:
        page.screenshot(path=str(OUT / "open_fail.png"), full_page=True)
        print("content frame not found; frames:", [f.url[:80] for f in page.frames]); browser.close(); raise SystemExit
    time.sleep(2.5)
    print("FRAME:", fr.url[:130])

    # nav-group labels + which dds have a value, + the record-status dd
    nav = fr.evaluate("""() => {
      const lab = id => { const e=document.getElementById(id); return e?(e.textContent||'').trim():null; };
      const groups = [];
      for (let g=0; g<8; g++) {
        const l = lab(`nav:form:G:${g}:R:0:C:0:la`);
        if (!l) continue;
        const ddv = document.getElementById(`nav:form:G:${g}:R:1:C:0:dd_input`);
        const dav = document.getElementById(`nav:form:G:${g}:R:1:C:0:da_input`);
        groups.push({g, label:l, type: ddv?'dd':(dav?'date':'?'),
                     value: (ddv?ddv.value:(dav?dav.value:''))});
      }
      const go = document.getElementById('button:form:B');
      return {groups, go: go?{id:'button:form:B', title:go.title}:null};
    }""")
    print("NAV GROUPS:", json.dumps(nav, indent=1))

    PU = os.environ.get("EC_PU", "P1 Production Unit")
    # open the Production Unit dd (G1), list options, then select PU
    try:
        fr.locator('[id="nav:form:G:1:R:1:C:0:dd_button"]').click(timeout=4000)
        time.sleep(1.0)
        opts = fr.evaluate("""() => [...document.querySelectorAll('[id="nav:form:G:1:R:1:C:0:dd_panel"] tr[data-item-label]')]
            .map(e => (e.getAttribute('data-item-label')||'').trim()).filter(t=>t)""")
        print("PU options count:", len(opts), "first 12:", opts[:12])
        row = fr.locator(f'[id="nav:form:G:1:R:1:C:0:dd_panel"] tr[data-item-label="{PU}"]')
        if row.count() == 0:
            PU = opts[0] if opts else PU
            row = fr.locator(f'[id="nav:form:G:1:R:1:C:0:dd_panel"] tr[data-item-label="{PU}"]')
        print("selecting PU:", PU)
        row.first.click(timeout=4000)
        time.sleep(1.5)
    except Exception as e:
        print("PU select failed:", str(e)[:120])

    # select Facility Class 1 (G3) — required (Well Hookup OR Facility Class 1)
    for gidx, gname in [(3, "Facility Class 1"), (4, "Well Hookup")]:
        try:
            fr.locator(f'[id="nav:form:G:{gidx}:R:1:C:0:dd_button"]').click(timeout=4000)
            time.sleep(1.0)
            o = fr.evaluate(f"""() => [...document.querySelectorAll('[id="nav:form:G:{gidx}:R:1:C:0:dd_panel"] tr[data-item-label]')]
                .map(e => (e.getAttribute('data-item-label')||'').trim()).filter(t=>t)""")
            print(f"{gname} options:", len(o), o[:8])
            real = [x for x in o if x and x.lower() not in ("", "all")]
            if real:
                fr.locator(f'[id="nav:form:G:{gidx}:R:1:C:0:dd_panel"] tr[data-item-label="{real[0]}"]').first.click(timeout=4000)
                print(f"selected {gname}:", real[0]); time.sleep(1.2)
                break
            else:
                page.keyboard.press("Escape")
        except Exception as e:
            print(f"{gname} select failed:", str(e)[:100])

    # click GO with the scope set
    try:
        fr.locator('[id="button:form:B"]').click(timeout=5000)
        page.wait_for_load_state("networkidle", timeout=30000)
        time.sleep(3.5)
        print("clicked GO")
    except Exception as e:
        print("GO click failed:", str(e)[:120])

    # dump any datatable that appeared in the frame + any error/growl message
    grid = fr.evaluate("""() => {
      const vis = e => e && e.offsetParent !== null;
      const tbls = [...document.querySelectorAll('[id$="T_data"]')].filter(vis).map(t=>({id:t.id, rows:t.querySelectorAll('tr').length}));
      let headers=[], row0=[];
      const first=[...document.querySelectorAll('[id$="T_data"]')].find(vis);
      if (first){ const base=first.id.replace(/_data$/,'');
        headers=[...document.querySelectorAll('[id="'+base+'_head"] th')].map(th=>(th.textContent||'').trim()).filter(t=>t);
        row0=[...document.querySelectorAll('[id^="'+base+':0:"]')].map(e=>({id:e.id,type:e.type||e.tagName.toLowerCase(),val:String(e.value||'').slice(0,20)})).filter(c=>/(_in|:in|_dd_input|_cb|_da_input|:dd)$/.test(c.id));
      }
      const msgs=[...document.querySelectorAll('.ui-messages-error-summary, .ui-growl-message, .ui-message-error-detail')].map(e=>(e.textContent||'').trim()).filter(t=>t);
      return {tbls, headers, row0, msgs};
    }""")
    (OUT / "grid_after_go.json").write_text(json.dumps(grid, indent=2), encoding="utf-8")
    page.screenshot(path=str(OUT / "after_go2.png"), full_page=True)
    print("TABLES:", grid["tbls"])
    print("HEADERS:", grid["headers"])
    print("ROW0 cells:", json.dumps(grid["row0"], indent=1)[:2000])
    print("MSGS:", grid["msgs"])
    browser.close()
print("DONE")
