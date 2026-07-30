# Dry-test the popup handler on more DB-CONFIRMED popup screens (from class_attr_property_cnfg PopupURL). NO Save.
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright
EC=Path(r"C:\Projects\ChoongYin_OS\workstreams\master-plan\ec-automation"); sys.path.insert(0,str(EC/"py"))
import ec_object_iud as ec
URL="https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"
# screen names for DB-confirmed popup classes likely to open + hold data
CANDS=["Tank","Storage","Sub Area","Stream","Well","Truck","Trailer","Transport System","Test Separator"]
def run(pg,scr):
    try:
        pg.goto(URL,wait_until="networkidle",timeout=45000); pg.wait_for_timeout(400)
        ec.open_object_screen(pg,scr); pg.wait_for_timeout(1000)
        try:
            if pg.locator('css=[id="nav:form:G:0:R:1:C:1:dd_input"]').count():
                ec.select_dropdown(pg,"nav:form:G:0:R:1:C:1:dd","ECP Norway"); pg.wait_for_timeout(300); ec.click_go(pg); pg.wait_for_timeout(1000)
        except Exception: pass
        ec._open_new_object(pg); pg.wait_for_timeout(1000)
        pins=pg.evaluate("""()=>{const o=[];const b='tab:tabPanel:objectForm:form:G:0:R:';
          for(let r=0;r<24;r++){if(document.getElementById(b+r+':C:1:pin')){
            const lc=document.getElementById(b+r+':C:0')||document.querySelector('[id^="'+b+r+':C:0"]');
            o.push((lc?(lc.innerText||'').trim():''));}}return o;}""")
        if not pins: print(f"  {scr:18s}: form has no rendered pin (nav/conditional)"); return
        lbl=pins[0]; r=ec._resolve_field(pg,"objectForm",lbl)
        try:
            ec.pick_popup(pg,r["id"],"__FIRST__"); val=pg.eval_on_selector(ec._css(r["id"]),"e=>e.value")
            print(f"  {scr:18s}: {len(pins)} popup(s) | '{lbl}' -> {'PASS '+repr(val) if val and val.strip() else 'EMPTY'}")
        except Exception as e:
            print(f"  {scr:18s}: {len(pins)} popup(s) | '{lbl}' empty/err: {repr(e)[:45]}")
    except Exception as e:
        print(f"  {scr:18s}: (open) {repr(e)[:40]}")
with sync_playwright() as p:
    b=p.chromium.launch(headless=True,args=["--ignore-certificate-errors"])
    pg=b.new_context(ignore_https_errors=True,viewport={"width":1920,"height":1080}).new_page()
    ec.login(pg,URL,"sysadmin","sysadmin")
    print("BATCH DRY-TEST (DB-confirmed popup screens):")
    for s in CANDS: run(pg,s)
    b.close()
