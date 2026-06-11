"""READ-ONLY: replicate the Area suite sequence exactly and dump panel DOM at
each step to find why tr[data-item-label='Production Unit'] never shows:
1. nav dd open -> dump structure (data-item-label?)
2. pick 'Production Unit', GO
3. New Object form; fill code/name like the suite (incl date Tab-out)
4. open Op PU dd -> dump panel structure + visibility + item presence."""
import json
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

EC_URL = "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"
_scan = json.loads(Path(r"c:/Projects/ChoongYin_OS/tmp/screen_scan/assets_scan.json").read_text(encoding="utf-8"))
URL = next(r["url"] for r in _scan.values()
           if r.get("section") == "Basic Objects" and r["screen"] == "Area")
NAV = "nav:form:G:0:R:1:C:1:dd"
OPPU = "tab:tabPanel:objectForm:form:G:0:R:7:C:1:dd"
SHOT = r"c:/Projects/ChoongYin_OS/tmp/screen_scan/shots"

PANEL_JS = """(dd) => {
    const p = document.getElementById(dd + '_panel');
    if (!p) return {exists: false};
    const rows = [];
    p.querySelectorAll('tr[data-item-label]').forEach(r => rows.push(r.getAttribute('data-item-label')));
    return {exists: true, visible: p.offsetParent !== null, nRows: rows.length,
            labels: rows.slice(0, 8), text: p.innerText.trim().substring(0, 120)};
}"""

with sync_playwright() as p:
    b = p.chromium.launch(headless=True, args=["--ignore-certificate-errors"])
    ctx = b.new_context(ignore_https_errors=True, viewport={"width": 1680, "height": 1200})
    page = ctx.new_page()
    page.goto(EC_URL, wait_until="domcontentloaded", timeout=45000)
    page.fill("#username", "sysadmin")
    page.fill("#password", "sysadmin")
    page.click("#kc-login")
    page.wait_for_url("**/dashboard**", timeout=60000)
    page.wait_for_timeout(1500)
    page.goto(URL, wait_until="domcontentloaded", timeout=45000)
    page.wait_for_timeout(2500)

    print("1) nav panel:")
    page.click(f"[id='{NAV}_button']")
    page.wait_for_timeout(2500)
    print("  ", page.evaluate(PANEL_JS, NAV))

    print("2) pick Production Unit + GO")
    page.click(f"[id='{NAV}_panel'] tr[data-item-label='Production Unit']")
    page.wait_for_timeout(1500)
    page.click("[id='button:form:B']")
    try:
        page.wait_for_load_state("networkidle", timeout=15000)
    except Exception:
        pass
    page.wait_for_timeout(1800)

    print("3) New Object + fill like suite")
    page.hover("xpath=//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'ui-icon-insert')]]")
    item = page.locator("xpath=//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'ui-icon-insert')]]//ul//a[normalize-space(.)='New Object']")
    item.wait_for(state="visible", timeout=8000)
    item.click()
    page.wait_for_timeout(2000)
    code = f"PROBE_{time.strftime('%H%M%S')}"
    for fid, val in [("tab:tabPanel:objectForm:form:G:0:R:0:C:1:in", code),
                     ("tab:tabPanel:objectForm:form:G:0:R:1:C:1:in", "Probe " + code)]:
        page.fill(f"[id='{fid}']", val)
        page.evaluate("(id)=>{const e=document.getElementById(id); if(e){e.dispatchEvent(new Event('change',{bubbles:true}));e.dispatchEvent(new Event('blur',{bubbles:true}));}}", fid)
        page.wait_for_timeout(400)
    page.fill("[id='tab:tabPanel:objectForm:form:G:0:R:4:C:1:da_input']", "2000-01-01")
    page.keyboard.press("Tab")
    page.wait_for_timeout(1000)

    print("4) Op PU dd:")
    print("   before click:", page.evaluate(PANEL_JS, OPPU))
    page.click(f"[id='{OPPU}_button']")
    for i in range(4):
        page.wait_for_timeout(1500)
        info = page.evaluate(PANEL_JS, OPPU)
        print(f"   t+{(i + 1) * 1.5:.1f}s:", info)
        if info.get("nRows"):
            break
    page.screenshot(path=f"{SHOT}/probe_area_seq_oppu.png")
    # NOTE: form abandoned - nothing saved
    ctx.close()
    b.close()
print("done (READ-ONLY, abandoned form)")
