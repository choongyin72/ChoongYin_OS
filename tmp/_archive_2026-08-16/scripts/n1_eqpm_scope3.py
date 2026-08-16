"""Resolve the equipment nav scope from DB: distinct OP_AREA + OP_FCTY_1 (codes+names) for equipment
that has EQPM_DAY_STATUS data on 2024-02-06, so the UI nav (PU/Area/FacilityClass1) targets data.
Also resolve the PU above each area. Read-only."""
import os, oracledb
c=oracledb.connect(user='ECKERNEL_EC',password='energy',dsn=os.environ.get('EC_DB_DSN','localhost:1521/ORCL'),tcp_connect_timeout=15);cur=c.cursor()
def show(t,sql):
    print(f"=== {t} ===")
    try:
        cur.execute(sql);cols=[d[0] for d in cur.description];print(" | ".join(cols))
        for r in cur.fetchall()[:20]: print("  "+" | ".join("" if v is None else str(v)[:38] for v in r))
    except Exception as e: print("  ERR",str(e)[:160])
# distinct operational area + facility-class-1 codes for the data-equipment
show("distinct OP_AREA / OP_FCTY_1 for equipment with data on 2024-02-06",
    "SELECT DISTINCT e.OP_AREA_CODE, e.OP_FCTY_1_CODE, COUNT(*) n FROM OV_EQPM e "
    "WHERE e.OBJECT_ID IN (SELECT OBJECT_ID FROM EQPM_DAY_STATUS WHERE TRUNC(DAYTIME)=TO_DATE('2024-02-06','YYYY-MM-DD')) "
    "GROUP BY e.OP_AREA_CODE, e.OP_FCTY_1_CODE ORDER BY n DESC")
# resolve area code -> name + its PU (parent) via object-name helper if available
show("area code -> name (OV_AREA)",
    "SELECT CODE, NAME FROM OV_AREA WHERE CODE IN (SELECT DISTINCT OP_AREA_CODE FROM OV_EQPM e "
    "WHERE e.OBJECT_ID IN (SELECT OBJECT_ID FROM EQPM_DAY_STATUS WHERE TRUNC(DAYTIME)=TO_DATE('2024-02-06','YYYY-MM-DD'))) ")
show("facility class1 code -> name (OV_PROD_FCTY_CLASS_1 or similar)",
    "SELECT table_name FROM all_tables WHERE owner='ECKERNEL_EC' AND table_name LIKE 'OV_%FCTY%' ORDER BY table_name FETCH FIRST 15 ROWS ONLY")
cur.close();c.close();print("DONE")
