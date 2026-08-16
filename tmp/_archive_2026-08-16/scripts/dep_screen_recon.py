"""READ-ONLY recon of the excluded dependency screens (Financial 7 + Commercial 6).
Loads each screen, dumps navigator + form/grid structure + dropdown labels, screenshots.
NO inserts/saves - pure observation, used to draft the dependency map.
"""
import json
import os
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

URL = os.environ.get("EC_URL", "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/")
USER = os.environ.get("EC_USER", "sysadmin")
PASS = os.environ.get("EC_PASS", "sysadmin")

OUT = Path(r"c:/Projects/ChoongYin_OS/tmp/dep_recon")
OUT.mkdir(parents=True, exist_ok=True)

SCREENS = [
    # Financial Objects leftovers
    "Account Mapping Assistance",
    "Cost Object Mapping Assistance",
    "Exchange Rate Setup",
    "Exchange Rates",
    "Financial Posting Setup",
    "VAT Country Setup",
    "Payment Scheme Setup",
    # Commercial Objects leftovers
    "Customer VAT Reg No",
    "Vendor VAT Reg No",
    "Restricted Customer Setup",
    "Restricted Vendor Setup",
    "Field Group Setup",
    "Maintain Equity Share",
]

DUMP_JS = """
() => {
  const vis = e => e && e.offsetParent !== null;
  const txt = e => (e.textContent || '').trim();
  // navigator labels + inputs
  const nav = [...document.querySelectorAll('[id^="nav:form"]')]
    .filter(e => vis(e) && /(_la|:dd|_input|_in)$/.test(e.id))
    .map(e => ({id: e.id, tag: e.tagName, text: txt(e).slice(0, 50), val: (e.value||'').slice(0,30)}))
    .slice(0, 40);
  // visible dropdowns anywhere + their label text (PrimeFaces selects)
  const dds = [...document.querySelectorAll('[id$=":dd"], select')]
    .filter(vis)
    .map(e => ({id: e.id, options: [...(e.options||[])].slice(0,8).map(o => txt(o)).filter(Boolean)}))
    .slice(0, 25);
  // form row labels (insert form pattern)
  const rows = [...document.querySelectorAll('[id*=":form:G:"][id$=":la"], [id*="form"][id$="_la"]')]
    .filter(vis).map(e => ({id: e.id, label: txt(e).slice(0, 60)}))
    .filter(r => r.label).slice(0, 60);
  // data grids
  const grids = [...document.querySelectorAll('tbody[id$=":T_data"]')]
    .map(e => ({id: e.id, rows: e.querySelectorAll('tr').length, visible: vis(e)}));
  // toolbar menu labels (Insert/Delete submenus reveal the editable entity)
  const toolbar = [...document.querySelectorAll('[id*="screenToolbar"] span, [id*="Toolbar"] a')]
    .filter(vis).map(txt).filter(t => t && t.length < 35).slice(0, 30);
  const label = txt(document.querySelector('[id="screenToolbar:form:screenLabel"]'));
  return {screenLabel: label, nav, dropdowns: dds, formLabels: rows, grids, toolbar};
}
"""

results = {}
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    ctx = browser.new_context(ignore_https_errors=True, viewport={"width": 1920, "height": 1080})
    page = ctx.new_page()
    page.goto(URL, wait_until="domcontentloaded", timeout=60000)
    page.fill('[id="username"]', USER)
    page.fill('[id="password"]', PASS)
    page.click('[id="kc-login"]')
    page.wait_for_selector('[id="menu:searchForm:searchTxt"]', timeout=60000)
    page.wait_for_load_state("networkidle", timeout=30000)

    for name in SCREENS:
        tag = name.lower().replace(" ", "_")
        try:
            box = page.locator('[id="menu:searchForm:searchTxt"]')
            box.fill("")
            box.type(name, delay=50)
            page.wait_for_load_state("networkidle", timeout=10000)
            time.sleep(0.8)
            link = page.locator(f'xpath=//*[self::label or self::span][contains(@class,"tv-link") and normalize-space(text())="{name}"]')
            n = link.count()
            if n == 0:
                results[name] = {"status": "NOT_FOUND_IN_TREEVIEW"}
                print(f"!! {name}: not found in treeview")
                continue
            link.first.click()
            page.wait_for_load_state("networkidle", timeout=20000)
            time.sleep(2.0)
            data = page.evaluate(DUMP_JS)
            data["status"] = "OK"
            results[name] = data
            page.screenshot(path=str(OUT / f"{tag}.png"), full_page=True)
            print(f"OK {name}: grids={[(g['id'], g['rows']) for g in data['grids']][:3]}")
        except Exception as e:
            results[name] = {"status": f"ERROR: {e}"}
            print(f"!! {name}: {e}")

    browser.close()

(OUT / "dep_recon.json").write_text(json.dumps(results, indent=1), encoding="utf-8")
print(f"\nsaved -> {OUT / 'dep_recon.json'}")
