"""Dump the first rows of the Contract Area grid (manageObject:form:T_data) to see which COLUMN holds the
code (the RF Row Exists first-cell check failed). READ-ONLY. py -X utf8 tmp/scripts/ca_grid_cols.py"""
import os
from playwright.sync_api import sync_playwright

EC_URL = os.environ.get("EC_URL", "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/")
USER, PWD = os.environ.get("EC_USER", "sysadmin"), os.environ.get("EC_PWD", "sysadmin")


def esc(i):
    return "#" + i.replace(":", "\\:")


with sync_playwright() as p:
    b = p.chromium.launch(headless=True, args=["--ignore-certificate-errors"])
    page = b.new_context(ignore_https_errors=True, viewport={"width": 1700, "height": 1000}).new_page()
    page.goto(EC_URL, wait_until="domcontentloaded", timeout=60000); page.wait_for_timeout(2500)
    page.fill("#username", USER); page.fill("#password", PWD); page.locator("#kc-login").first.click()
    page.wait_for_timeout(3500)
    box = page.locator(esc("menu:searchForm:searchTxt")); box.click(); box.type("Contract Area", delay=40)
    page.wait_for_timeout(2200)
    page.locator("xpath=//*[contains(@class,'tv-link') and normalize-space(text())='Contract Area']").first.click()
    page.wait_for_load_state("networkidle", timeout=20000); page.wait_for_timeout(1500)
    # nav BU = ECP Norway
    page.locator(esc("nav:form:G:0:R:1:C:1:dd_button")).first.click(); page.wait_for_timeout(1000)
    page.locator("xpath=//*[@id='nav:form:G:0:R:1:C:1:dd_panel']//tr[normalize-space(@data-item-label)='ECP Norway']").first.click()
    page.wait_for_load_state("networkidle", timeout=15000); page.wait_for_timeout(800)
    page.locator(esc("button:form:B")).first.click()
    page.wait_for_load_state("networkidle", timeout=20000); page.wait_for_timeout(1200)

    # column headers
    heads = page.evaluate("""() => { const h=document.querySelector("[id='manageObject:form'] thead, #manageObject\\\\:form thead");
        const ths=[...document.querySelectorAll("th")].filter(t=>t.offsetParent).map(t=>(t.innerText||'').trim()).filter(Boolean);
        return ths.slice(0,12); }""")
    print("visible TH labels:", heads)
    rows = page.evaluate("""() => { const t=document.getElementById('manageObject:form:T_data'); if(!t) return [];
        const o=[]; t.querySelectorAll('tr').forEach(tr=>{const c=[];tr.querySelectorAll('td').forEach(td=>c.push((td.textContent||'').trim()));
            if(c.some(x=>x)) o.push(c);}); return o.slice(0,3); }""")
    for i, r in enumerate(rows):
        print(f"row{i} cells:", r)
    b.close()
print("DONE")
