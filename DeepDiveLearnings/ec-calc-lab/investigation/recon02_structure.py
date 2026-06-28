"""Phase-1 recon (READ-ONLY): template equations + variable linkage + EC_PROD EQUATIONS exemplars."""
import oracledb, re
cur=oracledb.connect(user="ECKERNEL_EC",password="energy",dsn="localhost:1521/ORCL").cursor()
TPL='96D793BCA1230AE5E053020011ACDFC8'
EC_PROD='96D6E0ED1D5A0571E053020011ACE2E9'
def c(v):
    v = v.read() if hasattr(v,'read') else v
    return v or ''
def deml(x):
    s=c(x); s=re.sub(r'<[^>]+>',' ',s); s=re.sub(r'\s+',' ',s); return s.strip()
print("=== template CALC_EQUATION rows ===")
for r in cur.execute("SELECT exec_order,description,condition,equation FROM CALC_EQUATION WHERE object_id=:o ORDER BY exec_order",[TPL]):
    print(f"  [{r[0]}] {c(r[1])[:60]}")
    cc=deml(r[2]);
    if cc: print(f"        cond= {cc[:90]}")
    print(f"        eqn = {deml(r[3])[:150]}")
print("\n=== CALC link tables (CALC%VAR%) ===")
for r in cur.execute("SELECT table_name FROM all_tables WHERE table_name LIKE 'CALC%VAR%' ORDER BY 1"): print("  ",r[0])
print("\n=== EC_PROD EQUATIONS/MAIN calcs (smallest by #eqn) ===")
rows=cur.execute("""SELECT object_code,(SELECT COUNT(*) FROM calc_equation e WHERE e.object_id=c.object_id) neq
 FROM calculation c WHERE calc_context_id=:p AND calc_type='EQUATIONS' AND calc_scope='MAIN' AND (end_date IS NULL OR end_date>SYSDATE) ORDER BY neq""",[EC_PROD]).fetchall()
print(f"  ({len(rows)} found)")
for r in rows[:12]: print("   ",r)
