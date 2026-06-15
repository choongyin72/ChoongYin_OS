"""READ-ONLY decisive recon: FA=EC -> read Message Type options -> pick freetext -> Subject -> GO ->
dump the compose panel (template:form): body field + any distribution/recipient selector. NO Send click."""
import time
import json
from playwright.sync_api import sync_playwright

URL = "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"
SCREEN = "Send Freetext Message"


def pick(fr, dd, label):
    fr.click(f'[id="{dd}_button"]', timeout=5000)
    time.sleep(0.6)
    fr.click(f'xpath=//*[@id="{dd}_panel"]//*[normalize-space(@data-item-label)="{label}"]', timeout=5000)
    time.sleep(1.0)


def panel_opts(fr, dd):
    fr.click(f'[id="{dd}_button"]', timeout=5000)
    time.sleep(0.7)
    res = fr.evaluate(
        """(pid)=>{const p=document.getElementById(pid); if(!p) return null;
           return [...p.querySelectorAll('li,tr')].map(r=>r.getAttribute('data-item-label')).filter(Boolean).slice(0,40);}""",
        dd + "_panel",
    )
    time.sleep(0.3)
    return res


with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    page = b.new_context(ignore_https_errors=True, viewport={"width": 1680, "height": 1000}).new_page()
    page.goto(URL, wait_until="domcontentloaded", timeout=60000)
    page.fill('[id="username"]', "sysadmin")
    page.fill('[id="password"]', "sysadmin")
    page.click('[id="kc-login"]')
    page.wait_for_selector('[id="menu:searchForm:searchTxt"]', timeout=60000)
    time.sleep(1.0)
    page.locator('[id="menu:searchForm:searchTxt"]').type(SCREEN, delay=25)
    time.sleep(1.2)
    page.locator(f'xpath=//*[contains(@class,"tv-link") and normalize-space(text())="{SCREEN}"]').first.click()
    page.wait_for_load_state("networkidle", timeout=30000)
    time.sleep(2.5)
    fr = next((f for f in page.frames if "dashboard.jsf" in (f.url or "") and "top=false" in (f.url or "")), None) or page

    FA = "nav:form:G:0:R:1:C:1:dd"
    MT = "nav:form:G:0:R:1:C:2:dd"
    print("pick FA=EC ...")
    pick(fr, FA, "EC")
    print("Message Type options under FA=EC:", json.dumps(panel_opts(fr, MT)))

    b.close()
print("DONE")
