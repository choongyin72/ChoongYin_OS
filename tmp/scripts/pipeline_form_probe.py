"""Pipeline insert-form probe: fill trio, then inspect/pick the Op Production Unit dd
(R21) — verify the selection actually commits to the input. NO SAVE."""
import os
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

URL = os.environ.get("EC_URL", "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/")
OUT = Path(r"c:/Projects/ChoongYin_OS/tmp/dispatching_recon")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_context(ignore_https_errors=True, viewport={"width": 1920, "height": 1080}).new_page()
    page.goto(URL, wait_until="domcontentloaded", timeout=60000)
    page.fill('[id="username"]', "sysadmin")
    page.fill('[id="password"]', "sysadmin")
    page.click('[id="kc-login"]')
    page.wait_for_selector('[id="menu:searchForm:searchTxt"]', timeout=60000)
    box = page.locator('[id="menu:searchForm:searchTxt"]')
    box.type("Pipeline", delay=50)
    time.sleep(1.2)
    page.locator('xpath=//*[contains(@class,"tv-link") and normalize-space(text())="Pipeline"]').first.click()
    page.wait_for_load_state("networkidle", timeout=20000)
    time.sleep(2)
    page.locator('xpath=//li[contains(@class,"ui-menu-parent")][.//span[contains(@class,"ui-icon-insert")]]').hover()
    item = page.locator('xpath=//ul[contains(@class,"ui-menu-child")]//li//a[normalize-space(.)="New Object" and contains(@onclick,"insert")]')
    item.wait_for(state="visible", timeout=10000)
    item.click()
    page.wait_for_load_state("networkidle", timeout=15000)
    time.sleep(1.5)
    # dump ALL form labels + row of each dd (fresh truth, not recon-cache)
    rows = page.evaluate("""() => {
        const out = [];
        document.querySelectorAll('[id^="tab:tabPanel:objectForm:form:G:0:R:"]').forEach(e => {
            const m = e.id.match(/R:(\\d+):C:(\\d+):(la|dd|in|da_input|cb)$/);
            if (!m) return;
            if (m[3] === 'la') { out.push([+m[1], 'label', (e.textContent||'').trim().slice(0,30)]); }
            else if (m[2] === '1') { out.push([+m[1], m[3], e.id]); }
        });
        return out.sort((a,b) => a[0]-b[0]); }""")
    for r in rows:
        if r[1] == "label" and r[2]:
            print(r)
    # fill trio
    page.fill('[id="tab:tabPanel:objectForm:form:G:0:R:2:C:1:in"]', "AUTOTEST_PROBE")
    page.fill('[id="tab:tabPanel:objectForm:form:G:0:R:3:C:1:in"]', "Probe")
    page.fill('[id="tab:tabPanel:objectForm:form:G:0:R:5:C:1:da_input"]', "2003-01-01")
    page.keyboard.press("Escape")
    time.sleep(1.5)
    dd = "tab:tabPanel:objectForm:form:G:0:R:21:C:1:dd"
    page.click(f'[id="{dd}_button"]')
    try:
        page.wait_for_selector(f'[id="{dd}_panel"] tr[data-item-label]', timeout=8000)
        opts = page.evaluate(f"""() => [...document.querySelectorAll('[id="{dd}_panel"] tr[data-item-label]')]
            .map(tr => tr.getAttribute('data-item-label')).slice(0, 8)""")
        print("R21 dd options:", opts)
        page.locator(f'[id="{dd}_panel"] tr[data-item-label="P1 Production Unit"]').first.click()
        page.wait_for_load_state("networkidle", timeout=12000)
        time.sleep(1.5)
        val = page.evaluate(f"""() => {{ const e = document.querySelector('[id="{dd}_input"]');
            const h = document.querySelector('[id="{dd}_hinput"]');
            return {{input: e ? e.value : None, hidden: h ? h.value : null}}; }}""".replace("None", "null"))
        print("after pick:", val)
    except Exception as e:
        print("R21 dd failed:", str(e)[:150])
    page.screenshot(path=str(OUT / "pipeline_form_probe.png"), full_page=True)
    browser.close()
