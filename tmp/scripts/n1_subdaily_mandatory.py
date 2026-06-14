"""Detect MANDATORY (yellow) cells on the sub-daily '- by Well' grid + pick a clean test target.
Cascade FRMW PU/Area/Facility 1/Well 1 @2024-10-01, GO, then for each grid row read every C{c} input:
its column header, current value, and whether it is 'yellow/mandatory' (EC marks these via a CSS
class and/or a yellowish background — report computed background-color + class). Also pull, from the
DB, a row/hour that already has a NON-NULL editable value (e.g. AVG_OIL_RATE) so the live edit test
is unambiguous + exactly revertible. Read-only."""
import time, json, os
import oracledb
from playwright.sync_api import sync_playwright

URL = "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"
SCREEN = "Sub Daily Production Well Status 1 - by Well"
DATE = "2024-10-01"
OID = "AEBC774296C611E6E053020011ACFDF3"
GRID = "subDailyWellStatusTable:form"

# DB: hours with a non-null AVG_OIL_RATE (clean revertible target)
c = oracledb.connect(user='ECKERNEL_EC', password='energy', dsn=os.environ.get('EC_DB_DSN', 'localhost:1521/ORCL'), tcp_connect_timeout=15)
cur = c.cursor()
cur.execute("SELECT TO_CHAR(DAYTIME,'HH24:MI') hhmi, AVG_OIL_RATE, AVG_GAS_RATE, ON_STREAM_HRS "
            "FROM PWEL_SUB_DAY_STATUS WHERE OBJECT_ID=:o AND TRUNC(DAYTIME)=TO_DATE(:d,'YYYY-MM-DD') "
            "AND AVG_OIL_RATE IS NOT NULL ORDER BY DAYTIME", o=OID, d=DATE)
print("=== DB hours with non-null AVG_OIL_RATE (candidate test rows) ===")
for r in cur.fetchall():
    print("  hhmi", r[0], "| AVG_OIL_RATE", r[1], "| AVG_GAS_RATE", r[2], "| ON_STREAM_HRS", r[3])
cur.close(); c.close()


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

    # for row 0 (00:00) and the row whose Daytime=19:00, classify each C{c} input as mandatory/yellow
    info = fr.evaluate(f"""()=>{{
      const t=document.getElementById('{GRID}:T_data'); if(!t) return {{}};
      const rows=[...t.querySelectorAll('tr')];
      function classify(tr){{
        const day=(tr.querySelector('[id$=":C1_in"]')||{{}}).value||'';
        const cells=[...tr.querySelectorAll('[id*=":C"]')].map(e=>{{
          const cs=getComputedStyle(e); const td=e.closest('td'); const tdcs=td?getComputedStyle(td):null;
          const bg=cs.backgroundColor; const tdbg=tdcs?tdcs.backgroundColor:'';
          const yellowish = /2[0-9][0-9], ?2[0-9][0-9], ?(1[0-9][0-9]|[0-9]?[0-9])/.test(bg+' '+tdbg);
          return {{id:e.id.split(':T:')[1], cls:e.className, bg, tdbg, yellow:yellowish, val:(e.value!==undefined?e.value:'')}};
        }});
        return {{day, mandatory:cells.filter(c=>c.yellow).map(c=>c.id), sample:cells.slice(0,8)}};
      }}
      const out={{}};
      rows.forEach((tr,n)=>{{const d=(tr.querySelector('[id$=":C1_in"]')||{{}}).value||''; if(d.endsWith('00:00')||d.endsWith('19:00')) out['row'+n]=classify(tr);}});
      return out;}}""")
    print("\n=== mandatory/yellow classification (00:00 vs 19:00 rows) ===")
    print(json.dumps(info, indent=1)[:2500])
    b.close()
print("DONE")
