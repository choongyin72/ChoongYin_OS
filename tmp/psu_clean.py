import sys
from pathlib import Path
from playwright.sync_api import sync_playwright
EC = Path(r"C:\Projects\ChoongYin_OS\workstreams\master-plan\ec-automation"); sys.path.insert(0, str(EC / "py"))
import ec_object_iud as ec
URL = "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"
GRID = "manageObject:form:T_data"
with sync_playwright() as p:
    b = p.chromium.launch(headless=True, args=["--ignore-certificate-errors"])
    pg = b.new_context(ignore_https_errors=True, viewport={"width":1920,"height":1080}).new_page()
    ec.login(pg, URL, "sysadmin", "sysadmin")
    ec.open_object_screen(pg, "Production Sub Unit"); pg.wait_for_timeout(1200)
    ec.click_go(pg); pg.wait_for_timeout(1500)
    try:
        ec.closeObjectRecord(pg, GRID, "AUTOTEST_PSU_001", "01-Jan-2000")
        print("closeObjectRecord issued")
    except Exception as e:
        print("cleanup ERR:", repr(e)[:150])
    b.close()
