import sys
from pathlib import Path
from playwright.sync_api import sync_playwright
EC=Path(r"C:\Projects\ChoongYin_OS\workstreams\master-plan\ec-automation"); sys.path.insert(0,str(EC/"py"))
import ec_object_iud as ec
URL="https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"
def try_screen(pg, scr, label, nav=None):
    try:
        pg.goto(URL,wait_until="networkidle",timeout=60000); pg.wait_for_timeout(500)
        ec.open_object_screen(pg,scr); pg.wait_for_timeout(1200)
        if nav:
            ec.select_dropdown(pg,nav[0],nav[1]); pg.wait_for_timeout(500); ec.click_go(pg); pg.wait_for_timeout(1200)
        ec._open_new_object(pg); pg.wait_for_timeout(1200)
        r=ec._resolve_field(pg,"objectForm",label)
        if not (r and r["kind"]=="popup"): print(f"{scr}: '{label}' not popup ({r})"); return
        ec.pick_popup(pg, r["id"], "__FIRST__")
        val=pg.eval_on_selector(ec._css(r["id"]),"e=>e.value")
        print(f"{scr}: pick '{label}' -> {val!r}  => {'PASS' if val and val.strip() else 'EMPTY'}")
    except Exception as e:
        print(f"{scr}: {repr(e)[:110]}")
with sync_playwright() as p:
    b=p.chromium.launch(headless=True,args=["--ignore-certificate-errors"])
    pg=b.new_context(ignore_https_errors=True,viewport={"width":1920,"height":1080}).new_page()
    ec.login(pg,URL,"sysadmin","sysadmin")
    try_screen(pg,"Meter","Delivery Point Name",nav=("nav:form:G:0:R:1:C:1:dd","ECP Norway"))
    try_screen(pg,"Analysis Point","Facility Object Link")
    b.close()
