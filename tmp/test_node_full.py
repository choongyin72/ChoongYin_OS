# Full OV-GM IUD flow on Node (cascade -> insert parent=nav PU -> list? -> delete -> self-clean). Local AUTOTEST.
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright
EC=Path(r"C:\Projects\ChoongYin_OS\workstreams\master-plan\ec-automation"); sys.path.insert(0,str(EC/"py"))
import ec_object_iud as ec
URL="https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"; GRID="manageObject:form:T_data"; CODE="AUTOTEST_ND_T1"
def fill_label(pg,form,label,val,kind):
    r=ec._resolve_field(pg,form,label)
    if not r: print(f"    !! field not found: {label}"); return False
    ec.fill_field(pg,r["id"],val,kind if kind!='auto' else r["kind"]); return True
with sync_playwright() as p:
    b=p.chromium.launch(headless=True,args=["--ignore-certificate-errors"])
    pg=b.new_context(ignore_https_errors=True,viewport={"width":1920,"height":1080}).new_page()
    ec.login(pg,URL,"sysadmin","sysadmin")
    ec.open_object_screen(pg,"Node"); pg.wait_for_timeout(1200)
    for col in (1,2,3): ec.select_dropdown(pg,"nav:form:G:0:R:1:C:%d:dd_input"%col,"__FIRST__"); pg.wait_for_timeout(800)
    pu=pg.eval_on_selector(ec._css("nav:form:G:0:R:1:C:1:dd_input"),"e=>e.value"); print("nav PU:",repr(pu))
    ec.click_go(pg); pg.wait_for_timeout(1500)
    # INSERT
    ec._open_new_object(pg); pg.wait_for_timeout(1200)
    fill_label(pg,"objectForm","Node Code",CODE,"text")
    fill_label(pg,"objectForm","Node Name","AUTOTEST Node T1","text")
    fill_label(pg,"objectForm","Start Date","2000-01-01","date")
    fill_label(pg,"objectForm","Calculation Sequence Number","1","text")
    # parent-dd = nav PU (grid visibility) - set to the captured PU value
    r=ec._resolve_field(pg,"objectForm","Op Production Unit")
    if r: ec.select_dropdown(pg,r["id"],pu)
    ec.save(pg); err=ec.ec_error(pg); print("insert ec_error:",repr(err)[:120]); ec.click_go(pg); pg.wait_for_timeout(1500)
    listed=ec.wait_for_row(pg,GRID,CODE); print("row LISTED after insert+GO:",listed)
    b.close()
