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
    ec.open_object_screen(pg,"Analysis Point"); pg.wait_for_timeout(1200)
    ec._open_new_object(pg); pg.wait_for_timeout(1200)
    r=ec._resolve_field(pg,"objectForm","Facility Object Link")
    print("resolved:", r)
    pin=r["id"]
    pg.evaluate("(id)=>{const b=document.getElementById(id+'B'); if(b) b.click();}", pin)
    pg.wait_for_timeout(4000)
    info=pg.evaluate("""() => {
      const iframes=[...document.querySelectorAll('iframe')].map(f=>({id:f.id, src:(f.src||'').slice(-60), vis:f.offsetParent!==null}));
      const dlgs=[...document.querySelectorAll("div[role='dialog'], .ui-dialog, [id*='dialog'], [id*='opup']")].filter(d=>d.offsetParent!==null).map(d=>({id:d.id, cls:(d.className||'').slice(0,40)}));
      const grids=[...document.querySelectorAll("[id$=':T_data']")].map(t=>t.id);
      const msg=(document.getElementById('dialogForm:dialogMsg')||{}).innerText||'';
      return {iframes, dlgs, grids, msg:msg.slice(0,120)};
    }""")
    print("after pinB click:")
    print("  iframes:", info["iframes"])
    print("  dialogs:", info["dlgs"])
    print("  grids  :", info["grids"])
    print("  msg    :", repr(info["msg"]))
    b.close()
