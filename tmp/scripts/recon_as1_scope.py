"""Find AS1_Well_001's nav scope (PU/Area/Facility/Well names) for the Daily Prod Well Status navigator.
Read-only. py -X utf8 this."""
import os
import oracledb

conn = oracledb.connect(user="ECKERNEL_EC", password="energy",
                        dsn=os.environ.get("EC_DB_DSN", "localhost:1521/ORCL"))
cur = conn.cursor()


def show(label, sql, **kw):
    try:
        cur.execute(sql, **kw)
        cols = [d[0] for d in cur.description]
        rows = cur.fetchall()
        print(f"\n== {label} == cols={cols}")
        for r in rows[:10]:
            print("  ", r)
    except Exception as e:
        print(f"\n== {label} == ERR {str(e)[:130]}")


# ov_well columns then row
cur.execute("SELECT column_name FROM user_tab_columns WHERE table_name='OV_WELL' ORDER BY column_id")
print("OV_WELL cols:", [r[0] for r in cur.fetchall()][:40])
show("OV_WELL AS1_Well_001", "SELECT * FROM ov_well WHERE object_code='AS1_Well_001'")
# common hierarchy view
show("well hookup / hierarchy", "SELECT * FROM ov_well_hookup WHERE well_code='AS1_Well_001' AND ROWNUM<=3")
conn.close()
print("\nDONE")
