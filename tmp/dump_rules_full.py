# READ-ONLY: full dump of the 4 rules + child/group/combination rows from ec14151, to author the upsert SQL.
import json, oracledb
DSN="db.ec14151.woodside-pluto.tieto-og.cloud:1521/ec14151"
c=oracledb.connect(user="ECKERNEL_EC",password="energy",dsn=DSN); cur=c.cursor()
IDS=(1147,1148,1149,1150)

def lob(v):
    try:
        import oracledb as o
        if isinstance(v,o.LOB): return v.read()
    except Exception: pass
    return v

def dump(label, sql, binds=None):
    cur.execute(sql, binds or {})
    cols=[d[0] for d in cur.description]
    rows=[{cols[i]:lob(v) for i,v in enumerate(r)} for r in cur.fetchall()]
    print(f"\n##### {label} ({len(rows)} rows) cols={cols}")
    for r in rows: print(json.dumps(r, default=str))
    return rows, cols

inlist=",".join(str(i) for i in IDS)
dump("CTRL_CHECK_RULES", f"select * from ctrl_check_rules where check_id in ({inlist}) order by check_id")
dump("TV_CTRL_CHECK_RULE_VARIABLE", f"select * from tv_ctrl_check_rule_variable where check_id in ({inlist}) order by check_id, variable_name")
for t in ("tv_ctrl_check_rule_subq_var","tv_ctrl_check_rule_func_p"):
    try: dump(t.upper(), f"select * from {t} where check_id in ({inlist}) order by check_id")
    except Exception as e: print(f"\n##### {t.upper()} ERR {str(e)[:80]}")
# combination + group (resolve group ids from combination)
comb,_=dump("TV_CTRL_CHECK_COMBINATION", f"select * from tv_ctrl_check_combination where check_id in ({inlist})")
gids=sorted({r.get('CHECK_GROUP_ID') or r.get('GROUP_ID') for r in comb if (r.get('CHECK_GROUP_ID') or r.get('GROUP_ID'))})
print("\n>>> group ids from combination:", gids)
if gids:
    gl=",".join("'%s'"%g for g in gids)
    dump("TV_CTRL_CHECK_GROUP", f"select * from tv_ctrl_check_group where check_group_id in ({gl})")
c.close()
