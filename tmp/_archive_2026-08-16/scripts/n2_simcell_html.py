"""Dump the Simulate cell innerHTML + test a JS-click toggle, so the RF keyword targets the
real clickable child deterministically (headed actionability was flaky on the cell container)."""
import time, json
from playwright.sync_api import sync_playwright
URL="https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"; SCREEN="Daily Allocation"; DATE="2003-01-01"
CELL="dateStartJob:form:G:0:R:1:C:2"; INP=CELL+":cb"
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
    info=fr.evaluate(f"""()=>{{const c=document.getElementById('{CELL}'); const i=document.getElementById('{INP}');
      return {{cellTag:c?c.tagName:'NONE', cellClass:c?c.className:'', cellHTML:c?c.innerHTML.slice(0,500):'', visible:c?(c.offsetWidth+'x'+c.offsetHeight):'', inputChecked:i?i.checked:null}};}}""")
    print("cell:", json.dumps(info, indent=1))
    # Try JS-click on the child box (first element child) and report effect
    res=fr.evaluate(f"""()=>{{const c=document.getElementById('{CELL}'); const i=document.getElementById('{INP}');
      const box=c?(c.querySelector('.ECCheckbox,.ui-chkbox-box,div,span,label')||c):null;
      const before=i?i.checked:null; if(box) box.click();
      return {{clicked: box?box.className||box.tagName:'none', before, after:i?i.checked:null}};}}""")
    print("js-click child box:", json.dumps(res))
    b.close()
print("DONE")
