"""Recon updateAttributes + objectdates ids for Report Area RF T3 (temp insert -> dump -> close)."""
import os
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright
EC = Path(r"C:\Projects\ChoongYin_OS\workstreams\master-plan\ec-automation")
sys.path.insert(0, str(EC / "py")); sys.path.insert(0, str(EC / "libraries"))
import ec_object_iud as ec
URL = "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"
GRID = "manage_object_nav_nav:form:T_data"; CODE = "AUTOTEST_RPTA_RECON"
def dump(pg, form):
    return pg.evaluate("""(form)=>{const base='tab:tabPanel:'+form+':form:G:0:R:';const out=[];
      for(let r=0;r<12;r++){let el=null,kind='';
        const inn=document.getElementById(base+r+':C:1:in');const dai=document.getElementById(base+r+':C:1:da_input');
        const dai3=document.getElementById(base+r+':C:3:da_input');
        if(inn){el=inn;kind='text';}else if(dai){el=dai;kind='date';}else if(dai3){el=dai3;kind='date-C3';}
        if(!el)continue;
        const l0=document.getElementById(base+r+':C:0')||document.querySelector('[id^="'+base+r+':C:0"]');
        const l2=document.getElementById(base+r+':C:2')||document.querySelector('[id^="'+base+r+':C:2"]');
        out.push({r,label0:l0?(l0.innerText||'').trim().slice(0,18):'',label2:l2?(l2.innerText||'').trim().slice(0,10):'',id:el.id.replace('tab:tabPanel:'+form+':form:G:0:R:',''),kind});}return out;}""", form)
with sync_playwright() as p:
    br = p.chromium.launch(headless=True, args=["--ignore-certificate-errors"])
    pg = br.new_context(ignore_https_errors=True, viewport={"width":1920,"height":1080}).new_page()
    ec.login(pg, URL, os.environ.get("EC_USER", "sysadmin"), os.environ.get("EC_PASS", "sysadmin")); ec.open_object_screen(pg, "Report Area"); ec.click_go(pg)
    ec.insertObjectRecord(pg, GRID, [
        {"label":"Report Area Code","value":CODE,"kind":"text"},
        {"label":"Report Area Name","value":"AUTOTEST recon","kind":"text"},
        {"label":"Start date","value":"2000-01-01","kind":"date"}])
    ec.select_row(pg, GRID, CODE)
    for form in ["updateAttributes","objectdates"]:
        print(f"=== {form} ===")
        for row in dump(pg, form): print("  ", row)
    ec.closeObjectRecord(pg, GRID, CODE, "2000-01-01")
    import DbVerify as db
    print("residual after close:", db.count_like("ov_report_area","AUTOTEST"))
    br.close()
