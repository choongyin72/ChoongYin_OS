"""Find a data-bearing PU for WR.0001 (READ-ONLY): for each Production Unit option, select it,
then check whether the Facility Class 1 (G3) and Well Hookup (G4) dds have options. Report PUs
that yield a usable scope so the grid can be populated."""
import os, time, json
from pathlib import Path
from playwright.sync_api import sync_playwright

URL = "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"
SCREEN = "Daily Production Well Status 1"
OUT = Path(r"c:/Projects/ChoongYin_OS/tmp/wr0001_recon"); OUT.mkdir(parents=True, exist_ok=True)

def open_dd_count(fr, gidx):
    """open nav dd for group gidx, return its option labels, then close."""
    try:
        fr.locator(f'[id="nav:form:G:{gidx}:R:1:C:0:dd_button"]').click(timeout=4000)
        time.sleep(0.7)
        opts = fr.evaluate(f"""() => [...document.querySelectorAll('[id="nav:form:G:{gidx}:R:1:C:0:dd_panel"] tr[data-item-label]')]
            .map(e => (e.getAttribute('data-item-label')||'').trim()).filter(t=>t)""")
        fr.locator(f'[id="nav:form:G:{gidx}:R:1:C:0:dd_button"]').click(timeout=2000)  # close
        time.sleep(0.2)
        return opts
    except Exception:
        return []

def select_dd(fr, gidx, label):
    fr.locator(f'[id="nav:form:G:{gidx}:R:1:C:0:dd_button"]').click(timeout=4000); time.sleep(0.7)
    fr.locator(f'[id="nav:form:G:{gidx}:R:1:C:0:dd_panel"] tr[data-item-label="{label}"]').first.click(timeout=4000)
    time.sleep(1.0)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_context(ignore_https_errors=True, viewport={"width":1920,"height":1080}).new_page()
    page.goto(URL, wait_until="domcontentloaded", timeout=60000)
    page.fill('[id="username"]', "sysadmin"); page.fill('[id="password"]', "sysadmin"); page.click('[id="kc-login"]')
    page.wait_for_selector('[id="menu:searchForm:searchTxt"]', timeout=60000)
    sel = f'xpath=//*[contains(@class,"tv-link") and normalize-space(text())="{SCREEN}"]'
    fr = None
    for _ in range(2):
        page.fill('[id="menu:searchForm:searchTxt"]', ""); page.locator('[id="menu:searchForm:searchTxt"]').type(SCREEN, delay=40)
        page.wait_for_selector(sel, timeout=15000); time.sleep(0.6); page.locator(sel).first.click()
        page.wait_for_load_state("networkidle", timeout=30000)
        for _ in range(25):
            fr = next((f for f in page.frames if "daily_well_status" in f.url), None)
            if fr: break
            time.sleep(1.0)
        if fr: break
    if not fr:
        print("frame not loaded"); browser.close(); raise SystemExit
    time.sleep(2.0)

    # set the navigator Date to a data-bearing date (seed epoch) — dds are date-filtered
    DATE = os.environ.get("EC_DATE", "2003-01-01")
    try:
        di = fr.locator('[id="nav:form:G:0:R:1:C:0:da_input"]')
        di.fill(DATE); di.press("Tab"); time.sleep(1.5)
        print("set Date =", DATE)
    except Exception as e:
        print("date set failed:", str(e)[:80])

    pus = open_dd_count(fr, 1)  # Production Unit options
    print(f"{len(pus)} PUs to scan")
    findings = []
    for pu in pus:
        try:
            select_dd(fr, 1, pu)
            fc = open_dd_count(fr, 3)   # Facility Class 1
            wh = open_dd_count(fr, 4)   # Well Hookup
            if fc or wh:
                findings.append({"pu": pu, "facility_class_1": fc[:5], "fc_n": len(fc), "well_hookup": wh[:5], "wh_n": len(wh)})
                print(f"  HIT  {pu:42} FC1={len(fc):3}  WH={len(wh):3}")
            else:
                print(f"  --   {pu:42} FC1=0  WH=0")
        except Exception as e:
            print(f"  ERR  {pu}: {str(e)[:60]}")
    (OUT / "scope_scan.json").write_text(json.dumps(findings, indent=2), encoding="utf-8")
    print("\nDATA-BEARING PUs:", json.dumps(findings, indent=1))
    browser.close()
print("DONE")
