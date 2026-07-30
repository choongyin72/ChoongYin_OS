import sys
from pathlib import Path
from playwright.sync_api import sync_playwright
EC = Path(r"C:\Projects\ChoongYin_OS\workstreams\master-plan\ec-automation"); sys.path.insert(0, str(EC / "py"))
import ec_object_iud as ec
URL = "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"
with sync_playwright() as p:
    b = p.chromium.launch(headless=True, args=["--ignore-certificate-errors"])
    pg = b.new_context(ignore_https_errors=True, viewport={"width":1920,"height":1080}).new_page()
    ec.login(pg, URL, "sysadmin", "sysadmin")
    ec.open_object_screen(pg, "Production Sub Unit"); pg.wait_for_timeout(1500)
    ec.click_go(pg); pg.wait_for_timeout(1500)
    info = pg.evaluate("""()=>{const ids=['manageObject:form:T_data','manage_object_nav_nav:form:T_data','nav:form:T_data'];
        const present=ids.filter(i=>document.getElementById(i)); 
        const anyT=[...document.querySelectorAll("[id$=':T_data']")].map(e=>e.id);
        return {present, anyT};}""")
    print("grid present:", info["present"])
    print("all T_data grids:", info["anyT"])
    b.close()
