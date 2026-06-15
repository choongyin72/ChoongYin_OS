"""READ-ONLY: confirm the Injection Flowline daily-status screen exists + its nav model (date fields +
cascade dropdowns + grid id), mirroring the PFLW recon. NO writes. Searches a few likely names."""
import time
import json
from playwright.sync_api import sync_playwright

URL = "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"
TERMS = ["Daily Injection Flowline", "Injection Flowline", "Daily Injection", "Injection Flow"]

with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    page = b.new_context(ignore_https_errors=True, viewport={"width": 1680, "height": 1000}).new_page()
    page.goto(URL, wait_until="domcontentloaded", timeout=60000)
    page.fill('[id="username"]', "sysadmin")
    page.fill('[id="password"]', "sysadmin")
    page.click('[id="kc-login"]')
    page.wait_for_selector('[id="menu:searchForm:searchTxt"]', timeout=60000)
    time.sleep(1.0)
    target = None
    for term in TERMS:
        page.fill('[id="menu:searchForm:searchTxt"]', "")
        page.locator('[id="menu:searchForm:searchTxt"]').type(term, delay=20)
        time.sleep(1.3)
        hits = page.evaluate("""()=>[...document.querySelectorAll('.tv-link')].map(e=>e.textContent.trim()).filter(Boolean)""")
        print(f"search '{term}' -> {json.dumps(hits[:10])}")
        if not target:
            for h in hits:
                if "injection" in h.lower() and "flowline" in h.lower():
                    target = h
                    break
    if not target:
        print("\nNO injection-flowline screen found by these terms.")
        b.close(); raise SystemExit(0)
    print(f"\n=== opening '{target}' ===")
    page.fill('[id="menu:searchForm:searchTxt"]', "")
    page.locator('[id="menu:searchForm:searchTxt"]').type(target, delay=20)
    time.sleep(1.3)
    page.locator(f'xpath=//*[contains(@class,"tv-link") and normalize-space(text())="{target}"]').first.click()
    page.wait_for_load_state("networkidle", timeout=30000)
    time.sleep(2.5)
    fr = next((f for f in page.frames if "dashboard.jsf" in (f.url or "") and "top=false" in (f.url or "")), None) or page
    nav = fr.evaluate(r"""()=>{
      const all=[...document.querySelectorAll('[id*="nav:form"]')];
      const labels=all.filter(e=>/:la$/.test(e.id)).map(e=>({id:e.id,t:(e.textContent||'').trim().slice(0,20)}));
      const dates=all.filter(e=>/da_input$/.test(e.id)).map(e=>e.id);
      const dds=all.filter(e=>/:dd$/.test(e.id)).map(e=>e.id);
      const grids=[...document.querySelectorAll('[id$=":T_data"],[id$=":T"]')].map(e=>e.id).slice(0,8);
      return {labels,dates,dds,grids};
    }""")
    print("LABELS:", json.dumps(nav["labels"]))
    print("DATE FIELDS:", json.dumps(nav["dates"]))
    print("CASCADE DDs:", json.dumps(nav["dds"]))
    print("GRIDS:", json.dumps(nav["grids"]))
    b.close()
print("DONE")
