"""READ-ONLY: open Area's New Object form, click the Op Production Unit dropdown,
dump the panel's innerHTML/innerText after a generous wait."""
import os
import json
from pathlib import Path

from playwright.sync_api import sync_playwright

EC_URL = "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"
_scan = json.loads(Path(r"c:/Projects/ChoongYin_OS/tmp/screen_scan/assets_scan.json").read_text(encoding="utf-8"))
URL = next(r["url"] for r in _scan.values()
           if r.get("section") == "Basic Objects" and r["screen"] == "Area")
DD = "tab:tabPanel:objectForm:form:G:0:R:7:C:1:dd"

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
    page.wait_for_timeout(2500)
    page.hover("xpath=//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'ui-icon-insert')]]")
    item = page.locator("xpath=//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'ui-icon-insert')]]//ul//a[normalize-space(.)='New Object']")
    item.wait_for(state="visible", timeout=8000)
    item.click()
    page.wait_for_timeout(2000)
    page.click(f"[id='{DD}_button']")
    page.wait_for_timeout(3500)
    info = page.evaluate("""(dd) => {
        const panel = document.getElementById(dd + '_panel');
        if (!panel) return {exists: false};
        return {exists: true, visible: panel.offsetParent !== null,
                text: panel.innerText.trim().substring(0, 500),
                html: panel.innerHTML.substring(0, 800)};
    }""", DD)
    print(json.dumps(info, indent=1)[:1500])
    page.screenshot(path=r"c:/Projects/ChoongYin_OS/tmp/screen_scan/shots/probe_area_op_pu.png")
    ctx.close()
    b.close()
