"""Generate the EC screen deep-dive CHECKLIST.md from BUSINESS_FUNCTION (sandbox). Re-runnable."""
import oracledb
from pathlib import Path
MOD={ "CO":"Core / Common Config","PO":"Production Operations (stream status)","GD":"Gas Dispatch / Nominations",
 "CD":"Config Data (Node/Stream)","WR":"Well & Reservoir","SA":"Sales Accounting / Contract Calc",
 "CP":"Commercial Planning / Lifting","PP":"Production Planning","SP":"Document Management","VO":"Volume / Split Keys",
 "SD":"Sales & Dispatch (Gas)","PR":"Pricing","FC":"Forecast","TO":"Terminal Operations","IN":"Inventory",
 "PT":"Production Testing","MHM":"Message Handling (MHM)","PD":"Production Deferment","RP":"Reporting",
 "PA":"Process Automation","RC":"Royalty / Contract Setup","LM":"Lab & Measurements (Lite)","HA":"Allocation / Status Processes",
 "CM":"Chemical Management","IS":"Integration Services (ECIS)","FI":"Financial Items","CA":"Cargo & Parcel","LA":"Lifting Account","WL":"Workflow / Task List"}
EXCLUDE={"JSF","UPG","XXTEST","ZX"}
con=oracledb.connect(user="ECKERNEL_EC",password="energy",dsn="localhost:1521/ORCL"); cur=con.cursor()
cur.execute("""SELECT CASE WHEN INSTR(bf_code,'.')>0 THEN SUBSTR(bf_code,1,INSTR(bf_code,'.')-1) ELSE '(o)' END pfx,
   bf_code, name, url FROM business_function WHERE bf_code IS NOT NULL ORDER BY bf_code""")
from collections import defaultdict
d=defaultdict(list)
for pfx,code,name,url in cur.fetchall():
    if pfx in EXCLUDE: continue
    d[pfx].append((code,name,url))
con.close()
order=sorted(d, key=lambda k:-len(d[k]))
total=sum(len(v) for v in d.values())
out=["# EC Screen Deep-Dive — Master Checklist","",
 f"_Auto-generated from `BUSINESS_FUNCTION` (sandbox). **{total} screens / {len(d)} modules** (test/framework prefixes excluded)._","",
 "Status key: `[ ]` ready · `[x]` done (note written) · `[~]` in progress · `[-]` skipped (project-customised / N/A).",
 "Per-screen deep-dive = Help (code/desc/screenshots) + DB view (OV_/TV_/DV_, screen type) + live recon. Notes in `notes/<BF_CODE>.md`.",""]
for pfx in order:
    out.append(f"## {pfx} — {MOD.get(pfx,pfx)}  ({len(d[pfx])})")
    for code,name,url in d[pfx]:
        out.append(f"- [ ] **{code}** — {name}")
    out.append("")
Path("DeepDiveLearnings/ec-screens/CHECKLIST.md").write_text("\n".join(out),encoding="utf-8")
print("wrote CHECKLIST.md —",total,"screens,",len(d),"modules")
print("module order:", ", ".join(f"{p}({len(d[p])})" for p in order))
