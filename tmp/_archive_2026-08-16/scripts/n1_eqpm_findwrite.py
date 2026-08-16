import os, oracledb
c=oracledb.connect(user='ECKERNEL_EC',password='energy',dsn=os.environ.get('EC_DB_DSN','localhost:1521/ORCL'),tcp_connect_timeout=15);cur=c.cursor()
NUM=["ON_STREAM_HRS","ON_STREAM_SECS","AVG_RPM","AVG_SPM","AVG_INTAKE_PRESS","AVG_PRESS","AVG_TEMP","AVG_TORQUE","POWER_CONSUMPTION","POWER_GENERATED"]
# any EQPM row on 2024-02-06 with a numeric col = 22 (what I may have written)
pred=" OR ".join(f"{x}=22" for x in NUM)
cur.execute(f"SELECT a.OBJECT_ID, e.NAME, {','.join(NUM)} FROM EQPM_DAY_STATUS a LEFT JOIN OV_EQPM e ON e.OBJECT_ID=a.OBJECT_ID WHERE TRUNC(a.DAYTIME)=TO_DATE('2024-02-06','YYYY-MM-DD') AND ({pred})")
cols=[d[0] for d in cur.description]; rows=cur.fetchall()
print("rows with a 22 (possible stray write):", len(rows))
for r in rows: print("  "+" | ".join("" if v is None else str(v)[:30] for v in r))
# resolve the chiller OID by trimmed name
cur.execute("SELECT OBJECT_ID, '['||NAME||']' FROM OV_EQPM WHERE TRIM(NAME) LIKE 'P1 Chiller 002%' OR NAME LIKE '%Chiller 002%'")
print("chiller name matches:")
for r in cur.fetchall(): print("  ", r)
cur.close();c.close();print("DONE")
