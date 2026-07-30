# Validate the generic Playwright popup handler across several screens (resolve-by-label + pick first-available; NO Save).
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright
EC=Path(r"C:\Projects\ChoongYin_OS\workstreams\master-plan\ec-automation"); sys.path.insert(0,str(EC/"py"))
import ec_object_iud as ec
URL="https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"
SCREENS=["Carrier","Customer","Company Contact","Analysis Point","Chemical Product"]
with sync_playwright() as p:
    b=p.chromium.launch(headless=True,args=["--ignore-certificate-errors"])
    pg=b.new_context(ignore_https_errors=True,viewport={"width":1920,"height":1080}).new_page()
    ec.login(pg,URL,"sysadmin","sysadmin")
    for scr in SCREENS:
        try:
            pg.goto(URL,wait_until="networkidle",timeout=60000); pg.wait_for_timeout(500)
            ec.open_object_screen(pg,scr); pg.wait_for_timeout(1200)
            ec._open_new_object(pg); pg.wait_for_timeout(1200)
            pins=pg.evaluate("""() => { const out=[]; const base='tab:tabPanel:objectForm:form:G:0:R:';
              for(let r=0;r<20;r++){ if(document.getElementById(base+r+':C:1:pin')){
                const lc=document.getElementById(base+r+':C:0')||document.querySelector('[id^="'+base+r+':C:0"]');
                out.push({r, lbl:(lc?(lc.innerText||'').trim():'')}); } } return out; }""")
            if not pins:
                print(f"{scr}: no pin/pinB popup fields on New form (dropdowns/other)"); continue
            lbl=pins[0]["lbl"]
            r=ec._resolve_field(pg,"objectForm",lbl)
            tag=f"{scr}: popup field '{lbl}' -> kind={r and r['kind']}"
            try:
                ec.pick_popup(pg, r["id"], "__FIRST__")
                val=pg.eval_on_selector(ec._css(r["id"]),"e=>e.value")
                print(f"{tag} | pick first -> {val!r}  => {'PASS' if val and val.strip() else 'EMPTY'}")
            except Exception as e:
                print(f"{tag} | pick FAILED (likely empty source/nav-scope): {repr(e)[:80]}")
        except Exception as e:
            print(f"{scr}: could not open/new-form: {repr(e)[:90]}")
    b.close()
