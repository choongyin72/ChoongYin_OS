"""Phase-1 recon (READ-ONLY): exemplar 01_TEST_CALCULATION recipe (eqn+vars+mappings) + RUN feasibility."""
import oracledb, re
cur=oracledb.connect(user="ECKERNEL_EC",password="energy",dsn="localhost:1521/ORCL").cursor()
def c(v):
    v=v.read() if hasattr(v,'read') else v; return v or ''
def deml(x):
    s=c(x); s=re.sub(r'<[^>]+>',' ',s); s=re.sub(r'\s+',' ',s); return s.strip()
ex=cur.execute("SELECT object_id FROM calculation WHERE object_code='01_TEST_CALCULATION'").fetchone()[0]
print("01_TEST_CALCULATION object_id=",ex)
print("\n=== its equations ===")
for r in cur.execute("SELECT exec_order,description,equation FROM calc_equation WHERE object_id=:o ORDER BY exec_order",[ex]):
    print(f"  [{r[0]}] {c(r[1])[:45]} :: {deml(r[2])[:110]}")
print("\n=== CALC_VARIABLE_LOCAL linkage (does object_id = calc id?) ===")
print("  cols:", ", ".join([r[0] for r in cur.execute("SELECT column_name FROM all_tab_columns WHERE table_name='CALC_VARIABLE_LOCAL' ORDER BY column_id")][:14]))
loc=cur.execute("SELECT COUNT(*) FROM calc_variable_local WHERE object_id=:o",[ex]).fetchone()[0]
print(f"  calc_variable_local rows for this calc: {loc}")
print("\n=== CALC_VAR_READ_MAPPING cols ==="); print("  ",", ".join([r[0] for r in cur.execute("SELECT column_name FROM all_tab_columns WHERE table_name='CALC_VAR_READ_MAPPING' ORDER BY column_id")]))
print("=== CALC_VAR_WRITE_MAPPING cols ==="); print("  ",", ".join([r[0] for r in cur.execute("SELECT column_name FROM all_tab_columns WHERE table_name='CALC_VAR_WRITE_MAPPING' ORDER BY column_id")]))
print("\n=== RUN FEASIBILITY ===")
print("  CALC_BATCH_LOG cols:", ", ".join([r[0] for r in cur.execute("SELECT column_name FROM all_tab_columns WHERE table_name='CALC_BATCH_LOG' ORDER BY column_id")][:12]))
for t in ("CALC_BATCH_LOG","CALC_PROCESS_LOG","CALC_PROCESS_DETAIL_LOG"):
    print(f"  {t} rows: {cur.execute(f'SELECT COUNT(*) FROM {t}').fetchone()[0]}")
# any alloc-job run history at all (proves engine runs here)?
for t in ("EC4E_ALLOC_JOB_LOG","ALLOC_JOB_LOG","CALC_JOB","DEPENDENT_CALC_JOB"):
    try: print(f"  {t} rows: {cur.execute(f'SELECT COUNT(*) FROM {t}').fetchone()[0]}")
    except Exception as e: print(f"  {t}: {str(e)[:45]}")
# engine package present?
print("  EC4E_CALCULATION pkg present:", cur.execute("SELECT COUNT(*) FROM all_objects WHERE object_name='EC4E_CALCULATION' AND object_type LIKE 'PACKAGE%'").fetchone()[0])
