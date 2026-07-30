import re
from pathlib import Path
PY = Path(r"C:\Projects\ChoongYin_OS\workstreams\master-plan\ec-automation\py")
CRED = re.compile(r"""['"]sysadmin['"]"""); FILL = re.compile(r"""#(?:username|password)['"]\s*,\s*['"][^'"]+['"]""")
ENV_OK = ("os.environ","getenv","EC_USER","EC_PASS","ec_session")
new = ["port","berth","canal","revenue_stream_category","stream_item_category","split_item_other",
       "inventory_area","reservoir_block","reservoir_formation","blend","chemical_transport_tank",
       "calculation_context","dummy_tag_event_object","transactional_inventory_layout_set"]
r16=r20=0; scanned=0
for slug in new:
    f=PY/("%s_iud.py"%slug)
    if not f.exists(): print("MISSING",f.name); continue
    scanned+=1
    for n,line in enumerate(f.read_text(encoding="utf-8",errors="replace").splitlines(),1):
        if not any(t in line for t in ENV_OK) and (CRED.search(line) or FILL.search(line)):
            print("R16",f.name,n,line.strip()[:80]); r16+=1
        for ch in line:
            if ord(ch)>127: print("R20",f.name,n,hex(ord(ch))); r20+=1; break
print("scanned %d drivers | R16=%d R20=%d -> %s"%(scanned,r16,r20,"CLEAN" if r16==0 and r20==0 else "VIOLATIONS"))
