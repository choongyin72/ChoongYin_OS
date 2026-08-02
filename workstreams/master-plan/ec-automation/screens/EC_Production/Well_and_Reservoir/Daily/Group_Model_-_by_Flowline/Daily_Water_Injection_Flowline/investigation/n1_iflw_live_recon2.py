"""READ-ONLY live recon of 'Daily Water Injection Flowline, by Flowline' using PFLW's proven frame-poll
+ cascade approach. Fills From/To=2019-12-20, cascades PU/Area/Facility/Flowline to the P1 scope, GO,
then dumps the grid id + header->C{c} map + row0 cell ids so we can target ON_STREAM_HRS. NO save."""
import os
import time, json
from playwright.sync_api import sync_playwright

URL = "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"
SCREEN = "Daily Water Injection Flowline, by Flowline"
SHOT = "C:/Projects/ChoongYin_OS/tmp/"


def get_frame(page):
    for _ in range(40):
        for fr in page.frames:
            try:
                if fr.evaluate("""()=>!!document.querySelector('[id="nav:form:G:0:R:1:C:0:da_input"]')"""):
                    return fr
            except Exception:
                pass
        time.sleep(0.5)
    return page


def dd_opts(fr, g):
    fr.click(f'[id="nav:form:G:{g}:R:1:C:0:dd_button"]', timeout=5000)
    time.sleep(0.6)
    o = fr.evaluate(f"""()=>[...document.querySelectorAll('[id="nav:form:G:{g}:R:1:C:0:dd_panel"] tr[data-item-label]')].map(e=>(e.getAttribute('data-item-label')||'').trim()).filter(t=>t)""")
    return o


def dd_pick(fr, g, needle):
    o = dd_opts(fr, g)
    cand = next((x for x in o if needle.lower() in x.lower()), None)
    if cand:
        fr.click(f'xpath=//*[@id="nav:form:G:{g}:R:1:C:0:dd_panel"]//tr[normalize-space(@data-item-label)="{cand}"]', timeout=5000)
        time.sleep(1.2)
    return {"options": o, "picked": cand}


with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    page = b.new_context(ignore_https_errors=True, viewport={"width": 1680, "height": 1000}).new_page()
    page.goto(URL, wait_until="domcontentloaded", timeout=60000)
    page.fill('[id="username"]', os.environ.get("EC_USER", "sysadmin")); page.fill('[id="password"]', os.environ.get("EC_PASS", "sysadmin")); page.click('[id="kc-login"]')
    page.wait_for_selector('[id="menu:searchForm:searchTxt"]', timeout=60000); time.sleep(1.0)
    page.locator('[id="menu:searchForm:searchTxt"]').type(SCREEN, delay=20); time.sleep(1.3)
    page.locator(f'xpath=//*[contains(@class,"tv-link") and normalize-space(text())="{SCREEN}"]').first.click()
    page.wait_for_load_state("networkidle", timeout=30000); time.sleep(2.0)
    fr = get_frame(page)
    print("frame found:", fr != page)
    fr.fill('[id="nav:form:G:0:R:1:C:0:da_input"]', "2019-12-20")
    fr.fill('[id="nav:form:G:1:R:1:C:0:da_input"]', "2019-12-20")
    time.sleep(0.4)
    for g, needle in [(2, "P1"), (3, "P1"), (4, "P1"), (5, "F003 WI")]:
        r = dd_pick(fr, g, needle)
        print(f"G:{g} picked={r['picked']!r}  options={json.dumps(r['options'][:12])}")
    fr.click('[id="button:form:B"]', timeout=8000)
    page.wait_for_load_state("networkidle", timeout=30000); time.sleep(2.5)
    page.screenshot(path=SHOT+"iflw_after_go2.png", full_page=True)
    info = fr.evaluate(r"""()=>{
      const grids=[...document.querySelectorAll('[id$=":T_data"]')].map(t=>({id:t.id, rows:t.querySelectorAll('tr').length}));
      // header -> column index map for the first data grid
      let headers=[];
      const g=grids.find(x=>x.rows>0)||grids[0];
      if(g){
        const tbl=document.getElementById(g.id);
        const table=tbl?tbl.closest('table')||tbl.parentElement:null;
        const ths=[...document.querySelectorAll(`[id="${g.id}"] tr:first-child td, th .ui-column-title`)];
      }
      // generic: row0 cell inputs with their C index
      const cells=[...document.querySelectorAll('[id*=":T:0:C:"]')].filter(e=>['INPUT','TEXTAREA','SELECT'].includes(e.tagName)).map(e=>e.id).slice(0,40);
      // column header labels (PrimeFaces)
      const hdr=[...document.querySelectorAll('.ui-datatable-frozenlayout th .ui-column-title, .ui-datatable th .ui-column-title, th[role="columnheader"] .ui-column-title')].map(e=>(e.textContent||'').trim()).filter(Boolean).slice(0,40);
      return {grids, cells, hdr};
    }""")
    print("\nGRIDS:", json.dumps(info["grids"]))
    print("HEADERS:", json.dumps(info["hdr"]))
    print("ROW0 CELL IDS:", json.dumps(info["cells"]))
    b.close()
print("DONE")
