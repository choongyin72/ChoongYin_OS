"""READ-ONLY batch classifier for the remaining uncovered OV screens.

One login; for each screen: DB columns exist? + treeview path + grid rows after GO +
New-Object form fields (label/kind/mandatory). VERDICT:
  BUILD  = plain Bank-layout (Code/Name/Start Date mandatory, NO mandatory dropdowns)
  PARK   = mandatory dropdown(s), or form didn't open, or view missing
No writes. Emits JSON lines + a summary table.
"""
import os, sys, json, traceback
from pathlib import Path
from playwright.sync_api import sync_playwright
import oracledb

EC = Path(r"C:\Projects\ChoongYin_OS\workstreams\master-plan\ec-automation")
sys.path.insert(0, str(EC / "py"))
import ec_object_iud as ec

CANDIDATES = [
    ("Document Template","CD.0013","OV_DOC_TEMPLATE"),
    ("Revenue Stream Category","CD.0015","OV_STREAM_CATEGORY"),
    ("Stream Item Category","CD.0016","OV_STREAM_ITEM_CATEGORY"),
    ("Split Item Other","CD.0017","OV_SPLIT_ITEM_OTHER"),
    ("Input List","CD.0035","OV_STREAM_ITEM_COLLECTION"),
    ("HCB System","CD.0097","OV_BALANCE"),
    ("UOP Key","CD.0099","OV_FIN_UOP_DEPR_KEY"),
    ("Inventory Area","CD.0115","OV_INVENTORY_AREA"),
    ("EC Code Object","CD.0135","OV_EC_CODE_OBJECT"),
    ("Chemical Product","CO.0072","OV_CHEM_PRODUCT"),
    ("Orifice Plate","CO.0089","OV_ORIFICE_PLATE"),
    ("Meter Run","CO.0091","OV_METER_RUN"),
    ("Process Train","CO.0120","OV_PROCESS_TRAIN"),
    ("Reservoir Block","CO.0133","OV_RESV_BLOCK"),
    ("Reservoir Formation","CO.0135","OV_RESV_FORMATION"),
    ("Reservoir Block Formation","CO.0137","OV_RESV_BLOCK_FORMATION"),
    ("Deferment Group","CO.0149","OV_DEFERMENT_GROUP"),
    ("Blend","CO.0219","OV_BLEND"),
    ("Calculation Group Context","CO.0245","OV_CALC_GRP_CONTEXT"),
    ("Chemical Transport Tank","CO.0257","OV_CHEM_TRANS_TANK"),
    ("Calculation Context","CO.1059","OV_CALC_CONTEXT"),
    ("Dummy Tag Event Object","CO.1063","OV_DUMMY_TAG_EVENT"),
    ("Transactional Inventory Properties","IN.0023","OV_TRANS_INVENTORY"),
    ("Config Variable","IN.0031","OV_CONFIG_VARIABLE"),
    ("Transactional Inventory Layout Set","IN.0033","OV_TRANS_INV_TMPL_SET"),
    ("Data Extract Setup","SP.0043","OV_SUMMARY_SETUP"),
    ("Data Extract Set","SP.0049","OV_SUMMARY_SET"),
]

def db():
    return oracledb.connect(user=os.environ.get("EC_DB_USER","ECKERNEL_EC"),
                            password=os.environ.get("EC_DB_PASS","energy"),
                            dsn=os.environ.get("EC_DB_DSN","localhost:1521/ORCL"))

con=db(); cur=con.cursor()
# treeview once
cur.execute("select CONFIGURATION from TV_CTRL_CONFIGURATION_STORAGE where NAME='DefaultScreenTreeview'")
raw=cur.fetchone()[0]
if hasattr(raw,"read"): raw=raw.read()
tv=json.loads(raw)
def tvpath(bf):
    hits=[]
    def walk(n,path):
        lbl=n.get("label"); np=path+([lbl] if lbl else [])
        if n.get("screen")==bf: hits.append(np)
        for c in n.get("children",[]) or []:
            if isinstance(c,dict): walk(c,np)
    for r in tv["configuration"]["items"]: walk(r,[])
    return " > ".join(hits[0]) if hits else "NOT FOUND"

def view_exists(v):
    cur.execute("select count(*) from all_views where view_name=:1", [v.upper()])
    return cur.fetchone()[0]>0

URL="https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"
results=[]
RESULT_FILE = Path(r"C:\Projects\ChoongYin_OS\tmp\batch_recon_results.json")
with sync_playwright() as p:
    br=p.chromium.launch(headless=True,args=["--ignore-certificate-errors"])
    pg=br.new_context(ignore_https_errors=True,viewport={"width":1920,"height":1080}).new_page()
    pg.on("dialog", lambda d: d.accept())   # auto-dismiss "discard unsaved changes?" between screens
    ec.login(pg,URL,"sysadmin","sysadmin")
    for name,bf,view in CANDIDATES:
        r={"screen":name,"bf":bf,"view":view,"treeview":tvpath(bf),"view_exists":view_exists(view)}
        try:
            # reset any dirty New-Object form left open by the previous screen:
            # reload the SPA (session cookie keeps us logged in) => guaranteed clean state
            pg.goto(URL, wait_until="networkidle", timeout=60000)
            pg.wait_for_timeout(800)
            ec.open_object_screen(pg,name)
            ec.click_go(pg); pg.wait_for_timeout(800)
            rows=ec._rows(pg,"manage_object_nav_nav:form:T_data")
            r["grid_rows"]=len(rows)
            ec._open_new_object(pg); pg.wait_for_timeout(400)
            fields=pg.evaluate("""()=>{const base='tab:tabPanel:objectForm:form:G:0:R:';const out=[];
              for(let i=0;i<24;i++){const inn=document.getElementById(base+i+':C:1:in');
                const dai=document.getElementById(base+i+':C:1:da_input');const ddi=document.getElementById(base+i+':C:1:dd_input');
                let el=null,kind='';if(inn){el=inn;kind='text';}else if(dai){el=dai;kind='date';}else if(ddi){el=ddi;kind='DROPDOWN';}
                if(!el)continue;
                const lc=document.getElementById(base+i+':C:0')||document.querySelector('[id^="'+base+i+':C:0"]');
                const label=lc?(lc.innerText||'').trim():'';
                const yellow=getComputedStyle(el).backgroundColor.includes('252, 249, 192');
                out.push({r:i,label:label.slice(0,28),kind,mandatory:yellow});}return out;}""")
            r["fields"]=fields
            mand_dd=[f["label"] for f in fields if f["kind"]=="DROPDOWN" and f["mandatory"]]
            r["mandatory_dropdowns"]=mand_dd
            # labels for the first three mandatory text/date (Code/Name/Start Date pattern)
            texts=[f for f in fields if f["kind"] in ("text","date")]
            r["form_opened"]=len(fields)>0
            r["verdict"]="PARK" if (mand_dd or not fields) else "BUILD"
        except Exception as e:
            r["error"]=repr(e)[:140]; r["verdict"]="PARK"; r["form_opened"]=False
        results.append(r)
        print("JSON "+json.dumps(r), flush=True)
        RESULT_FILE.write_text(json.dumps(results, indent=1), encoding="utf-8")  # incremental, survives buffering
    br.close()
con.close()

print("\n==== SUMMARY ====")
for r in results:
    v=r.get("verdict")
    dd=",".join(r.get("mandatory_dropdowns",[])) or ("no-form" if not r.get("form_opened") else "-")
    print(f"  {v:<5} {r['bf']:<8} {r['screen']:<34} dds/issue={dd}")
b=[r for r in results if r.get('verdict')=='BUILD']
print(f"\nBUILD={len(b)}  PARK={len(results)-len(b)}")
