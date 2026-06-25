"""RECON (read-only): open 'Well Gas Component Analysis' and dump its navigator field labels + GO button
+ whether a component_set grid exists — to COMPARE its layout against the stream comp screens
(PO.0020/PO.0019: 8-field nav G:0/G:1 dates + PU/Area/Facility/Stream/Analysis Status/Sampling,
go_button:form:B, component_set:form grid). No edits."""
import os
from playwright.sync_api import sync_playwright

EC_URL = os.environ.get("EC_URL", "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/")
SCREENS = ["Well Gas Component Analysis", "Gas Well Component Analysis"]


def css(fid):
    return "#" + fid.replace(":", "\\:")


def ajax(page, t=15000):
    try:
        page.wait_for_load_state("networkidle", timeout=t)
    except Exception:
        pass
    page.wait_for_timeout(900)


with sync_playwright() as p:
    b = p.chromium.launch(headless=True, args=["--ignore-certificate-errors"])
    page = b.new_context(ignore_https_errors=True, viewport={"width": 1900, "height": 1000}).new_page()
    page.goto(EC_URL, wait_until="domcontentloaded", timeout=45000)
    page.fill("#username", "sysadmin"); page.fill("#password", "sysadmin"); page.click("#kc-login")
    page.wait_for_selector(css("menu:searchForm:searchTxt"), timeout=60000); ajax(page)
    opened = None
    for name in SCREENS:
        box = page.locator(css("menu:searchForm:searchTxt")); box.click(); box.fill(""); box.type(name, delay=45); ajax(page, 6000)
        link = page.locator(f"xpath=//*[contains(@class,'tv-link') and normalize-space(text())='{name}']")
        if link.count():
            link.first.click(); ajax(page); opened = name; break
    print("opened:", opened)
    mm = page.locator(css("screenToolbar:form:minmaxMenu"))
    if mm.count() and mm.first.is_visible():
        mm.first.click(); ajax(page)
    # dump nav field groups + their labels
    nav = page.evaluate("""() => {
        const out=[];
        document.querySelectorAll("[id^='nav:form:G:']").forEach(e=>{
          const m=e.id.match(/nav:form:(G:\\d+):R:1:C:0:(da_input|dd_button|in)/);
          if(m){ let lbl=''; const b=document.getElementById('nav:form:'+m[1]+':R:1:C:0:dd_button');
            if(b) lbl=(b.innerText||b.title||'').trim();
            out.push({grp:m[1], kind:m[2], label:lbl}); }
        });
        return [...new Map(out.map(o=>[o.grp,o])).values()]; }""")
    print("NAV groups:")
    for n in nav:
        print(f"   {n['grp']:6s} {n['kind']:10s} {n['label']}")
    print("GO buttons present:", page.evaluate("""() => ['go_button:form:B','button:form:B','navButton:form:B']
        .filter(id=>document.getElementById(id))"""))
    print("component_set grid present:", page.evaluate("""() => !!document.querySelector("[id^='component_set:form:T']")"""))
    print("analysis header grid present:", page.evaluate("""() => !!document.querySelector("[id^='analysis:form:T']")"""))
    page.screenshot(path=r"c:\Projects\ChoongYin_OS\tmp\recon_comp\wellgas_screen.png")
    b.close()
print("DONE")
