"""DB recon for Analysis Point (OV-GM). OV_ANALYSIS_POINT columns + sample rows + Op PU/Area/Facility
distribution -> pick a POPULATED nav scope for recon/suite + understand the groupmodel linkage. READ-ONLY."""
import os, oracledb
cur = oracledb.connect(user="ECKERNEL_EC", password=os.environ.get("EC_DB_PWD", "energy"),
                       dsn=os.environ.get("EC_DB_DSN", "localhost:1521/ORCL"), tcp_connect_timeout=15).cursor()

print("=== OV_ANALYSIS_POINT columns ===")
cur.execute("""SELECT column_name FROM all_tab_columns WHERE owner='ECKERNEL_EC'
               AND table_name='OV_ANALYSIS_POINT' ORDER BY column_id""")
cols = [r[0] for r in cur.fetchall()]
print("  ", ", ".join(cols))
cur.execute("SELECT COUNT(*) FROM ECKERNEL_EC.OV_ANALYSIS_POINT")
print("  total rows:", cur.fetchone()[0])

# op-parent style columns (to find the groupmodel scope linkage)
op_cols = [c for c in cols if any(k in c for k in ("PU", "PRODUCTIONUNIT", "AREA", "FACILITY", "OP_", "CODE", "TYPE"))]
print("\n=== scope/code-ish columns ===\n  ", op_cols)

print("\n=== sample rows (code/name + any *PU*/*AREA*/*FACILITY* cols) ===")
sel = [c for c in cols if c in ("CODE", "NAME") or any(k in c for k in ("PRODUCTIONUNIT", "OP_PU", "OP_AREA", "FACILITY", "ANALYSIS_POINT_TYPE", "AP_TYPE", "TYPE"))][:10]
if sel:
    cur.execute(f"SELECT {','.join(sel)} FROM ECKERNEL_EC.OV_ANALYSIS_POINT FETCH FIRST 8 ROWS ONLY")
    names = [d[0] for d in cur.description]
    for r in cur.fetchall():
        print("  ", dict(zip(names, [str(x)[:24] for x in r])))

print("\n=== AUTOTEST residue? ===")
cur.execute("SELECT COUNT(*) FROM ECKERNEL_EC.OV_ANALYSIS_POINT WHERE code LIKE 'AUTOTEST%'")
print("  AUTOTEST rows:", cur.fetchone()[0])
cur.close()
print("\nDONE")
