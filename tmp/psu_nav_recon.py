import sys
from pathlib import Path
from playwright.sync_api import sync_playwright
EC=Path(r"C:\Projects\ChoongYin_OS\workstreams\master-plan\ec-automation");sys.path.insert(0,str(EC/"py"))
import ec_object_iud as ec
URL="https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"
with sync_playwright() as p:
    b=p.chromium.launch(headless=True,args=["--ignore-certificate-errors"])
    pg=b.new_context(ignore_https_errors=True,viewport={"width":1920,"height":1080}).new_page()
    ec.login(pg,URL,"sysadmin","sysadmin")
    ec.open_object_screen(pg,"Production Sub Unit");pg.wait_for_timeout(1500)
    # dump navigator panel fields (labels + input ids) BEFORE GO
    nav=pg.evaluate("""()=>{
      const out=[];
      document.querySelectorAll("[id^='nav:form'] input, [id^='nav:form'] select").forEach(e=>{
        out.push({id:e.id, tag:e.tagName, type:e.type||'', ph:e.placeholder||''});});
      const labels=[...document.querySelectorAll("[id^='nav:form'] .ECCell, [id^='nav:form'] label")].map(l=>l.textContent.trim()).filter(Boolean);
      const go=!!document.getElementById('button:form:B');
      return {inputs:out.slice(0,20), labels:labels.slice(0,20), go};}""")
    print("GO present:",nav["go"])
    print("nav labels:",nav["labels"])
    print("nav inputs:")
    for i in nav["inputs"]: print("  ",i)
    b.close()
