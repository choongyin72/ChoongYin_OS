"""OV-specific live scan for Stream - by Group Model (CO.0027, class STREAM). READ-ONLY (never Saves).
Reuses the exact recipe from scan_ec_screen.py but forces the OV branch (the generic script's
class_property_cnfg LABEL lookup for "Stream - by Group Model" didn't match, since the real class
LABEL is "Stream"; class_cnfg already independently confirmed CLASS_TYPE=OBJECT via resolve_ec_screen.py
with SCREEN="stream"). Confirms objectForm/updateAttributes/objectdates ids + mandatory + labels."""
import os
from playwright.sync_api import sync_playwright

EC_URL = os.environ.get("EC_URL", "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/")
SCREEN = "Stream - by Group Model"
HEADED = os.environ.get("EC_HEADED", "0") == "1"
YELLOW = "rgb(252, 249, 192)"


def css(fid):
    return "#" + fid.replace(":", "\\:")


def ajax(page, t=15000):
    try:
        page.wait_for_load_state("networkidle", timeout=t)
    except Exception:
        pass
    page.wait_for_timeout(900)


def dump_inputs(page, id_substr):
    return page.evaluate("""(sub) => [...document.querySelectorAll('input,select,textarea')]
        .filter(e=>e.id && e.id.includes(sub) && e.type!=='hidden')
        .map(e=>{ const y=getComputedStyle(e).backgroundColor==='""" + YELLOW + """';
            let lab='';
            const m=e.id.match(/^(.*:R:\\d+):C:\\d+:/);
            if(m){ const lc=document.getElementById(m[1]+':C:0:la')||document.getElementById(m[1]+':C:0:out')||document.querySelector("[id^='"+m[1]+":C:0']"); if(lc) lab=(lc.innerText||lc.value||'').trim(); }
            if(!lab){ const r=e.closest('tr'); if(r){const c=[...r.querySelectorAll('td,th,label')].map(x=>(x.innerText||'').trim()).filter(Boolean); lab=c[0]||'';} }
            return {id:e.id, val:e.value, mandatory:y, label:lab}; }).slice(0,40)""", id_substr)


with sync_playwright() as p:
    b = p.chromium.launch(headless=not HEADED, slow_mo=600 if HEADED else 0, args=["--ignore-certificate-errors"])
    page = b.new_context(ignore_https_errors=True, viewport={"width": 1900, "height": 1000}).new_page()
    page.goto(EC_URL, wait_until="domcontentloaded", timeout=45000)
    page.fill("#username", "sysadmin"); page.fill("#password", "sysadmin"); page.click("#kc-login")
    page.wait_for_selector(css("menu:searchForm:searchTxt"), timeout=60000); ajax(page)
    box = page.locator(css("menu:searchForm:searchTxt")); box.click(); box.fill(""); box.type(SCREEN, delay=45); ajax(page, 7000)
    tv_link = page.locator(f"xpath=//*[self::label or self::span][contains(@class,'tv-link') and normalize-space(text())='{SCREEN}']").first
    tv_link.click()
    ajax(page)
    mm = page.locator(css("screenToolbar:form:minmaxMenu"))
    if mm.count() and mm.first.is_visible():
        mm.first.click(); ajax(page)
    page.wait_for_timeout(1500)

    # REAL navigator shape (confirmed via stream_group_model_nav_shape.py live DOM dump):
    # Row 1 (R:1): Date(C:0) + 3-level SAME-ROW cascade PU(C:1)->Area(C:2)->Facility Class 1(C:3).
    # Row 3 (R:3, C:0): a SEPARATE 4th mandatory dropdown labelled "Stream" (own row/label at R:2),
    # NOT "Facility Class 2" as assumed pre-scan, and NOT on the same row/increasing-column as the
    # first 3 - a distinct shape from Area's single-row addressing.
    row1 = [("C:1", "AS1 EC Exploration Norway"), ("C:2", "AS1_Area"), ("C:3", "AS1_Facility_01")]
    for col, val in row1:
        ddp = f"nav:form:G:0:R:1:{col}:dd"
        btn = page.locator(css(ddp + "_button")).first
        btn.wait_for(state="visible", timeout=15000)
        btn.click()
        page.wait_for_timeout(900)
        opt = page.locator(f"xpath=//*[@id='{ddp}_panel']//tr[@data-item-label='{val}']").first
        opt.wait_for(state="visible", timeout=8000)
        opt.click()
        page.wait_for_timeout(1500)
        print(f"nav R:1:{col} <- {val} (real DOM id: {ddp}_input)")

    # R:3:C:0 "Stream" dropdown - list its available options rather than assume a value
    ddp = "nav:form:G:0:R:3:C:0:dd"
    btn = page.locator(css(ddp + "_button")).first
    btn.wait_for(state="visible", timeout=15000)
    btn.click()
    page.wait_for_timeout(900)
    opts = page.evaluate("""(id) => [...document.querySelectorAll("[id='"+id+"_panel'] tr[data-item-label]")]
        .map(e => e.getAttribute('data-item-label')).slice(0,15)""", ddp)
    print(f"nav R:3:C:0 ('Stream') available options (first 15): {opts}")
    if opts:
        opt = page.locator(f"xpath=//*[@id='{ddp}_panel']//tr[@data-item-label='{opts[0]}']").first
        opt.click()
        page.wait_for_timeout(1200)
        print(f"nav R:3:C:0 <- {opts[0]} (picked first available)")
    else:
        page.keyboard.press("Escape")
        print("nav R:3:C:0 has NO options available under this PU/Area/FacilityClass1 scope")

    page.locator(css("button:form:B")).first.click()
    ajax(page, 20000)
    print("GO clicked")

    grid = None
    for _ in range(20):
        grid = page.evaluate("""() => { const t=[...document.querySelectorAll("[id$=':T_data']")]
            .filter(e=>e.offsetParent||e.querySelector('tr'));
            return t.length? t[0].id : null; }""")
        if grid:
            break
        page.wait_for_timeout(1000)
    print("grid id:", grid)

    # UPDATE / DELETE: select an existing row (if any) -> updateAttributes + objectdates
    try:
        sp = page.locator(f"xpath=//*[@id='{grid}']//tr//span[normalize-space(text())!='']").first
        if sp.count():
            sp.click(); ajax(page); page.wait_for_timeout(1200)
            print("\nUPDATE updateAttributes fields (id | mandatory | label):")
            for f in dump_inputs(page, "updateAttributes:form"):
                print(f"   {f['id']:55s} mand={f['mandatory']!s:5s} {f['label'][:22]}")
            print("DELETE objectdates fields:")
            for f in dump_inputs(page, "objectdates:form"):
                print(f"   {f['id']:55s} {f['label'][:22]}")
        else:
            print("(no existing row under this nav scope to select for UPDATE/DELETE scan)")
    except Exception as e:
        print("  row-select scan err:", str(e)[:70])

    # INSERT: hover Insert -> New Object -> dump objectForm
    try:
        page.locator("xpath=//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'ui-icon-insert')]]").first.hover()
        page.wait_for_timeout(900)
        links = page.locator("xpath=//ul[contains(@class,'ui-menu-child')]//li//a")
        for i in range(links.count()):
            if links.nth(i).is_visible() and links.nth(i).text_content(timeout=800).strip() == "New Object":
                links.nth(i).click(); break
        ajax(page)
        print("\nINSERT objectForm fields (id | mandatory | label):")
        for f in dump_inputs(page, "objectForm:form"):
            print(f"   {f['id']:55s} mand={f['mandatory']!s:5s} {f['label'][:22]}")
    except Exception as e:
        print("  insert-form scan err:", str(e)[:70])
    b.close()
print("\nDONE (read-only scan; nothing saved).")
