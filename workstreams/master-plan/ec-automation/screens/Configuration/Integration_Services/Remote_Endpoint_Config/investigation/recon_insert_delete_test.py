import os, sys, time
sys.path.insert(0, r"C:\Projects\ChoongYin_OS\workstreams\master-plan\ec-automation\py")
import ec_object_iud as ec
from playwright.sync_api import sync_playwright

URL = os.environ.get("EC_URL", "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/")
USER = os.environ.get("EC_USER", "sysadmin")
PW = os.environ.get("EC_PASS", "sysadmin")
CODE = "autotest-rec-%d" % int(time.time())


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
    ec.open_object_screen(pg, "Remote Endpoint Configuration")
    pg.wait_for_timeout(1500)

    ins_icon = pg.locator("xpath=//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'ui-icon-insert')]]")
    ins_icon.first.hover()
    pg.wait_for_timeout(500)
    item = pg.locator(
        "xpath=//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'ui-icon-insert')]]"
        "//ul[contains(@class,'ui-menu-child')]//a"
    ).first
    item.click()
    ec.wait_ajax(pg)
    pg.wait_for_timeout(1000)

    row = pg.evaluate(
        "() => { const m = document.querySelectorAll('input[id^=\"endpointconfig:form:T:\"][id$=\":C0_in\"]');"
        " for (const e of m) { if ((e.value||'') === '') { const parts = e.id.split(':'); return parseInt(parts[3]); } }"
        " return -1; }"
    )
    print("blank row:", row)
    base = "endpointconfig:form:T:%d:C" % row
    type_cell(pg, base + "0_in", CODE)
    type_cell(pg, base + "1_in", "AUTOTEST REC")
    ec.select_dropdown(pg, base + "2_dd_input", "__FIRST__")
    method = ec.save(pg)
    err = ec.ec_error(pg)
    print("save:", method, "err:", err)
    pg.wait_for_timeout(1000)

    if not err:
        # delete (physical, INVARIANT) - select row and use toolbar delete
        row2 = pg.evaluate(
            "(code) => { const m = document.querySelectorAll('input[id^=\"endpointconfig:form:T:\"][id$=\":C0_in\"]');"
            " for (const e of m) { if ((e.value||'') === code) { const parts = e.id.split(':'); return parseInt(parts[3]); } }"
            " return -1; }",
            CODE,
        )
        print("row to delete:", row2)
        cell = pg.locator('css=[id="endpointconfig:form:T:%d:C0_in"]' % row2)
        cell.click()
        pg.wait_for_timeout(400)
        del_icon = pg.locator("xpath=//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'ui-icon-delete')]]")
        del_icon.first.hover()
        pg.wait_for_timeout(500)
        del_items = pg.evaluate(
            "() => Array.from(document.querySelectorAll("
            "\"li.ui-menu-parent:has(span.ui-icon-delete) ul.ui-menu-child a\""
            ")).map(a => a.textContent)"
        )
        print("delete submenu items:", del_items)
        if del_items:
            di = pg.locator(
                "xpath=//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'ui-icon-delete')]]"
                "//ul[contains(@class,'ui-menu-child')]//a"
            ).first
            di.click()
            ec.wait_ajax(pg)
            pg.wait_for_timeout(1000)
            derr = ec.ec_error(pg)
            print("delete err:", derr)
            m2 = ec.save(pg)
            print("save after delete:", m2)
            derr2 = ec.ec_error(pg)
            print("save err:", derr2)

    br.close()
print("CODE:", CODE)
