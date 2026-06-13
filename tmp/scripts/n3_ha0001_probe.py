"""N3 make-or-break probe: open HA.0001 'Daily Data Status Processes' and learn the RUN mechanism —
synchronous button (+ log, like HA.0002) vs BPM dispatch (the stalling executor). Read-only: open,
walk nav if any, dump the action controls / buttons / any process grid + log table ids. NO run fired."""
import time, json
from playwright.sync_api import sync_playwright
URL="https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"
CANDIDATES=["Daily Data Status Processes","Data Status Processes","Status Processes"]

with sync_playwright() as p:
    b=p.chromium.launch(headless=True); page=b.new_context(ignore_https_errors=True,viewport={"width":1680,"height":1000}).new_page()
    page.goto(URL,wait_until="domcontentloaded",timeout=60000)
    page.fill('[id="username"]',"sysadmin"); page.fill('[id="password"]',"sysadmin"); page.click('[id="kc-login"]')
    page.wait_for_selector('[id="menu:searchForm:searchTxt"]',timeout=60000)
    fr=None; opened=None
    for name in CANDIDATES:
        sel=f'xpath=//*[contains(@class,"tv-link") and normalize-space(text())="{name}"]'
        page.fill('[id="menu:searchForm:searchTxt"]',""); page.locator('[id="menu:searchForm:searchTxt"]').type(name,delay=40)
        try: page.wait_for_selector(sel,timeout=8000)
        except Exception: continue
        time.sleep(0.6)
        try: page.locator(sel).first.click()
        except Exception: continue
        page.wait_for_load_state("networkidle",timeout=30000); time.sleep(2.0)
        # find the screen iframe (com.ec.prod.ha.screens family)
        for _ in range(20):
            fr=next((f for f in page.frames if "ha.screens" in f.url or "status" in f.url.lower() or "edit_" in f.url),None)
            if fr: break
            time.sleep(1.0)
        opened=name
        if fr: break
    if not fr:
        print("screen not loaded; tried:", CANDIDATES);
        # dump treeview hits to see exact label
        hits=page.evaluate("""()=>[...document.querySelectorAll('.tv-link')].map(e=>e.textContent.trim()).filter(t=>/status/i.test(t)).slice(0,20)""")
        print("treeview 'status' labels:", json.dumps(hits)); b.close(); raise SystemExit
    print("OPENED:", opened, "| frame url:", fr.url[:90])
    time.sleep(1.5)
    info=fr.evaluate("""()=>{
      const txt=(document.body.innerText||'').replace(/\\s+/g,' ');
      const btns=[...document.querySelectorAll('a,button,span.ui-button-text')].map(e=>({id:e.id||(e.closest('[id]')?.id||''),t:(e.textContent||'').trim()})).filter(x=>x.t && x.t.length<40).slice(0,40);
      const tables=[...document.querySelectorAll('[id$=":T_data"]')].map(e=>e.id).slice(0,20);
      const navDates=[...document.querySelectorAll('[id*="da_input"]')].map(e=>e.id).slice(0,6);
      const runHints=(txt.match(/(Run|Execute|Verify|Approve|Process automation|RUNNING|WAITING|Simulate|Status Process)[^.]{0,30}/gi)||[]).slice(0,12);
      const bpmBell=/process automation/i.test(txt);
      return {tables, navDates, btns, runHints, bpmBell, bodyLen:txt.length};
    }""")
    print("nav date fields:", json.dumps(info["navDates"]))
    print("tables (T_data):", json.dumps(info["tables"]))
    print("BPM 'process automation' text present:", info["bpmBell"])
    print("run-ish text hints:", json.dumps(info["runHints"]))
    print("buttons (id,text):")
    for x in info["btns"]:
        if x["t"]: print("   ", json.dumps(x))
    page.screenshot(path="c:/Projects/ChoongYin_OS/tmp/n3_ha0001.png", full_page=True)
    b.close()
print("DONE")
