"""Precise mandatory-cell detection: EC encodes it in the cell class as '{mandatory:true|false}'.
For the FRMW Well 1 00:00 row, list EVERY C{c} input that is mandatory:true, with its column header +
current value (empty mandatory = the silent-Save-reject cause). Map C{c} -> header so we know what to
fill. Also find which C{c} is AVG_OIL_RATE (the revert-safe edit target) by value match (2500).
Read-only."""
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

    res = fr.evaluate(f"""()=>{{
      const t=document.getElementById('{GRID}:T_data'); if(!t) return {{}};
      // find the 00:00 row
      let row=null; t.querySelectorAll('tr').forEach(tr=>{{const d=(tr.querySelector('[id$=":C1_in"]')||{{}}).value||''; if(d.endsWith('00:00')) row=tr;}});
      if(!row) return {{err:'no 00:00 row'}};
      const cells=[...row.querySelectorAll('[id*=":C"]')].map(e=>{{
        const m=(e.className||'').match(/mandatory:(true|false)/);
        return {{c:(e.id.split(':T:')[1]||e.id), mandatory:m?m[1]:'?', val:(e.value!==undefined?e.value:'').trim()}};
      }});
      const mand=cells.filter(c=>c.mandatory==='true');
      const oil=cells.filter(c=>c.val==='2500.00'||c.val==='2500');
      const gas=cells.filter(c=>c.val==='3000.00'||c.val==='3000');
      return {{mandatory_cells:mand, empty_mandatory:mand.filter(c=>!c.val), cells_eq_2500:oil.map(c=>c.c), cells_eq_3000:gas.map(c=>c.c), total_cells:cells.length}};
    }}""")
    print(json.dumps(res, indent=1))
    b.close()
print("DONE")
