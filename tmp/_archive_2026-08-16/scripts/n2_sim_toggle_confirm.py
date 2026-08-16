"""Confirm the reliable Simulate toggle: from the hidden input, walk to its checkbox container and
click the visible box; verify input.checked flips to True. Report the exact element clicked + path."""
import time, json
from playwright.sync_api import sync_playwright
URL="https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"; SCREEN="Daily Allocation"; DATE="2003-01-01"
INP="dateStartJob:form:G:0:R:1:C:2:cb"
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
    res=fr.evaluate(f"""()=>{{const i=document.getElementById('{INP}'); if(!i) return {{err:'no-input'}};
      const before=i.checked;
      const cell=i.closest('.ECCheckboxCell')||i.closest('td')||i.parentElement;
      const box=cell?cell.querySelector('div,span,label'):null;
      const target=box||i; const path=[]; let e=target; for(let k=0;k<3&&e;k++){{path.push(e.tagName+'.'+(e.className||'').trim().replace(/\\s+/g,'.'));e=e.parentElement;}}
      if(!before) target.click();
      return {{before, after:document.getElementById('{INP}').checked, clicked:target.tagName+'.'+(target.className||''), cellClass:cell?cell.className:'', path}};}}""")
    print(json.dumps(res, indent=1))
    b.close()
print("DONE")
