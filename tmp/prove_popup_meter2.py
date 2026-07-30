import sys
from pathlib import Path
from playwright.sync_api import sync_playwright
EC=Path(r"C:\Projects\ChoongYin_OS\workstreams\master-plan\ec-automation"); sys.path.insert(0,str(EC/"py"))
import ec_object_iud as ec
URL="https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"
with sync_playwright() as p:
    b=p.chromium.launch(headless=True,args=["--ignore-certificate-errors"])
    pg=b.new_context(ignore_https_errors=True,viewport={"width":1920,"height":1080}).new_page()
    ec.login(pg,URL,"sysadmin","sysadmin")
    ec.open_object_screen(pg,"Meter"); pg.wait_for_timeout(1200)
    ec.select_dropdown(pg,"nav:form:G:0:R:1:C:1:dd","ECP Norway"); pg.wait_for_timeout(600)
    ec.click_go(pg); pg.wait_for_timeout(1500)
    ec._open_new_object(pg); pg.wait_for_timeout(1200)
    r=ec._resolve_field(pg,"objectForm","Delivery Point Name")
    print("resolve:", r)
    ec.pick_popup(pg, r["id"], "__FIRST__")
    val=pg.eval_on_selector(ec._css(r["id"]),"e=>e.value")
    print("pin value after first-available pick:", repr(val))
    print("PLAYWRIGHT POPUP PROOF (Meter):", "PASS" if val and val.strip() else "FAIL")
    b.close()
