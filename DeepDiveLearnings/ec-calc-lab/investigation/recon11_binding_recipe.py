"""Phase-0 (READ-ONLY): learn the EC_PROD read/write binding recipe (CLS_NAME + SQL_SYNTAX) +
candidate gross-vol source + _ALLOC target + calc delete-set (reversibility). Sandbox only."""
import oracledb, os, re
cur=oracledb.connect(user=os.environ.get("EC_DB_USER","ECKERNEL_EC"),password=os.environ.get("EC_DB_PASS","energy"),dsn=os.environ.get("EC_DB_DSN","localhost:1521/ORCL")).cursor()
def c(v):
    v=v.read() if hasattr(v,'read') else v; return (v or '')
EC_PROD='96D6E0ED1D5A0571E053020011ACE2E9'
print("=== READ mappings whose var is EC_PROD-context (CLS_NAME | SQL_SYNTAX) ===")
q="""SELECT rm.cls_name, rm.sql_syntax FROM calc_var_read_mapping rm
 WHERE rm.calc_var_signature IN (SELECT calc_var_signature FROM calc_variable_local WHERE calc_context_id=:p)
 AND rownum<=12"""
for r in cur.execute(q,[EC_PROD]):
    print(f"  {c(r[0])[:32]:32} | {c(r[1])[:80]}")
print("\n=== WRITE mappings (EC_PROD) -> _ALLOC targets ===")
q2="""SELECT wm.cls_name, wm.sql_syntax FROM calc_var_write_mapping wm
 WHERE wm.calc_var_signature IN (SELECT calc_var_signature FROM calc_variable_local WHERE calc_context_id=:p)
 AND rownum<=12"""
for r in cur.execute(q2,[EC_PROD]):
    print(f"  {c(r[0])[:32]:32} | {c(r[1])[:80]}")
print("\n=== distinct CLS_NAME across ALL read mappings (data-source vocabulary) ===")
for r in cur.execute("SELECT DISTINCT cls_name FROM calc_var_read_mapping WHERE cls_name IS NOT NULL AND rownum<=200"):
    nm=c(r[0])
    if any(k in nm.upper() for k in ('PWEL','STRM','VOL','PROD','WELL','MEAS')): print("  read:",nm)
print("\n=== distinct CLS_NAME across ALL write mappings containing ALLOC ===")
for r in cur.execute("SELECT DISTINCT cls_name FROM calc_var_write_mapping WHERE UPPER(cls_name) LIKE '%ALLOC%' AND rownum<=200"):
    print("  write:",c(r[0]))
