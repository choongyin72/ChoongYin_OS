"""Dump each Dispatching screen's NAVIGATOR dropdowns (ids + label + first options) and
the grid tbody id after picking the first nav option + GO. Read-only."""
import json
import os
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

URL = os.environ.get("EC_URL", "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/")
OUT = Path(r"c:/Projects/ChoongYin_OS/tmp/dispatching_recon")
SCREENS = ["Delivery Point", "Delivery Stream", "Nomination Point",
           "Pipeline Segment", "Transport System", "Transport Zone"]

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
        try:
            page.goto(URL, wait_until="domcontentloaded", timeout=60000)
            page.wait_for_selector('[id="menu:searchForm:searchTxt"]', timeout=30000)
            time.sleep(0.8)
            box = page.locator('[id="menu:searchForm:searchTxt"]')
            box.fill("")
            box.type(name, delay=50)
            time.sleep(1)
            page.locator(f'xpath=//*[contains(@class,"tv-link") and normalize-space(text())="{name}"]').first.click()
            page.wait_for_load_state("networkidle", timeout=20000)
            time.sleep(2)
            # navigator header labels + dd ids
            hdr = page.evaluate("""() => {
                const vis = e => e && e.offsetParent !== null;
                const las = [...document.querySelectorAll('[id^="nav:form"][id$="_la"], [id^="nav:form"] label')]
                  .filter(vis).map(e => (e.textContent||'').trim()).filter(t => t);
                const dds = [...document.querySelectorAll('[id^="nav:form"][id$=":dd"]')]
                  .filter(vis).map(e => e.id);
                return {labels: las.slice(0,8), dds}; }""")
            entry = {"nav": hdr, "options": {}}
            for dd in hdr["dds"]:
                try:
                    page.click(f'[id="{dd}_button"]', timeout=5000)
                    page.wait_for_selector(f'[id="{dd}_panel"] tr[data-item-label]', timeout=6000)
                    opts = page.evaluate(f"""() => [...document.querySelectorAll('[id="{dd}_panel"] tr[data-item-label]')]
                        .map(tr => tr.getAttribute('data-item-label')).slice(0, 8)""")
                    entry["options"][dd] = opts
                    page.keyboard.press("Escape")
                    time.sleep(0.4)
                except Exception as e:
                    entry["options"][dd] = [f"FAILED: {str(e)[:60]}"]
            # pick first option of first dd + GO -> tbody id
            first_dd = hdr["dds"][0] if hdr["dds"] else None
            if first_dd and entry["options"][first_dd] and not entry["options"][first_dd][0].startswith("FAILED"):
                page.click(f'[id="{first_dd}_button"]')
                page.wait_for_selector(f'[id="{first_dd}_panel"] tr[data-item-label]', timeout=6000)
                page.locator(f'[id="{first_dd}_panel"] tr[data-item-label]').first.click()
                page.wait_for_load_state("networkidle", timeout=15000)
                time.sleep(1)
                page.click('[id="button:form:B"]')
                page.wait_for_load_state("networkidle", timeout=20000)
                time.sleep(2.5)
                tb = page.evaluate("""() => [...document.querySelectorAll('tbody[id$=":T_data"]')]
                    .map(e => ({id: e.id, rows: e.querySelectorAll('tr').length}))""")
                entry["grid_after_pick_go"] = tb
            results[name] = entry
            print(f"{name}: labels={hdr['labels']} dds={len(hdr['dds'])} grid={entry.get('grid_after_pick_go')}")
            for dd, opts in entry["options"].items():
                print(f"    {dd} -> {opts[:5]}")
        except Exception as e:
            results[name] = {"error": str(e)[:200]}
            print(f"!! {name}: {str(e)[:140]}")
    browser.close()

(OUT / "nav_probe.json").write_text(json.dumps(results, indent=1), encoding="utf-8")
