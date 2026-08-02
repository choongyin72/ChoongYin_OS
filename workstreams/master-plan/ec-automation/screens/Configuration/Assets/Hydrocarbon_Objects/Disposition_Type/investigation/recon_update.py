"""READ-mostly recon: insert a temp Disposition Type row, dump updateAttributes + objectdates
field ids/labels (needed for the RF T3), then close it (End=Start self-clean). tmp scratch."""
import os, sys
from pathlib import Path
from playwright.sync_api import sync_playwright
EC = Path(r"C:\Projects\ChoongYin_OS\workstreams\master-plan\ec-automation")
sys.path.insert(0, str(EC / "py")); sys.path.insert(0, str(EC / "libraries"))
import ec_object_iud as ec

URL = "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"
GRID = "manage_object_nav_nav:form:T_data"
CODE = "AUTOTEST_DISP_RECON"

def dump(pg, form):
    return pg.evaluate("""(form)=>{const base='tab:tabPanel:'+form+':form:G:0:R:';const out=[];
      for(let r=0;r<20;r++){let el=null,kind='';
        const inn=document.getElementById(base+r+':C:1:in');const dai=document.getElementById(base+r+':C:1:da_input');
        const ddi=document.getElementById(base+r+':C:1:dd_input');const dai3=document.getElementById(base+r+':C:3:da_input');
        if(inn){el=inn;kind='text';}else if(dai){el=dai;kind='date';}else if(ddi){el=ddi;kind='dd';}else if(dai3){el=dai3;kind='date-C3';}
        if(!el)continue;
        const l0=document.getElementById(base+r+':C:0')||document.querySelector('[id^="'+base+r+':C:0"]');
        const l2=document.getElementById(base+r+':C:2')||document.querySelector('[id^="'+base+r+':C:2"]');
        out.push({r,label0:l0?(l0.innerText||'').trim().slice(0,20):'',label2:l2?(l2.innerText||'').trim().slice(0,12):'',id:el.id.replace('tab:tabPanel:'+form+':form:G:0:R:',''),kind});}
      return out;}""", form)

with sync_playwright() as p:
    br = p.chromium.launch(headless=True, args=["--ignore-certificate-errors"])
    pg = br.new_context(ignore_https_errors=True, viewport={"width":1920,"height":1080}).new_page()
    ec.login(pg, URL, os.environ.get("EC_USER", "sysadmin"), os.environ.get("EC_PASS", "sysadmin")); ec.open_object_screen(pg, "Disposition Type"); ec.click_go(pg)
    ec.insertObjectRecord(pg, GRID, [
        {"label":"Disposition Code","value":CODE,"kind":"text"},
        {"label":"Disposition Name","value":"AUTOTEST recon","kind":"text"},
        {"label":"Start Date","value":"2000-01-01","kind":"date"}])
    ec.select_row(pg, GRID, CODE)
    for form in ["updateAttributes","objectdates"]:
        print(f"=== {form} ===")
        for row in dump(pg, form): print("  ", row)
    # self-clean
    ec.closeObjectRecord(pg, GRID, CODE, "2000-01-01")
    import DbVerify as db
    print("residual after close:", db.count_like("ov_disposition_type","AUTOTEST"))
    br.close()
