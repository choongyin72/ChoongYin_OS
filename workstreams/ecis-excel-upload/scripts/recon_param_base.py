"""Crack the param ORA-01779: is TV_ACTION_INSTANCE_PARAM a view? what's the base table + its columns?
read the trigger around line 85. Read-only. py -X utf8 this.
"""
import os
import oracledb

conn = oracledb.connect(user="ECKERNEL_EC", password="energy",
                        dsn=os.environ.get("EC_DB_DSN", "localhost:1521/ORCL"))
cur = conn.cursor()


def show(label, sql, **kw):
    cur.execute(sql, **kw)
    print(f"\n== {label} ==")
    for r in cur.fetchall():
        print("  ", r)


show("object types",
     "SELECT object_name, object_type FROM user_objects WHERE object_name IN "
     "('TV_ACTION_INSTANCE_PARAM','ACTION_INSTANCE_PARAM','TV_ACTION_INSTANCE','ACTION_INSTANCE') ORDER BY object_name")

# if base table ACTION_INSTANCE_PARAM exists, list NOT NULL columns
show("ACTION_INSTANCE_PARAM (base) NOT NULL columns",
     "SELECT column_name, data_type, nullable FROM user_tab_columns WHERE table_name='ACTION_INSTANCE_PARAM' ORDER BY column_id")

# trigger body around the failing line
cur.execute("SELECT line, text FROM user_source WHERE name='IUD_ACTION_INSTANCE_PARAM' AND type='TRIGGER' AND line BETWEEN 60 AND 100 ORDER BY line")
print("\n== IUD_ACTION_INSTANCE_PARAM trigger lines 60-100 ==")
for ln, txt in cur.fetchall():
    print(f"  {ln:3} {txt.rstrip()}")

conn.close()
print("\nDONE")
