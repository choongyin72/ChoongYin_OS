"""Independent DB re-read: any AUTOTEST residue in OV_ANALYSIS_POINT? READ-ONLY."""
import os, oracledb
cur = oracledb.connect(user="ECKERNEL_EC", password=os.environ.get("EC_DB_PWD", "energy"),
                       dsn=os.environ.get("EC_DB_DSN", "localhost:1521/ORCL"), tcp_connect_timeout=15).cursor()
cur.execute("""SELECT code, name, object_start_date, end_date FROM ECKERNEL_EC.OV_ANALYSIS_POINT
               WHERE code LIKE 'AUTOTEST%' OR name LIKE 'AUTOTEST%'""")
rows = cur.fetchall()
print("OV_ANALYSIS_POINT AUTOTEST residue rows:", len(rows))
for r in rows:
    print("  ", r)
cur.close()
print("DONE")
