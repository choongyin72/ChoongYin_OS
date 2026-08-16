"""Read-only crack of the Send Freetext Message screen (no send — pure recon). Find the screen in the
treeview, open it, dump its nav/form structure + the Send button id + the message-type/distribution
selectors + subject/body fields. Mirrors EC's SendFreetextMessagePage (nav form + template form +
SendButton). NO message is sent."""
import time, json
from playwright.sync_api import sync_playwright
URL = "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"
with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    page = b.new_context(ignore_https_errors=True, viewport={"width": 1680, "height": 1000}).new_page()
    page.goto(URL, wait_until="domcontentloaded", timeout=60000)
    page.fill('[id="username"]', "sysadmin"); page.fill('[id="password"]', "sysadmin"); page.click('[id="kc-login"]')
    page.wait_for_selector('[id="menu:searchForm:searchTxt"]', timeout=60000); time.sleep(1.0)
    for term in ("Send Free", "Free Text Message", "Freetext", "Send Message"):
        page.fill('[id="menu:searchForm:searchTxt"]', ""); page.locator('[id="menu:searchForm:searchTxt"]').type(term, delay=25); time.sleep(1.2)
        hits = page.evaluate("""()=>[...document.querySelectorAll('.tv-link')].map(e=>e.textContent.trim()).filter(Boolean)""")
        if hits:
            print(f"search '{term}' ->", json.dumps(hits[:12]));
    # open the most likely one
    target = None
    page.fill('[id="menu:searchForm:searchTxt"]', ""); page.locator('[id="menu:searchForm:searchTxt"]').type("Free Text", delay=25); time.sleep(1.2)
    cand = page.evaluate("""()=>[...document.querySelectorAll('.tv-link')].map(e=>e.textContent.trim()).filter(t=>/free ?text|send.*message/i.test(t))""")
    print("\ncandidates:", json.dumps(cand))
    if cand:
        target = cand[0]
        sel = f'xpath=//*[contains(@class,"tv-link") and normalize-space(text())="{target}"]'
        page.locator(sel).first.click(); page.wait_for_load_state("networkidle", timeout=30000); time.sleep(2.5)
        fr = next((f for f in page.frames if "dashboard.jsf" in (f.url or "") and "top=false" in (f.url or "")), None) or page
        info = fr.evaluate("""()=>{
          const forms=[...new Set([...document.querySelectorAll('[id*=":form"]')].map(e=>e.id.split(':form')[0]+':form'))].slice(0,12);
          const btns=[...document.querySelectorAll('button,[id*="Button"],a[title]')].map(e=>({id:e.id,t:(e.textContent||e.title||'').trim().slice(0,20)})).filter(x=>x.id).slice(0,20);
          const inputs=[...document.querySelectorAll('input,textarea,select,[id$="dd"]')].map(e=>e.id).filter(Boolean).slice(0,25);
          return {forms, btns, inputs};}""")
        print(f"\n=== opened '{target}' ===")
        print("forms:", json.dumps(info["forms"]))
        print("buttons:", json.dumps(info["btns"]))
        print("inputs:", json.dumps(info["inputs"]))
    b.close()
print("DONE")
