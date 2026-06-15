"""READ-ONLY: cascade to P1 0600 F003 WI + GO, then dump row-0 grid cells (C-index -> text + editable
input id) to nail the ON_STREAM_HRS column; print the on-screen Flowline Name. NO save."""
import time, json
from playwright.sync_api import sync_playwright
URL="https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"; SCREEN="Daily Water Injection Flowline, by Flowline"
def get_frame(page):
    for _ in range(40):
        for fr in page.frames:
            try:
                if fr.evaluate("""()=>!!document.querySelector('[id="nav:form:G:0:R:1:C:0:da_input"]')"""): return fr
            except Exception: pass
        time.sleep(0.5)
    return page
def pick(fr,g,needle):
    fr.click(f'[id="nav:form:G:{g}:R:1:C:0:dd_button"]',timeout=5000); time.sleep(0.6)
    o=fr.evaluate(f"""()=>[...document.querySelectorAll('[id="nav:form:G:{g}:R:1:C:0:dd_panel"] tr[data-item-label]')].map(e=>(e.getAttribute('data-item-label')||'').trim()).filter(t=>t)""")
    c=next((x for x in o if needle.lower() in x.lower()),None)
    if c: fr.click(f'xpath=//*[@id="nav:form:G:{g}:R:1:C:0:dd_panel"]//tr[normalize-space(@data-item-label)="{c}"]',timeout=5000); time.sleep(1.2)
    return c
with sync_playwright() as p:
    b=p.chromium.launch(headless=True)
    page=b.new_context(ignore_https_errors=True,viewport={"width":1680,"height":1000}).new_page()
    page.goto(URL,wait_until="domcontentloaded",timeout=60000)
    page.fill('[id="username"]',"sysadmin"); page.fill('[id="password"]',"sysadmin"); page.click('[id="kc-login"]')
    page.wait_for_selector('[id="menu:searchForm:searchTxt"]',timeout=60000); time.sleep(1.0)
    page.locator('[id="menu:searchForm:searchTxt"]').type(SCREEN,delay=20); time.sleep(1.3)
    page.locator(f'xpath=//*[contains(@class,"tv-link") and normalize-space(text())="{SCREEN}"]').first.click()
    page.wait_for_load_state("networkidle",timeout=30000); time.sleep(2.0)
    fr=get_frame(page)
    fr.fill('[id="nav:form:G:0:R:1:C:0:da_input"]',"2019-12-20"); fr.fill('[id="nav:form:G:1:R:1:C:0:da_input"]',"2019-12-20"); time.sleep(0.4)
    for g,n in [(2,"P1"),(3,"P1"),(4,"P1"),(5,"F003 WI")]: pick(fr,g,n)
    fr.click('[id="button:form:B"]',timeout=8000); page.wait_for_load_state("networkidle",timeout=30000); time.sleep(2.5)
    cells=fr.evaluate(r"""()=>{
      const out=[];
      for(let c=0;c<14;c++){
        const td=document.querySelector(`[id="daily_flowline_status:form:T:0:C${c}"]`);
        const inp=document.querySelector(`[id="daily_flowline_status:form:T:0:C${c}_in"]`);
        if(td||inp) out.push({C:c, text:(td?td.textContent.trim():'').slice(0,20), in_id: inp?inp.id:null, in_val: inp?inp.value:null});
      }
      return out;
    }""")
    print("ROW0 CELLS:", json.dumps(cells, indent=1))
    b.close()
print("DONE")
