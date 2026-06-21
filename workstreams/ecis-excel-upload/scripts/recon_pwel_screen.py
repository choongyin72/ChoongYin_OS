"""Find the daily-well-status screen name + url. Read-only. py -X utf8 this."""
import os
import oracledb

conn = oracledb.connect(user="ECKERNEL_EC", password="energy",
                        dsn=os.environ.get("EC_DB_DSN", "localhost:1521/ORCL"))
cur = conn.cursor()

cur.execute("SELECT column_name FROM user_tab_columns WHERE table_name='BUSINESS_FUNCTION' ORDER BY column_id")
print("BUSINESS_FUNCTION cols:", [r[0] for r in cur.fetchall()])

for label, like in [("WELL+STATUS", "%WELL%STATUS%"), ("DAILY+WELL", "%DAILY%WELL%"),
                    ("WELL+DAY", "%WELL%DAY%"), ("PROD+WELL", "%PROD%WELL%")]:
    try:
        cur.execute("SELECT name, url FROM business_function WHERE UPPER(name) LIKE :l AND ROWNUM<=15", l=like)
        rows = cur.fetchall()
        print(f"\n== {label} ({len(rows)}) ==")
        for r in rows:
            print("  ", r)
    except Exception as e:
        print(f"\n== {label} == ERR {str(e)[:120]}")

conn.close()
print("\nDONE")
