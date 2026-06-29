import os, oracledb, re
def say(m): print(m, flush=True)
def rd(v):
    try: return v.read() if hasattr(v,'read') else v
    except: return v
def sml(s):
    if not s: return ''
    s=rd(s); s=re.sub(r'<[^>]+>',' ',str(s)); s=re.sub(r'\s+',' ',s); return s.strip()
EC_PROD='96D6E0ED1D5A0571E053020011ACE2E9'
c=oracledb.connect(user=os.environ.get('EC_DB_USER','ECKERNEL_EC'),password=os.environ.get('EC_DB_PASS','energy'),dsn=os.environ.get('EC_DB_DSN','localhost:1521/ORCL'))
cur=c.cursor()
say("=== resolve the read/write-map object_ids ===")
cur.execute("select distinct object_id from calc_var_write_mapping")
for (oid,) in cur.fetchall():
    cur.execute("select ecdp_objects.GetObjCode(:o) from dual",{'o':oid}); say("   %s -> %s" % (oid[:14]+'..', rd(cur.fetchone()[0])))
say("\n=== EC_PROD READ mappings (var <- CLS.attr) ===")
cur.execute("""select v.name, r.cls_name, r.sql_syntax from calc_var_read_mapping r
  join calc_variable_local v on v.object_id=r.object_id and v.calc_var_signature=r.calc_var_signature
  where r.object_id=:o and v.name is not null fetch first 10 rows only""",{'o':EC_PROD})
for nm,cls,sq in cur.fetchall(): say("   %-20s <- %-20s %s" % (nm, cls, sml(sq)[:45]))
say("\n=== EC_PROD WRITE mappings (var -> CLS.attr) ===")
cur.execute("""select v.name, w.cls_name, w.sql_syntax from calc_var_write_mapping w
  join calc_variable_local v on v.object_id=w.object_id and v.calc_var_signature=w.calc_var_signature
  where w.object_id=:o and v.name is not null fetch first 10 rows only""",{'o':EC_PROD})
for nm,cls,sq in cur.fetchall(): say("   %-20s -> %-20s %s" % (nm, cls, sml(sq)[:45]))
c.close()
