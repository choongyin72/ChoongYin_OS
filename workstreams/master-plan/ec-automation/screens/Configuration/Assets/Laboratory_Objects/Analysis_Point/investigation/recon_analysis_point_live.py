"""Live recon for Analysis Point (OV-GM, 3-level cascade) with the POPULATED P1 scope: dump exact nav dd
ids, fill PU/Area/Facility = P1, GO, then select a row -> updateAttributes + objectdates ids. READ-ONLY.
py -X utf8 tmp/scripts/recon_analysis_point_live.py"""
import os
from playwright.sync_api import sync_playwright

EC_URL = os.environ.get("EC_URL", "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/")
USER, PWD = os.environ.get("EC_USER", "sysadmin"), os.environ.get("EC_PASS", "sysadmin")
YELLOW = "rgb(252, 249, 192)"
SCOPE = ["P1 Production Unit", "P1 Area", "P1 Facility 1"]


def esc(i):
    return "#" + i.replace(":", "\\:")


def ajax(page, t=20000):
    try:
        page.wait_for_load_state("networkidle", timeout=t)
    except Exception:
        pass
    page.wait_for_timeout(900)


def dump(page, sub):
    return page.evaluate("""(args)=>{const [sub,Y]=args; return [...document.querySelectorAll('input,select,textarea')]
        .filter(e=>e.id&&e.id.includes(sub)&&e.type!=='hidden').map(e=>{const y=getComputedStyle(e).backgroundColor===Y;
        let lab='';const m=e.id.match(/^(.*:R:\\d+):C:\\d+:/); if(m){const lc=document.querySelector("[id^='"+m[1]+":C:0']"); if(lc) lab=(lc.innerText||lc.value||'').trim();}
        return {id:e.id,mand:y,label:lab};}).slice(0,12);}""", [sub, YELLOW])


with sync_playwright() as p:
    b = p.chromium.launch(headless=True, args=["--ignore-certificate-errors"])
    page = b.new_context(ignore_https_errors=True, viewport={"width": 1900, "height": 1000}).new_page()
    page.goto(EC_URL, wait_until="domcontentloaded", timeout=45000)
    page.fill("#username", USER); page.fill("#password", PWD); page.click("#kc-login")
    page.wait_for_selector(esc("menu:searchForm:searchTxt"), timeout=60000); ajax(page)
    box = page.locator(esc("menu:searchForm:searchTxt")); box.click(); box.type("Analysis Point", delay=45); ajax(page, 7000)
    page.locator("xpath=//*[contains(@class,'tv-link') and normalize-space(text())='Analysis Point']").first.click(); ajax(page)
    mm = page.locator(esc("screenToolbar:form:minmaxMenu"))
    if mm.count() and mm.first.is_visible(): mm.first.click(); ajax(page)

    nav_dds = page.evaluate("""()=>[...document.querySelectorAll("[id^='nav:form:G:0:'][id$='dd_input']")].map(e=>e.id)""")
    print("NAV dd ids (DOM order = PU, Area, Facility):")
    for i in nav_dds:
        print("  ", i)
    nav_date = page.evaluate("""()=>{const e=[...document.querySelectorAll("[id^='nav:form:G:0:'][id$='da_input']")][0];return e?e.id:null;}""")
    print("NAV date id:", nav_date)

    # fill cascade in DOM order with P1 scope
    for ddinput, val in zip(nav_dds, SCOPE):
        ddp = ddinput[:-len("_input")]
        page.locator(esc(ddp + "_button")).first.click(); page.wait_for_timeout(900)
        opt = page.locator(f"xpath=//*[@id='{ddp}_panel']//tr[normalize-space(@data-item-label)='{val}']")
        if opt.count() == 0:
            print(f"   [WARN] '{val}' not in {ddp} options; first option used")
            opt = page.locator(f"xpath=//*[@id='{ddp}_panel']//tr[@data-item-label]")
        picked = (opt.first.get_attribute("data-item-label") or "").strip()
        opt.first.click(); ajax(page, 12000)
        print(f"   set {ddp.split(':')[-1]} <- {picked}")
    page.locator(esc("button:form:B")).first.click(); ajax(page, 20000)

    grid = page.evaluate("""()=>{const t=[...document.querySelectorAll("[id$=':T_data']")].filter(e=>e.querySelector('tr'));return t.length?t[0].id:null;}""")
    rc = page.locator(f"xpath=//*[@id='{grid}']/tr").count() if grid else 0
    print(f"\ngrid id: {grid}  row count: {rc}")

    if grid and rc:
        sp = page.locator(f"xpath=//*[@id='{grid}']//tr[1]//span[normalize-space(text())!='']").first
        if sp.count():
            print("selecting row:", (sp.text_content() or '').strip())
            sp.click(); ajax(page); page.wait_for_timeout(900)
            print("\nUPDATE updateAttributes (id | mand | label):")
            for f in dump(page, "updateAttributes:form"):
                print(f"   {f['id']:56s} mand={f['mand']!s:5s} {f['label'][:24]}")
            print("DELETE objectdates (End Date = C:3):")
            for f in dump(page, "objectdates:form"):
                print(f"   {f['id']:56s} {f['label'][:24]}")
    b.close()
print("\nDONE (read-only).")
