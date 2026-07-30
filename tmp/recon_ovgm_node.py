# Recon Group-B OV-GM (Node): navigator cascade dds, fill first-available parent->child + GO, grid populate, New-form fields.
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
    # (1) dump navigator dd fields (label + id)
    navs=pg.evaluate("""()=>{const o=[];
      for(let r=0;r<6;r++){const id='nav:form:G:0:R:'+r+':C:1:dd_input';
        if(document.getElementById(id)){const lc=document.getElementById('nav:form:G:0:R:'+r+':C:0')||document.querySelector('[id^="nav:form:G:0:R:'+r+':C:0"]');
          o.push({r,lbl:(lc?(lc.innerText||'').trim():'')});}}return o;}""")
    print("navigator dds:", navs)
    # (2) fill cascade first-available parent->child in row order, then GO
    for n in navs:
        dd="nav:form:G:0:R:%d:C:1:dd" % n["r"]
        try: ec.select_dropdown(pg, dd, "__FIRST__"); pg.wait_for_timeout(700)
        except Exception as e: print(f"  nav fill R{n['r']} ({n['lbl']}) err:", repr(e)[:60])
    ec.click_go(pg); pg.wait_for_timeout(1500)
    # (3) grid populated?
    g=pg.evaluate("""()=>{const t=document.getElementById('manageObject:form:T_data');
      if(!t)return{grid:'absent'}; const rows=[...t.querySelectorAll('tr')].map(r=>(r.innerText||'').trim()).filter(Boolean);
      return{grid:'present', n:rows.length, sample:rows.slice(0,3)};}""")
    print("grid after cascade+GO:", g)
    # (4) New-form fields (identify parent-dd + popups)
    try:
        ec._open_new_object(pg); pg.wait_for_timeout(1200)
        flds=pg.evaluate("""()=>{const o=[];const b='tab:tabPanel:objectForm:form:G:0:R:';
          for(let r=0;r<16;r++){for(const s of ['C:1:in','C:1:da_input','C:1:dd_input','C:1:pin']){
            if(document.getElementById(b+r+':'+s)){const lc=document.getElementById(b+r+':C:0')||document.querySelector('[id^="'+b+r+':C:0"]');
              const y=getComputedStyle(document.getElementById(b+r+':'+s)).backgroundColor.includes('252, 249, 192');
              o.push({r,kind:s.split(':').pop(),lbl:(lc?(lc.innerText||'').trim():''),mand:y});break;}}}return o;}""")
        print("New-form fields:")
        for f in flds: print("   R%s %-9s %-26s %s" % (f["r"],f["kind"],f["lbl"][:26],"[M]" if f["mand"] else ""))
    except Exception as e:
        print("New form:", repr(e)[:90])
    b.close()
