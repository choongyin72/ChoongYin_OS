"""Meter form: probe the Delivery Point POPUP PICKER (pin/pinB cells) — click pinB,
dump the dialog structure (the new T2 gesture to learn). NO SAVE."""
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
    box.type("Meter", delay=50)
    time.sleep(1.2)
    page.locator('xpath=//*[contains(@class,"tv-link") and normalize-space(text())="Meter"]').first.click()
    page.wait_for_load_state("networkidle", timeout=20000)
    time.sleep(2)
    page.locator('xpath=//li[contains(@class,"ui-menu-parent")][.//span[contains(@class,"ui-icon-insert")]]').hover()
    item = page.locator('xpath=//ul[contains(@class,"ui-menu-child")]//li//a[normalize-space(.)="New Object" and contains(@onclick,"insert")]')
    item.wait_for(state="visible", timeout=10000)
    item.click()
    page.wait_for_load_state("networkidle", timeout=15000)
    time.sleep(1.5)
    page.fill('[id="tab:tabPanel:objectForm:form:G:0:R:2:C:1:da_input"]', "2003-01-01")
    page.keyboard.press("Escape")
    time.sleep(1)
    # the Delivery Point picker cells: ...R:5:C:1:pin (text) + pinB (button)
    pin = page.evaluate("""() => [...document.querySelectorAll('[id^="tab:tabPanel:objectForm:form:G:0:R:5:"]')]
        .map(e => ({id: e.id, tag: e.tagName}))""")
    print("R5 cells:", pin)
    try:
        with page.expect_popup(timeout=10000) as pop_info:
            page.click('[id="tab:tabPanel:objectForm:form:G:0:R:5:C:1:pinB"]')
        pop = pop_info.value
        pop.wait_for_load_state("domcontentloaded", timeout=20000)
        time.sleep(3)
        info = pop.evaluate("""() => ({url: location.href.slice(0,120),
            grids: [...document.querySelectorAll('tbody[id]')].map(t => ({id: t.id, rows: t.querySelectorAll('tr').length})).slice(0,5),
            inputs: [...document.querySelectorAll('input')].map(i => i.id).filter(Boolean).slice(0,10),
            btns: [...document.querySelectorAll('button, a')].map(b => (b.textContent||'').trim()).filter(t => t && t.length<20).slice(0,10)})""")
        print('POPUP WINDOW:', info)
        pop.screenshot(path=str(OUT / 'meter_popup_window.png'), full_page=True)
        pop.close()
    except Exception as e:
        print('no popup window:', str(e)[:120])
        page.wait_for_load_state('networkidle', timeout=15000)
        time.sleep(2.5)
    dlg = page.evaluate("""() => {
      const vis = e => e && e.offsetParent !== null;
      const dialogs = [...document.querySelectorAll('.ui-dialog')].filter(vis)
        .map(d => ({id: d.id, title: (d.querySelector('.ui-dialog-title')||{}).textContent}));
      const grids = [...document.querySelectorAll('.ui-dialog tbody[id]')].filter(vis)
        .map(t => ({id: t.id, rows: t.querySelectorAll('tr').length}));
      const inputs = [...document.querySelectorAll('.ui-dialog input')].filter(vis)
        .map(i => i.id).slice(0, 10);
      const btns = [...document.querySelectorAll('.ui-dialog button, .ui-dialog a.ui-button')].filter(vis)
        .map(b => ({id: b.id, t: (b.textContent||'').trim().slice(0,20)})).slice(0, 8);
      return {dialogs, grids, inputs, btns}; }""")
    print("popup:", dlg)
    page.screenshot(path=str(OUT / "meter_popup.png"), full_page=True)
    browser.close()
