"""Read-only probe: what does the Node New-Object 'Op Production Unit' panel actually offer
after nav cascade + Start Date=2000-01-01? Compare to the captured nav C1 PU. NEVER saves."""
import sys
from pathlib import Path
EC = Path(r"C:\Projects\ChoongYin_OS\workstreams\master-plan\ec-automation")
sys.path.insert(0, str(EC / "py"))
import ec_object_iud as ec
from playwright.sync_api import sync_playwright

URL = "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"
OP_PU_DD = "tab:tabPanel:objectForm:form:G:0:R:15:C:1:dd"   # from scan
START_ID = "tab:tabPanel:objectForm:form:G:0:R:3:C:1:da_input"

with sync_playwright() as p:
    br = p.chromium.launch(headless=True, args=["--ignore-certificate-errors"])
    pg = br.new_context(ignore_https_errors=True, viewport={"width": 1920, "height": 1080}).new_page()
    ec.login(pg, URL, "sysadmin", "sysadmin")
    ec.open_object_screen(pg, "Node")
    pu = ec.apply_ovgm_navigator(pg)
    print("nav C1 PU =", repr(pu))
    ec._open_new_object(pg); pg.wait_for_timeout(800)
    # set start date first (Op PU is date-filtered)
    ec.fill_field(pg, START_ID, "2000-01-01", "date"); pg.wait_for_timeout(800)
    # open Op PU panel + dump options
    pg.locator(ec._css(OP_PU_DD + "_button")).first.click(); pg.wait_for_timeout(1500)
    opts = pg.evaluate("""(p)=>{const pan=document.getElementById(p+'_panel'); if(!pan) return null;
        return Array.from(pan.querySelectorAll('tr[data-item-label]')).map(t=>t.getAttribute('data-item-label'));}""", OP_PU_DD)
    print("Op PU panel option count:", None if opts is None else len(opts))
    if opts:
        print("first 8 options (repr, to expose whitespace):")
        for o in opts[:8]:
            print("   ", repr(o))
        norm = [ " ".join(o.split()) for o in opts ]
        print("nav PU present (normalized match)?", (pu and " ".join(pu.split()) in norm))
        print("first option normalized == nav PU?", (opts and " ".join(opts[0].split()) == " ".join((pu or '').split())))
    br.close()
