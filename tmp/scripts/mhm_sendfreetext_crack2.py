"""Read-only crack of the 'Send Freetext Message' screen — nav/forms + Send button + field ids.
NO message is sent (pure recon). Mirrors EC's SendFreetextMessagePage (nav form + template form +
SendButton)."""
import time, json
from playwright.sync_api import sync_playwright

URL = "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"
SCREEN = "Send Freetext Message"

JS = r"""
() => {
  const forms = [...new Set([...document.querySelectorAll('[id*=":form"]')]
      .map(e => e.id.split(':form')[0] + ':form'))].slice(0, 14);
  const btns = [...document.querySelectorAll('a[title], button, [id*="Send"], [id*="Button"]')]
      .map(e => ({ id: e.id, t: (e.textContent || e.title || '').trim().slice(0, 22) }))
      .filter(x => x.id && /send|button|go|ok|transmit/i.test(x.id + ' ' + x.t)).slice(0, 18);
  const flds = [...document.querySelectorAll('input, textarea, [id$="dd"], [id$="dd_input"]')]
      .map(e => e.id).filter(i => i && !/ViewState|searchForm|tvForm|favorite|treeView/.test(i)).slice(0, 30);
  return { forms, btns, flds };
}
"""

with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    page = b.new_context(ignore_https_errors=True, viewport={"width": 1680, "height": 1000}).new_page()
    page.goto(URL, wait_until="domcontentloaded", timeout=60000)
    page.fill('[id="username"]', "sysadmin"); page.fill('[id="password"]', "sysadmin"); page.click('[id="kc-login"]')
    page.wait_for_selector('[id="menu:searchForm:searchTxt"]', timeout=60000); time.sleep(1.0)
    page.locator('[id="menu:searchForm:searchTxt"]').type(SCREEN, delay=25); time.sleep(1.2)
    sel = f'xpath=//*[contains(@class,"tv-link") and normalize-space(text())="{SCREEN}"]'
    page.wait_for_selector(sel, timeout=12000); page.locator(sel).first.click()
    page.wait_for_load_state("networkidle", timeout=30000); time.sleep(2.5)
    fr = next((f for f in page.frames if "dashboard.jsf" in (f.url or "") and "top=false" in (f.url or "")), None) or page
    info = fr.evaluate(JS)
    print("forms:", json.dumps(info["forms"]))
    print("send/buttons:", json.dumps(info["btns"]))
    print("fields:", json.dumps(info["flds"]))
    b.close()
print("DONE")
