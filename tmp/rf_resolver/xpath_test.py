"""READ-ONLY: validate the label-driven xpath resolves the right input (no row index). Bank form."""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright
EC = Path(r"C:\Projects\ChoongYin_OS\workstreams\master-plan\ec-automation")
sys.path.insert(0, str(EC / "py"))
import ec_object_iud as ec
URL = "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"

def xp(form, label):
    return (f"xpath=//span[contains(@id,':{form}:form:') and contains(@id,':C:0:la')]"
            f"[normalize-space(text())='{label}']/ancestor::div[contains(@class,'tableRow')][1]"
            f"//input")

with sync_playwright() as p:
    br = p.chromium.launch(headless=True, args=["--ignore-certificate-errors"])
    pg = br.new_context(ignore_https_errors=True, viewport={"width":1920,"height":1080}).new_page()
    ec.login(pg, URL, "sysadmin", "sysadmin"); ec.open_object_screen(pg, "Bank"); ec.click_go(pg)
    ec._open_new_object(pg)
    for label, expect in [("Code","R:0:C:1:in"),("Name","R:1:C:1:in"),("Start Date","R:2:C:1:da_input"),("Description","R:4:C:1:in")]:
        loc = pg.locator(xp("objectForm", label).replace("xpath=",""))
        n = loc.count()
        got = loc.first.get_attribute("id") if n else None
        ok = n == 1 and got and got.endswith(expect)
        print(f"  {label:<12} count={n} id_tail={(got or '')[-18:]:<18} -> {'OK' if ok else 'MISMATCH'}")
    br.close()
