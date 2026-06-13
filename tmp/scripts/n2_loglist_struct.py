"""N2: run the POSITIVE allocation (Testing allocation RUN_NO / 01 Run No .test / 2003-01-01)
with Simulate ON, then dump the log_list:form:T_data structure: row ids, ordering, and each
row's cell texts — so the RF reader targets the newest run's Exit Status correctly. Simulate =
no DB write."""
import time, json
from playwright.sync_api import sync_playwright
URL="https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"; SCREEN="Daily Allocation"; DATE="2003-01-01"

def opts(fr,g):
    fr.locator(f'[id="nav:form:G:{g}:R:1:C:0:dd_button"]').click(timeout=4000); time.sleep(0.9)
    return fr.evaluate(f"""()=>[...document.querySelectorAll('[id="nav:form:G:{g}:R:1:C:0:dd_panel"] tr[data-item-label]')].map(e=>(e.getAttribute('data-item-label')||'')).filter(t=>t.trim())""")
def pick(fr,g,label):
    fr.locator(f'[id="nav:form:G:{g}:R:1:C:0:dd_panel"] tr[data-item-label="{label}"]').first.click(timeout=4000); time.sleep(1.3)

def dump_log(fr, tag):
    res = fr.evaluate("""()=>{const t=document.getElementById('log_list:form:T_data'); if(!t)return {n:0,rows:[]};
      const rows=[...t.querySelectorAll('tr')].map(tr=>({id:tr.id||'',ri:tr.getAttribute('data-ri'),cells:[...tr.querySelectorAll('td')].map(td=>(td.textContent||'').trim()).filter(x=>x!==undefined)}));
      return {n:rows.length, rows};}""")
    print(f"--- log_list [{tag}] rows={res['n']} ---")
    for r in res["rows"][:6]:
        print("   ri=%s id=%s cells=%s" % (r["ri"], r["id"], json.dumps(r["cells"])))

with sync_playwright() as p:
    b=p.chromium.launch(headless=True); page=b.new_context(ignore_https_errors=True,viewport={"width":1680,"height":1000}).new_page()
    page.goto(URL,wait_until="domcontentloaded",timeout=60000)
    page.fill('[id="username"]',"sysadmin"); page.fill('[id="password"]',"sysadmin"); page.click('[id="kc-login"]')
    page.wait_for_selector('[id="menu:searchForm:searchTxt"]',timeout=60000)
    sel='xpath=//*[contains(@class,"tv-link") and normalize-space(text())="Daily Allocation"]'; fr=None
    for _ in range(3):
        page.fill('[id="menu:searchForm:searchTxt"]',""); page.locator('[id="menu:searchForm:searchTxt"]').type(SCREEN,delay=40)
        try: page.wait_for_selector(sel,timeout=12000)
        except Exception: pass
        time.sleep(0.6)
        try: page.locator(sel).first.click()
        except Exception: continue
        page.wait_for_load_state("networkidle",timeout=30000)
        for _ in range(25):
            fr=next((f for f in page.frames if "edit_daily_alloc" in f.url),None)
            if fr: break
            time.sleep(1.0)
        if fr: break
    if not fr: print("NOT LOADED"); b.close(); raise SystemExit
    time.sleep(2.0)
    for g in (0,1):
        di=fr.locator(f'[id="nav:form:G:{g}:R:1:C:0:da_input"]'); di.fill(DATE); di.press("Tab"); time.sleep(1.0)
    opts(fr,2); pick(fr,2,"Testing allocation RUN_NO")
    opts(fr,3); g4=opts(fr,4); pick(fr,4,g4[0])
    fr.locator('[id="button:form:B"]').click(timeout=5000); page.wait_for_load_state("networkidle",timeout=30000); time.sleep(2.0)
    dump_log(fr, "before RUN")
    chk=fr.evaluate("""()=>{const lbl=[...document.querySelectorAll('*')].find(e=>e.children.length===0&&(e.textContent||'').trim()==='Simulate'); if(!lbl)return 'no-label'; let s=lbl.closest('td,div,span')||lbl.parentElement; for(let i=0;i<5&&s;i++){const box=s.querySelector('.ui-chkbox-box'); if(box){if(!box.classList.contains('ui-state-active'))box.click(); return box.classList.contains('ui-state-active')?'on':'off-after-click';} s=s.parentElement;} return 'no-box';}""")
    print("Simulate set ->", chk); time.sleep(0.8)
    fr.locator('[id="ProdAllocButton:form:B"]').click(timeout=6000); print("RUN clicked")
    page.wait_for_load_state("networkidle",timeout=90000); time.sleep(6.0)
    dump_log(fr, "after RUN")
    b.close()
print("DONE")
