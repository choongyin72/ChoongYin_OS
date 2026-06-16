"""READ-ONLY: FA=EC -> MT -> open Subject popup (C:4) and screenshot it -> fill a subject -> GO ->
screenshot + dump the compose body (template:form) incl. any editable recipient field. NO Send click."""
import time
import json
from playwright.sync_api import sync_playwright

URL = "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"
SCREEN = "Send Freetext Message"
MT_LABEL = "FRMW Test Msg 1 for message body"
SHOT = "C:/Projects/ChoongYin_OS/tmp/"


def pick(fr, dd, label):
    fr.click(f'[id="{dd}_button"]', timeout=5000)
    time.sleep(0.6)
    fr.click(f'xpath=//*[@id="{dd}_panel"]//*[normalize-space(@data-item-label)="{label}"]', timeout=5000)
    time.sleep(1.0)


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

    pick(fr, "nav:form:G:0:R:1:C:1:dd", "EC")
    pick(fr, "nav:form:G:0:R:1:C:2:dd", MT_LABEL)

    # open the Subject popup
    try:
        fr.click('[id="nav:form:G:0:R:1:C:4:dd_button"]', timeout=5000)
        time.sleep(1.2)
    except Exception as e:
        print("subject button err:", str(e)[:80])
    page.screenshot(path=SHOT + "mhm_subject_popup.png")
    # dump any dialog/popup content + inputs
    dlg = fr.evaluate(
        r"""()=>{
          const dialogs=[...document.querySelectorAll('[role=dialog],.ui-dialog,[id*=Popup],[id*=popup]')]
            .filter(d=>d.offsetParent!==null).map(d=>({id:d.id, txt:(d.innerText||'').slice(0,200)}));
          const inputs=[...document.querySelectorAll('input[type=text],textarea')]
            .filter(e=>e.offsetParent!==null).map(e=>({id:e.id})).slice(0,40);
          const opts=[...document.querySelectorAll('[data-item-label]')].filter(e=>e.offsetParent!==null)
            .map(e=>e.getAttribute('data-item-label')).slice(0,30);
          return {dialogs, inputs, opts};
        }"""
    )
    print("SUBJECT POPUP dialogs:", json.dumps(dlg["dialogs"], indent=1)[:1200])
    print("\nvisible inputs:", json.dumps(dlg["inputs"]))
    print("\nvisible data-item-labels:", json.dumps(dlg["opts"]))
    b.close()
print("DONE")
