"""READ-ONLY recon for Input List (CD.0035): confirm form fields + list the VALID options of the
mandatory 'List Category' dropdown (so the IUD test can pick a real value). No writes."""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

EC = Path(r"C:\Projects\ChoongYin_OS\workstreams\master-plan\ec-automation")
sys.path.insert(0, str(EC / "py"))
import ec_object_iud as ec

URL = "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"
with sync_playwright() as p:
    br = p.chromium.launch(headless=True, args=["--ignore-certificate-errors"])
    pg = br.new_context(ignore_https_errors=True, viewport={"width": 1920, "height": 1080}).new_page()
    ec.login(pg, URL, "sysadmin", "sysadmin")
    print("screen:", ec.open_object_screen(pg, "Input List"))
    ec.click_go(pg)
    ec._open_new_object(pg)
    pg.wait_for_timeout(500)
    # dump form fields
    fields = pg.evaluate("""()=>{const base='tab:tabPanel:objectForm:form:G:0:R:';const out=[];
      for(let r=0;r<20;r++){const inn=document.getElementById(base+r+':C:1:in');
        const dai=document.getElementById(base+r+':C:1:da_input');const ddi=document.getElementById(base+r+':C:1:dd_input');
        let el=null,kind='';if(inn){el=inn;kind='text';}else if(dai){el=dai;kind='date';}else if(ddi){el=ddi;kind='DROPDOWN';}
        if(!el)continue;const lc=document.getElementById(base+r+':C:0')||document.querySelector('[id^="'+base+r+':C:0"]');
        const label=lc?(lc.innerText||'').trim():'';
        const yellow=getComputedStyle(el).backgroundColor.includes('252, 249, 192');
        out.push({r,label:label.slice(0,26),kind,mandatory:yellow,id:el.id});}return out;}""")
    print("=== objectForm fields ===")
    for f in fields:
        print(f"  R{f['r']:<2} {f['label']:<26} {f['kind']:<9} mand={f['mandatory']}  id={f['id']}")
    # find the List Category dd + list options
    dd = next((f for f in fields if f["kind"] == "DROPDOWN"), None)
    if dd:
        prefix = dd["id"][:-6] if dd["id"].endswith("_input") else dd["id"]
        print("\nDROPDOWN label=%r prefix=%s" % (dd["label"], prefix))
        try:
            pg.locator("css=[id=\"%s_button\"]" % prefix.replace('"', '')).first.click()
            pg.wait_for_timeout(1200)
            opts = pg.evaluate("""(pfx)=>{const pan=document.getElementById(pfx+'_panel');if(!pan)return[];
              return Array.from(pan.querySelectorAll('tr[data-item-label]')).map(tr=>tr.getAttribute('data-item-label').trim()).slice(0,15);}""", prefix)
            print("OPTIONS (up to 15):", opts)
        except Exception as e:
            print("panel read err:", repr(e)[:150])
    br.close()
print("(READ-ONLY, no save)")
