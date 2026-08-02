"""READ-ONLY confirmation probe for phase-B build:
1. Sub Area: select PU 'Production Unit' -> list the Area dd options (user said
   Area = 'Production Unit'; confirm such an option exists).
2. Object List Setup: List Class=FIN_ACCOUNT, Object List='OPEX GL Equipment
   Rental', GO -> capture item grid id + current items + Insert row mechanics
   (open Insert > Object List Item, dump new-row DOM)."""
import os
import json
from pathlib import Path

from playwright.sync_api import sync_playwright

EC_URL = "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"
SCAN = Path(r"c:/Projects/ChoongYin_OS/tmp/screen_scan/assets_scan.json")
SHOTS = Path(r"c:/Projects/ChoongYin_OS/tmp/screen_scan/shots")
scan = json.loads(SCAN.read_text(encoding="utf-8"))
URL = {r["screen"]: r["url"] for r in scan.values()
       if r.get("section") == "Basic Objects" and r.get("url")}

GRID_JS = r"""() => {
    const out = [];
    document.querySelectorAll("tbody[id$=':form:T_data']").forEach(t => {
        const rows = [];
        t.querySelectorAll('tr').forEach(tr => {
            const cells = [];
            tr.querySelectorAll('td').forEach(td => cells.push((td.textContent || '').trim()));
            if (cells.some(c => c)) rows.push(cells.slice(0, 5));
        });
        out.push({id: t.id, rows: rows.slice(0, 12)});
    });
    return out;
}"""

ROW_INPUTS_JS = r"""() => {
    const out = [];
    document.querySelectorAll("input[id*=':T:'], button[id*=':T:'][id$='dd_button'], select[id*=':T:']").forEach(e => {
        if (e.offsetParent !== null) out.push({tag: e.tagName, id: e.id, type: e.type || ''});
    });
    return out.slice(0, 30);
}"""


def pick(page, dd, value):
    page.click(f"[id='{dd}_button']")
    page.wait_for_selector(f"[id='{dd}_panel']", state="visible", timeout=10000)
    page.wait_for_timeout(1200)
    page.click(f"[id='{dd}_panel'] >> text=\"{value}\"")
    page.wait_for_timeout(1500)


with sync_playwright() as p:
    b = p.chromium.launch(headless=True, args=["--ignore-certificate-errors"])
    ctx = b.new_context(ignore_https_errors=True, viewport={"width": 1680, "height": 1200})
    page = ctx.new_page()
    page.on("dialog", lambda d: d.accept())
    page.goto(EC_URL, wait_until="domcontentloaded", timeout=45000)
    page.fill("#username", os.environ.get("EC_USER", "sysadmin"))
    page.fill("#password", os.environ.get("EC_PASS", "sysadmin"))
    page.click("#kc-login")
    page.wait_for_url("**/dashboard**", timeout=60000)
    page.wait_for_timeout(1500)

    # --- 1. Sub Area cascade under PU 'Production Unit'
    print("=== Sub Area: Areas under PU 'Production Unit' ===")
    page.goto(URL["Sub Area"], wait_until="domcontentloaded", timeout=45000)
    try:
        page.wait_for_load_state("networkidle", timeout=20000)
    except Exception:
        pass
    page.wait_for_timeout(1500)
    try:
        pick(page, "nav:form:G:0:R:1:C:1:dd", "Production Unit")
        dd2 = "nav:form:G:0:R:1:C:2:dd"
        page.click(f"[id='{dd2}_button']")
        page.wait_for_selector(f"[id='{dd2}_panel']", state="visible", timeout=10000)
        page.wait_for_timeout(1500)
        txt = page.evaluate(
            "(pid) => { const e=document.getElementById(pid); return e ? e.innerText.trim().substring(0,400) : null }",
            f"{dd2}_panel")
        print("  Area options:", repr(txt))
        page.keyboard.press("Escape")
    except Exception as e:
        print("  ERR:", str(e)[:150])

    # --- 2. Object List Setup with user's values
    print("=== Object List Setup: FIN_ACCOUNT / OPEX GL Equipment Rental ===")
    page.goto(URL["Object List Setup"], wait_until="domcontentloaded", timeout=45000)
    try:
        page.wait_for_load_state("networkidle", timeout=20000)
    except Exception:
        pass
    page.wait_for_timeout(1500)
    try:
        pick(page, "nav:form:G:1:R:1:C:0:dd", "FIN_ACCOUNT")
        pick(page, "nav:form:G:2:R:1:C:0:dd", "OPEX GL Equipment Rental")
        page.click("[id='button:form:B']")
        try:
            page.wait_for_load_state("networkidle", timeout=15000)
        except Exception:
            pass
        page.wait_for_timeout(2000)
        page.screenshot(path=str(SHOTS / "phaseb_OLS_after_go.png"))
        grids = page.evaluate(GRID_JS)
        print("  grids after GO:", json.dumps(grids)[:900])
        # open Insert > Object List Item
        page.hover("xpath=//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'ui-icon-insert')]]")
        item = page.locator("xpath=//ul[contains(@class,'ui-menu-child')]//li//a[normalize-space(.)='Object List Item']")
        item.wait_for(state="visible", timeout=8000)
        item.click()
        page.wait_for_timeout(2000)
        page.screenshot(path=str(SHOTS / "phaseb_OLS_insert_row.png"))
        print("  row inputs after Insert:", json.dumps(page.evaluate(ROW_INPUTS_JS))[:900])
    except Exception as e:
        print("  ERR:", str(e)[:200])
    ctx.close()
    b.close()
print("confirm probe done (READ-ONLY, nothing saved)")
