"""READ-ONLY: confirm 'Daily Gas Injection Flowline, by Flowline' - cascade P1 Facility 1 -> P1 F004 GI,
GO, dump grid id + C2 cell (expect daily_flowline_status:form, C2=On Strm[hr]). Also check flowline-name
uniqueness (the WI '0600' trap). NO save."""
import os
import time, json
from playwright.sync_api import sync_playwright
URL="https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"; SCREEN="Daily Gas Injection Flowline, by Flowline"
def get_frame(page):
    for _ in range(40):
        for fr in page.frames:
            try:
                if fr.evaluate("""()=>!!document.querySelector('[id="nav:form:G:0:R:1:C:0:da_input"]')"""): return fr
            except Exception: pass
        time.sleep(0.5)
    return page
def opts(fr,g):
    fr.click(f'[id="nav:form:G:{g}:R:1:C:0:dd_button"]',timeout=5000); time.sleep(0.6)
    return fr.evaluate(f"""()=>[...document.querySelectorAll('[id="nav:form:G:{g}:R:1:C:0:dd_panel"] tr[data-item-label]')].map(e=>(e.getAttribute('data-item-label')||'').trim()).filter(t=>t)""")
def pick(fr,g,label):
    fr.click(f'[id="nav:form:G:{g}:R:1:C:0:dd_button"]',timeout=5000); time.sleep(0.5)
    fr.click(f'xpath=//*[@id="nav:form:G:{g}:R:1:C:0:dd_panel"]//tr[normalize-space(@data-item-label)="{label}"]',timeout=5000); time.sleep(1.0)
with sync_playwright() as p:
    b=p.chromium.launch(headless=True)
    page=b.new_context(ignore_https_errors=True,viewport={"width":1920,"height":1080}).new_page()
    page.goto(URL,wait_until="domcontentloaded",timeout=60000)
    page.fill('[id="username"]', os.environ.get("EC_USER", "sysadmin")); page.fill('[id="password"]', os.environ.get("EC_PASS", "sysadmin")); page.click('[id="kc-login"]')
    page.wait_for_selector('[id="menu:searchForm:searchTxt"]',timeout=60000); time.sleep(1.0)
    page.locator('[id="menu:searchForm:searchTxt"]').type(SCREEN,delay=20); time.sleep(1.3)
    hits=page.evaluate("""()=>[...document.querySelectorAll('.tv-link')].map(e=>e.textContent.trim()).filter(Boolean)""")
    print("search hits:", json.dumps([h for h in hits if 'Gas Injection Flowline' in h][:6]))
    page.locator(f'xpath=//*[contains(@class,"tv-link") and normalize-space(text())="{SCREEN}"]').first.click()
    page.wait_for_load_state("networkidle",timeout=30000); time.sleep(2.0)
    fr=get_frame(page)
    fr.fill('[id="nav:form:G:0:R:1:C:0:da_input"]',"2019-12-20"); fr.fill('[id="nav:form:G:1:R:1:C:0:da_input"]',"2019-12-20"); time.sleep(0.4)
    pick(fr,2,"P1 Production Unit"); pick(fr,3,"P1 Area"); pick(fr,4,"P1 Facility 1")
    flopts=opts(fr,5)
    print("flowline options under P1 Facility 1:", json.dumps(flopts))
    target="P1 F004 GI" if "P1 F004 GI" in flopts else (flopts[0] if flopts else None)
    if target: 
        fr.click(f'xpath=//*[@id="nav:form:G:5:R:1:C:0:dd_panel"]//tr[normalize-space(@data-item-label)="{target}"]',timeout=5000); time.sleep(1.0)
    print("picked flowline:", target)
    fr.click('[id="button:form:B"]',timeout=8000); page.wait_for_load_state("networkidle",timeout=30000); time.sleep(2.0)
    info=fr.evaluate(r"""()=>{
      const grids=[...document.querySelectorAll('[id$=":T_data"]')].map(t=>({id:t.id,rows:t.querySelectorAll('tr').length}));
      const cells=[]; for(let c=0;c<10;c++){const e=document.querySelector(`[id="daily_flowline_status:form:T:0:C${c}_in"]`); if(e)cells.push({C:c,val:e.value});}
      return {grids,cells};
    }""")
    print("grids:", json.dumps(info["grids"]))
    print("row0 cells:", json.dumps(info["cells"]))
    b.close()
print("DONE")
