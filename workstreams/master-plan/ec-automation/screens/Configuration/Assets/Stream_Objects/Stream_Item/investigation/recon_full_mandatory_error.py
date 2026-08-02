import os, sys
sys.path.insert(0, r"C:\Projects\ChoongYin_OS\workstreams\master-plan\ec-automation\py")
import ec_object_iud as ec
from playwright.sync_api import sync_playwright

URL = os.environ.get("EC_URL", "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/")
USER = os.environ.get("EC_USER", "sysadmin")
PW = os.environ.get("EC_PASS", "sysadmin")
CODE = "AUTOTEST_SI_008"

with sync_playwright() as p:
    br = p.chromium.launch(headless=True, args=["--ignore-certificate-errors"])
    pg = br.new_context(ignore_https_errors=True, viewport={"width": 1920, "height": 1080}).new_page()
    ec.login(pg, URL, USER, PW)
    ec.open_object_screen(pg, "Stream Item")
    pg.locator("#buttongo\:form\:B").click()
    ec.wait_ajax(pg)
    pg.wait_for_timeout(1000)
    ec._open_new_object(pg)
    pg.wait_for_timeout(800)
    for label, val, kind in [
        ("Stream Item Code", CODE, "text"),
        ("Name", "AUTOTEST SI 008", "text"),
        ("Start Date", "2003-01-01", "date"),
    ]:
        r = ec._resolve_field(pg, "objectForm", label)
        ec.fill_field(pg, r["id"], val, kind)
    ec.save(pg)
    pg.wait_for_timeout(1000)
    full = pg.evaluate(
        "() => { const n = document.getElementById('ECNotificationArea') || document.getElementById('ECClientNotificationArea'); return n ? n.textContent.trim() : 'NONE'; }"
    )
    print("FULL untruncated:")
    print(full)
    br.close()
