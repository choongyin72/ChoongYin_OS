"""Where does the grid's 21 live? Scan this well/day's PWEL_DAY_STATUS row for any column = 21,
and look for raw/measured sibling tables (READ-ONLY DB). Data-integrity investigation."""
import os
import oracledb
conn = oracledb.connect(user="ECKERNEL_EC", password="energy", dsn="localhost:1521/ORCL", tcp_connect_timeout=15)
cur = conn.cursor()
OID = "96D7FD4CB6490217E053020011AC1940"

# 1) full PWEL_DAY_STATUS row — print any non-null numeric/text column, flag any == 21
cur.execute("SELECT * FROM ECKERNEL_EC.PWEL_DAY_STATUS WHERE OBJECT_ID=:o AND TRUNC(DAYTIME)=DATE '2003-01-01'", o=OID)
names = [d[0] for d in cur.description]
row = cur.fetchone()
print("=== PWEL_DAY_STATUS non-null cols for AS2_Onshore Well no 2 / 2003-01-01 ===")
if row:
    for n, v in zip(names, row):
        if v is not None and str(v) not in ("0",):
            mark = "  <== 21!" if str(v) in ("21", "21.0") else ""
            print(f"   {n:26} = {v}{mark}")
else:
    print("   (no row)")

# 2) any 'raw' / 'measured' / 'manual' sibling day-status tables for prod wells?
print("\n=== candidate raw/measured well day tables ===")
cur.execute("""SELECT table_name FROM all_tables WHERE owner='ECKERNEL_EC'
   AND (table_name LIKE 'PWEL%RAW%' OR table_name LIKE '%RAW%PWEL%' OR table_name LIKE 'PWEL%MEAS%'
        OR table_name LIKE 'PWEL%MANUAL%' OR table_name LIKE 'PWEL%ENTRY%' OR table_name LIKE 'PWEL%DAY%')
   ORDER BY table_name""")
for r in cur.fetchall(): print("   ", r[0])

conn.close(); print("\nDONE")
