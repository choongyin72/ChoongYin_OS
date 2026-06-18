"""RECON v2 (read-only) WR.0010.01: fill ONLY mandatory nav (Date + PU + Area + Facility Class 1), GO,
dump the analysis HEADER grid, SELECT the P1 W260 row (Analysis No 1088 @ 2025-04-01), then dump the
component grid to map the editable mol% cell. Also reports which nav fields are mandatory (yellow class).
No edits."""
import os
from playwright.sync_api import sync_playwright

EC_URL = os.environ.get("EC_URL", "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/")
SCREEN = "Well Gas Component Analysis"
DATE = "2025-04-01"
WELL = "W260"


def css(fid):
    return "#" + fid.replace(":", "\\:")


def ajax(page, t=15000):
    try:
        page.wait_for_load_state("networkidle", timeout=t)
    except Exception:
        pass
    page.wait_for_timeout(900)


def pick(page, group, value):
    pre = f"nav:form:{group}:R:1:C:0:dd"
    item = f"xpath=//*[@id='{pre}_panel']//tr[normalize-space(@data-item-label)='{value}']"
    page.click(css(pre + "_button"))
    try:
        page.locator(item).first.wait_for(state="visible", timeout=5000)
    except Exception:
        page.keyboard.press("Escape"); page.wait_for_timeout(1000); page.click(css(pre + "_button"))
        page.locator(item).first.wait_for(state="visible", timeout=6000)
    page.locator(item).first.click(); ajax(page, 10000)


with sync_playwright() as p:
    b = p.chromium.launch(headless=True, args=["--ignore-certificate-errors"])
    page = b.new_context(ignore_https_errors=True, viewport={"width": 1900, "height": 1000}).new_page()
    page.goto(EC_URL, wait_until="domcontentloaded", timeout=45000)
    page.fill("#username", "sysadmin"); page.fill("#password", "sysadmin"); page.click("#kc-login")
    page.wait_for_selector(css("menu:searchForm:searchTxt"), timeout=60000); ajax(page)
    box = page.locator(css("menu:searchForm:searchTxt")); box.click(); box.fill(""); box.type(SCREEN, delay=45); ajax(page, 7000)
    page.locator(f"xpath=//*[contains(@class,'tv-link') and normalize-space(text())='{SCREEN}']").first.click(); ajax(page)
    mm = page.locator(css("screenToolbar:form:minmaxMenu"))
    if mm.count() and mm.first.is_visible():
        mm.first.click(); ajax(page)
    # report which nav inputs/dds look mandatory (EC marks mandatory cells with a yellow/mandatory class)
    mand = page.evaluate("""() => [...document.querySelectorAll("[id^='nav:form:G:']")]
        .filter(e=>/da_input$|dd_input$|:in$/.test(e.id))
        .map(e=>({id:e.id.replace('nav:form:','').replace(':R:1:C:0',''), cls:e.className,
                  bg:getComputedStyle(e).backgroundColor})).slice(0,12)""")
    print("nav inputs (id, class, bg):")
    for m in mand:
        print("  ", m["id"], "|", m["cls"][:40], "|", m["bg"])
    # fill ONLY mandatory: dates + PU + Area + Facility Class 1
    for fid in page.evaluate("""() => [...document.querySelectorAll("[id^='nav:form:']")].map(e=>e.id).filter(id=>/:da_input$/.test(id))"""):
        el = page.locator(css(fid)); el.click(); el.fill(DATE); page.keyboard.press("Tab"); page.wait_for_timeout(300)
    pick(page, "G:2", "P1 Production Unit")
    pick(page, "G:3", "P1 Area")
    pick(page, "G:4", "P1 Facility 1")
    for go in ("go_button:form:B", "navButton:form:B", "button:form:B"):
        loc = page.locator(css(go))
        if loc.count() and loc.first.is_visible():
            loc.first.click(); ajax(page, 18000); break
    # dump the analysis HEADER grid rows
    arows = page.evaluate("""() => { const out=[];
        document.querySelectorAll("[id^='analysis:form:T:'][id$=':C1_in'], [id^='analysis:form:T:'][id$=':C1_la']").forEach(()=>{});
        document.querySelectorAll("table tr").forEach(tr=>{
          const ins=[...tr.querySelectorAll("input[id^='analysis:form:T:']")];
          if(!ins.length) return;
          out.push({rid: ins[0].id, vals: ins.slice(0,7).map(i=>i.value)});
        }); return out; }""")
    print(f"\nanalysis header rows ({len(arows)}):")
    for r in arows[:10]:
        print("  ", r["rid"], r["vals"])
    # find + click the P1 W260 row
    target = next((r for r in arows if any(WELL in str(v) for v in r["vals"])), None)
    print("\ntarget analysis row:", target["rid"] if target else None)
    if target:
        page.locator(css(target["rid"])).click(); ajax(page, 12000)
    comp = page.evaluate("""() => { const out=[];
        document.querySelectorAll("table tr").forEach(tr=>{
          const ins=[...tr.querySelectorAll("input[id^='component_set:form:T:']")].filter(i=>i.type!=='hidden');
          if(!ins.length) return;
          const cells=[...tr.querySelectorAll('td,th')].map(c=>(c.innerText||'').trim());
          out.push({label: cells.find(t=>t)||'', inputs: ins.map(i=>({id:i.id.split(':form:')[1], val:i.value, ro:i.readOnly}))});
        }); return out; }""")
    print(f"\ncomponent grid rows ({len(comp)}):")
    for r in comp[:12]:
        print("  ", r["label"][:18], "->", [(i["id"], i["val"], "ro" if i["ro"] else "EDIT") for i in r["inputs"]])
    page.screenshot(path=r"c:\Projects\ChoongYin_OS\tmp\recon_comp\wellgas_grid2.png", full_page=True)
    b.close()
print("DONE")
