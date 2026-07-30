"""Read-only: confirm OV_NODE has CODE + NAME columns (local sandbox)."""
import os
import oracledb

dsn = os.environ.get("EC_DB_DSN", "localhost:1521/ORCL")
usr = os.environ.get("EC_DB_USER", "ECKERNEL_EC")
pwd = os.environ.get("EC_DB_PASS", "energy")
con = oracledb.connect(user=usr, password=pwd, dsn=dsn)
cur = con.cursor()
cur.execute("""
    SELECT column_name FROM all_tab_columns
    WHERE table_name = 'OV_NODE' AND column_name IN ('CODE','NAME','OBJECT_START_DATE','OBJECT_END_DATE')
    ORDER BY column_name
""")
cols = [r[0] for r in cur.fetchall()]
print("OV_NODE relevant columns:", cols)
cur.execute("SELECT COUNT(*) FROM OV_NODE WHERE CODE LIKE 'AUTOTEST%'")
print("existing AUTOTEST rows in OV_NODE:", cur.fetchone()[0])
con.close()
