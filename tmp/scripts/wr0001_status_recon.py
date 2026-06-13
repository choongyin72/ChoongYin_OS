"""WR.0001 Daily Production Well Status — N1 daily-status-grid recon (READ-ONLY).
Answers the 7 unknowns in pattern_n1_daily_status_grid_design.md:
 1) date navigator + GO ids   2) extra object-scope selector?   3) rows pre-populated or add?
 4) grid id + editable columns  5) (DB table — separate)  6) record-status/lock  7) inline validation.
Dumps navigator BEFORE and AFTER GO. No writes, no Save."""
import os
import time
import json
from pathlib import Path

from playwright.sync_api import sync_playwright

URL = os.environ.get("EC_URL", "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/")
SCREEN = os.environ.get("EC_SCREEN", "Daily Production Well Status")
OUT = Path(r"c:/Projects/ChoongYin_OS/tmp/wr0001_recon")
OUT.mkdir(parents=True, exist_ok=True)

DUMP = """() => {
  const vis = e => e && e.offsetParent !== null;
  const grab = sel => [...document.querySelectorAll(sel)]
    .filter(vis)
    .map(e => ({id: e.id, tag: e.tagName.toLowerCase(), type: e.type||'',
                val: (e.value!==undefined? String(e.value).slice(0,40):''),
                title: e.title||'', txt: (e.textContent||'').trim().slice(0,30)}));
  // any nav/button/date/dd inputs anywhere on the page
  const navInputs = grab('[id^="nav:"], [id*=":nav:"]');
  const buttons   = grab('button, a.ui-button, [id$=":B"]').filter(b => /go|apply|search|run|B$/i.test(b.id+b.txt+b.title));
  const dates     = grab('input[id$="da_input"]');
  const dds       = grab('[id$=":dd_input"], [id$="_dd_input"]');
  // find any datatable bodies present
  const tables = [...document.querySelectorAll('[id$="T_data"]')]
    .filter(vis).map(t => ({id: t.id, rows: t.querySelectorAll('tr').length}));
  // headers + row0 cells of the first visible table
  let headers = [], row0 = [];
  const firstTbl = [...document.querySelectorAll('[id$="T_data"]')].find(vis);
  if (firstTbl) {
    const base = firstTbl.id.replace(/_data$/, '');
    headers = [...document.querySelectorAll('[id="'+base+'_head"] th')].map(th => (th.textContent||'').trim()).filter(t=>t);
    row0 = [...document.querySelectorAll('[id^="'+base+':0:"]')]
      .map(e => ({id: e.id, type: e.type||e.tagName.toLowerCase(), val: String(e.value||'').slice(0,30)}))
      .filter(c => /(_in|:in|_dd_input|_cb|_da_input|:dd)$/.test(c.id));
  }
  return {navInputs, buttons, dates, dds, tables, headers, row0};
}"""

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_context(ignore_https_errors=True, viewport={"width": 1920, "height": 1080}).new_page()
    page.goto(URL, wait_until="domcontentloaded", timeout=60000)
    page.fill('[id="username"]', "sysadmin")
    page.fill('[id="password"]', "sysadmin")
    page.click('[id="kc-login"]')
    page.wait_for_selector('[id="menu:searchForm:searchTxt"]', timeout=60000)
    box = page.locator('[id="menu:searchForm:searchTxt"]')
    box.type(SCREEN, delay=40)
    time.sleep(1.5)
    # list all search-result items so we pick the EXACT one
    results = page.evaluate("""() => [...document.querySelectorAll('[id^="menu:searchForm:searchList"] a, .tv-link')]
        .filter(e => e.offsetParent).map(e => (e.textContent||'').trim()).filter(t=>t)""")
    print("search results:", results)
    # click the anchor whose text exactly equals SCREEN
    link = page.locator(f'xpath=//a[normalize-space(text())="{SCREEN}"] | //*[contains(@class,"tv-link") and normalize-space(text())="{SCREEN}"]')
    print("exact matches:", link.count())
    link.first.click()
    page.wait_for_load_state("networkidle", timeout=30000)
    time.sleep(3.5)

    # traverse ALL frames — EC status screens render in a content iframe
    frames_info = []
    for fr in page.frames:
        try:
            fi = fr.evaluate(DUMP)
            fi["_frame_url"] = fr.url[:120]
            if fi["navInputs"] or fi["dates"] or fi["dds"] or fi["tables"]:
                frames_info.append(fi)
        except Exception as e:
            frames_info.append({"_frame_url": fr.url[:120], "_err": str(e)[:80]})
    (OUT / "frames_before.json").write_text(json.dumps(frames_info, indent=2), encoding="utf-8")
    print("=== FRAMES (before GO) ===  frame count:", len(page.frames))
    for fi in frames_info:
        print("FRAME", fi.get("_frame_url"))
        print("  dates:", [d["id"] for d in fi.get("dates", [])])
        print("  dds:", [d["id"] for d in fi.get("dds", [])])
        print("  tables:", fi.get("tables"))
        print("  buttons:", [(b["id"], b["title"]) for b in fi.get("buttons", [])][:10])

    before = page.evaluate(DUMP)
    (OUT / "before_go.json").write_text(json.dumps(before, indent=2), encoding="utf-8")
    page.screenshot(path=str(OUT / "before_go.png"), full_page=True)
    print("=== BEFORE GO ===")
    print("nav inputs:", json.dumps(before["navInputs"], indent=1)[:1500])
    print("dates:", [d["id"] for d in before["dates"]])
    print("dds:", [d["id"] for d in before["dds"]])
    print("buttons:", [(b["id"], b["txt"], b["title"]) for b in before["buttons"]][:15])
    print("tables:", before["tables"])

    # try clicking a GO/Apply button if present (read-only — just reloads the grid)
    clicked = None
    for b in before["buttons"]:
        if b["id"].endswith(":B") or "go" in (b["txt"]+b["title"]).lower():
            try:
                page.locator(f'[id="{b["id"]}"]').first.click(timeout=4000)
                clicked = b["id"]
                break
            except Exception as e:
                print("click failed", b["id"], str(e)[:80])
    if clicked:
        print("clicked GO:", clicked)
        page.wait_for_load_state("networkidle", timeout=30000)
        time.sleep(3.0)
        after = page.evaluate(DUMP)
        (OUT / "after_go.json").write_text(json.dumps(after, indent=2), encoding="utf-8")
        page.screenshot(path=str(OUT / "after_go.png"), full_page=True)
        print("=== AFTER GO ===")
        print("tables:", after["tables"])
        print("headers:", after["headers"])
        print("row0:", json.dumps(after["row0"], indent=1)[:1800])
    else:
        print("no GO button clicked")
    browser.close()
print("DONE — artifacts in", OUT)
