"""READ-ONLY: dump the real Send Freetext nav-form structure — all ids containing 'nav:form', every
dropdown (id ending dd / label), date inputs, and any *_panel. So we use EXACT locators. NO send."""
import time
import json
from playwright.sync_api import sync_playwright

URL = "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"
SCREEN = "Send Freetext Message"

JS = r"""
() => {
  const all = [...document.querySelectorAll('[id*="nav:form"]')];
  const dds = all.filter(e => /:dd$/.test(e.id) || e.classList.contains('ui-selectonemenu'))
                 .map(e => ({id: e.id, label: (e.getAttribute('data-item-label')||e.textContent||'').trim().slice(0,40)}));
  const labels = all.filter(e => /label/i.test(e.className) || e.tagName==='LABEL')
                    .map(e => ({id: e.id, t: (e.textContent||'').trim().slice(0,30)})).filter(x=>x.t).slice(0,30);
  const inputs = all.filter(e => ['INPUT','TEXTAREA'].includes(e.tagName))
                    .map(e => ({id: e.id, type: e.type})).slice(0,40);
  const navIds = all.map(e => e.id).filter(Boolean).slice(0, 80);
  return {count: all.length, dds, labels, inputs, navIds};
}
"""

with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    page = b.new_context(ignore_https_errors=True, viewport={"width": 1680, "height": 1000}).new_page()
    page.goto(URL, wait_until="domcontentloaded", timeout=60000)
    page.fill('[id="username"]', "sysadmin")
    page.fill('[id="password"]', "sysadmin")
    page.click('[id="kc-login"]')
    page.wait_for_selector('[id="menu:searchForm:searchTxt"]', timeout=60000)
    time.sleep(1.0)
    page.locator('[id="menu:searchForm:searchTxt"]').type(SCREEN, delay=25)
    time.sleep(1.2)
    sel = f'xpath=//*[contains(@class,"tv-link") and normalize-space(text())="{SCREEN}"]'
    page.wait_for_selector(sel, timeout=12000)
    page.locator(sel).first.click()
    page.wait_for_load_state("networkidle", timeout=30000)
    time.sleep(2.5)
    fr = next((f for f in page.frames if "dashboard.jsf" in (f.url or "") and "top=false" in (f.url or "")), None) or page
    info = fr.evaluate(JS)
    print("nav:form element count:", info["count"])
    print("\nDROPDOWNS:", json.dumps(info["dds"], indent=1))
    print("\nLABELS:", json.dumps(info["labels"], indent=1))
    print("\nINPUTS:", json.dumps(info["inputs"], indent=1))
    print("\nNAV IDS (first 80):", json.dumps(info["navIds"], indent=1))
    b.close()
print("DONE")
