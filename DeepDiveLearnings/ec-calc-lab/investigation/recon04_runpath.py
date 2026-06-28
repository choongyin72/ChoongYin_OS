"""Phase-1 run-path probe (READ-ONLY): how is a calc actually run here? Sandbox only."""
import oracledb
cur=oracledb.connect(user="ECKERNEL_EC",password="energy",dsn="localhost:1521/ORCL").cursor()
def has(t):
    try: return cur.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
    except Exception as e: return f"ERR {str(e)[:35]}"

print("=== the 1 DEPENDENT_CALC_JOB row ===")
print("  cols:", ", ".join([r[0] for r in cur.execute("SELECT column_name FROM all_tab_columns WHERE table_name='DEPENDENT_CALC_JOB' ORDER BY column_id")][:12]))
for r in cur.execute("SELECT * FROM DEPENDENT_CALC_JOB WHERE rownum<=3"): print("  ",r)

print("\n=== calc collection / job-ish tables ===")
for t in ("CALC_COLLECTION","CALC_COLLECTION_CALC","CALC_GROUP","CALC_GROUP_CONTEXT","CALC_JOB_RUN","BUSINESS_ACTION"):
    print(f"  {t}: {has(t)}")

print("\n=== EC4E_CALCULATION public run entry points (procedures) ===")
for r in cur.execute("""SELECT procedure_name FROM all_procedures WHERE object_name='EC4E_CALCULATION'
   AND procedure_name IS NOT NULL AND (UPPER(procedure_name) LIKE '%RUN%' OR UPPER(procedure_name) LIKE '%CALC%' OR UPPER(procedure_name) LIKE '%EXEC%' OR UPPER(procedure_name) LIKE '%PROCESS%') AND rownum<=25 ORDER BY procedure_name"""):
    print("  ",r[0])

print("\n=== how was Daily Allocation (proven N2 run) triggered? BUSINESS_ACTION calc-ish ===")
try:
    for r in cur.execute("""SELECT object_code, description FROM business_action WHERE UPPER(object_code) LIKE '%ALLOC%' OR UPPER(object_code) LIKE '%CALC%' AND rownum<=15"""):
        print("  ",r)
except Exception as e: print("  ",str(e)[:60])

print("\n=== is there a Calculation run SCREEN (treeview)? search class labels ===")
for r in cur.execute("""SELECT DISTINCT property_value FROM class_property_cnfg WHERE property_code='LABEL'
   AND (UPPER(property_value) LIKE '%CALCULATION%' OR UPPER(property_value) LIKE '%CALC JOB%') AND rownum<=15"""):
    print("  ",r[0])
