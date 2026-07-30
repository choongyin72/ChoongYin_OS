import sys
from pathlib import Path
from playwright.sync_api import sync_playwright
EC=Path(r"C:\Projects\ChoongYin_OS\workstreams\master-plan\ec-automation"); sys.path.insert(0,str(EC/"py"))
import ec_object_iud as ec
with sync_playwright() as p:
    b=p.chromium.launch(headless=True,args=["--ignore-certificate-errors"])
    pg=b.new_context(ignore_https_errors=True,viewport={"width":1920,"height":1080}).new_page()
    ec.login(pg,"https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/","sysadmin","sysadmin")
    si=pg.locator("#menu\:searchForm\:searchTxt"); si.wait_for(state="visible",timeout=30000)
    si.clear(); si.type("Deferment",delay=60); pg.wait_for_timeout(2500)
    labels=pg.eval_on_selector_all("label.tv-link, span.tv-link","els=>els.map(e=>e.textContent.trim())")
    print("tv-link matches for 'Deferment':", labels)
    b.close()
