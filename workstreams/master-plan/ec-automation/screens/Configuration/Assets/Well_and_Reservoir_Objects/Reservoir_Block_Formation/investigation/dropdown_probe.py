import os
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright
EC=Path(r"C:\Projects\ChoongYin_OS\workstreams\master-plan\ec-automation"); sys.path.insert(0,str(EC/"py"))
import ec_object_iud as ec
with sync_playwright() as p:
    b=p.chromium.launch(headless=True,args=["--ignore-certificate-errors"])
    pg=b.new_context(ignore_https_errors=True,viewport={"width":1920,"height":1080}).new_page()
    ec.login(pg, "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/", os.environ.get("EC_USER", "sysadmin"), os.environ.get("EC_PASS", "sysadmin"))
    ec.open_object_screen(pg,"Reservoir Block Formation"); ec.click_go(pg); ec._open_new_object(pg); pg.wait_for_timeout(600)
    for lbl,rid in [("Reservoir Block","R:8"),("Reservoir Formation","R:9")]:
        r=ec._resolve_field(pg,"objectForm",lbl)
        if not r: print(lbl,"NOT RESOLVED"); continue
        pfx=r["id"][:-6]
        pg.locator("css=[id=\"%s_button\"]"%pfx).first.click(); pg.wait_for_timeout(900)
        opts=pg.evaluate("(p)=>{const pan=document.getElementById(p+'_panel');if(!pan)return[];return Array.from(pan.querySelectorAll('tr[data-item-label]')).map(t=>t.getAttribute('data-item-label').trim()).slice(0,6);}",pfx)
        print(lbl,"first options:",opts)
        pg.keyboard.press("Escape"); pg.wait_for_timeout(300)
    b.close()
