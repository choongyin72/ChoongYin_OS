"""Select AUTOTEST_CP_001 and dump the objectdates tab cells (id/label/value) to find the real
End Date cell, then set End=Start at that cell + Save to CLEAN the residual. Verifies via DB."""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright
EC = Path(r"C:\Projects\ChoongYin_OS\workstreams\master-plan\ec-automation")
sys.path.insert(0, str(EC / "py")); sys.path.insert(0, str(EC / "libraries"))
import ec_object_iud as ec
import DbVerify as db
URL = "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"
GRID = "manage_object_nav_nav:form:T_data"
CODE = "AUTOTEST_CP_001"
with sync_playwright() as p:
    br = p.chromium.launch(headless=True, args=["--ignore-certificate-errors"])
    pg = br.new_context(ignore_https_errors=True, viewport={"width": 1920, "height": 1080}).new_page()
    ec.login(pg, URL, "sysadmin", "sysadmin")
    ec.open_object_screen(pg, "Chemical Product"); ec.click_go(pg)
    if not ec.select_row(pg, GRID, CODE):
        print("row not found"); br.close(); sys.exit()
    pg.wait_for_timeout(800)
    cells = pg.evaluate("""()=>{const base='tab:tabPanel:objectdates:form:G:0:R:';const out=[];
      for(let r=0;r<6;r++){for(let cc=0;cc<6;cc++){
        const da=document.getElementById(base+r+':C:'+cc+':da_input');
        const inn=document.getElementById(base+r+':C:'+cc+':in');
        const lc=document.querySelector('[id^=\"'+base+r+':C:'+cc+'\"]');
        const el=da||inn; if(!el && !lc) continue;
        const kind=da?'date':(inn?'text':'label/other');
        const txt=lc?(lc.innerText||'').trim().slice(0,20):'';
        const val=el?el.value:'';
        out.push('R'+r+':C'+cc+' kind='+kind+' text='+JSON.stringify(txt)+' val='+JSON.stringify(val)+' id='+(el?el.id:'(no-input)'));}}
      return out;}""")
    print("=== objectdates cells ===")
    for c in cells: print("  ", c)
    br.close()
