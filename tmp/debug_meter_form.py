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
    ec.open_object_screen(pg,"Meter"); pg.wait_for_timeout(1200)
    ec.select_dropdown(pg,"nav:form:G:0:R:1:C:1:dd","__FIRST__"); pg.wait_for_timeout(500)
    ec.click_go(pg); pg.wait_for_timeout(1500)
    ec._open_new_object(pg); pg.wait_for_timeout(1500)
    dump=pg.evaluate("""() => {
      const out=[]; const base='tab:tabPanel:objectForm:form:G:0:R:';
      for(let r=0;r<14;r++){
        const kinds=[];
        for(const suf of ['C:1:in','C:1:da_input','C:1:dd_input','C:1:pin','C:1:pinB','C:1:dd_button']){
          if(document.getElementById(base+r+':'+suf)) kinds.push(suf);}
        const lc=document.getElementById(base+r+':C:0')||document.querySelector('[id^="'+base+r+':C:0"]');
        const lbl=lc?(lc.innerText||'').trim():'(no label cell)';
        if(kinds.length||lc) out.push({r, lbl, kinds});
      }
      // also: does ANY objectForm exist? list distinct form keys present
      const forms=[...new Set([...document.querySelectorAll("[id*=':form:G:0:R:0:C:0']")].map(e=>e.id.split(':form:')[0]))];
      return {rows:out, formsPresent:forms.slice(0,8)};
    }""")
    print("forms present:", dump["formsPresent"])
    for row in dump["rows"]: print("  R%s | %-28s | %s" % (row["r"], row["lbl"][:28], row["kinds"]))
    b.close()
