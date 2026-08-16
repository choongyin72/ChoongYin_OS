"""Final sub-daily crack: cascade FRMW PU/Area/Facility 1/Well 1 @2024-10-01, GO, then dump the
subDailyWellStatusTable grid layout: column HEADERS (map C{c} -> measured column), the first data
rows' leading cell texts (confirm rows = hourly DAYTIME intervals 00:00..23:00), and the editable
cell id pattern (T:{r}:C{c}_in). Read-only."""
import time, json, os
from playwright.sync_api import sync_playwright

URL = "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"
SCREEN = "Sub Daily Production Well Status 1 - by Well"
DATE = "2024-10-01"
GRID = "subDailyWellStatusTable:form"


def dd_opts(fr, g):
    fr.locator(f'[id="nav:form:G:{g}:R:1:C:0:dd_button"]').click(timeout=4000); time.sleep(0.7)
    return fr.evaluate(f"""()=>[...document.querySelectorAll('[id="nav:form:G:{g}:R:1:C:0:dd_panel"] tr[data-item-label]')].map(e=>(e.getAttribute('data-item-label')||'').trim()).filter(t=>t)""")


def dd_pick(fr, g, label):
    fr.locator(f'[id="nav:form:G:{g}:R:1:C:0:dd_panel"] tr[data-item-label="{label}"]').first.click(timeout=4000); time.sleep(1.1)


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
    dd_opts(fr, 1); dd_pick(fr, 1, "FRMW PU")
    dd_opts(fr, 2); dd_pick(fr, 2, "FRMW Area")
    dd_opts(fr, 3); dd_pick(fr, 3, "FRMW Facility 1")
    dd_opts(fr, 4); dd_pick(fr, 4, "FRMW Well 1")
    fr.locator('[id="button:form:B"]').click(timeout=5000); page.wait_for_load_state("networkidle", timeout=30000); time.sleep(2.5)

    info = fr.evaluate(f"""()=>{{
      const out={{}};
      // column header labels
      const heads=[...document.querySelectorAll('[id^="{GRID}:T:"] th, [id^="{GRID}"] th')].map(th=>(th.textContent||'').trim()).filter(Boolean);
      out.headers=heads.slice(0,40);
      const t=document.getElementById('{GRID}:T_data');
      if(t){{
        const trs=[...t.querySelectorAll('tr')];
        out.nrows=trs.length;
        out.firstRowsLeadCells=trs.slice(0,5).map(tr=>[...tr.querySelectorAll('td')].slice(0,6).map(td=>(td.textContent||'').trim().slice(0,16)));
        // editable cell ids in row 0 and row 1
        out.row0inputs=[...trs[0].querySelectorAll('[id*=":C"]')].slice(0,10).map(e=>e.id);
        // all distinct C{{c}} indexes present as _in inputs in row0
        out.row0_in=[...trs[0].querySelectorAll('[id$="_in"]')].slice(0,12).map(e=>e.id);
      }}
      return out;}}""")
    print("HEADERS:", json.dumps(info.get("headers")))
    print("\nnrows:", info.get("nrows"))
    print("first rows lead cells:", json.dumps(info.get("firstRowsLeadCells")))
    print("\nrow0 cell ids:", json.dumps(info.get("row0inputs")))
    print("row0 _in ids:", json.dumps(info.get("row0_in")))
    page.screenshot(path="tmp/n1_subdaily_grid_full.png", full_page=True)
    b.close()
print("DONE")
