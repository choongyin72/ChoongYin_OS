"""Read-only confirm before building the sub-daily suite: cascade to FRMW Well 1 @2024-10-01, GO,
read row0/row1 C0(Well Name)/C1(Daytime)/C3(On Strm[hr]) DISPLAY values, then DB-read
PWEL_SUB_DAY_STATUS.ON_STREAM_HRS for FRMW Well 1 at the HH:MI shown — to (a) learn the Daytime
display format (for HH:MI extraction), (b) cross-check C3 == ON_STREAM_HRS at the matching hour."""
import time, json, os, re
import oracledb
from playwright.sync_api import sync_playwright

URL = "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"
SCREEN = "Sub Daily Production Well Status 1 - by Well"
DATE = "2024-10-01"
WELL_OID = "AEBC774296C611E6E053020011ACFDF3"
GRID = "subDailyWellStatusTable:form"


def dd_opts(fr, g):
    fr.locator(f'[id="nav:form:G:{g}:R:1:C:0:dd_button"]').click(timeout=4000); time.sleep(0.7)
    return fr.evaluate(f"""()=>[...document.querySelectorAll('[id="nav:form:G:{g}:R:1:C:0:dd_panel"] tr[data-item-label]')].map(e=>(e.getAttribute('data-item-label')||'').trim()).filter(t=>t)""")


def dd_pick(fr, g, label):
    fr.locator(f'[id="nav:form:G:{g}:R:1:C:0:dd_panel"] tr[data-item-label="{label}"]').first.click(timeout=4000); time.sleep(1.1)


rows_ui = []
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

    def cellval(r, c, suf="_in"):
        return fr.evaluate(f"""()=>{{const e=document.getElementById('{GRID}:T:{r}:C{c}{suf}'); return e? (e.value!==undefined? e.value : e.textContent).trim() : null;}}""")
    for r in range(0, 4):
        rows_ui.append({"r": r, "C0_la": cellval(r, 0, "_la"), "C1_Daytime": cellval(r, 1), "C2_OnTest": cellval(r, 2), "C3_OnStrm": cellval(r, 3)})
    print("UI rows:", json.dumps(rows_ui, indent=0))
    b.close()

# DB cross-check
c = oracledb.connect(user='ECKERNEL_EC', password='energy', dsn=os.environ.get('EC_DB_DSN', 'localhost:1521/ORCL'), tcp_connect_timeout=15)
cur = c.cursor()
print("\n=== DB ON_STREAM_HRS by hour for FRMW Well 1 @", DATE, "===")
cur.execute("SELECT TO_CHAR(DAYTIME,'HH24:MI') hhmi, SUMMER_TIME, ON_STREAM_HRS FROM PWEL_SUB_DAY_STATUS "
            "WHERE OBJECT_ID=:o AND TRUNC(DAYTIME)=TO_DATE(:d,'YYYY-MM-DD') ORDER BY DAYTIME FETCH FIRST 6 ROWS ONLY",
            o=WELL_OID, d=DATE)
for r in cur.fetchall():
    print("  ", r)
# match each UI row's HH:MI -> DB ON_STREAM_HRS
print("\n=== match UI C3 vs DB ON_STREAM_HRS ===")
for row in rows_ui:
    dt = row["C1_Daytime"] or ""
    m = re.search(r"(\d{1,2}:\d{2})", dt)
    if not m:
        print(f"  row{row['r']}: no HH:MI in Daytime {dt!r}"); continue
    hhmi = m.group(1).zfill(5)
    cur.execute("SELECT ON_STREAM_HRS FROM PWEL_SUB_DAY_STATUS WHERE OBJECT_ID=:o AND TRUNC(DAYTIME)=TO_DATE(:d,'YYYY-MM-DD') AND TO_CHAR(DAYTIME,'HH24:MI')=:h",
                o=WELL_OID, d=DATE, h=hhmi)
    dbrow = cur.fetchone()
    print(f"  row{row['r']} Daytime={dt!r} hhmi={hhmi} | UI C3={row['C3_OnStrm']!r} | DB ON_STREAM_HRS={dbrow[0] if dbrow else 'NO ROW'}")
cur.close(); c.close(); print("\nDONE")
