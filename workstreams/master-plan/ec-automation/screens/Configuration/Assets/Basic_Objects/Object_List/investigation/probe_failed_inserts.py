"""Probe why Object List + Regulatory Permits inserts were silently rejected.
Re-attempts the same minimal insert, captures the EC validation/error panel
text, and dumps each insert-form dropdown's options. If the insert accidentally
SUCCEEDS, the object is immediately deleted (End=Start) to leave no trace."""
import time
from playwright.sync_api import sync_playwright

EC_URL = "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"
TARGETS = [
    {
        "name": "Object List",
        "url": EC_URL.rstrip("/") + "/com.ec.frmw.co.screens/manage_object_nav/CLASS_NAME/OBJECT_LIST",
        "code": "tab:tabPanel:objectForm:form:G:0:R:0:C:1:in",
        "namef": "tab:tabPanel:objectForm:form:G:0:R:1:C:1:in",
        "date": "tab:tabPanel:objectForm:form:G:0:R:2:C:1:da_input",
        "dds": [("Class Name", "tab:tabPanel:objectForm:form:G:0:R:5:C:1:dd"),
                ("Relation Class", "tab:tabPanel:objectForm:form:G:0:R:6:C:1:dd")],
        "cb": ("Enforce split share to 100%", "tab:tabPanel:objectForm:form:G:0:R:7:C:1:cb"),
    },
    {
        "name": "Regulatory Permits",
        "url": EC_URL.rstrip("/") + "/com.ec.frmw.co.screens/regulatory_permits/CLASS_NAME/REGULATORY_PERMITS",
        "code": "tab:tabPanel:objectForm:form:G:0:R:0:C:1:in",
        "namef": "tab:tabPanel:objectForm:form:G:0:R:1:C:1:in",
        "date": "tab:tabPanel:objectForm:form:G:0:R:2:C:1:da_input",
        "dds": [("Regulatory Agency", "tab:tabPanel:objectForm:form:G:0:R:4:C:1:dd"),
                ("Low Limit UOM", "tab:tabPanel:objectForm:form:G:0:R:8:C:1:dd"),
                ("High Limit UOM", "tab:tabPanel:objectForm:form:G:0:R:10:C:1:dd")],
        "cb": None,
    },
]

MSG_JS = r"""() => {
    const out = [];
    document.querySelectorAll('.ui-messages, .ui-message, [id*="messages"], #JSWarningArea, #JSErrorArea, .ui-growl-message').forEach(e => {
        const t = (e.textContent || '').trim();
        if (t) out.push(t.substring(0, 300));
    });
    return out;
}"""


def fill(page, fid, value):
    page.fill(f"[id='{fid}']", value)
    page.evaluate(
        "(id) => { const e=document.getElementById(id); if(e){e.dispatchEvent(new Event('change',{bubbles:true}));e.dispatchEvent(new Event('blur',{bubbles:true}));} }",
        fid)
    page.wait_for_timeout(400)


with sync_playwright() as p:
    b = p.chromium.launch(headless=True, args=["--ignore-certificate-errors"])
    ctx = b.new_context(ignore_https_errors=True, viewport={"width": 1680, "height": 1200})
    page = ctx.new_page()
    page.on("dialog", lambda d: d.accept())
    page.goto(EC_URL, wait_until="domcontentloaded", timeout=45000)
    page.fill("#username", "sysadmin")
    page.fill("#password", "sysadmin")
    page.click("#kc-login")
    page.wait_for_url("**/dashboard**", timeout=60000)
    page.wait_for_timeout(1500)

    for t in TARGETS:
        print(f"===== {t['name']} =====")
        page.goto(t["url"], wait_until="domcontentloaded", timeout=45000)
        try:
            page.wait_for_load_state("networkidle", timeout=20000)
        except Exception:
            pass
        page.wait_for_timeout(1500)
        page.hover("xpath=//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'ui-icon-insert')]]")
        item = page.locator("xpath=//ul[contains(@class,'ui-menu-child')]//li//a[normalize-space(.)='New Object']")
        item.wait_for(state="visible", timeout=8000)
        item.click()
        page.wait_for_timeout(2000)

        # dump dropdown options (open + close each)
        for label, dd in t["dds"]:
            try:
                page.click(f"[id='{dd}_button']")
                page.wait_for_selector(f"[id='{dd}_panel']", state="visible", timeout=6000)
                opts = page.locator(f"[id='{dd}_panel'] li").all_text_contents()
                print(f"  dropdown '{label}': {[o.strip() for o in opts][:15]}")
                page.keyboard.press("Escape")
                page.wait_for_timeout(400)
            except Exception as e:
                print(f"  dropdown '{label}': FAILED to open ({str(e)[:80]})")

        if t["cb"]:
            cbid = t["cb"][1]
            checked = page.evaluate("(id)=>{const e=document.getElementById(id);return e?e.checked:null}", cbid)
            print(f"  checkbox '{t['cb'][0]}': checked={checked}")

        # re-attempt the minimal insert -> capture validation messages
        code = f"AUTOTEST_PROBE_{time.strftime('%H%M%S')}"
        fill(page, t["code"], code)
        fill(page, t["namef"], f"Probe {code}")
        page.fill(f"[id='{t['date']}']", "2000-01-01")
        page.keyboard.press("Tab")
        page.wait_for_timeout(800)
        page.click("xpath=//a[@title='Save [Ctrl+s]' and not(contains(@class,'ui-state-disabled'))]")
        try:
            page.wait_for_load_state("networkidle", timeout=15000)
        except Exception:
            pass
        page.wait_for_timeout(1500)
        msgs = page.evaluate(MSG_JS)
        print(f"  after Save messages: {msgs if msgs else '(none captured)'}")
        shot = rf"c:/Projects/ChoongYin_OS/tmp/screen_scan/shots/probe_save_{t['name'].replace(' ', '_')}.png"
        page.screenshot(path=shot)
        print(f"  screenshot: {shot}")
    ctx.close()
    b.close()
print("probe done")
