"""Replicate the OLS item insert exactly as the suite does, Save, and capture:
EC messages/banner, the new row's cell states (mandatory/yellow), screenshot.
If the save unexpectedly SUCCEEDS, delete the row again (leave no trace)."""
import os
import json
from pathlib import Path

from playwright.sync_api import sync_playwright

EC_URL = "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"
_scan = json.loads(Path(r"c:/Projects/ChoongYin_OS/tmp/screen_scan/assets_scan.json").read_text(encoding="utf-8"))
URL = next(r["url"] for r in _scan.values()
           if r.get("section") == "Basic Objects" and r["screen"] == "Object List Setup")
GRID = "tab:tabPanel:object_list_table:form:T_data"
PREFIX = "tab:tabPanel:object_list_table:form:T"

CELLS_JS = r"""(args) => {
    const [grid, row] = args;
    const t = document.getElementById(grid);
    const out = [];
    t.querySelectorAll("[id^='" + 'tab:tabPanel:object_list_table:form:T:' + row + ":']").forEach(e => {
        if (e.offsetParent === null) return;
        const st = window.getComputedStyle(e);
        out.push({id: e.id.split(':').pop(), tag: e.tagName, val: (e.value || '').substring(0, 20),
                  bg: st.backgroundColor, mand: ((e.className || '') + (e.title || '')).includes('mandatory:true')});
    });
    return out;
}"""

MSG_JS = r"""() => {
    const out = [];
    document.querySelectorAll('.ui-messages, .ui-message, [id*="messages" i], .ui-growl-message, [id*="rror" i], [id*="arning" i]').forEach(e => {
        const t = (e.textContent || '').trim();
        if (t) out.push(t.substring(0, 250));
    });
    return out.slice(0, 8);
}"""


def pick(page, dd, val):
    page.click(f"[id='{dd}_button']")
    page.wait_for_selector(f"[id='{dd}_panel'] tr[data-item-label]", state="visible", timeout=10000)
    page.click(f"[id='{dd}_panel'] tr[data-item-label='{val}']")
    page.wait_for_timeout(1500)


with sync_playwright() as p:
    b = p.chromium.launch(headless=True, args=["--ignore-certificate-errors"])
    ctx = b.new_context(ignore_https_errors=True, viewport={"width": 1680, "height": 1200})
    page = ctx.new_page()
    page.goto(EC_URL, wait_until="domcontentloaded", timeout=45000)
    page.fill("#username", os.environ.get("EC_USER", "sysadmin"))
    page.fill("#password", os.environ.get("EC_PASS", "sysadmin"))
    page.click("#kc-login")
    page.wait_for_url("**/dashboard**", timeout=60000)
    page.wait_for_timeout(1500)
    page.goto(URL, wait_until="domcontentloaded", timeout=45000)
    page.wait_for_timeout(2000)
    pick(page, "nav:form:G:1:R:1:C:0:dd", "FIN_ACCOUNT")
    pick(page, "nav:form:G:2:R:1:C:0:dd", "OPEX GL Equipment Rental")
    page.click("[id='button:form:B']")
    page.wait_for_timeout(2500)

    page.hover("xpath=//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'ui-icon-insert')]]")
    item = page.locator("xpath=//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'ui-icon-insert')]]//ul//a[normalize-space(.)='Object List Item']")
    item.wait_for(state="visible", timeout=8000)
    item.click()
    page.wait_for_timeout(2500)

    # blank row index
    row = page.evaluate(
        "(g) => { const t=document.getElementById(g); for (const e of t.querySelectorAll(\"input[id$='C2_dd_input']\")) { if(!(e.value||'')) { const m=e.id.match(/:T:(\\d+):/); if(m) return +m[1]; } } return -1; }",
        GRID)
    print("blank row:", row)
    print("cells BEFORE fill:", json.dumps(page.evaluate(CELLS_JS, [GRID, row]))[:900])

    pick(page, f"{PREFIX}:{row}:C2_dd", "6931250")
    row = page.evaluate(
        "(g) => { const t=document.getElementById(g); for (const e of t.querySelectorAll(\"input[id$='C2_dd_input']\")) { if((e.value||'')==='6931250') { const m=e.id.match(/:T:(\\d+):/); if(m) return +m[1]; } } return -1; }",
        GRID)
    print("row after select:", row)
    # date cell
    has_cal = page.locator(f"[id='{PREFIX}:{row}:C0_da_input']").count()
    if has_cal:
        page.fill(f"[id='{PREFIX}:{row}:C0_da_input']", "2003-01-01")
        page.keyboard.press("Tab")
    else:
        page.click(f"[id='{PREFIX}:{row}:C0_in']")
        page.type(f"[id='{PREFIX}:{row}:C0_in']", "2003-01-01", delay=40)
        page.keyboard.press("Tab")
    page.wait_for_timeout(1200)
    print("cells AFTER fill:", json.dumps(page.evaluate(CELLS_JS, [GRID, row]))[:900])

    page.click("xpath=//a[@title='Save [Ctrl+s]' and not(contains(@class,'ui-state-disabled'))]")
    page.wait_for_timeout(2500)
    print("messages after Save:", page.evaluate(MSG_JS))
    page.screenshot(path=r"c:/Projects/ChoongYin_OS/tmp/screen_scan/shots/probe_ols_save.png")
    ctx.close()
    b.close()
print("done")
