"""Clean AUTOTEST_CP_001 via REAL KEYSTROKES on End Date (click, Ctrl+A, type, Tab) instead of .fill().
If object_end_date persists -> both cleans AND reveals the fix for date-close on this screen."""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright
EC = Path(r"C:\Projects\ChoongYin_OS\workstreams\master-plan\ec-automation")
sys.path.insert(0, str(EC / "py")); sys.path.insert(0, str(EC / "libraries"))
import ec_object_iud as ec
import oracledb
URL = "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"
GRID = "manage_object_nav_nav:form:T_data"; CODE = "AUTOTEST_CP_001"
EID = "tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input"
def enddate():
    c=oracledb.connect(user='ECKERNEL_EC',password='energy',dsn='localhost:1521/ORCL');cur=c.cursor()
    cur.execute("select object_end_date from ov_chem_product where code=:1",[CODE]); r=cur.fetchone(); c.close()
    return (r[0] if r else "ABSENT")
with sync_playwright() as p:
    br = p.chromium.launch(headless=True, args=["--ignore-certificate-errors"])
    pg = br.new_context(ignore_https_errors=True, viewport={"width": 1920, "height": 1080}).new_page()
    ec.login(pg, URL, "sysadmin", "sysadmin")
    ec.open_object_screen(pg, "Chemical Product"); ec.click_go(pg)
    ec.select_row(pg, GRID, CODE); pg.wait_for_timeout(600)
    fld = pg.locator(ec._css(EID))
    fld.click(); pg.keyboard.press("Control+A"); pg.keyboard.type("2000-01-01"); pg.keyboard.press("Tab")
    pg.wait_for_timeout(600)
    print("val:", fld.input_value())
    print("save:", ec.save(pg), "err:", repr(ec.ec_error(pg)))
    ec.click_go(pg); pg.wait_for_timeout(800)
    print("DB end_date:", enddate())
    br.close()
