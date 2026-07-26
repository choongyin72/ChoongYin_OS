"""READ-ONLY recon for Berth (CD.0099, OV_FIN_UOP_DEPR_KEY): DB columns + treeview path +
live New-Object form (labels/mandatory/kind) + grid behavior. No writes. tmp scratch."""
import os, sys, json
from pathlib import Path
from playwright.sync_api import sync_playwright
import oracledb

EC = Path(r"C:\Projects\ChoongYin_OS\workstreams\master-plan\ec-automation")
sys.path.insert(0, str(EC / "py"))
import ec_object_iud as ec

def db():
    return oracledb.connect(user=os.environ.get("EC_DB_USER","ECKERNEL_EC"),
                            password=os.environ.get("EC_DB_PASS","energy"),
                            dsn=os.environ.get("EC_DB_DSN","localhost:1521/ORCL"))

# --- columns ---
con = db(); cur = con.cursor()
cur.execute("""select column_name,data_type,nullable from all_tab_columns
               where table_name='OV_FIN_UOP_DEPR_KEY' order by column_id""")
print("=== OV_FIN_UOP_DEPR_KEY columns ===")
for c in cur.fetchall(): print(f"  {c[0]:<24} {c[1]:<10} null={c[2]}")
# --- row count (real data present?) ---
try:
    cur.execute("select count(*) from OV_FIN_UOP_DEPR_KEY"); print("OV_FIN_UOP_DEPR_KEY row count:", cur.fetchone()[0])
except Exception as e:
    print("count err:", repr(e)[:120])
# --- treeview path (screen CD.0099) ---
cur.execute("select CONFIGURATION from TV_CTRL_CONFIGURATION_STORAGE where NAME='DefaultScreenTreeview'")
raw = cur.fetchone()[0]
if hasattr(raw,"read"): raw = raw.read()
con.close()
data = json.loads(raw); hits=[]
def walk(n,path):
    lbl=n.get("label"); np=path+([lbl] if lbl else [])
    if n.get("screen")=="CD.0099": hits.append(np)
    for c in n.get("children",[]) or []:
        if isinstance(c,dict): walk(c,np)
for r in data["configuration"]["items"]: walk(r,[])
print("\nTREEVIEW PATH (CD.0099):", " > ".join(hits[0]) if hits else "NOT FOUND")

URL="https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"
with sync_playwright() as p:
    br=p.chromium.launch(headless=True,args=["--ignore-certificate-errors"])
    pg=br.new_context(ignore_https_errors=True,viewport={"width":1920,"height":1080}).new_page()
    ec.login(pg,URL,"sysadmin","sysadmin")
    print("\nscreen:", ec.open_object_screen(pg,"UOP Key"))
    ec.click_go(pg)
    rows=ec._rows(pg,"manage_object_nav_nav:form:T_data")
    print("grid rows after GO (first col, up to 8):", [r[0] for r in rows[:8]] if rows else "(none)")
    # pagination?
    try:
        print("paginator pages:", pg.locator("css=.ui-paginator-page").count())
    except Exception: pass
    ec._open_new_object(pg)
    fields=pg.evaluate("""()=>{const base='tab:tabPanel:objectForm:form:G:0:R:';const out=[];
      for(let r=0;r<24;r++){const inn=document.getElementById(base+r+':C:1:in');
        const dai=document.getElementById(base+r+':C:1:da_input');const ddi=document.getElementById(base+r+':C:1:dd_input');
        let el=null,kind='';if(inn){el=inn;kind='text';}else if(dai){el=dai;kind='date';}else if(ddi){el=ddi;kind='DROPDOWN';}
        if(!el)continue;
        const lc=document.getElementById(base+r+':C:0')||document.querySelector('[id^="'+base+r+':C:0"]');
        const label=lc?(lc.innerText||'').trim():'';
        const yellow=getComputedStyle(el).backgroundColor.includes('252, 249, 192');
        out.push({r,label:label.slice(0,26),kind,mandatory:yellow});}return out;}""")
    print("\n=== New Object form (objectForm) ===")
    for f in fields: print(f"  R{f['r']:<2} {f['label']:<26} {f['kind']:<9} mandatory={f['mandatory']}")
    dd=[f for f in fields if f["kind"]=="DROPDOWN" and f["mandatory"]]
    print("\nMANDATORY DROPDOWNS:", [f["label"] for f in dd] if dd else "NONE -> engine handles as-is (plain)")
    br.close()
print("\n(READ-ONLY, no save)")
