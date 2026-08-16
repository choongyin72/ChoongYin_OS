"""READ-ONLY: full nav (FA=EC, MT, Subject='Testing of Message Body') -> GO -> screenshot + dump the
compose body (template:form): body editor + any recipient/distribution field + the Send button.
NO Send click (stops before SendButton:form)."""
import time
import json
from playwright.sync_api import sync_playwright

URL = "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"
SCREEN = "Send Freetext Message"
MT_LABEL = "FRMW Test Msg 1 for message body"
SUBJECT = "Testing of Message Body"
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
    pick(fr, "nav:form:G:0:R:1:C:4:dd", SUBJECT)
    time.sleep(0.5)
    fr.click('[id="button:form:B"]', timeout=8000)
    page.wait_for_load_state("networkidle", timeout=30000)
    time.sleep(2.5)
    page.screenshot(path=SHOT + "mhm_compose_body.png", full_page=True)

    dump = fr.evaluate(
        r"""()=>{
          const vis = e => e.offsetParent!==null;
          const inTemplate = id => id && id.startsWith('template:form');
          const fields=[...document.querySelectorAll('input,textarea,[contenteditable=true],iframe')]
            .filter(vis).map(e=>({id:e.id, tag:e.tagName, type:e.type||'', name:e.name||'',
              val:(e.value||e.textContent||'').slice(0,40)}));
          const tmplFields = fields.filter(f=>inTemplate(f.id));
          const ddInTmpl = [...document.querySelectorAll('[id^="template:form"][id$=":dd"]')].filter(vis)
            .map(e=>({id:e.id, sel:(document.getElementById(e.id+'_input')||{}).value||''}));
          const labels=[...document.querySelectorAll('[id^="template:form"]')].filter(vis)
            .filter(e=>/recipient|to|distribution|receiver|address|mail/i.test(e.textContent||''))
            .map(e=>({id:e.id, t:(e.textContent||'').trim().slice(0,30)})).slice(0,20);
          return {tmplFieldCount: tmplFields.length, tmplFields: tmplFields.slice(0,30),
                  ddInTmpl, recipientLabels: labels, allVisFieldCount: fields.length};
        }"""
    )
    print("template:form field count:", dump["tmplFieldCount"])
    print("template:form fields:", json.dumps(dump["tmplFields"], indent=1))
    print("\ntemplate dropdowns:", json.dumps(dump["ddInTmpl"]))
    print("\nrecipient-ish labels in template:", json.dumps(dump["recipientLabels"]))
    b.close()
print("DONE")
