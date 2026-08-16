"""N2 probe: (1) find the Simulate checkbox's STABLE id + state, (2) find the RUN button context,
(3) click RUN and POLL log_list row-count + RunningJobs over ~25s to learn how a fresh run surfaces
(new row? in-place update? dedup?). Positive scope, Simulate left at default. No DB write expected."""
import time, json
from playwright.sync_api import sync_playwright
URL="https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"; SCREEN="Daily Allocation"; DATE="2003-01-01"

def opts(fr,g):
    fr.locator(f'[id="nav:form:G:{g}:R:1:C:0:dd_button"]').click(timeout=4000); time.sleep(0.9)
    return fr.evaluate(f"""()=>[...document.querySelectorAll('[id="nav:form:G:{g}:R:1:C:0:dd_panel"] tr[data-item-label]')].map(e=>(e.getAttribute('data-item-label')||'')).filter(t=>t.trim())""")
def pick(fr,g,label):
    fr.locator(f'[id="nav:form:G:{g}:R:1:C:0:dd_panel"] tr[data-item-label="{label}"]').first.click(timeout=4000); time.sleep(1.3)

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

    # (1) dump every checkbox + its label text + stable ids
    cbs = fr.evaluate("""()=>{const out=[];
      document.querySelectorAll('.ui-chkbox, .ui-selectbooleancheckbox, input[type=checkbox]').forEach(el=>{
        const wrap = el.closest('.ui-chkbox')||el.parentElement;
        const box = wrap?wrap.querySelector('.ui-chkbox-box'):null;
        const hidden = wrap?wrap.querySelector('input'):null;
        // nearby label: previous/next sibling text or parent row text
        let labtxt=''; const row=el.closest('tr,div,td'); if(row) labtxt=(row.textContent||'').trim().slice(0,40);
        out.push({tag:el.className||el.tagName, wrapId:wrap?wrap.id:'', boxId:box?box.id:'', boxClass:box?box.className:'', hiddenId:hidden?hidden.id:'', active: box?box.classList.contains('ui-state-active'):null, near:labtxt});
      });
      // de-dup by wrapId+boxId
      const seen=new Set(); return out.filter(o=>{const k=o.wrapId+o.boxId; if(seen.has(k))return false; seen.add(k); return true;});
    }""")
    print("CHECKBOXES:")
    for c in cbs: print("  ", json.dumps(c))

    def logcount(): return fr.evaluate("""()=>{const t=document.getElementById('log_list:form:T_data'); return t?t.querySelectorAll('tr').length:0;}""")
    def running(): return fr.evaluate("""()=>{const t=document.getElementById('RunningJobs:form:T_data'); return t?(t.innerText||'').replace(/\\s+/g,' ').trim().slice(0,80):'';}""")
    before=logcount(); print("\nlog rows before RUN:", before)
    fr.locator('[id="ProdAllocButton:form:B"]').click(timeout=6000); print("RUN clicked")
    for i in range(13):
        time.sleep(2.0)
        try: page.wait_for_load_state("networkidle",timeout=8000)
        except Exception: pass
        print(f"  t+{(i+1)*2:>2}s  logrows={logcount()}  running='{running()}'")
    # final top row
    top=fr.evaluate("""()=>{const t=document.getElementById('log_list:form:T_data'); if(!t)return null; const tr=t.querySelector('tr'); return tr?[...tr.querySelectorAll('td')].map(td=>(td.textContent||'').trim()):null;}""")
    print("top row cells:", json.dumps(top))
    b.close()
print("DONE")
