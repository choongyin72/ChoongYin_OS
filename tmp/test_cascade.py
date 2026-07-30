# Test the OV-GM navigator-cascade fill on Node: fill nav dds C1->C2->C3 first-available (parent->child), GO, grid populate?
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright
EC=Path(r"C:\Projects\ChoongYin_OS\workstreams\master-plan\ec-automation"); sys.path.insert(0,str(EC/"py"))
import ec_object_iud as ec
URL="https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"
with sync_playwright() as p:
    b=p.chromium.launch(headless=True,args=["--ignore-certificate-errors"])
    pg=b.new_context(ignore_https_errors=True,viewport={"width":1920,"height":1080}).new_page()
    ec.login(pg,URL,"sysadmin","sysadmin")
    ec.open_object_screen(pg,"Node"); pg.wait_for_timeout(1500)
    picked=[]
    for col in (1,2,3):
        dd="nav:form:G:0:R:1:C:%d:dd_input" % col
        try:
            ec.select_dropdown(pg, dd, "__FIRST__"); pg.wait_for_timeout(900)
            v=pg.eval_on_selector(ec._css(dd),"e=>e.value")
            picked.append((col, v)); print(f"  nav C{col} picked -> {v!r}")
        except Exception as e:
            print(f"  nav C{col} FAILED: {repr(e)[:80]}"); break
    ec.click_go(pg); pg.wait_for_timeout(1800)
    g=pg.evaluate("""()=>{const t=document.getElementById('manageObject:form:T_data');
      if(!t)return{grid:'ABSENT'};const rows=[...t.querySelectorAll('tr')].map(r=>(r.innerText||'').trim()).filter(Boolean);
      return{grid:'present',n:rows.length,sample:rows.slice(0,2)};}""")
    print("after cascade+GO, grid:", g)
    b.close()
