"""READ-ONLY recon of Configuration > Assets > Dispatching Objects (next coverage section).
8 OV screens + 1 TV (Nomination Cycle). For OV screens: opens the New Object form,
dumps row labels + input ids + mandatory (yellow) flags, then navigates away WITHOUT saving.
"""
import json
import os
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

URL = os.environ.get("EC_URL", "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/")
USER = os.environ.get("EC_USER", "sysadmin")
PASS = os.environ.get("EC_PASS", "sysadmin")
OUT = Path(r"c:/Projects/ChoongYin_OS/tmp/dispatching_recon")
OUT.mkdir(parents=True, exist_ok=True)

SCREENS = [
    ("Delivery Point", "OV"),
    ("Delivery Stream", "OV"),
    ("Meter", "OV"),
    ("Nomination Point", "OV"),
    ("Pipeline", "OV-GM"),
    ("Pipeline Segment", "OV"),
    ("Transport System", "OV"),
    ("Transport Zone", "OV"),
    ("Nomination Cycle", "TV"),
]

STRUCT_JS = """
() => {
  const vis = e => e && e.offsetParent !== null;
  const txt = e => (e.textContent || '').trim();
  const nav = [...document.querySelectorAll('[id^="nav:form"]')]
    .filter(e => vis(e) && /(_la|:dd|_da_input)$/.test(e.id))
    .map(e => ({id: e.id, text: txt(e).slice(0,40)})).slice(0, 30);
  const grids = [...document.querySelectorAll('tbody[id$=":T_data"]')]
    .map(e => ({id: e.id, rows: e.querySelectorAll('tr').length, visible: vis(e)}));
  const go = [...document.querySelectorAll('[id="button:form:B"]')].filter(vis).length;
  const toolbar = [...document.querySelectorAll('[id*="creenToolbar"] .ui-menuitem-text')]
    .filter(vis).map(txt).filter(t => t).slice(0, 20);
  return {nav, grids, hasGo: go > 0, toolbar};
}
"""

FORM_JS = """
() => {
  const vis = e => e && e.offsetParent !== null;
  const txt = e => (e.textContent || '').trim();
  const rows = [];
  document.querySelectorAll('[id^="tab:tabPanel:objectForm:form:G:"][id$=":la"]').forEach(la => {
    if (!vis(la)) return;
    const m = la.id.match(/G:(\\d+):R:(\\d+):C:(\\d+)/);
    if (!m) return;
    const base = la.id.replace(/:la$/, '').replace(/:C:\\d+$/, '');
    const cell = [...document.querySelectorAll(`[id^="${base}:C:"]`)]
      .filter(e => vis(e) && /(:in|_da_input|:dd|:cb)$/.test(e.id))[0];
    let mand = false, kind = null, cid = null;
    if (cell) {
      cid = cell.id;
      kind = cell.id.endsWith('_da_input') ? 'date' : cell.id.endsWith(':dd') ? 'dropdown'
           : cell.id.endsWith(':cb') ? 'checkbox' : 'text';
      const bg = getComputedStyle(cell).backgroundColor;
      mand = /255,\\s*255,\\s*(1[0-9]{2}|2[0-2][0-9])/.test(bg) || /ffffcc|ffff99/i.test(bg);
    }
    rows.push({row: +m[2], label: txt(la).slice(0,40), input: cid, kind, mandatory: mand});
  });
  return rows.sort((a,b) => a.row - b.row);
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

    for name, typ in SCREENS:
        tag = name.lower().replace(" ", "_")
        try:
            # fresh app page per screen: silently discards any open (unsaved) form,
            # which otherwise triggers EC's unsaved-changes dialog and blocks navigation
            page.goto(URL, wait_until="domcontentloaded", timeout=60000)
            page.wait_for_selector('[id="menu:searchForm:searchTxt"]', timeout=30000)
            page.wait_for_load_state("networkidle", timeout=20000)
            time.sleep(0.5)
            box = page.locator('[id="menu:searchForm:searchTxt"]')
            box.fill("")
            box.type(name, delay=50)
            page.wait_for_load_state("networkidle", timeout=10000)
            time.sleep(0.8)
            link = page.locator(f'xpath=//*[self::label or self::span][contains(@class,"tv-link") and normalize-space(text())="{name}"]')
            if link.count() == 0:
                results[name] = {"status": "NOT_FOUND"}
                print(f"!! {name}: not in treeview")
                continue
            link.first.click()
            page.wait_for_load_state("networkidle", timeout=20000)
            time.sleep(2.0)
            data = page.evaluate(STRUCT_JS)
            data["type_guess"] = typ
            page.screenshot(path=str(OUT / f"{tag}_list.png"), full_page=True)

            if typ.startswith("OV"):
                # open the New Object form (no save), dump labels, leave by navigating on
                ins = page.locator('xpath=//li[contains(@class,"ui-menu-parent")][.//span[contains(@class,"ui-icon-insert")]]')
                if ins.count() > 0:
                    ins.first.hover()
                    item = page.locator('xpath=//ul[contains(@class,"ui-menu-child")]//li//a[normalize-space(.)="New Object"]')
                    item.wait_for(state="visible", timeout=10000)
                    item.click()
                    page.wait_for_load_state("networkidle", timeout=15000)
                    time.sleep(1.5)
                    data["form"] = page.evaluate(FORM_JS)
                    page.screenshot(path=str(OUT / f"{tag}_form.png"), full_page=True)
                else:
                    data["form"] = "NO_INSERT_MENU"
            data["status"] = "OK"
            results[name] = data
            nf = len(data.get("form", [])) if isinstance(data.get("form"), list) else data.get("form")
            print(f"OK {name} [{typ}] go={data['hasGo']} grids={[(g['id'],g['rows']) for g in data['grids'] if g['visible']][:2]} formRows={nf}")
        except Exception as e:
            results[name] = {"status": f"ERROR: {e}"}
            print(f"!! {name}: {str(e)[:140]}")

    browser.close()

(OUT / "dispatching_recon.json").write_text(json.dumps(results, indent=1), encoding="utf-8")
print(f"\nsaved -> {OUT / 'dispatching_recon.json'}")
