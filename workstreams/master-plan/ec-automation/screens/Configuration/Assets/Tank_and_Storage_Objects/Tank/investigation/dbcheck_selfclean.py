"""Independent DB self-clean check - FRESH oracledb connection, run AFTER the live 5/5 run,
scans OV_TANK's CODE and NAME columns for any AUTOTEST% residual."""
import os
import oracledb

conn = oracledb.connect(
    user=os.environ.get("EC_DB_USER", "ECKERNEL_EC"),
    password=os.environ.get("EC_DB_PASS", "energy"),
    dsn=os.environ.get("EC_DB_DSN", "localhost:1521/ORCL"),
)
cur = conn.cursor()
cur.execute("SELECT CODE, NAME FROM OV_TANK WHERE UPPER(CODE) LIKE 'AUTOTEST%' OR UPPER(NAME) LIKE 'AUTOTEST%'")
rows = cur.fetchall()
print("residual AUTOTEST% rows in OV_TANK:", len(rows))
for r in rows:
    print("  ", r)
conn.close()
