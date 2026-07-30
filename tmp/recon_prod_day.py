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
    ec.open_object_screen(pg,"Production Day Table"); pg.wait_for_timeout(1500)
    # toolbar: is Delete enabled? + New present?
    tb=pg.evaluate("""()=>{
      const del=[...document.querySelectorAll("[class*='ui-icon-delete']")].map(e=>({vis:e.offsetParent!==null}));
      const ins=[...document.querySelectorAll("[class*='ui-icon-insert']")].length;
      const grids=[...document.querySelectorAll("[id$=':T_data']")].map(t=>t.id);
      return {delete_icons:del.length, insert_icons:ins, grids};}""")
    print("toolbar:", tb)
    try:
        ec._open_new_object(pg); pg.wait_for_timeout(1200)
        fields=pg.evaluate("""()=>{const o=[];const b='tab:tabPanel:objectForm:form:G:0:R:';
          for(let r=0;r<14;r++){for(const s of ['C:1:in','C:1:da_input','C:1:dd_input','C:1:pin']){
            if(document.getElementById(b+r+':'+s)){const lc=document.getElementById(b+r+':C:0')||document.querySelector('[id^="'+b+r+':C:0"]');
              o.push({r,kind:s.split(':').pop(),lbl:(lc?(lc.innerText||'').trim():'')});break;}}}return o;}""")
        print("New-form fields:")
        for f in fields: print("  R%s %-10s %s" % (f["r"], f["kind"], f["lbl"]))
    except Exception as e:
        print("New form:", repr(e)[:100])
    b.close()
