import sys
from pathlib import Path
from playwright.sync_api import sync_playwright
EC = Path(r"C:\Projects\ChoongYin_OS\workstreams\master-plan\ec-automation"); sys.path.insert(0, str(EC / "py"))
import ec_object_iud as ec
URL = "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"
SCREENS = [("Constant Standard","CO.0102"),("Stream Item","CD.0008"),("Production Day Table","CO.1033")]
GRIDS = ["manage_object_nav_nav:form:T_data","nav:form:T_data","manageObject:form:T_data"]
with sync_playwright() as p:
    b=p.chromium.launch(headless=True,args=["--ignore-certificate-errors"])
    pg=b.new_context(ignore_https_errors=True,viewport={"width":1920,"height":1080}).new_page()
    ec.login(pg,URL,"sysadmin","sysadmin")
    for name,bf in SCREENS:
        try:
            pg.goto(URL,wait_until="networkidle",timeout=60000); pg.wait_for_timeout(600)
            ec.open_object_screen(pg,name); pg.wait_for_timeout(1500)
            info=pg.evaluate("""(grids)=>{
              const present=grids.filter(g=>document.getElementById(g));
              const go=!!document.getElementById('button:form:B');
              const anyGrid=[...document.querySelectorAll("[id$=':T_data']")].map(e=>e.id);
              const newBtn=[...document.querySelectorAll("a[title*='New'],button[title*='New']")].length;
              return {present,go,anyGrid,newBtn};}""",GRIDS)
            print(f"{bf} {name}: go={info['go']} present={info['present']} allgrids={info['anyGrid']} newbtns={info['newBtn']}")
        except Exception as e:
            print(f"{bf} {name}: ERR {repr(e)[:80]}")
    b.close()
