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
    ec.open_object_screen(pg, "Stream Item")
    pg.locator("#buttongo\:form\:B").click()
    ec.wait_ajax(pg)
    pg.wait_for_timeout(1000)
    ec._open_new_object(pg)
    pg.wait_for_timeout(800)

    rows = pg.evaluate("""() => {
        const base = 'tab:tabPanel:objectForm:form:G:0:R:';
        const out = [];
        for (let r = 0; r < 80; r++) {
            const inn = document.getElementById(base + r + ':C:1:in');
            const dai = document.getElementById(base + r + ':C:1:da_input');
            const ddi = document.getElementById(base + r + ':C:1:dd_input');
            const pin = document.getElementById(base + r + ':C:1:pin');
            const cb  = document.getElementById(base + r + ':C:1:cb');
            let el = null, kind = '';
            if (inn) { el = inn; kind = 'text'; }
            else if (dai) { el = dai; kind = 'date'; }
            else if (ddi) { el = ddi; kind = 'dropdown'; }
            else if (pin) { el = pin; kind = 'popup'; }
            else if (cb) { el = cb; kind = 'checkbox'; }
            if (!el) continue;
            const lc = document.getElementById(base + r + ':C:0') || document.querySelector('[id^="' + base + r + ':C:0"]');
            const label = lc ? (lc.innerText || '').trim() : '';
            const mand = (el.className || '').includes('mandatory') || (el.className || '').includes('Mandatory');
            out.push([r, label, kind, mand]);
        }
        return out;
    }""")
    for row in rows:
        print(row)
    br.close()
