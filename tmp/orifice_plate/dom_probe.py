"""Dump EVERY input/select/textarea in the Orifice Plate New-Object form with id, tag, type, and
background-color (mandatory=yellow). Reveals how numeric fields (Diameter, Measurement Temp) are
structured so the generic mandatory-scanner can catch them. Read-only."""
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
    ec.open_object_screen(pg, "Orifice Plate"); ec.click_go(pg); ec._open_new_object(pg); pg.wait_for_timeout(600)
    rows = pg.evaluate("""()=>{
      const root=document.querySelector('[id*=":objectForm:form:"]') || document;
      const els=root.querySelectorAll('input,select,textarea');
      const out=[];
      els.forEach(e=>{
        const bg=getComputedStyle(e).backgroundColor;
        const yellow=bg.includes('252, 249, 192');
        // find nearest ECCell label in the same tableRow
        let lbl='';
        const row=e.closest('.tableRow')||e.closest('tr');
        if(row){const s=row.querySelector('span.ECCell, span[class*=ECCell]'); if(s) lbl=(s.innerText||'').trim();}
        out.push({id:e.id, tag:e.tagName.toLowerCase(), type:e.type||'', vis:e.offsetParent!==null, yellow, bg, label:lbl.slice(0,26)});
      });
      return out;}""")
    print("=== all form inputs (visible + mandatory flagged) ===")
    for r in rows:
        if r["vis"] and r["type"] not in ("hidden",):
            print("  yellow=%-5s %-10s type=%-8s label=%-26s id=%s" % (r["yellow"], r["tag"], r["type"], r["label"], r["id"]))
    br.close()
