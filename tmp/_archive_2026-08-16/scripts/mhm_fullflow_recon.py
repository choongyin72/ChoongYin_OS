"""READ-ONLY full-flow recon of Send Freetext Message: dump Functional Area (C:1), Message Type (C:2),
Subject (C:4) dropdown options; then fill FA+Type+Subject, click GO, and dump the compose panel
(recipient/distribution selector + body field). NO send (we stop before any Send click)."""
import time
import json
from playwright.sync_api import sync_playwright

URL = "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"
SCREEN = "Send Freetext Message"


def options(fr, dd):
    """Open a primefaces dropdown via its _button and read its _panel options."""
    try:
        fr.click(f'[id="{dd}_button"]', timeout=4000)
    except Exception as e:
        return {"dd": dd, "err": str(e)[:70]}
    time.sleep(0.6)
    res = fr.evaluate(
        """(pid)=>{const p=document.getElementById(pid); if(!p) return null;
           return [...p.querySelectorAll('li,tr')].map(r=>({label:r.getAttribute('data-item-label'),
             text:(r.textContent||'').trim().slice(0,40)})).filter(o=>o.label||o.text).slice(0,30);}""",
        dd + "_panel",
    )
    try:
        fr.keyboard.press("Escape")
    except Exception:
        pass
    time.sleep(0.3)
    return {"dd": dd, "options": res}


def pick(fr, dd, label):
    fr.click(f'[id="{dd}_button"]', timeout=4000)
    time.sleep(0.5)
    fr.click(f'xpath=//*[@id="{dd}_panel"]//*[normalize-space(@data-item-label)="{label}"]', timeout=4000)
    time.sleep(0.6)


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

    print("FUNCTIONAL AREA (C:1):", json.dumps(options(fr, "nav:form:G:0:R:1:C:1:dd")))
    print("\nMESSAGE TYPE (C:2):", json.dumps(options(fr, "nav:form:G:0:R:1:C:2:dd")))
    print("\nSUBJECT (C:4):", json.dumps(options(fr, "nav:form:G:0:R:1:C:4:dd")))

    # try to drive: date, then Message Type = first freetext-looking option, then GO, dump compose
    try:
        page  # date
        fr.fill('[id="nav:form:G:0:R:1:C:0:da_input"]', "2024-02-06")
        time.sleep(0.3)
        # GO via the navigator button — find a button id
        btns = fr.evaluate(
            """()=>[...document.querySelectorAll('button,[id*="Button"],a[title]')]
                 .map(e=>({id:e.id,t:(e.textContent||e.title||'').trim().slice(0,20)}))
                 .filter(x=>x.id && /go|button|ok|search|apply/i.test(x.id+' '+x.t)).slice(0,15)"""
        )
        print("\nBUTTONS:", json.dumps(btns))
    except Exception as e:
        print("drive err:", str(e)[:120])

    b.close()
print("DONE")
