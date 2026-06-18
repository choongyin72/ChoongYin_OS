"""Check whether the mis-aimed probe dirtied MOL_PCT on the oil target (originally all MOL_PCT NULL,
WT_PCT=0.1). Read MOL_PCT + WT_PCT for every component of P1 ALLOC S001 OIL @ 2023-06-01. Read-only."""
import os
import oracledb

conn = oracledb.connect(user="ECKERNEL_EC", password=os.environ.get("EC_DB_PWD", "energy"),
                        dsn=os.environ.get("EC_DB_DSN", "localhost:1521/ORCL"), tcp_connect_timeout=15)
cur = conn.cursor()
rows = cur.execute("""SELECT COMPONENT_NO, MOL_PCT, WT_PCT FROM ECKERNEL_EC.DV_STRM_COMP_ANALYSIS
                      WHERE OBJECT_CODE='P1 ALLOC S001 OIL' AND TRUNC(DAYTIME)=TO_DATE('2023-06-01','YYYY-MM-DD')
                      ORDER BY COMPONENT_NO""").fetchall()
print("COMPONENT_NO | MOL_PCT | WT_PCT")
dirty = []
for c, m, w in rows:
    flag = "  <-- MOL_PCT DIRTY (was NULL)" if m is not None else ""
    if m is not None:
        dirty.append(c)
    print(f"  {c:6s} | {m} | {w}{flag}")
print("\nDIRTY components (MOL_PCT not NULL):", dirty if dirty else "NONE - clean")
cur.close(); conn.close()
