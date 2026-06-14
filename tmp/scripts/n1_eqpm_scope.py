"""Discover the nav scope for equipment day-status rows (EQPM_DAY_STATUS) on 2024-02-06: equipment
names + their facility hierarchy, so the UI recon lands on data. Read-only."""
import os, oracledb
c=oracledb.connect(user='ECKERNEL_EC',password='energy',dsn=os.environ.get('EC_DB_DSN','localhost:1521/ORCL'),tcp_connect_timeout=15);cur=c.cursor()
def show(t,sql):
    print(f"=== {t} ===")
    try:
        cur.execute(sql);cols=[d[0] for d in cur.description];print(" | ".join(cols))
        for r in cur.fetchall()[:15]: print("  "+" | ".join("" if v is None else str(v)[:40] for v in r))
    except Exception as e: print("  ERR",str(e)[:140])
show("equipment names with data on 2024-02-06 (via OV_EQPM)",
    "SELECT a.OBJECT_ID, e.NAME FROM EQPM_DAY_STATUS a LEFT JOIN OV_EQPM e ON e.OBJECT_ID=a.OBJECT_ID "
    "WHERE TRUNC(a.DAYTIME)=TO_DATE('2024-02-06','YYYY-MM-DD') ORDER BY e.NAME FETCH FIRST 15 ROWS ONLY")
# OV_EQPM columns that hint facility/PU/area scope
show("OV_EQPM scope-ish columns",
    "SELECT column_name FROM all_tab_columns WHERE table_name='OV_EQPM' AND (column_name LIKE '%FCTY%' OR column_name LIKE '%FACIL%' OR column_name LIKE '%PROD_UNIT%' OR column_name LIKE '%AREA%' OR column_name LIKE '%PARENT%' OR column_name LIKE '%CLASS%') ORDER BY column_id")
# sample OV_EQPM row scope values for one equipment with data
show("sample equipment scope (first data equipment)",
    "SELECT e.NAME, e.OP_FCTY_CLASS_1_NAME, e.PROD_AREA_NAME, e.PROD_UNIT_NAME FROM OV_EQPM e "
    "WHERE e.OBJECT_ID IN (SELECT OBJECT_ID FROM EQPM_DAY_STATUS WHERE TRUNC(DAYTIME)=TO_DATE('2024-02-06','YYYY-MM-DD')) "
    "FETCH FIRST 8 ROWS ONLY")
cur.close();c.close();print("DONE")
