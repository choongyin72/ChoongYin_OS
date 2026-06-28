"""Phase-0 (READ-ONLY): concrete read attr + test well/day + scratch col cleanliness. Sandbox only."""
import oracledb, os
cur=oracledb.connect(user=os.environ.get("EC_DB_USER","ECKERNEL_EC"),password=os.environ.get("EC_DB_PASS","energy"),dsn=os.environ.get("EC_DB_DSN","localhost:1521/ORCL")).cursor()
def c(v):
    v=v.read() if hasattr(v,'read') else v; return (v or '')
print("=== PWEL_DAY_DATA read attributes (sql_syntax) - look for a MEASURED input ===")
seen=set()
for r in cur.execute("SELECT DISTINCT sql_syntax FROM calc_var_read_mapping WHERE cls_name='PWEL_DAY_DATA'"):
    a=c(r[0])
    if a and a not in seen: seen.add(a)
print("   "+", ".join(sorted(seen))[:600])
print("\n=== physical PWEL_DAY_ALLOC row count + is it populated? ===")
try: print("   PWEL_DAY_ALLOC rows:", cur.execute("SELECT COUNT(*) FROM PWEL_DAY_ALLOC").fetchone()[0])
except Exception as e: print("   PWEL_DAY_ALLOC:",str(e)[:50])
print("=== physical input table PWEL_DAY_STATUS gross-vol candidates ===")
cols=[r[0] for r in cur.execute("SELECT column_name FROM all_tab_columns WHERE table_name='PWEL_DAY_STATUS' AND (column_name LIKE '%VOL%' OR column_name LIKE '%GRS%' OR column_name LIKE '%RATE%') ORDER BY column_id")]
print("   "+", ".join(cols)[:400])
print("\n=== a test well+day with measured data (far-past) ===")
try:
    for r in cur.execute("""SELECT object_id, daytime FROM PWEL_DAY_STATUS WHERE daytime < DATE '2015-01-01' AND rownum<=3 ORDER BY daytime"""):
        print("   well_id=%s day=%s"%(c(r[0])[:18],r[1]))
except Exception as e: print("   ",str(e)[:60])
