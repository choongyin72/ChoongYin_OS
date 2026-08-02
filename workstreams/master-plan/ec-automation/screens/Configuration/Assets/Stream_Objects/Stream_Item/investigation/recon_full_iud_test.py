import os, sys, time
sys.path.insert(0, r"C:\Projects\ChoongYin_OS\workstreams\master-plan\ec-automation\py")
import ec_object_iud as ec
from playwright.sync_api import sync_playwright

URL = os.environ.get("EC_URL", "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/")
USER = os.environ.get("EC_USER", "sysadmin")
PW = os.environ.get("EC_PASS", "sysadmin")
CODE = "AUTOTEST_SI_%d" % int(time.time())
DESC1 = "AUTOTEST desc v1"
DESC2 = "AUTOTEST desc v2"
START_DATE = "2003-01-01"

POPUP_LABELS = [
    "Stream Item Category", "Product", "Field", "Company", "Stream",
    "Measurement Node", "Calc. Method", "Conversion Method", "Master UOM Group",
    "Daily Accrual Method", "Monthly Accrual Method", "Reporting Category",
]

with sync_playwright() as p:
    br = p.chromium.launch(headless=True, args=["--ignore-certificate-errors"])
    pg = br.new_context(ignore_https_errors=True, viewport={"width": 1920, "height": 1080}).new_page()
    ec.login(pg, URL, USER, PW)
    ec.open_object_screen(pg, "Stream Item")
    pg.locator("#buttongo\:form\:B").click()
    ec.wait_ajax(pg)
    pg.wait_for_timeout(1000)

    # INSERT
    ec._open_new_object(pg)
    pg.wait_for_timeout(800)
    for label, val, kind in [("Stream Item Code", CODE, "text"), ("Start Date", START_DATE, "date"),
                              ("Description", DESC1, "text")]:
        r = ec._resolve_field(pg, "objectForm", label)
        ec.fill_field(pg, r["id"], val, kind)
    for label in POPUP_LABELS:
        r = ec._resolve_field(pg, "objectForm", label)
        ec.fill_field(pg, r["id"], "__FIRST__", r["kind"])
    r = ec._resolve_field(pg, "objectForm", "Name")
    ec.fill_field(pg, r["id"], "AUTOTEST SI NAME (ignored - server-derived)", "text")
    method = ec.save(pg)
    err = ec.ec_error(pg)
    print("INSERT save method:", method, "err:", err)
    pg.wait_for_timeout(1000)

    if not err:
        # UPDATE: re-select the row, go to updateAttributes, change Description
        pg.locator("#buttongo\\:form\\:B").click()
        ec.wait_ajax(pg)
        pg.wait_for_timeout(1000)
        ok = ec.select_row(pg, "nav:form:T_data", CODE)
        print("select_row for update:", ok)
        if ok:
            ru = ec._resolve_field(pg, "updateAttributes", "Description")
            print("update Description field:", ru)
            if ru:
                ec.fill_field(pg, ru["id"], DESC2, ru["kind"])
                ec.save(pg)
                err2 = ec.ec_error(pg)
                print("UPDATE save err:", err2)

        # DELETE (self-clean): End Date = Start Date
        pg.wait_for_timeout(500)
        try:
            ec.closeObjectRecord(pg, "nav:form:T_data", CODE, START_DATE)
            print("DELETE (close) done")
        except Exception as e:
            print("DELETE failed:", e)

    br.close()
print("CODE:", CODE)
