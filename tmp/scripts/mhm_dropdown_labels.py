"""READ-ONLY: open Send Freetext Message, open the Message Type (C:1) + Distribution (C:2) nav
dropdowns and dump each option's data-item-label + visible text, so the suite uses the EXACT labels.
NO send. Confirms AUTOTEST_FREETEXT_INVALID is selectable too."""
import time
import json
from playwright.sync_api import sync_playwright

URL = "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"
SCREEN = "Send Freetext Message"


def dump_panel(fr, dd_id):
    # click the dropdown trigger to render its panel, then read options
    try:
        fr.click(f'[id="{dd_id}"]', timeout=5000)
    except Exception as e:
        return {"error": f"click {dd_id}: {str(e)[:80]}"}
    time.sleep(0.8)
    js = """
    (panelId) => {
      const p = document.getElementById(panelId);
      if (!p) return {panel: panelId, found: false};
      const rows = [...p.querySelectorAll('[data-item-label], li, tr')]
        .map(r => ({label: r.getAttribute('data-item-label'), text: (r.textContent||'').trim().slice(0,40)}))
        .filter(o => o.label || o.text);
      return {panel: panelId, found: true, options: rows.slice(0, 40)};
    }
    """
    res = fr.evaluate(js, dd_id + "_panel")
    # close panel
    try:
        fr.keyboard.press("Escape")
    except Exception:
        pass
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
    sel = f'xpath=//*[contains(@class,"tv-link") and normalize-space(text())="{SCREEN}"]'
    page.wait_for_selector(sel, timeout=12000)
    page.locator(sel).first.click()
    page.wait_for_load_state("networkidle", timeout=30000)
    time.sleep(2.5)
    fr = next((f for f in page.frames if "dashboard.jsf" in (f.url or "") and "top=false" in (f.url or "")), None) or page

    print("MESSAGE TYPE dd (C:1):")
    print(json.dumps(dump_panel(fr, "nav:form:G:0:R:1:C:1:dd"), indent=1))
    print("\nDISTRIBUTION dd (C:2):")
    print(json.dumps(dump_panel(fr, "nav:form:G:0:R:1:C:2:dd"), indent=1))
    b.close()
print("DONE")
