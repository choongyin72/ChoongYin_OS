"""Phase-0 (READ-ONLY): exact read/write SQL_SYNTAX format + gross-vol col + alloc col + safe test well/day."""
import oracledb, os
cur=oracledb.connect(user=os.environ.get("EC_DB_USER","ECKERNEL_EC"),password=os.environ.get("EC_DB_PASS","energy"),dsn=os.environ.get("EC_DB_DSN","localhost:1521/ORCL")).cursor()
def c(v):
    v=v.read() if hasattr(v,'read') else v; return (v or '')
print("=== sample READ mapping for PWEL_DAY_DATA (SQL_SYNTAX format) ===")
for r in cur.execute("SELECT sql_syntax FROM calc_var_read_mapping WHERE cls_name='PWEL_DAY_DATA' AND rownum<=4"):
    print("   ",c(r[0])[:90])
print("=== sample WRITE mapping for PWEL_DAY_ALLOC ===")
for r in cur.execute("SELECT sql_syntax FROM calc_var_write_mapping WHERE cls_name='PWEL_DAY_ALLOC' AND rownum<=4"):
    print("   ",c(r[0])[:90])
print("\n=== PWEL_DAY_DATA columns (gross-vol candidates) ===")
print("   "+", ".join([r[0] for r in cur.execute("SELECT column_name FROM all_tab_columns WHERE table_name='PWEL_DAY_DATA' ORDER BY column_id")]))
print("\n=== PWEL_DAY_ALLOC columns (alloc output candidates) ===")
print("   "+", ".join([r[0] for r in cur.execute("SELECT column_name FROM all_tab_columns WHERE table_name='PWEL_DAY_ALLOC' ORDER BY column_id")]))
print("\n=== PWEL_DAY_DATA: a far-past day with data (candidate test scope) ===")
for r in cur.execute("""SELECT object_id, daytime, count(*) FROM PWEL_DAY_DATA
  WHERE daytime < DATE '2015-01-01' GROUP BY object_id, daytime ORDER BY daytime FETCH FIRST 5 ROWS ONLY"""):
    print("   well_id=%s day=%s n=%s"%(r[0][:16],r[1],r[2]))
