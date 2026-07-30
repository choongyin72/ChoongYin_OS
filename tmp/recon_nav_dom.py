# Map the navigator DOM of a Group-B OV-GM screen (Node) to identify the cascade dropdowns robustly (labels empty via ECCell).
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
    dump=pg.evaluate("""()=>{
      // every dd_input under nav:form + its nearest text label (try several label sources)
      const out=[];
      document.querySelectorAll("[id^='nav:form'] input[id$='dd_input']").forEach(e=>{
        const id=e.id;
        // label candidates: preceding sibling text, aria-label, a label[for], the row's first cell text
        let lbl=e.getAttribute('aria-label')||'';
        if(!lbl){const row=e.closest('tr')||e.closest("[class*='tableRow']"); if(row){const t=(row.innerText||'').trim(); lbl=t.split('\n')[0];}}
        out.push({id, lbl});
      });
      // also dump ALL nav:form text spans (to see where the labels live)
      const labels=[...document.querySelectorAll("[id^='nav:form'] span, [id^='nav:form'] label")]
        .map(s=>({id:s.id||'', txt:(s.innerText||'').trim()})).filter(x=>x.txt && x.txt.length<30).slice(0,20);
      return {dds:out, labelSpans:labels};}""")
    print("nav dd_inputs + inferred labels:")
    for d in dump["dds"]: print("   ", d["id"], "||", d["lbl"][:40])
    print("\nnav label spans (to locate the real labels):")
    for l in dump["labelSpans"]: print("   ", l["id"], "=", l["txt"])
    b.close()
