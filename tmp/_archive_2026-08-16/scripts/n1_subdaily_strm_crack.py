"""Crack 'Sub Daily Gas Stream Status - by Stream': robust frame, set date 2011-01-01, dump nav groups,
cascade to a P1 gas stream, GO, dump grid id + column HEADERS + row0 cells (find C for ON_STREAM_HRS
+ the Daytime cell). Also DB-check the gas stream's ON_STREAM_HRS null/non-null on the date. Read-only."""
import time, json, os
import oracledb
from playwright.sync_api import sync_playwright

URL = "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"
SCREEN = "Sub Daily Gas Stream Status - by Stream"
DATE = "2011-01-01"

# DB: the gas stream + its ON_STREAM_HRS on the date
c = oracledb.connect(user='ECKERNEL_EC', password='energy', dsn=os.environ.get('EC_DB_DSN', 'localhost:1521/ORCL'), tcp_connect_timeout=15)
cur = c.cursor()
cur.execute("""SELECT ov.NAME, ov.OBJECT_ID FROM OV_STREAM ov
  WHERE ov.OBJECT_ID IN (SELECT DISTINCT OBJECT_ID FROM STRM_SUB_DAY_STATUS WHERE RECORD_STATUS='P' AND TRUNC(DAYTIME)=TO_DATE(:d,'YYYY-MM-DD'))
  AND ov.STREAM_PHASE='GAS' AND ov.OP_AREA_CODE='P1_AREA'""", d=DATE)
gas = cur.fetchall()
print("GAS streams on", DATE, "under P1_AREA:", [(g[0]) for g in gas])
if gas:
    oid = gas[0][1]
    cur.execute("SELECT TO_CHAR(DAYTIME,'HH24:MI'), SUMMER_TIME, ON_STREAM_HRS, GRS_VOL FROM STRM_SUB_DAY_STATUS WHERE OBJECT_ID=:o AND TRUNC(DAYTIME)=TO_DATE(:d,'YYYY-MM-DD') ORDER BY DAYTIME FETCH FIRST 4 ROWS ONLY", o=oid, d=DATE)
    print("  sample hourly rows (hh:mi, summer, ON_STREAM_HRS, GRS_VOL):")
    for r in cur.fetchall():
        print("   ", r)
GAS_NAME = gas[0][0] if gas else None
cur.close(); c.close()


def frame(page):
    for _ in range(20):
        for fr in page.frames:
            try:
                if fr.evaluate("""()=>!!document.querySelector('[id="nav:form:G:0:R:1:C:0:da_input"]')"""):
                    return fr
            except Exception:
                pass
        time.sleep(1.0)
    return page


def opts(fr, g):
    fr.locator(f'[id="nav:form:G:{g}:R:1:C:0:dd_button"]').click(timeout=4000); time.sleep(0.6)
    o = fr.evaluate(f"""()=>[...document.querySelectorAll('[id="nav:form:G:{g}:R:1:C:0:dd_panel"] tr[data-item-label]')].map(e=>(e.getAttribute('data-item-label')||'').trim()).filter(t=>t)""")
    fr.locator(f'[id="nav:form:G:{g}:R:1:C:0:dd_button"]').click(timeout=2000); time.sleep(0.2)
    return o


def pick(fr, g, label):
    fr.locator(f'[id="nav:form:G:{g}:R:1:C:0:dd_button"]').click(timeout=4000); time.sleep(0.5)
    fr.locator(f'xpath=//*[@id="nav:form:G:{g}:R:1:C:0:dd_panel"]//tr[normalize-space(@data-item-label)="{label}"]').first.click(timeout=4000); time.sleep(1.1)


with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    page = b.new_context(ignore_https_errors=True, viewport={"width": 1680, "height": 1000}).new_page()
    page.goto(URL, wait_until="domcontentloaded", timeout=60000)
    page.fill('[id="username"]', "sysadmin"); page.fill('[id="password"]', "sysadmin"); page.click('[id="kc-login"]')
    page.wait_for_selector('[id="menu:searchForm:searchTxt"]', timeout=60000); time.sleep(1.0)
    sel = f'xpath=//*[contains(@class,"tv-link") and normalize-space(text())="{SCREEN}"]'
    page.locator('[id="menu:searchForm:searchTxt"]').type(SCREEN, delay=22)
    page.wait_for_selector(sel, timeout=12000); page.locator(sel).first.click()
    page.wait_for_load_state("networkidle", timeout=30000); time.sleep(3.0)
    fr = frame(page)
    groups = fr.evaluate("""()=>{const g={};document.querySelectorAll('[id^="nav:form:G:"]').forEach(e=>{const m=e.id.match(/nav:form:G:(\\d+):/);if(m){const i=m[1];g[i]=g[i]||{date:false,dd:false};if(/da_input/.test(e.id))g[i].date=true;if(/dd_button/.test(e.id))g[i].dd=true;}});return g;}""")
    print("nav groups:", json.dumps(groups))
    for gi, info in groups.items():
        if info.get("date"):
            di = fr.locator(f'[id="nav:form:G:{gi}:R:1:C:0:da_input"]'); di.fill(DATE); di.press("Tab"); time.sleep(0.8)
    # cascade dd groups; for the leaf, prefer the gas stream name
    for gi in sorted((int(k) for k in groups), key=int):
        if groups[str(gi)].get("dd"):
            o = opts(fr, gi)
            target = next((x for x in o if GAS_NAME and x.strip() == GAS_NAME), None) or (o[0] if o else None)
            if target:
                print(f"  G{gi}({len(o)}): {o[:5]} -> {target!r}")
                pick(fr, gi, target.strip())
            else:
                print(f"  G{gi}: empty")
    fr.locator('[id="button:form:B"]').click(timeout=5000); page.wait_for_load_state("networkidle", timeout=30000); time.sleep(2.5)
    grids = fr.evaluate("""()=>[...document.querySelectorAll('[id$=":T_data"]')].map(t=>({id:t.id,rows:t.querySelectorAll('tr').length}))""")
    print("grids:", json.dumps(grids))
    info = fr.evaluate("""()=>{const t=document.querySelector('[id$=":T_data"]');if(!t)return{};
      const grid=t.id.replace(':T_data','');
      const heads=[...document.querySelectorAll('[id^="'+grid+'"] th')].map(th=>(th.textContent||'').trim()).filter(Boolean).slice(0,30);
      const row0=[...t.querySelectorAll('tr')][0];
      const cells=row0?[...row0.querySelectorAll('[id*=":C"]')].slice(0,12).map(e=>({c:(e.id.split(':T:0:')[1]||e.id.split(':T:')[1]||e.id),val:(e.value!==undefined?e.value:(e.textContent||'').trim()).slice(0,14)})):[];
      return {grid, headers:heads, cells};}""")
    print("grid:", info.get("grid")); print("HEADERS:", json.dumps(info.get("headers"))); print("ROW0:", json.dumps(info.get("cells")))
    b.close()
print("DONE")
