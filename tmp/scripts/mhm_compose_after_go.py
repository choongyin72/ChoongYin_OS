"""READ-ONLY: FA=EC -> MT='FRMW Test Msg 1 for message body' -> Subject -> GO (button:form:B) ->
dump the compose area: ALL dropdowns (id + selected text + panel options), textareas/inputs, and any
text mentioning a distribution/recipient. Determines whether the SAFE distribution can be chosen here.
NO Send click (stops before SendButton:form)."""
import time
import json
from playwright.sync_api import sync_playwright

URL = "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"
SCREEN = "Send Freetext Message"
MT_LABEL = "FRMW Test Msg 1 for message body"


def pick(fr, dd, label):
    fr.click(f'[id="{dd}_button"]', timeout=5000)
    time.sleep(0.6)
    fr.click(f'xpath=//*[@id="{dd}_panel"]//*[normalize-space(@data-item-label)="{label}"]', timeout=5000)
    time.sleep(1.2)


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
    # Subject (C:4) — type a value into its input if present
    try:
        fr.fill('[id="nav:form:G:0:R:1:C:4:dd_input"]', "AUTOTEST recon")
    except Exception:
        pass
    time.sleep(0.4)
    print("clicking GO (button:form:B) ...")
    fr.click('[id="button:form:B"]', timeout=8000)
    page.wait_for_load_state("networkidle", timeout=30000)
    time.sleep(2.0)

    dump = fr.evaluate(
        r"""() => {
          const ddTriggers = [...document.querySelectorAll('[id$=":dd"]')].map(e=>({
              id:e.id, sel:(document.getElementById(e.id+'_input')||{}).value || (e.textContent||'').trim().slice(0,40)}));
          const areas = [...document.querySelectorAll('textarea,input[type=text]')].map(e=>({id:e.id, val:(e.value||'').slice(0,30)}));
          const formIds = [...new Set([...document.querySelectorAll('[id*=":form"]')].map(e=>e.id.split(':form')[0]+':form'))];
          const bodyText = document.body.innerText;
          const distMention = /distribution|recipient|receiver|free.?text/i.test(bodyText);
          return {ddTriggers, areas: areas.slice(0,40), formIds, distMention};
        }"""
    )
    print("\nFORMS:", json.dumps(dump["formIds"]))
    print("\nDROPDOWNS (id / selected):", json.dumps(dump["ddTriggers"], indent=1))
    print("\nTEXT FIELDS:", json.dumps(dump["areas"], indent=1))
    print("\nmentions distribution/recipient:", dump["distMention"])
    fr.evaluate("()=>0")
    # screenshot for the eye
    page.screenshot(path="C:/Projects/ChoongYin_OS/tmp/mhm_compose_after_go.png", full_page=True)
    b.close()
print("DONE")
