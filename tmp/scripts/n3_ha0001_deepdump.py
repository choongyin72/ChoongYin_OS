"""N3 deeper-dive: dump ALL nav:form groups (is there a scope dd beyond dates?), the statusProcess
frozen-table real row nodes (statusProcess:form:T:* not :T_data), and any process names in the body.
Try GO, then also try selecting in the statusProcess grid. Read-only structure crack."""
import time, json
from playwright.sync_api import sync_playwright
URL="https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"; SCREEN="Daily Data Status Processes"
DATE="2003-01-01"
with sync_playwright() as p:
    b=p.chromium.launch(headless=True); page=b.new_context(ignore_https_errors=True,viewport={"width":1680,"height":1000}).new_page()
    page.goto(URL,wait_until="domcontentloaded",timeout=60000)
    page.fill('[id="username"]',"sysadmin"); page.fill('[id="password"]',"sysadmin"); page.click('[id="kc-login"]')
    page.wait_for_selector('[id="menu:searchForm:searchTxt"]',timeout=60000)
    sel=f'xpath=//*[contains(@class,"tv-link") and normalize-space(text())="{SCREEN}"]'; fr=None
    for _ in range(3):
        page.fill('[id="menu:searchForm:searchTxt"]',""); page.locator('[id="menu:searchForm:searchTxt"]').type(SCREEN,delay=40)
        try: page.wait_for_selector(sel,timeout=12000)
        except Exception: pass
        time.sleep(0.6)
        try: page.locator(sel).first.click()
        except Exception: continue
        page.wait_for_load_state("networkidle",timeout=30000)
        for _ in range(20):
            fr=next((f for f in page.frames if "dashboard.jsf" in f.url and "top=false" in f.url),None)
            if fr: break
            time.sleep(1.0)
        if fr: break
    if not fr: print("NOT LOADED"); b.close(); raise SystemExit
    time.sleep(2.0)
    # ALL nav groups (labels + control types) BEFORE go
    nav=fr.evaluate("""()=>{
      const groups={};
      document.querySelectorAll('[id^="nav:form:G:"]').forEach(e=>{
        const m=e.id.match(/nav:form:G:(\\d+)/); if(!m)return; const g=m[1];
        groups[g]=groups[g]||{labels:new Set(),hasDate:false,hasDd:false};
        if(/da_input/.test(e.id))groups[g].hasDate=true;
        if(/dd_button|_panel/.test(e.id))groups[g].hasDd=true;
      });
      // labels near nav
      const labs=[...document.querySelectorAll('[id^="nav:form"] label, [id^="nav:form"] .label, nav, [id^="nav:form"] td')].map(e=>(e.textContent||'').trim()).filter(t=>t&&t.length<30).slice(0,20);
      return {groups:Object.fromEntries(Object.entries(groups).map(([k,v])=>[k,{hasDate:v.hasDate,hasDd:v.hasDd}])), navLabels:[...new Set(labs)]};
    }""")
    print("nav groups:", json.dumps(nav["groups"]))
    print("nav labels:", json.dumps(nav["navLabels"]))
    for g in (0,1):
        try:
            di=fr.locator(f'[id="nav:form:G:{g}:R:1:C:0:da_input"]'); di.fill(DATE); di.press("Tab"); time.sleep(0.8)
        except Exception: pass
    try:
        fr.locator('[id="button:form:B"]').click(timeout=6000); page.wait_for_load_state("networkidle",timeout=30000); time.sleep(3.0)
        print("GO clicked")
    except Exception as e: print("GO err:", str(e)[:80])
    # statusProcess grid real rows + process names in body
    res=fr.evaluate("""()=>{
      const trs=[...document.querySelectorAll('[id^="statusProcess:form"] tr')].map(tr=>({id:tr.id||'', cells:[...tr.querySelectorAll('td')].map(td=>(td.textContent||'').trim()).filter(Boolean).slice(0,6)})).filter(r=>r.cells.length).slice(0,25);
      const body=(document.body.innerText||'').replace(/\\s+/g,' ');
      const procNames=['P3_VERIFY_FCTY','Verify P3 Facility','VER_ONS_FCTY','Verify daily Onshore','P1_FwdUpd','Verify','Approve'].filter(n=>body.includes(n));
      // all buttons/links with run-ish OR icon titles
      const acts=[...document.querySelectorAll('a[title],button[title],a,button')].map(e=>({id:e.id||'',title:e.getAttribute('title')||'',t:(e.textContent||'').trim().slice(0,24)})).filter(x=>/run|verif|approv|execut|start|process|play/i.test((x.title+' '+x.t))).slice(0,20);
      const allTdata=[...document.querySelectorAll('[id$="_data"]')].map(e=>({id:e.id,rows:e.querySelectorAll('tr').length}));
      return {gridRows:trs, procNames, acts, allTdata};
    }""")
    print("\nstatusProcess grid rows:")
    for r in res["gridRows"]: print("   ", json.dumps(r))
    print("\nprocess names found in body:", json.dumps(res["procNames"]))
    print("\nall *_data containers + row counts:", json.dumps(res["allTdata"]))
    print("\nrun-ish actions (id,title,text):")
    for a in res["acts"]: print("   ", json.dumps(a))
    page.screenshot(path="c:/Projects/ChoongYin_OS/tmp/n3_ha0001_deep.png", full_page=True)
    b.close()
print("DONE")
