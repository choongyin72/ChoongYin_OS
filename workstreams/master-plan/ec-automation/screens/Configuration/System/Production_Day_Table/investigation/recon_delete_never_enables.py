import os, sys
sys.path.insert(0, r"C:\Projects\ChoongYin_OS\workstreams\master-plan\ec-automation\py")
import ec_object_iud as ec
from playwright.sync_api import sync_playwright

URL = os.environ.get("EC_URL", "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/")
USER = os.environ.get("EC_USER", "sysadmin")
PW = os.environ.get("EC_PASS", "sysadmin")

with sync_playwright() as p:
    br = p.chromium.launch(headless=True, args=["--ignore-certificate-errors"])
    pg = br.new_context(ignore_https_errors=True, viewport={"width": 1920, "height": 1080}).new_page()
    ec.login(pg, URL, USER, PW)
    ec.open_object_screen(pg, "Production Day Table")
    pg.wait_for_timeout(1500)

    for row in [3, 7, 15]:
        tr_loc = pg.locator('css=[id="production_day:form:T:%d:C0_in"]' % row).locator("xpath=ancestor::tr[1]")
        if tr_loc.count() == 0:
            print(row, "no such row")
            continue
        box = tr_loc.bounding_box()
        pg.mouse.click(box["x"] + box["width"] - 5, box["y"] + box["height"] / 2)
        ec.wait_ajax(pg)
        pg.wait_for_timeout(600)
        cls = pg.locator("xpath=//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'ui-icon-delete')]]").first.get_attribute("class")
        print(row, "delete class:", cls)

    br.close()
