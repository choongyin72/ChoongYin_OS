"""Independent post-run check: oil target left as found (all MOL_PCT NULL, WT_PCT original ~0.1)."""
import os
import oracledb

cur = oracledb.connect(user="ECKERNEL_EC", password=os.environ.get("EC_DB_PWD", "energy"),
                       dsn=os.environ.get("EC_DB_DSN", "localhost:1521/ORCL"), tcp_connect_timeout=15).cursor()
rows = cur.execute("""SELECT COMPONENT_NO, MOL_PCT, WT_PCT FROM ECKERNEL_EC.DV_STRM_COMP_ANALYSIS
                      WHERE OBJECT_CODE='P1 ALLOC S001 OIL' AND TRUNC(DAYTIME)=TO_DATE('2023-06-01','YYYY-MM-DD')
                      ORDER BY COMPONENT_NO""").fetchall()
dirty = [c for c, m, w in rows if m is not None]
print("C1 (Methane):", [r for r in rows if r[0] == 'C1'])
print("MOL_PCT dirty:", dirty if dirty else "NONE - clean")
print("WT_PCT all:", [(c, w) for c, m, w in rows])
