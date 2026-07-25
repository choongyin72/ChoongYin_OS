"""READ-ONLY recon for Disposition Type (CO.0208, OV_DISPOSITION_TYPE).
DB columns + live New-Object form (labels/mandatory/kind) + grid id. No writes. tmp scratch."""
import os, sys
from pathlib import Path
from playwright.sync_api import sync_playwright
import oracledb

EC = Path(r"C:\Projects\ChoongYin_OS\workstreams\master-plan\ec-automation")
sys.path.insert(0, str(EC / "py"))
sys.path.insert(0, str(EC / "libraries"))
import ec_object_iud as ec

# --- DB columns ---
con = oracledb.connect(user=os.environ.get("EC_DB_USER", "ECKERNEL_EC"),
                       password=os.environ.get("EC_DB_PASS", "energy"),
                       dsn=os.environ.get("EC_DB_DSN", "localhost:1521/ORCL"))
cur = con.cursor()
cur.execute("""select column_name, data_type, nullable from all_tab_columns
               where table_name='OV_DISPOSITION_TYPE' order by column_id""")
print("=== OV_DISPOSITION_TYPE columns ===")
for c in cur.fetchall():
    print(f"  {c[0]:<24} {c[1]:<12} null={c[2]}")
con.close()

URL = "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"
with sync_playwright() as p:
    br = p.chromium.launch(headless=True, args=["--ignore-certificate-errors"])
    pg = br.new_context(ignore_https_errors=True, viewport={"width": 1920, "height": 1080}).new_page()
    ec.login(pg, URL, "sysadmin", "sysadmin")
    lbl = ec.open_object_screen(pg, "Disposition Type")
    print("\nscreen label:", lbl)
    # grid id present?
    grid = pg.evaluate("""()=>{const dt=[...document.querySelectorAll('div.ui-datatable[id]')].filter(e=>e.offsetParent!==null);return dt.map(e=>e.id).slice(0,4);}""")
    print("visible datatables:", grid)
    rows = ec._rows(pg, "manage_object_nav_nav:form:T_data")
    print("grid rows (first col, up to 6):", [r[0] for r in rows[:6]] if rows else "(none)")
    # open New Object -> dump objectForm fields
    ec._open_new_object(pg)
    fields = pg.evaluate("""()=>{const base='tab:tabPanel:objectForm:form:G:0:R:';const out=[];
      for(let r=0;r<20;r++){const inn=document.getElementById(base+r+':C:1:in');
        const dai=document.getElementById(base+r+':C:1:da_input');
        const ddi=document.getElementById(base+r+':C:1:dd_input');
        let el=null,kind='';if(inn){el=inn;kind='text';}else if(dai){el=dai;kind='date';}else if(ddi){el=ddi;kind='DROPDOWN';}
        if(!el)continue;
        const lc=document.getElementById(base+r+':C:0')||document.querySelector('[id^="'+base+r+':C:0"]');
        const label=lc?(lc.innerText||'').trim():'';
        const yellow=getComputedStyle(el).backgroundColor.includes('252, 249, 192');
        out.push({r,label:label.slice(0,24),kind,mandatory:yellow});}
      return out;}""")
    print("\n=== New Object form (objectForm) ===")
    for f in fields:
        print(f"  R{f['r']:<2} {f['label']:<24} {f['kind']:<9} mandatory={f['mandatory']}")
    dd = [f for f in fields if f["kind"] == "DROPDOWN" and f["mandatory"]]
    print("\nMANDATORY DROPDOWNS:", [f["label"] for f in dd] if dd else "NONE -> engine handles as-is (plain)")
    br.close()
print("\n(READ-ONLY, no save)")
