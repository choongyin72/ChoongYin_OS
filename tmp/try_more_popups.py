# Try the generic popup handler on several UNBUILT OV-GM screens (set nav BU first so the popup list can populate).
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright
EC=Path(r"C:\Projects\ChoongYin_OS\workstreams\master-plan\ec-automation"); sys.path.insert(0,str(EC/"py"))
import ec_object_iud as ec
URL="https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"
CANDS=["Transport System","Nomination Point","Pipeline","Carrier Nomination","Cargo","Berth Nomination","Deal"]
def run(pg, scr):
    try:
        pg.goto(URL,wait_until="networkidle",timeout=60000); pg.wait_for_timeout(500)
        ec.open_object_screen(pg,scr); pg.wait_for_timeout(1200)
        # set a nav BU if the screen has the standard BU dropdown, then GO
        try:
            if pg.locator('css=[id="nav:form:G:0:R:1:C:1:dd_input"]').count():
                ec.select_dropdown(pg,"nav:form:G:0:R:1:C:1:dd","ECP Norway"); pg.wait_for_timeout(400)
        except Exception: pass
        try: ec.click_go(pg); pg.wait_for_timeout(1200)
        except Exception: pass
        ec._open_new_object(pg); pg.wait_for_timeout(1200)
        pins=pg.evaluate("""()=>{const o=[];const base='tab:tabPanel:objectForm:form:G:0:R:';
          for(let r=0;r<20;r++){ if(document.getElementById(base+r+':C:1:pin')){
            const lc=document.getElementById(base+r+':C:0')||document.querySelector('[id^="'+base+r+':C:0"]');
            o.push({r,lbl:(lc?(lc.innerText||'').trim():'')});}} return o;}""")
        if not pins: print(f"{scr}: no popup fields"); return
        lbl=pins[0]["lbl"]; r=ec._resolve_field(pg,"objectForm",lbl)
        try:
            ec.pick_popup(pg,r["id"],"__FIRST__")
            val=pg.eval_on_selector(ec._css(r["id"]),"e=>e.value")
            print(f"{scr}: popup '{lbl}' -> {val!r}  => {'PASS' if val and val.strip() else 'EMPTY'}")
        except Exception as e:
            print(f"{scr}: popup '{lbl}' -> {repr(e)[:70]}")
    except Exception as e:
        print(f"{scr}: (open/newform) {repr(e)[:70]}")
with sync_playwright() as p:
    b=p.chromium.launch(headless=True,args=["--ignore-certificate-errors"])
    pg=b.new_context(ignore_https_errors=True,viewport={"width":1920,"height":1080}).new_page()
    ec.login(pg,URL,"sysadmin","sysadmin")
    for s in CANDS: run(pg,s)
    b.close()
