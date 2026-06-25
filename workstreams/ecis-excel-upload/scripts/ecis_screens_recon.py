"""Screen recon: Mapping Configuration (load AUDREY) + Schedules (find AudreyExcelImport)
+ Upload Files screen. Read-only — screenshots + structure dumps for the learning doc."""
import json
import os
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

URL = os.environ.get("EC_URL", "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/")
OUT = Path(r"c:/Projects/ChoongYin_OS/tmp/ecis_recon")
OUT.mkdir(parents=True, exist_ok=True)

SCREENS = ["Mapping Configuration", "Target Mapping Configuration", "Upload Files",
           "Staging Area", "Import History", "Schedules"]

def goto_screen(page, name):
    page.goto(URL, wait_until="domcontentloaded", timeout=60000)
    page.wait_for_selector('[id="menu:searchForm:searchTxt"]', timeout=30000)
    time.sleep(0.8)
    box = page.locator('[id="menu:searchForm:searchTxt"]')
    box.fill("")
    box.type(name, delay=50)
    time.sleep(1.2)
    link = page.locator(f'xpath=//*[self::label or self::span][contains(@class,"tv-link") and normalize-space(text())="{name}"]')
    if link.count() == 0:
        # report what DID match
        cands = page.evaluate("""() => [...document.querySelectorAll('.tv-link')]
            .map(e => (e.textContent||'').trim()).filter(t => t).slice(0, 15)""")
        return cands
    link.first.click()
    page.wait_for_load_state("networkidle", timeout=20000)
    time.sleep(2.0)
    return None

DUMP = """
() => {
  const vis = e => e && e.offsetParent !== null;
  const txt = e => (e.textContent||'').trim();
  const nav = [...document.querySelectorAll('[id^="nav:form"]')]
    .filter(e => vis(e) && /(_la|:dd$|_input|:in)$/.test(e.id))
    .map(e => ({id: e.id, t: (txt(e)||e.value||'').slice(0,30)})).slice(0, 16);
  const grids = [...document.querySelectorAll('tbody[id$=":T_data"]')]
    .map(e => ({id: e.id, rows: e.querySelectorAll('tr').length, vis: vis(e)}));
  const tabs = [...document.querySelectorAll('.ui-tabs-header, [role="tab"]')]
    .filter(vis).map(txt).filter(t => t).slice(0, 12);
  const buttons = [...document.querySelectorAll('button, a.ui-button')]
    .filter(vis).map(txt).filter(t => t && t.length < 30).slice(0, 15);
  return {nav, grids, tabs, buttons};
}
"""

results = {}
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_context(ignore_https_errors=True, viewport={"width": 1920, "height": 1080}).new_page()
    page.goto(URL, wait_until="domcontentloaded", timeout=60000)
    page.fill('[id="username"]', "sysadmin")
    page.fill('[id="password"]', "sysadmin")
    page.click('[id="kc-login"]')
    page.wait_for_selector('[id="menu:searchForm:searchTxt"]', timeout=60000)

    for name in SCREENS:
        tag = name.lower().replace(" ", "_")
        try:
            miss = goto_screen(page, name)
            if miss is not None:
                results[name] = {"status": "NOT_FOUND", "treeview_matches": miss}
                print(f"!! {name}: not found; matches: {miss[:8]}")
                continue
            data = page.evaluate(DUMP)
            data["status"] = "OK"
            results[name] = data
            page.screenshot(path=str(OUT / f"{tag}.png"), full_page=True)
            print(f"OK {name}: grids={[(g['id'], g['rows']) for g in data['grids'] if g['vis']][:3]} tabs={data['tabs'][:6]}")
        except Exception as e:
            results[name] = {"status": f"ERROR: {str(e)[:160]}"}
            print(f"!! {name}: {str(e)[:120]}")
    browser.close()

(OUT / "ecis_screens.json").write_text(json.dumps(results, indent=1), encoding="utf-8")
print(f"saved -> {OUT}")
