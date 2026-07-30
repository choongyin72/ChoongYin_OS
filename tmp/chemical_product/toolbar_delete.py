"""Cleanup + diagnose: does Chemical Product use a TOOLBAR delete (physical) instead of End=Start?
Select AUTOTEST_CP_001, look for an enabled Delete toolbar action, click + confirm + Save, verify DB."""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright
EC = Path(r"C:\Projects\ChoongYin_OS\workstreams\master-plan\ec-automation")
sys.path.insert(0, str(EC / "py")); sys.path.insert(0, str(EC / "libraries"))
import ec_object_iud as ec
import DbVerify as db
URL = "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"
GRID = "manage_object_nav_nav:form:T_data"; CODE = "AUTOTEST_CP_001"
with sync_playwright() as p:
    br = p.chromium.launch(headless=True, args=["--ignore-certificate-errors"])
    pg = br.new_context(ignore_https_errors=True, viewport={"width": 1920, "height": 1080}).new_page()
    ec.login(pg, URL, "sysadmin", "sysadmin")
    ec.open_object_screen(pg, "Chemical Product"); ec.click_go(pg)
    ec.select_row(pg, GRID, CODE); pg.wait_for_timeout(600)
    # enumerate toolbar actions (title + disabled state)
    acts = pg.evaluate("""()=>Array.from(document.querySelectorAll('a[title]')).map(a=>({t:a.getAttribute('title'),
        dis:(a.className||'').includes('ui-state-disabled')})).filter(x=>/delete|remove/i.test(x.t))""")
    print("delete-ish toolbar actions:", acts)
    dele = pg.locator("xpath=//a[contains(@title,'Delete') and not(contains(@class,'ui-state-disabled'))]")
    if dele.count():
        dele.first.click(); ec.wait_ajax(pg); pg.wait_for_timeout(800)
        # a confirm dialog may appear
        yes = pg.locator("xpath=//button[.//span[normalize-space(.)='Yes']] | //a[normalize-space(.)='Yes'] | //button[normalize-space(.)='Yes']")
        if yes.count(): yes.first.click(); ec.wait_ajax(pg); pg.wait_for_timeout(600)
        try: ec.save(pg)
        except Exception as e: print("save:", repr(e)[:80])
        ec.click_go(pg); pg.wait_for_timeout(800)
    print("DB present after toolbar-delete attempt:", db.code_present("ov_chem_product", CODE))
    print("residual AUTOTEST:", db.count_like("ov_chem_product", "AUTOTEST"))
    br.close()
