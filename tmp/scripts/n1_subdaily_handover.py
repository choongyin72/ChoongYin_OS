"""Drive-then-handover live save test. I open a HEADED browser, log in, open the screen, set the
scope (date 2024-10-01 + FRMW PU/Area/Facility 1/Well 1), GO, and land on the grid. Then I HAND THE
WINDOW TO THE USER and just poll the DB (read-only) for ~8 min, watching FRMW Well 1 @ 2024-10-01
00:00 for ANY numeric-column change vs the saved baseline. The user edits WHP 210->211 (+ any yellow
mandatory field) and Saves in that window; when the DB changes I print exactly which column(s)
changed = proof the save gesture works + the WHP->column mapping. I do NOT revert here (deliberate,
next step). Baseline loaded from tmp/n1_subdaily_baseline.json."""
import time, json, os
import oracledb
from playwright.sync_api import sync_playwright

URL = "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"
SCREEN = "Sub Daily Production Well Status 1 - by Well"
DATE = "2024-10-01"; OID = "AEBC774296C611E6E053020011ACFDF3"; HH = "00:00"
BASE = json.load(open(r"c:/Projects/ChoongYin_OS/tmp/n1_subdaily_baseline.json"))["baseline"]
cols = list(BASE.keys())
sel = ", ".join(cols)


def read_row():
    c = oracledb.connect(user='ECKERNEL_EC', password='energy', dsn=os.environ.get('EC_DB_DSN', 'localhost:1521/ORCL'), tcp_connect_timeout=15)
    cur = c.cursor()
    cur.execute(f"SELECT {sel} FROM PWEL_SUB_DAY_STATUS WHERE OBJECT_ID=:o AND TRUNC(DAYTIME)=TO_DATE(:d,'YYYY-MM-DD') AND TO_CHAR(DAYTIME,'HH24:MI')=:h", o=OID, d=DATE, h=HH)
    r = cur.fetchone(); cur.close(); c.close()
    return {cols[i]: (None if r[i] is None else float(r[i])) for i in range(len(cols))}


def diff(cur):
    d = []
    for k in cols:
        b = BASE[k]; v = cur[k]
        if (b is None) != (v is None) or (b is not None and v is not None and b != v):
            d.append((k, b, v))
    return d


def dd_opts(fr, g):
    fr.locator(f'[id="nav:form:G:{g}:R:1:C:0:dd_button"]').click(timeout=4000); time.sleep(0.7)
    return fr.evaluate(f"""()=>[...document.querySelectorAll('[id="nav:form:G:{g}:R:1:C:0:dd_panel"] tr[data-item-label]')].map(e=>(e.getAttribute('data-item-label')||'').trim()).filter(t=>t)""")


def dd_pick(fr, g, label):
    fr.locator(f'[id="nav:form:G:{g}:R:1:C:0:dd_panel"] tr[data-item-label="{label}"]').first.click(timeout=4000); time.sleep(1.1)


with sync_playwright() as p:
    b = p.chromium.launch(headless=False, args=["--start-maximized"])
    page = b.new_context(ignore_https_errors=True, no_viewport=True).new_page()
    page.goto(URL, wait_until="domcontentloaded", timeout=60000)
    page.fill('[id="username"]', "sysadmin"); page.fill('[id="password"]', "sysadmin"); page.click('[id="kc-login"]')
    page.wait_for_selector('[id="menu:searchForm:searchTxt"]', timeout=60000); time.sleep(1.0)
    sel2 = f'xpath=//*[contains(@class,"tv-link") and normalize-space(text())="{SCREEN}"]'
    page.locator('[id="menu:searchForm:searchTxt"]').type(SCREEN, delay=30)
    page.wait_for_selector(sel2, timeout=12000); page.locator(sel2).first.click()
    page.wait_for_load_state("networkidle", timeout=30000); time.sleep(2.5)
    fr = next((f for f in page.frames if "dashboard.jsf" in (f.url or "") and "top=false" in (f.url or "")), None) or page
    di = fr.locator('[id="nav:form:G:0:R:1:C:0:da_input"]'); di.fill(DATE); di.press("Tab"); time.sleep(1.0)
    dd_opts(fr, 1); dd_pick(fr, 1, "FRMW PU")
    dd_opts(fr, 2); dd_pick(fr, 2, "FRMW Area")
    dd_opts(fr, 3); dd_pick(fr, 3, "FRMW Facility 1")
    dd_opts(fr, 4); dd_pick(fr, 4, "FRMW Well 1")
    fr.locator('[id="button:form:B"]').click(timeout=5000); page.wait_for_load_state("networkidle", timeout=30000); time.sleep(2.0)
    # locate the WHP cell (value ~210) on the 00:00 row, scroll into view as a hint
    try:
        fr.evaluate("""()=>{const t=document.getElementById('subDailyWellStatusTable:form:T_data');let row=null;t.querySelectorAll('tr').forEach(tr=>{const d=(tr.querySelector('[id$=\\":C1_in\\"]')||{}).value||'';if(d.endsWith('00:00'))row=tr;});if(row){const c=[...row.querySelectorAll('input')].find(e=>(e.value||'').replace(/,/g,'')==='210.00'||(e.value||'').replace(/,/g,'')==='210');if(c){c.scrollIntoView({block:'center',inline:'center'});c.style.outline='3px solid red';}}}""")
    except Exception:
        pass
    print("=" * 70)
    print("BROWSER READY — it's open on the 00:00 row (WHP cell outlined in RED).")
    print("DO: change WHP[psig] 210 -> 211, Tab, fill any YELLOW field, then SAVE.")
    print("I'm polling the DB; I'll auto-detect when it persists. (~8 min window)")
    print("=" * 70)
    detected = False
    for i in range(160):  # ~8 min at 3s
        time.sleep(3)
        try:
            d = diff(read_row())
        except Exception as e:
            print(f"  (db poll err {str(e)[:50]})"); continue
        if d:
            print(f"\n>>> DETECTED a DB change after {(i + 1) * 3}s:")
            for k, ob, nv in d:
                print(f"      {k}: {ob}  ->  {nv}")
            print(">>> SAVE GESTURE WORKS. (Tell me what you clicked.) Keeping browser open 20s...")
            detected = True
            time.sleep(20)
            break
    if not detected:
        print("\n(no DB change detected in the window — tell me what happened on save)")
    b.close()
print("DONE")
