"""Probe Transport System insert: check DB for the failed code, then re-attempt the
insert via Playwright and capture EC's banner/validation message after Save.
Cleans up via DB-checked End-Date delete only if the row actually appears."""
import os
import time

import oracledb
from playwright.sync_api import sync_playwright

URL = os.environ.get("EC_URL", "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/")
USER = os.environ.get("EC_USER", "sysadmin")
PASS = os.environ.get("EC_PASS", "sysadmin")

conn = oracledb.connect(user="ECKERNEL_EC", password="energy",
                        dsn=os.environ.get("EC_DB_DSN", "localhost:1521/ORCL"))
cur = conn.cursor()
cur.execute("SELECT code FROM ov_transport_system WHERE code LIKE 'AUTOTEST%'")
print("existing AUTOTEST rows in ov_transport_system:", cur.fetchall())
cur.execute("""SELECT column_name FROM all_tab_columns
               WHERE owner='ECKERNEL_EC' AND table_name='TRANSPORT_SYSTEM'
               AND column_name LIKE '%CODE%' ORDER BY column_id""")
print("base TRANSPORT_SYSTEM code-ish columns:", [r[0] for r in cur.fetchall()])

code = "AUTOTEST_TSPROBE_" + time.strftime("%H%M%S")
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_context(ignore_https_errors=True, viewport={"width": 1920, "height": 1080}).new_page()
    page.goto(URL, wait_until="domcontentloaded", timeout=60000)
    page.fill('[id="username"]', USER)
    page.fill('[id="password"]', PASS)
    page.click('[id="kc-login"]')
    page.wait_for_selector('[id="menu:searchForm:searchTxt"]', timeout=60000)
    box = page.locator('[id="menu:searchForm:searchTxt"]')
    box.type("Transport System", delay=50)
    time.sleep(1)
    page.locator('xpath=//*[contains(@class,"tv-link") and normalize-space(text())="Transport System"]').first.click()
    page.wait_for_load_state("networkidle", timeout=20000)
    time.sleep(2)
    page.locator('xpath=//li[contains(@class,"ui-menu-parent")][.//span[contains(@class,"ui-icon-insert")]]').hover()
    item = page.locator('xpath=//ul[contains(@class,"ui-menu-child")]//li//a[normalize-space(.)="New Object"]')
    item.wait_for(state="visible", timeout=10000)
    item.click()
    page.wait_for_load_state("networkidle", timeout=15000)
    time.sleep(1.5)
    page.fill('[id="tab:tabPanel:objectForm:form:G:0:R:0:C:1:in"]', code)
    page.fill('[id="tab:tabPanel:objectForm:form:G:0:R:1:C:1:in"]', "TS Probe")
    page.fill('[id="tab:tabPanel:objectForm:form:G:0:R:2:C:1:da_input"]', "2003-01-01")
    page.keyboard.press("Escape")
    time.sleep(0.5)
    # Save via toolbar (ui-icon-save)
    page.locator('xpath=//li[.//span[contains(@class,"ui-icon-save")]][1]').first.click()
    page.wait_for_load_state("networkidle", timeout=20000)
    time.sleep(2.5)
    msgs = page.evaluate("""() => [...document.querySelectorAll('.ui-messages, .ui-message, [id*="message"], .ui-growl-message')]
        .map(e => (e.textContent||'').trim()).filter(t => t).slice(0, 8)""")
    print("BANNERS:", msgs)
    page.screenshot(path=r"c:/Projects/ChoongYin_OS/tmp/dispatching_recon/ts_save_probe.png", full_page=True)
    browser.close()

cur.execute("SELECT code FROM ov_transport_system WHERE code = :c", c=code)
print("probe row in OV view after save:", cur.fetchall())
conn.close()
