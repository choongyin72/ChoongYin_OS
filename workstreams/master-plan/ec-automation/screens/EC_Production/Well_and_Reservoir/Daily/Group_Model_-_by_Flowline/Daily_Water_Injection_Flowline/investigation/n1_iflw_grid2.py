"""READ-ONLY decisive crack: PU 'P1 Production Unit' / Area 'P1 Area' / Facility 'P1 Facility 1' (exact)
/ Flowline 'P1 F003 WI' (exact, the DATA-bearing one) -> GO -> dump row cells (C-index -> text + input
id/value) to nail ON_STREAM_HRS. NO save."""
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
def opts(fr,g):
    fr.click(f'[id="nav:form:G:{g}:R:1:C:0:dd_button"]',timeout=5000); time.sleep(0.6)
    return fr.evaluate(f"""()=>[...document.querySelectorAll('[id="nav:form:G:{g}:R:1:C:0:dd_panel"] tr[data-item-label]')].map(e=>(e.getAttribute('data-item-label')||'').trim()).filter(t=>t)""")
def pick_exact(fr,g,label):
    o=opts(fr,g)
    if label in o:
        fr.click(f'xpath=//*[@id="nav:form:G:{g}:R:1:C:0:dd_panel"]//tr[normalize-space(@data-item-label)="{label}"]',timeout=5000); time.sleep(1.2); return True,o
    return False,o
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
    pick_exact(fr,2,"P1 Production Unit"); pick_exact(fr,3,"P1 Area")
    okf,_=pick_exact(fr,4,"P1 Facility 1")
    flopts=opts(fr,5)
    print("Facility 'P1 Facility 1' picked:",okf,"| flowline options:", json.dumps(flopts))
    okfl=False
    if "P1 F003 WI" in flopts:
        fr.click(f'xpath=//*[@id="nav:form:G:5:R:1:C:0:dd_panel"]//tr[normalize-space(@data-item-label)="P1 F003 WI"]',timeout=5000); time.sleep(1.2); okfl=True
    print("flowline 'P1 F003 WI' picked:",okfl)
    fr.click('[id="button:form:B"]',timeout=8000); page.wait_for_load_state("networkidle",timeout=30000); time.sleep(2.5)
    cells=fr.evaluate(r"""()=>{
      const out=[];
      document.querySelectorAll('[id^="daily_flowline_status:form:T:"]').forEach(e=>{
        const m=e.id.match(/:T:(\d+):C(\d+)(_in)?$/);
        if(m && (e.tagName==='INPUT'||e.tagName==='TEXTAREA'||(!m[3]))) out.push({id:e.id.split('daily_flowline_status:form:')[1], tag:e.tagName, text:(e.textContent||'').trim().slice(0,16), val:e.value!==undefined?e.value:null});
      });
      return out.slice(0,50);
    }""")
    print("ROW CELLS:", json.dumps(cells, indent=1))
    b.close()
print("DONE")
