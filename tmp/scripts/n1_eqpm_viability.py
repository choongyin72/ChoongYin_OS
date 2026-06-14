"""Viability recon for an N1 equipment screen (EQPM_DAY_STATUS, different object class).
(1) DB: equipment scope on a data day + numeric measured columns + object name source.
(2) UI: find a 'Daily Equipment Status'-type screen in treeview; open; check if it's the N1 grid
template (a *:T_data grid with C{c}_in cells) + dump nav. Read-only."""
import time, json, os
import oracledb
from playwright.sync_api import sync_playwright
URL="https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"

# --- DB part ---
c=oracledb.connect(user='ECKERNEL_EC',password='energy',dsn=os.environ.get('EC_DB_DSN','localhost:1521/ORCL'),tcp_connect_timeout=15);cur=c.cursor()
def show(t,sql):
    print(f"=== {t} ===")
    try:
        cur.execute(sql);cols=[d[0] for d in cur.description];print(" | ".join(cols))
        for r in cur.fetchall()[:10]: print("  "+" | ".join("" if v is None else str(v)[:40] for v in r))
    except Exception as e: print("  ERR",str(e)[:120])
show("EQPM_DAY_STATUS top data day",
     "SELECT TO_CHAR(TRUNC(DAYTIME),'YYYY-MM-DD') d,COUNT(*) n FROM EQPM_DAY_STATUS WHERE RECORD_STATUS='P' GROUP BY TRUNC(DAYTIME) ORDER BY n DESC FETCH FIRST 3 ROWS ONLY")
show("EQPM_DAY_STATUS numeric cols",
     "SELECT column_name FROM all_tab_columns WHERE table_name='EQPM_DAY_STATUS' AND data_type='NUMBER' AND column_name<>'OBJECT_ID' ORDER BY column_id FETCH FIRST 15 ROWS ONLY")
show("equipment name source? (EQPM_VERSION / OV_EQPM has NAME?)",
     "SELECT table_name FROM all_tab_columns WHERE column_name='NAME' AND table_name IN ('EQPM_VERSION','OV_EQPM','EQUIPMENT_VERSION') ")
cur.close();c.close()

# --- UI part ---
with sync_playwright() as p:
    b=p.chromium.launch(headless=True); page=b.new_context(ignore_https_errors=True,viewport={"width":1600,"height":1000}).new_page()
    page.goto(URL,wait_until="domcontentloaded",timeout=60000)
    page.fill('[id="username"]',"sysadmin"); page.fill('[id="password"]',"sysadmin"); page.click('[id="kc-login"]')
    page.wait_for_selector('[id="menu:searchForm:searchTxt"]',timeout=60000); time.sleep(1.0)
    page.locator('[id="menu:searchForm:searchTxt"]').type("Equipment",delay=30); time.sleep(2.0)
    eq=page.evaluate("""()=>[...document.querySelectorAll('.tv-link')].map(e=>e.textContent.trim()).filter(t=>/equip/i.test(t))""")
    print("\n=== treeview 'Equipment' screens ===")
    for x in eq: print("  ",x)
    # try open a 'Daily Equipment Status'-ish one
    target=next((x for x in eq if x.lower().startswith("daily") and "status" in x.lower()), None) or next((x for x in eq if "status" in x.lower()), None)
    print("opening:", target)
    if target:
        sel=f'xpath=//*[contains(@class,"tv-link") and normalize-space(text())="{target}"]'
        page.fill('[id="menu:searchForm:searchTxt"]',""); page.locator('[id="menu:searchForm:searchTxt"]').type(target,delay=30)
        try: page.wait_for_selector(sel,timeout=10000); page.locator(sel).first.click(); page.wait_for_load_state("networkidle",timeout=30000); time.sleep(2.5)
        except Exception as e: print("open err",str(e)[:80])
        fr=next((f for f in page.frames if "dashboard.jsf" in (f.url or "") and "top=false" in (f.url or "")),None) or page
        info=fr.evaluate("""()=>{
          const nav={}; document.querySelectorAll('[id^="nav:form:G:"]').forEach(e=>{const m=e.id.match(/nav:form:G:(\\d+)/);if(m){nav[m[1]]=nav[m[1]]||{date:false,dd:false};if(/da_input/.test(e.id))nav[m[1]].date=true;if(/dd_button/.test(e.id))nav[m[1]].dd=true;}});
          const grids=[...document.querySelectorAll('[id$=":T_data"]')].map(t=>t.id);
          const incell=[...document.querySelectorAll('input[id*=":C"][id*=":T:"]')].length;
          return {nav,grids,incell, frameUrl:(location&&location.href||'').slice(0,90)};}""")
        print("nav groups:", json.dumps(info["nav"]))
        print("grids:", json.dumps(info["grids"]))
        print("inline C-cell inputs present:", info["incell"])
    b.close()
print("DONE")
