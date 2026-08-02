import os, sys, time
sys.path.insert(0, r"C:\Projects\ChoongYin_OS\workstreams\master-plan\ec-automation\py")
sys.path.insert(0, r"C:\Projects\ChoongYin_OS\workstreams\master-plan\ec-automation\libraries")
import ec_object_iud as ec
import DbVerify as db
from playwright.sync_api import sync_playwright

URL = os.environ.get("EC_URL", "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/")
USER = os.environ.get("EC_USER", "sysadmin")
PW = os.environ.get("EC_PASS", "sysadmin")
CODE = "AUTOTEST_PDT_%d" % int(time.time())


def type_cell(page, cell_id, value):
    loc = page.locator('css=[id="%s"]' % cell_id)
    loc.click()
    loc.fill("")
    loc.type(value, delay=30)
    page.keyboard.press("Tab")
    ec.wait_ajax(page)
    page.wait_for_timeout(600)


with sync_playwright() as p:
    br = p.chromium.launch(headless=True, args=["--ignore-certificate-errors"])
    pg = br.new_context(ignore_https_errors=True, viewport={"width": 1920, "height": 1080}).new_page()
    ec.login(pg, URL, USER, PW)
    ec.open_object_screen(pg, "Production Day Table")
    pg.wait_for_timeout(1500)

    ins_icon = pg.locator("xpath=//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'ui-icon-insert')]]")
    ins_icon.first.hover()
    item = pg.locator(
        "xpath=//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'ui-icon-insert')]]"
        "//ul[contains(@class,'ui-menu-child')]//a[normalize-space(.)='Production Days']"
    )
    item.first.wait_for(state="visible", timeout=6000)
    item.first.click()
    ec.wait_ajax(pg)
    pg.wait_for_timeout(1500)

    row = pg.evaluate(
        "() => { const m = document.querySelectorAll('input[id^=\"production_day:form:T:\"][id$=\":C0_in\"]');"
        " for (const e of m) { if ((e.value||'') === '') { const r = e.id.match(/:T:(\d+):/); if (r) return parseInt(r[1]); } }"
        " return -1; }"
    )
    base = "production_day:form:T:%d:C" % row
    type_cell(pg, base + "0_in", CODE)
    ec.select_dropdown(pg, base + "1_dd_input", "__FIRST__")
    type_cell(pg, base + "2_da_input", "2003-01-01")
    type_cell(pg, base + "4_in", "AUTOTEST PDT RACE")

    t0 = time.time()
    ec.save(pg)
    err = ec.ec_error(pg)
    print("save err:", err)

    for elapsed_target in [0, 1, 2, 3, 5, 8]:
        while time.time() - t0 < elapsed_target:
            pg.wait_for_timeout(100)
        present = db.code_present("OV_PRODUCTION_DAY", CODE)
        print("t+%ds: code_present=%s" % (elapsed_target, present))

    br.close()
print("CODE:", CODE)
