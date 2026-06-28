"""Phase-1 (READ-ONLY): pull exact calc screen labels + paths from the treeview JSON."""
import oracledb, os, json
cur=oracledb.connect(user=os.environ.get("EC_DB_USER","ECKERNEL_EC"),password=os.environ.get("EC_DB_PASS","energy"),dsn=os.environ.get("EC_DB_DSN","localhost:1521/ORCL")).cursor()
row=cur.execute("""SELECT configuration FROM TV_CTRL_CONFIGURATION_STORAGE WHERE name='DefaultScreenTreeview'""").fetchone()
cfg=row[0].read() if hasattr(row[0],'read') else row[0]
data=json.loads(cfg)
hits=[]
def walk(node, path):
    if isinstance(node, dict):
        label=node.get('label',''); typ=node.get('type'); scr=node.get('screen')
        p=path+[label] if label else path
        if label and ('calc' in label.lower()) and typ!='FOLDER':
            hits.append((" > ".join(p[-4:]), scr))
        for k in ('items','children'):
            if k in node and isinstance(node[k],list):
                for ch in node[k]: walk(ch, p)
    elif isinstance(node, list):
        for ch in node: walk(ch, path)
walk(data, [])
print(f"=== calc-related treeview leaf screens ({len(hits)}) ===")
for path,scr in hits[:40]: print(f"  {scr or '-':12} | {path}")
