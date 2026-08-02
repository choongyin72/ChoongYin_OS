"""READ-ONLY: open Production Unit, open New Object form, dump every element id
+ text under the objectForm grid to learn the label id pattern."""
import os
import json
from playwright.sync_api import sync_playwright

EC_URL = "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"
URL = EC_URL.rstrip("/") + "/com.ec.frmw.co.screens/manage_object_nav/CLASS_NAME/PRODUCTIONUNIT"

JS = r"""() => {
    const out = [];
    document.querySelectorAll("[id^='tab:tabPanel:objectForm:form:']").forEach(el => {
        const txt = (el.childNodes.length && el.children.length === 0) ? (el.textContent || '').trim() : '';
        out.push({id: el.id, tag: el.tagName, cls: (el.className || '').toString().substring(0, 30), text: txt.substring(0, 40)});
    });
    return out.slice(0, 120);
}"""

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
    item = page.locator("xpath=//ul[contains(@class,'ui-menu-child')]//li//a[normalize-space(.)='New Object']")
    item.wait_for(state="visible", timeout=8000)
    item.click()
    page.wait_for_timeout(2000)
    for e in page.evaluate(JS):
        if e["text"] or ":R:" in e["id"]:
            print(f"{e['tag']:6s} {e['id'].replace('tab:tabPanel:objectForm:form:',''):34s} {e['cls']:30s} {e['text']}")
    ctx.close()
    b.close()
