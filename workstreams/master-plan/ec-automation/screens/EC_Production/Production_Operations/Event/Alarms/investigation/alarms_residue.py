"""Independent DB re-read: any AUTOTEST_ALARM residue in DV_ALARMS / FCTY_DAY_ALARM? READ-ONLY."""
import os, oracledb
cur = oracledb.connect(user="ECKERNEL_EC", password=os.environ.get("EC_DB_PWD", "energy"),
                       dsn=os.environ.get("EC_DB_DSN", "localhost:1521/ORCL"), tcp_connect_timeout=15).cursor()
for t in ("DV_ALARMS", "FCTY_DAY_ALARM"):
    cur.execute(f"SELECT COUNT(*) FROM ECKERNEL_EC.{t} WHERE REASON LIKE 'AUTOTEST_ALARM%'")
    n = cur.fetchone()[0]
    print(f"{t}: AUTOTEST_ALARM residue rows = {n}")
    if n:
        cur.execute(f"SELECT REASON, DAYTIME FROM ECKERNEL_EC.{t} WHERE REASON LIKE 'AUTOTEST_ALARM%'")
        for r in cur.fetchall():
            print("   ", r)
cur.close()
print("DONE")
