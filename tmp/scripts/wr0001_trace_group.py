"""Resolve a filled well's name + its groupmodel scope (READ-ONLY DB)."""
import os
import oracledb

conn = oracledb.connect(
    user=os.environ.get("EC_DB_USER", "ECKERNEL_EC"),
    password=os.environ.get("EC_DB_PASS", "energy"),
    dsn=os.environ.get("EC_DB_DSN", "localhost:1521/ORCL"),
    tcp_connect_timeout=15,
)
cur = conn.cursor()

def q(sql, label, n=20, **kw):
    print(f"\n=== {label} ===")
    try:
        cur.execute(sql, **kw)
        names = [d[0] for d in cur.description]
        rows = cur.fetchall()
        for r in rows[:n]:
            print("  ", tuple(str(v)[:34] for v in r))
        if not rows: print("   (none)")
        return rows
    except Exception as e:
        print("   ERR:", str(e)[:160]); return []

# the filled well on 2003-01-01
cur.execute("""SELECT OBJECT_ID FROM ECKERNEL_EC.PWEL_DAY_STATUS
               WHERE TRUNC(DAYTIME)=DATE '2003-01-01' AND ON_STREAM_HRS IS NOT NULL
               FETCH FIRST 1 ROWS ONLY""")
wid = cur.fetchone()[0]
print("well OBJECT_ID:", wid)

q("SELECT OBJECT_CODE, CLASS_NAME, TO_CHAR(START_DATE,'YYYY-MM-DD'), DESCRIPTION FROM ECKERNEL_EC.WELL WHERE OBJECT_ID=:i",
  "WELL identity", i=wid)
q("SELECT NAME, WELL_TYPE, TO_CHAR(DAYTIME,'YYYY-MM-DD') FROM ECKERNEL_EC.WELL_VERSION WHERE OBJECT_ID=:i",
  "WELL_VERSION name/type", i=wid)

# groupmodel: find junction/assignment tables that reference this well object id
q("""SELECT table_name FROM all_tables WHERE owner='ECKERNEL_EC'
     AND (table_name LIKE '%GROUP%CONN%' OR table_name LIKE '%GRP%CONN%'
          OR table_name LIKE '%OPER%ASSIGN%' OR table_name LIKE '%OBJECT_GROUP%'
          OR table_name LIKE '%WELL_HOOKUP_CONN%' OR table_name LIKE '%HOOKUP%WELL%'
          OR table_name LIKE '%GROUPMODEL%' OR table_name LIKE 'OA%' OR table_name LIKE '%GROUP_CONNECT%')
     ORDER BY table_name FETCH FIRST 40 ROWS ONLY""", "candidate groupmodel/junction tables")

# the well-hookup that has day-status data (from earlier sample) + its identity
q("""SELECT wh.OBJECT_CODE, wv.NAME FROM ECKERNEL_EC.WELL_HOOKUP wh
     LEFT JOIN ECKERNEL_EC.WELL_HOOKUP_VERSION wv ON wv.OBJECT_ID=wh.OBJECT_ID
     WHERE wh.OBJECT_ID IN (SELECT DISTINCT OBJECT_ID FROM ECKERNEL_EC.WELL_HOOKUP_DAY_STATUS)
     FETCH FIRST 10 ROWS ONLY""", "well-hookups that HAVE day-status rows")

conn.close(); print("\nDONE")
