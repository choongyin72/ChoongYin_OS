"""Enumerate EC treeview screens matching 'Daily'/'Status' to pick the next N1 coverage target.
Logs in, types search terms, dumps matching tv-link labels. Read-only."""
import time, json
from playwright.sync_api import sync_playwright
URL="https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"
TERMS=["Daily","Status","Monthly"]
with sync_playwright() as p:
    b=p.chromium.launch(headless=True); page=b.new_context(ignore_https_errors=True,viewport={"width":1500,"height":1000}).new_page()
    page.goto(URL,wait_until="domcontentloaded",timeout=60000)
    page.fill('[id="username"]',"sysadmin"); page.fill('[id="password"]',"sysadmin"); page.click('[id="kc-login"]')
    page.wait_for_selector('[id="menu:searchForm:searchTxt"]',timeout=60000); time.sleep(1.0)
    found={}
    for term in TERMS:
        page.fill('[id="menu:searchForm:searchTxt"]',""); page.locator('[id="menu:searchForm:searchTxt"]').type(term,delay=30)
        time.sleep(2.0)
        labels=page.evaluate("""()=>[...document.querySelectorAll('.tv-link')].map(e=>e.textContent.trim()).filter(t=>t)""")
        for l in labels: found[l]=found.get(l,0)+1
    # show all unique screen labels, highlight likely N1 (Daily ... Status)
    allk=sorted(found.keys())
    print("=== ALL matched screen labels (%d) ===" % len(allk))
    for l in allk: print("  ", l)
    print("\n=== likely N1 daily-status candidates ===")
    for l in allk:
        ll=l.lower()
        if ("daily" in ll or "monthly" in ll) and ("status" in ll or "well" in ll or "stream" in ll or "liquid" in ll or "water" in ll or "electric" in ll or "tank" in ll or "equip" in ll):
            print("  ", l)
    b.close()
print("DONE")
