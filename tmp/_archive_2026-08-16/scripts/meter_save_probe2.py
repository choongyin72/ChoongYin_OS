"""Meter popup: JS-click pinB -> wait iframe -> dump rows -> click a row -> verify the
main-form pin value + popup closed. The definitive probe for the T2 gesture."""
import os
import time

from playwright.sync_api import sync_playwright

URL = os.environ.get("EC_URL", "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/")
PINB = "tab:tabPanel:objectForm:form:G:0:R:5:C:1:pinB"
PIN = "tab:tabPanel:objectForm:form:G:0:R:5:C:1:pin"

with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    page = b.new_context(ignore_https_errors=True, viewport={"width": 1920, "height": 1080}).new_page()
    page.goto(URL, wait_until="domcontentloaded", timeout=60000)
    page.fill('[id="username"]', "sysadmin")
    page.fill('[id="password"]', "sysadmin")
    page.click('[id="kc-login"]')
    page.wait_for_selector('[id="menu:searchForm:searchTxt"]', timeout=60000)
    page.locator('[id="menu:searchForm:searchTxt"]').type("Meter", delay=50)
    time.sleep(1.2)
    page.locator('xpath=//*[contains(@class,"tv-link") and normalize-space(text())="Meter"]').first.click()
    page.wait_for_load_state("networkidle", timeout=20000)
    time.sleep(2)
    dd = "nav:form:G:0:R:1:C:1:dd"
    page.click(f'[id="{dd}_button"]')
    page.wait_for_selector(f'[id="{dd}_panel"] tr[data-item-label]', timeout=8000)
    page.locator(f'[id="{dd}_panel"] tr[data-item-label="ECP Norway"]').click()
    page.wait_for_load_state("networkidle", timeout=15000)
    time.sleep(1.5)
    page.click('[id="button:form:B"]')
    page.wait_for_load_state("networkidle", timeout=20000)
    time.sleep(2)
    page.locator('xpath=//li[contains(@class,"ui-menu-parent")][.//span[contains(@class,"ui-icon-insert")]]').hover()
    it = page.locator('xpath=//ul[contains(@class,"ui-menu-child")]//li//a[normalize-space(.)="New Object" and contains(@onclick,"insert")]')
    it.wait_for(state="visible", timeout=10000)
    it.click()
    page.wait_for_load_state("networkidle", timeout=15000)
    time.sleep(1.5)
    page.fill('[id="tab:tabPanel:objectForm:form:G:0:R:2:C:1:da_input"]', "2003-01-01")
    page.keyboard.press("Escape")
    time.sleep(2)

    page.evaluate(f"() => document.getElementById('{PINB}').click()")
    page.wait_for_function(
        "() => { const f = document.querySelector('#popupIFrame'); return f && f.offsetParent !== null && (f.src||'').includes('object_popup'); }",
        timeout=20000)
    time.sleep(5)
    fl = page.frame_locator('#popupIFrame')
    fl.locator('[id="PopupList:form:T_data"]').wait_for(state='visible', timeout=15000)
    rows = fl.locator('[id="PopupList:form:T_data"] tr').evaluate_all(
        """trs => trs.map(tr => [...tr.querySelectorAll('td')].slice(0,3).map(td => {
            const i = td.querySelector('input'); return i ? i.value : (td.textContent||'').trim().slice(0,30);}))""")
    print("popup rows:", rows[:8])
    fr = fl
    if rows and rows[0] and "No records" not in str(rows[0]):
        fl.locator('xpath=//tbody[@id="PopupList:form:T_data"]//tr[1]//td[1]').click()
        time.sleep(3)
        val = page.evaluate(f"""() => {{ const e = document.getElementById('{PIN}');
            return e ? e.value : 'GONE'; }}""")
        vis = page.evaluate("() => { const d = document.querySelector('#popupIFrame'); return d && d.offsetParent !== null; }")
        print("after row click: pin =", repr(val), "| popup open:", vis)
        # if still open, look for an OK/confirm button in the popup frame or main page
        if vis:
            btns = fl.locator('body').evaluate("""() => [...document.querySelectorAll('button, a')]
                .filter(e => e.offsetParent).map(b => ({id: b.id, t: (b.textContent||'').trim().slice(0,16)}))
                .filter(b => b.t).slice(0, 8)""")
            print("popup buttons:", btns)
    # RF-ORDER replication: code -> name -> date(Tab) -> type dd -> (popup already picked
    # BEFORE this block in this script flow) -> dump save state -> Save -> banner
    import time as _t
    page.fill('[id="tab:tabPanel:objectForm:form:G:0:R:0:C:1:in"]', 'AUTOTEST_MTRPROBE2')
    page.evaluate("() => { const e=document.getElementById('tab:tabPanel:objectForm:form:G:0:R:0:C:1:in'); e.dispatchEvent(new Event('change',{bubbles:true})); e.dispatchEvent(new Event('blur',{bubbles:true})); }")
    page.fill('[id="tab:tabPanel:objectForm:form:G:0:R:1:C:1:in"]', 'Meter Probe 2')
    page.evaluate("() => { const e=document.getElementById('tab:tabPanel:objectForm:form:G:0:R:1:C:1:in'); e.dispatchEvent(new Event('change',{bubbles:true})); e.dispatchEvent(new Event('blur',{bubbles:true})); }")
    td = 'tab:tabPanel:objectForm:form:G:0:R:4:C:1:dd'
    page.click(f'[id="{td}_button"]')
    page.wait_for_selector(f'[id="{td}_panel"] tr[data-item-label]', timeout=8000)
    page.locator(f'[id="{td}_panel"] tr[data-item-label="Entry"]').click()
    _t.sleep(1.5)
    state = page.evaluate("""() => [...document.querySelectorAll('a[title^="Save"]')]
        .map(a => ({title: a.title, cls: a.className.includes('ui-state-disabled') ? 'DISABLED' : 'enabled', vis: a.offsetParent !== null}))""")
    print('save anchors:', state)
    page.locator('xpath=//a[@title="Save [Ctrl+s]" and not(contains(@class,"ui-state-disabled"))]').first.click()
    _t.sleep(5)
    banner = page.evaluate("""() => { const t = [...document.querySelectorAll('div,span')]
        .map(e => (e.textContent||'').trim())
        .filter(t => t && t.length < 300 && (/Required fields|missing|error|failed|invalid/i.test(t)));
        return t.sort((a,b)=>a.length-b.length).slice(0,2); }""")
    print('SAVE banner:', banner)
    page.screenshot(path=r"c:/Projects/ChoongYin_OS/tmp/dispatching_recon/meter_save_probe2.png", full_page=True)
    b.close()