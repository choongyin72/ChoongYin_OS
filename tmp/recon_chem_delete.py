# Recon Chemical Product delete flow: insert AUTOTEST, attempt End=Start, capture child-FK, look for a UI child grid/tab.
import sys, time
from pathlib import Path
from playwright.sync_api import sync_playwright
EC=Path(r"C:\Projects\ChoongYin_OS\workstreams\master-plan\ec-automation"); sys.path.insert(0,str(EC/"py"))
import ec_object_iud as ec
URL="https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"
GRID="manage_object_nav_nav:form:T_data"
CODE="AUTOTEST_CHP_RECON1"
with sync_playwright() as p:
    b=p.chromium.launch(headless=True,args=["--ignore-certificate-errors"])
    pg=b.new_context(ignore_https_errors=True,viewport={"width":1920,"height":1080}).new_page()
    ec.login(pg,URL,"sysadmin","sysadmin")
    ec.open_object_screen(pg,"Chemical Product"); pg.wait_for_timeout(1200)
    ec.click_go(pg); pg.wait_for_timeout(1000)
    ec._open_new_object(pg); pg.wait_for_timeout(1200)
    flds=pg.evaluate("""()=>{const o=[];const b='tab:tabPanel:objectForm:form:G:0:R:';
      for(let r=0;r<12;r++){for(const s of ['C:1:in','C:1:da_input','C:1:dd_input','C:1:pin']){
        if(document.getElementById(b+r+':'+s)){const lc=document.getElementById(b+r+':C:0')||document.querySelector('[id^="'+b+r+':C:0"]');
          o.push({r,kind:s.split(':').pop(),lbl:(lc?(lc.innerText||'').trim():'')});break;}}}return o;}""")
    print("insert fields:", [(f["kind"],f["lbl"]) for f in flds])
    # try insert (Code/Name/Start + first dropdown first-available)
    try:
        r=ec._resolve_field(pg,"objectForm",flds[0]["lbl"]); ec.fill_field(pg,r["id"],CODE,"text")
        nm=next((f for f in flds if f["kind"]=="in" and f["lbl"]!=flds[0]["lbl"]),None)
        if nm: rr=ec._resolve_field(pg,"objectForm",nm["lbl"]); ec.fill_field(pg,rr["id"],"AUTOTEST Chem Recon","text")
        dt=next((f for f in flds if f["kind"]=="da_input"),None)
        if dt: rd=ec._resolve_field(pg,"objectForm",dt["lbl"]); ec.fill_field(pg,rd["id"],"2000-01-01","date")
        dd=next((f for f in flds if f["kind"]=="dd_input"),None)
        if dd: rdd=ec._resolve_field(pg,"objectForm",dd["lbl"]); ec.fill_field(pg,rdd["id"],"__FIRST__","dropdown")
        ec.save(pg); print("insert save issued; ec_error:", repr(ec.ec_error(pg))[:100]); ec.click_go(pg); pg.wait_for_timeout(1200)
    except Exception as e:
        print("insert err:", repr(e)[:120])
    # attempt delete via End=Start + capture error
    try:
        ec.closeObjectRecord(pg, GRID, CODE, "01-Jan-2000"); print("delete issued; ec_error:", repr(ec.ec_error(pg))[:160])
    except Exception as e:
        print("delete err:", repr(e)[:160])
    # look for child tabs/grids on the screen (usage report config)
    tabs=pg.evaluate("""()=>{const t=[...document.querySelectorAll("a[role='tab'], .ui-tabs-anchor, li[role='tab']")].map(x=>(x.innerText||'').trim()).filter(Boolean);
       const grids=[...document.querySelectorAll("[id$=':T_data']")].map(g=>g.id);
       return {tabs:t.slice(0,12), grids};}""")
    print("screen tabs:", tabs["tabs"]); print("screen grids:", tabs["grids"])
    b.close()
