"""READ-ONLY: open EC Code Object live, determine OV-vs-TV by how it renders.
OV = manage_object_nav controller + hover-insert 'New Object' -> objectForm detail.
TV = table-class (flat editable grid, physical Delete). No writes."""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright
EC = Path(r"C:\Projects\ChoongYin_OS\workstreams\master-plan\ec-automation")
sys.path.insert(0, str(EC / "py"))
import ec_object_iud as ec
URL = "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"
with sync_playwright() as p:
    br = p.chromium.launch(headless=True, args=["--ignore-certificate-errors"])
    pg = br.new_context(ignore_https_errors=True, viewport={"width":1920,"height":1080}).new_page()
    ec.login(pg, URL, "sysadmin", "sysadmin")
    ec.open_object_screen(pg, "EC Code Object")
    # find the content frame url (controller) + key markers
    info = pg.evaluate("""()=>{
      const url=location.href;
      const insertHover=document.querySelectorAll('li.ui-menu-parent span.ui-icon-insert').length;
      const objectForm=document.querySelectorAll('[id*=\"objectForm:form\"]').length;
      const manageGrid=!!document.getElementById('manage_object_nav_nav:form:T_data');
      const anyTdata=[...document.querySelectorAll('[id$=\":T_data\"]')].map(e=>e.id).slice(0,4);
      return {url, insertHover, objectForm, manageGrid, anyTdata};}""")
    print("content URL:", info["url"][:110])
    print("insert-hover (OV New-Object menu) present:", info["insertHover"])
    print("objectForm nodes:", info["objectForm"])
    print("manage_object grid present:", info["manageGrid"])
    print("*_T_data grids:", info["anyTdata"])
    # try the OV insert gesture to see if a New Object objectForm appears
    try:
        ec.click_go(pg)
        ec._open_new_object(pg)
        of = pg.evaluate("""()=>{const b='tab:tabPanel:objectForm:form:G:0:R:';const o=[];for(let r=0;r<6;r++){const lc=document.getElementById(b+r+':C:0')||document.querySelector('[id^=\"'+b+r+':C:0\"]');if(lc)o.push((lc.innerText||'').trim().slice(0,20));}return o;}""")
        print("OV New-Object form labels:", of if of else "(none -> not OV objectForm)")
    except Exception as e:
        print("OV insert gesture failed (-> likely TV/flat table):", repr(e)[:80])
    pg.screenshot(path=r"C:\Projects\ChoongYin_OS\tmp\eccode_screen.png")
    print("shot -> tmp/eccode_screen.png")
    br.close()
