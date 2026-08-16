"""Independent post-run check: well gas comp target left as found (MOL_PCT all 0.1, no dirty cell)."""
import os
import oracledb

cur = oracledb.connect(user="ECKERNEL_EC", password=os.environ.get("EC_DB_PWD", "energy"),
                       dsn=os.environ.get("EC_DB_DSN", "localhost:1521/ORCL"), tcp_connect_timeout=15).cursor()
rows = cur.execute("""SELECT COMPONENT_NO, MOL_PCT FROM ECKERNEL_EC.DV_WELL_COMP_ANALYSIS
                      WHERE OBJECT_CODE='P1_W260_GP_COMP_GAS' AND TRUNC(DAYTIME)=TO_DATE('2025-04-01','YYYY-MM-DD')
                      ORDER BY COMPONENT_NO""").fetchall()
print("components (NO, MOL_PCT):", rows)
bad = [r for r in rows if r[1] not in (0.1,)]
print("C1:", [r for r in rows if r[0] == 'C1'], "| C2:", [r for r in rows if r[0] == 'C2'])
print("non-0.1 (should be NONE):", bad if bad else "NONE - clean")
