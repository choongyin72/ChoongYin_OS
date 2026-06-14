"""Map PFLW grid C{c} -> column label (headers), so the suite targets the right cell for ON_STREAM_HRS.
Reuses the proven scope (Production Unit / Onshore area / Onshore facility / PRD_FLUID_ADFAY_54401),
GO, dumps the column header labels + the C0 label cell. Read-only."""
import time, json
from playwright.sync_api import sync_playwright
URL = "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"; SCREEN = "Daily Production Flowline, by Flowline"; DATE = "2003-09-20"


def frame(page):
    for _ in range(20):
        for fr in page.frames:
            try:
                if fr.evaluate("""()=>!!document.querySelector('[id="nav:form:G:0:R:1:C:0:da_input"]')"""):
                    return fr
            except Exception:
                pass
        time.sleep(1.0)
    return page


def pick(fr, g, label):
    fr.locator(f'[id="nav:form:G:{g}:R:1:C:0:dd_button"]').click(timeout=4000); time.sleep(0.5)
    fr.locator(f'xpath=//*[@id="nav:form:G:{g}:R:1:C:0:dd_panel"]//tr[normalize-space(@data-item-label)="{label}"]').first.click(timeout=4000); time.sleep(1.1)


with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    page = b.new_context(ignore_https_errors=True, viewport={"width": 1680, "height": 1000}).new_page()
    page.goto(URL, wait_until="domcontentloaded", timeout=60000)
    page.fill('[id="username"]', "sysadmin"); page.fill('[id="password"]', "sysadmin"); page.click('[id="kc-login"]')
    page.wait_for_selector('[id="menu:searchForm:searchTxt"]', timeout=60000); time.sleep(1.0)
    sel = f'xpath=//*[contains(@class,"tv-link") and normalize-space(text())="{SCREEN}"]'
    page.locator('[id="menu:searchForm:searchTxt"]').type(SCREEN, delay=25)
    page.wait_for_selector(sel, timeout=12000); page.locator(sel).first.click()
    page.wait_for_load_state("networkidle", timeout=30000); time.sleep(3.0)
    fr = frame(page)
    for g in (0, 1):
        di = fr.locator(f'[id="nav:form:G:{g}:R:1:C:0:da_input"]'); di.fill(DATE); di.press("Tab"); time.sleep(0.8)
    pick(fr, 2, "Production Unit"); pick(fr, 3, "Onshore area"); pick(fr, 4, "Onshore facility"); pick(fr, 5, "PRD_FLUID_ADFAY_54401")
    fr.locator('[id="button:form:B"]').click(timeout=5000); page.wait_for_load_state("networkidle", timeout=30000); time.sleep(2.5)
    info = fr.evaluate("""()=>{
      const heads=[...document.querySelectorAll('[id^="daily_flowline_status:form"] th')].map(th=>(th.textContent||'').trim()).filter(Boolean);
      const t=document.getElementById('daily_flowline_status:form:T_data');
      const row0=t?[...t.querySelectorAll('tr')][0]:null;
      const cells=row0?[...row0.querySelectorAll('[id*=":C"]')].map(e=>({c:(e.id.split(':T:0:')[1]||e.id), tag:e.tagName, val:(e.value!==undefined?e.value:(e.textContent||'').trim())})):[];
      return {headers:heads.slice(0,45), cells:cells.slice(0,16)};}""")
    print("HEADERS:", json.dumps(info.get("headers")))
    print("ROW0 CELLS:", json.dumps(info.get("cells")))
    b.close()
print("DONE")
