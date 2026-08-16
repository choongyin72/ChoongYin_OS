"""READ-ONLY: do IWEL_DAY_STATUS% physical tables exist? Resolve the monthly approve targets + counts."""
import os, oracledb
con=oracledb.connect(user=os.environ.get("EC_DB_USER","ECKERNEL_EC"),
 password=os.environ.get("EC_DB_PASS","energy"),
 dsn=os.environ.get("EC_DB_DSN","localhost:1521/ORCL"),tcp_connect_timeout=15)
cur=con.cursor()
cur.execute("SELECT table_name FROM all_tables WHERE owner='ECKERNEL_EC' AND table_name LIKE 'IWEL_DAY_STATUS%' ORDER BY 1")
tabs=[r[0] for r in cur.fetchall()]
print("IWEL_DAY_STATUS% physical tables:", tabs)
for t in tabs:
    try:
        cur.execute(f"SELECT RECORD_STATUS, COUNT(*) FROM {t} GROUP BY RECORD_STATUS ORDER BY 1")
        print(f"  {t}:", cur.fetchall())
    except Exception as e: print(f"  {t} ERR:", str(e)[:80])
# TABLE_ID resolution metadata: how EC maps TABLE_ID 'IWEL_DAY_STATUS_AIR' -> physical
cur.execute("""SELECT table_name FROM all_tables WHERE owner='ECKERNEL_EC'
 AND (table_name='CTRL_TABLE' OR table_name LIKE 'CTRL_TABLE%' OR table_name LIKE '%TABLE_DEF%')""")
print("\nTABLE_ID metadata candidates:", [r[0] for r in cur.fetchall()])
con.close();print("DONE")
