"""Phase-1 recon (READ-ONLY): dump clone-template EC_PAY_DD_LNG_DES_PREL_EST structure. Sandbox only."""
import oracledb
cur=oracledb.connect(user="ECKERNEL_EC",password="energy",dsn="localhost:1521/ORCL").cursor()
def cols(t): return [r[0] for r in cur.execute("SELECT column_name FROM all_tab_columns WHERE table_name=:t ORDER BY column_id",[t])]

print("=== CALC_EQUATION columns ==="); print("  "+", ".join(cols("CALC_EQUATION")))
print("=== CALC_VARIABLE columns ==="); print("  "+", ".join(cols("CALC_VARIABLE")))

row=cur.execute("SELECT object_id,object_code,description,calc_type,calc_scope,calc_context_id,calc_period,start_date,end_date FROM CALCULATION WHERE object_code='EC_PAY_DD_LNG_DES_PREL_EST'").fetchall()
print("\n=== template CALCULATION ===")
oid=None
for r in row:
    print("  ",r); oid=r[0]
print("  object_id=",oid)
# context name
ctx=cur.execute("SELECT object_id,object_code,description FROM CALC_CONTEXT").fetchall()
print("\n=== CALC_CONTEXT inventory (14) ===")
for c in ctx: print("  ",c)
