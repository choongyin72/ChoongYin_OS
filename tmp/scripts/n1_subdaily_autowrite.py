"""One informed automated WRITE attempt on the PROVEN-editable WHP cell (user's manual save persisted).
Unit-robust + exact-revert: navigate to FRMW Well 1 @2024-10-01 00:00; find the WHP cell (display
~3045.8 = DB AVG_WH_PRESS 210 bar); derive factor = UI_display/DB. Edit WHP via REAL keystrokes + Tab
(fire EC change), click the toolbar Save, poll the DB for AVG_WH_PRESS to change, assert it ≈
typed_display/factor (proves persist + the gesture + unit model). Then REVERT DB to the exact baseline
(210). Headless OK (automated). Read+write, fully self-reverting."""
import time, os, json
import oracledb
from playwright.sync_api import sync_playwright

URL = "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"
SCREEN = "Sub Daily Production Well Status 1 - by Well"
DATE = "2024-10-01"; OID = "AEBC774296C611E6E053020011ACFDF3"; HH = "00:00"
TYPED = "3000.00"     # new WHP display value (psi), distinct from 3045.80
DBCOL = "AVG_WH_PRESS"; BASELINE_DB = 210.0


def db_val():
    c = oracledb.connect(user='ECKERNEL_EC', password='energy', dsn=os.environ.get('EC_DB_DSN', 'localhost:1521/ORCL'), tcp_connect_timeout=15)
    cur = c.cursor()
    cur.execute(f"SELECT {DBCOL} FROM PWEL_SUB_DAY_STATUS WHERE OBJECT_ID=:o AND TRUNC(DAYTIME)=TO_DATE(:d,'YYYY-MM-DD') AND TO_CHAR(DAYTIME,'HH24:MI')=:h", o=OID, d=DATE, h=HH)
    v = cur.fetchone()[0]; cur.close(); c.close()
    return None if v is None else float(v)


def set_db(v):
    c = oracledb.connect(user='ECKERNEL_EC', password='energy', dsn=os.environ.get('EC_DB_DSN', 'localhost:1521/ORCL'), tcp_connect_timeout=15)
    cur = c.cursor()
    cur.execute(f"UPDATE PWEL_SUB_DAY_STATUS SET {DBCOL}=:v WHERE OBJECT_ID=:o AND TRUNC(DAYTIME)=TO_DATE(:d,'YYYY-MM-DD') AND TO_CHAR(DAYTIME,'HH24:MI')=:h", v=v, o=OID, d=DATE, h=HH)
    c.commit(); n = cur.rowcount; cur.close(); c.close(); return n


def dd_opts(fr, g):
    fr.locator(f'[id="nav:form:G:{g}:R:1:C:0:dd_button"]').click(timeout=4000); time.sleep(0.7)
    return fr.evaluate(f"""()=>[...document.querySelectorAll('[id="nav:form:G:{g}:R:1:C:0:dd_panel"] tr[data-item-label]')].map(e=>(e.getAttribute('data-item-label')||'').trim()).filter(t=>t)""")


def dd_pick(fr, g, label):
    fr.locator(f'[id="nav:form:G:{g}:R:1:C:0:dd_panel"] tr[data-item-label="{label}"]').first.click(timeout=4000); time.sleep(1.1)


print("DB AVG_WH_PRESS before:", db_val(), "(expect 210)")
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
    fr.locator('[id="button:form:B"]').click(timeout=5000); page.wait_for_load_state("networkidle", timeout=30000); time.sleep(2.0)

    # find the WHP cell id on the 00:00 row (display ~3045.8)
    cell = fr.evaluate("""()=>{const t=document.getElementById('subDailyWellStatusTable:form:T_data');let row=null;t.querySelectorAll('tr').forEach(tr=>{const d=(tr.querySelector('[id$=":C1_in"]')||{}).value||'';if(d.endsWith('00:00'))row=tr;});if(!row)return null;const c=[...row.querySelectorAll('input')].find(e=>{const v=(e.value||'').replace(/,/g,'');return v.startsWith('3045.8')||v==='3045.8022';});return c?{id:c.id,val:c.value}:null;}""")
    print("WHP cell:", json.dumps(cell))
    if not cell:
        print("WHP cell not found"); b.close(); raise SystemExit(1)
    disp0 = float(cell["val"].replace(",", ""))
    factor = disp0 / BASELINE_DB
    print(f"UI display before: {disp0} | DB before: {BASELINE_DB} | derived factor: {factor:.5f}")

    cid = cell["id"]
    loc = fr.locator(f'[id="{cid}"]')
    loc.click(); loc.press("Control+a"); loc.type(TYPED, delay=40); loc.press("Tab")
    time.sleep(1.2)
    # click toolbar Save (the proven N1 commit)
    saved = False
    for savesel in ['a[title="Save [Ctrl+s]"]', '[id="screenToolbar:form:menuBar"] a[title^="Save"]']:
        try:
            fr.locator(savesel).first.click(timeout=4000); saved = True; print("clicked save:", savesel); break
        except Exception:
            continue
    if not saved:
        page.keyboard.press("Control+s"); print("fallback Ctrl+s")
    page.wait_for_load_state("networkidle", timeout=20000); time.sleep(1.5)
    b.close()

# poll DB for the change
expected = float(TYPED) / factor
print(f"\nexpected DB AVG_WH_PRESS after = {float(TYPED)}/{factor:.5f} = {expected:.4f}")
got = None
for i in range(8):
    time.sleep(2); got = db_val()
    print(f"  t+{(i+1)*2}s DB AVG_WH_PRESS = {got}")
    if got is not None and abs(got - BASELINE_DB) > 0.001:
        break
if got is not None and abs(got - expected) < 0.05:
    print(f">>> AUTOMATED WRITE PERSISTED + unit-verified ({got} ~= {expected:.4f}). Gesture works.")
elif got is not None and abs(got - BASELINE_DB) > 0.001:
    print(f">>> persisted but value {got} != expected {expected:.4f} (recheck factor/column)")
else:
    print(">>> NO persist (DB unchanged) — automated gesture did not commit (do NOT loop; park).")

# exact revert
n = set_db(BASELINE_DB)
print(f"reverted DB {DBCOL} -> {BASELINE_DB} ({n} row); now = {db_val()}")
print("DONE")
