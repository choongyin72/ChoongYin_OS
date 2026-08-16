"""Sub-daily grid crack v2. The Facility-1 + Well-1 GO gave an empty grid. Two unknowns: (a) which
FRMW Facility the data-bearing FRMW Well 1 hangs under; (b) the grid's real id suffix (maybe not
:T_data). First resolve the facility from the DB, then drive the screen to that facility+well, GO,
and dump ALL grid-ish ids broadly (tables, :T:, status panels) + a screenshot. Read-only."""
import time, json, os
import oracledb
from playwright.sync_api import sync_playwright

URL = "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"
SCREEN = "Sub Daily Production Well Status 1 - by Well"
DATE = "2024-10-01"
WELL_OID = "AEBC774296C611E6E053020011ACFDF3"  # FRMW Well 1 (data-bearing)

# --- DB: find the facility/area linkage for the well ---
c = oracledb.connect(user='ECKERNEL_EC', password='energy',
                     dsn=os.environ.get('EC_DB_DSN', 'localhost:1521/ORCL'), tcp_connect_timeout=15)
cur = c.cursor()
print("=== columns on WELL_HOOKUP_VERSION (find facility/area FK cols) ===")
try:
    cur.execute("SELECT column_name FROM all_tab_columns WHERE table_name='WELL_HOOKUP_VERSION' "
                "AND (column_name LIKE '%FCTY%' OR column_name LIKE '%AREA%' OR column_name LIKE '%WELL%' "
                "OR column_name LIKE '%PROD_UNIT%' OR column_name LIKE '%FACIL%') ORDER BY column_id")
    print("  ", [r[0] for r in cur.fetchall()])
except Exception as e:
    print("  ERR", str(e)[:120])
print("=== any table linking this WELL_OID to a facility (scan hookup tables) ===")
try:
    cur.execute("SELECT table_name FROM all_tab_columns WHERE column_name='WELL_ID' AND owner='ECKERNEL_EC' "
                "AND table_name LIKE '%HOOKUP%' ORDER BY table_name")
    print("  hookup tables w/ WELL_ID:", [r[0] for r in cur.fetchall()])
except Exception as e:
    print("  ERR", str(e)[:120])
cur.close(); c.close()


def dd_opts(fr, g):
    fr.locator(f'[id="nav:form:G:{g}:R:1:C:0:dd_button"]').click(timeout=4000); time.sleep(0.7)
    return fr.evaluate(f"""()=>[...document.querySelectorAll('[id="nav:form:G:{g}:R:1:C:0:dd_panel"] tr[data-item-label]')].map(e=>(e.getAttribute('data-item-label')||'').trim()).filter(t=>t)""")


def dd_pick(fr, g, label):
    fr.locator(f'[id="nav:form:G:{g}:R:1:C:0:dd_panel"] tr[data-item-label="{label}"]').first.click(timeout=4000); time.sleep(1.1)


def crack(fr, facility):
    di = fr.locator('[id="nav:form:G:0:R:1:C:0:da_input"]'); di.fill(DATE); di.press("Tab"); time.sleep(1.0)
    dd_opts(fr, 1); dd_pick(fr, 1, "FRMW PU")
    dd_opts(fr, 2); dd_pick(fr, 2, "FRMW Area")
    g3 = dd_opts(fr, 3); dd_pick(fr, 3, facility)
    g4 = dd_opts(fr, 4)
    print(f"\n[{facility}] G4 well options:", g4)
    if "FRMW Well 1" in g4:
        dd_pick(fr, 4, "FRMW Well 1")
    fr.locator('[id="button:form:B"]').click(timeout=5000); fr.page.wait_for_load_state("networkidle", timeout=30000); time.sleep(2.5)
    dump = fr.evaluate("""()=>{
      const tdata=[...document.querySelectorAll('[id$=":T_data"]')].map(t=>t.id);
      const tables=[...document.querySelectorAll('table')].map(t=>t.id).filter(Boolean);
      const cells=[...document.querySelectorAll('[id*=":T:"]')].slice(0,8).map(e=>e.id);
      const inputs=document.querySelectorAll('input').length;
      const txt=(document.body.innerText||'').replace(/\\s+/g,' ');
      const hasHours=/00:00|01:00|On Stream|Daytime|Hour/i.test(txt);
      return {tdata, tables:tables.slice(0,15), cells, inputs, hasHours, txtlen:txt.length};}""")
    print("  tdata grids:", json.dumps(dump["tdata"]))
    print("  table ids:", json.dumps(dump["tables"]))
    print("  :T: cells:", json.dumps(dump["cells"]))
    print("  inputs:", dump["inputs"], "| hasHours/Daytime text:", dump["hasHours"], "| bodytxt:", dump["txtlen"])


with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    ctx = b.new_context(ignore_https_errors=True, viewport={"width": 1680, "height": 1000})
    page = ctx.new_page()
    page.goto(URL, wait_until="domcontentloaded", timeout=60000)
    page.fill('[id="username"]', "sysadmin"); page.fill('[id="password"]', "sysadmin"); page.click('[id="kc-login"]')
    page.wait_for_selector('[id="menu:searchForm:searchTxt"]', timeout=60000); time.sleep(1.0)
    sel = f'xpath=//*[contains(@class,"tv-link") and normalize-space(text())="{SCREEN}"]'
    page.locator('[id="menu:searchForm:searchTxt"]').type(SCREEN, delay=30)
    page.wait_for_selector(sel, timeout=12000); page.locator(sel).first.click()
    page.wait_for_load_state("networkidle", timeout=30000); time.sleep(2.5)
    fr = next((f for f in page.frames if "dashboard.jsf" in (f.url or "") and "top=false" in (f.url or "")), None) or page
    for fac in ("FRMW Facility 1", "FRMW Facility 2"):
        try:
            crack(fr, fac)
            page.screenshot(path=f"tmp/n1_subdaily_{fac.replace(' ', '_')}.png")
        except Exception as e:
            print(f"  [{fac}] ERR", str(e)[:120])
    b.close()
print("DONE")
