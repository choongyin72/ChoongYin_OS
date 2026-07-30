# Map Node's navigator cascade robustly: every nav dd + its label (via multiple label sources), in row order.
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
    m=pg.evaluate("""() => {
      const dds=[...document.querySelectorAll("input[id^='nav:form'][id$='dd_input']")];
      return dds.map(e=>{
        const id=e.id;
        // label sources: the ECCell span in the same nav cell/row, aria-label, prior label text
        let lbl=e.getAttribute('aria-label')||'';
        const cell=e.closest("div[class*='tableCell'], td");
        if(!lbl && cell){ const prev=cell.previousElementSibling; if(prev){ const s=prev.querySelector("span,label"); if(s) lbl=(s.innerText||'').trim(); if(!lbl) lbl=(prev.innerText||'').trim(); } }
        if(!lbl){ const row=e.closest('tr'); if(row){ const s=row.querySelector("span[class*='ECCell']"); if(s) lbl=(s.innerText||'').trim(); } }
        return {id, label:lbl};
      });
    }""")
    print("Node navigator dropdowns (in DOM order):")
    for d in m: print("   ", d["id"], "||", d["label"][:40])
    # also the GO button + grid presence
    extra=pg.evaluate("""()=>({go:!!document.getElementById('button:form:B'), grid:!!document.getElementById('manageObject:form:T_data')})""")
    print("GO present:", extra["go"], "| grid present pre-cascade:", extra["grid"])
    b.close()
