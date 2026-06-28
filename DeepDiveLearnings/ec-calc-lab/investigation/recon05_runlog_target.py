"""Phase-1 (READ-ONLY): precise run trigger + where EC_PROD calc results/errors land. Sandbox only."""
import oracledb
cur=oracledb.connect(user="ECKERNEL_EC",password="energy",dsn="localhost:1521/ORCL").cursor()
def t_exists(t):
    try: return cur.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
    except Exception as e: return f"ERR {str(e)[:30]}"
# backing class of "Daily Production Calculation Log"
print("=== 'Daily Production Calculation Log' backing class ===")
for r in cur.execute("SELECT class_name FROM class_property_cnfg WHERE property_code='LABEL' AND lower(property_value)='daily production calculation log'"):
    cn=r[0]; print("  class:",cn)
    meta=cur.execute("SELECT class_type,db_object_name FROM class_cnfg WHERE class_name=:c",[cn]).fetchall()
    print("  meta:",meta)
    for m in meta:
        for pref in ("","OV_","DV_","TV_"):
            n=t_exists(pref+m[1])
            if isinstance(n,int): print(f"    {pref}{m[1]}: {n} rows"); 
# broaden engine run-entry search across EC4E_* + ZWP_* packages
print("\n=== run-entry procedures (calc/alloc engines) ===")
for r in cur.execute("""SELECT object_name, procedure_name FROM all_procedures
  WHERE object_name LIKE 'EC4E_CALC%' AND procedure_name IS NOT NULL
  AND (UPPER(procedure_name) LIKE '%RUN%' OR UPPER(procedure_name) LIKE '%EXEC%' OR UPPER(procedure_name) LIKE '%PERFORM%' OR UPPER(procedure_name) LIKE '%CALC%' OR UPPER(procedure_name) LIKE '%BATCH%') AND rownum<=30 ORDER BY 1,2"""):
    print("  ",r[0],"::",r[1])
# which collection are the EC_PROD test calcs in (run grouping)?
print("\n=== CALC_COLLECTION cols + a few EC_PROD-ish sets ===")
print("  cols:", ", ".join([r[0] for r in cur.execute("SELECT column_name FROM all_tab_columns WHERE table_name='CALC_COLLECTION' ORDER BY column_id")][:10]))
for r in cur.execute("SELECT object_code, description FROM calc_collection WHERE rownum<=10"):
    print("  ",r)
