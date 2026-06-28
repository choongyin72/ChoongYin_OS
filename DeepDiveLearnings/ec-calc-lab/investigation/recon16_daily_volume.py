"""Phase-2 (READ-ONLY): EC_DAILY_VOLUME full structure (eqns + local vars + read/write mappings) = copy template."""
import oracledb, os, re
cur=oracledb.connect(user=os.environ.get("EC_DB_USER","ECKERNEL_EC"),password=os.environ.get("EC_DB_PASS","energy"),dsn=os.environ.get("EC_DB_DSN","localhost:1521/ORCL")).cursor()
def c(v):
    v=v.read() if hasattr(v,'read') else v; return (v or '')
def deml(x):
    s=c(x); s=re.sub(r'<[^>]+>',' ',s); s=re.sub(r'\s+',' ',s); return s.strip()
oid=cur.execute("SELECT object_id FROM calculation WHERE object_code='EC_DAILY_VOLUME'").fetchone()[0]
print("EC_DAILY_VOLUME object_id=",oid)
print("\n=== equations ===")
for r in cur.execute("SELECT exec_order,description,equation FROM calc_equation WHERE object_id=:o ORDER BY exec_order",[oid]):
    print(f"  [{r[0]}] {c(r[1])[:40]} :: {deml(r[2])[:120]}")
print("\n=== local vars (NAME | data_type | signature) ===")
sigs=[]
for r in cur.execute("SELECT name, calc_var_data_type, calc_var_signature FROM calc_variable_local WHERE object_id=:o",[oid]):
    print(f"  {c(r[0])[:22]:22} {c(r[1])[:10]:10} sig={c(r[2])[:24]}"); sigs.append(c(r[2]))
print("\n=== read mappings (var sig -> cls.attr) ===")
for s in sigs:
    for r in cur.execute("SELECT cls_name,sql_syntax FROM calc_var_read_mapping WHERE calc_var_signature=:s",[s]):
        print(f"  {s[:20]} READ  {c(r[0])}.{c(r[1])}")
    for r in cur.execute("SELECT cls_name,sql_syntax FROM calc_var_write_mapping WHERE calc_var_signature=:s",[s]):
        print(f"  {s[:20]} WRITE {c(r[0])}.{c(r[1])}")
