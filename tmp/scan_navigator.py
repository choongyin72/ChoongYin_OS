"""READ-ONLY: dump an OV-GM screen's NAVIGATOR panel (the gated cascade fields you must set before GO).
Reports each nav field: id, kind (text/date/dropdown), mandatory (yellow), + first few dropdown options.
Screenshot saved. Feeds the gated-navigator capability. Usage: py tmp/scan_navigator.py '<screen name>'"""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright
EC = Path(r"C:\Projects\ChoongYin_OS\workstreams\master-plan\ec-automation"); sys.path.insert(0, str(EC / "py"))
import ec_object_iud as ec
screen = sys.argv[1]
with sync_playwright() as p:
    b = p.chromium.launch(headless=True, args=["--ignore-certificate-errors"])
    pg = b.new_context(ignore_https_errors=True, viewport={"width": 1920, "height": 1080}).new_page()
    ec.login(pg, "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/", "sysadmin", "sysadmin")
    print("screen:", ec.open_object_screen(pg, screen))
    pg.wait_for_timeout(1200)
    slug = screen.lower().replace(" ", "_")
    Path("tmp/%s" % slug).mkdir(parents=True, exist_ok=True)
    try: pg.screenshot(path="tmp/%s/navigator.png" % slug)
    except Exception: pass
    nav = pg.evaluate("""()=>{
      const out=[];
      document.querySelectorAll('[id^=\"nav:form:\"]').forEach(e=>{
        const tag=e.tagName.toLowerCase(); if(!['input','select','textarea'].includes(tag)) return;
        if(e.type==='hidden'||e.offsetParent===null) return;
        const id=e.id; if(id.endsWith('dd_hinput')) return;
        let kind='text'; if(id.endsWith('da_input'))kind='date'; else if(id.endsWith('dd_input'))kind='dropdown';
        const yellow=getComputedStyle(e).backgroundColor.includes('252, 249, 192');
        // nearest header label
        let lbl=''; const cell=e.closest('.tableCell')||e.closest('td'); 
        if(cell){const row=cell.closest('.tableRow')||cell.closest('tr'); if(row){const h=row.querySelector('span[class*=ECCell]'); if(h)lbl=(h.innerText||'').trim();}}
        out.push({id,kind,mandatory:yellow,label:lbl});
      });
      const go=document.getElementById('button:form:B');
      return {fields:out, go_present:!!go};}""")
    print("GO button present:", nav["go_present"])
    print("=== navigator fields ===")
    for f in nav["fields"]:
        line="  %s %-9s %-22s %s" % ("[M]" if f["mandatory"] else "[ ]", f["kind"], f["label"], f["id"])
        print(line)
        if f["kind"]=="dropdown":
            pfx=f["id"][:-6]
            try:
                pg.locator("css=[id=\"%s_button\"]"%pfx).first.click(); pg.wait_for_timeout(700)
                opts=pg.evaluate("(p)=>{const pan=document.getElementById(p+'_panel');if(!pan)return[];return Array.from(pan.querySelectorAll('tr[data-item-label]')).map(t=>t.getAttribute('data-item-label').trim()).slice(0,5);}",pfx)
                print("        options:",opts); pg.keyboard.press("Escape"); pg.wait_for_timeout(200)
            except Exception as e: print("        (opts err %s)"%repr(e)[:50])
    b.close()
