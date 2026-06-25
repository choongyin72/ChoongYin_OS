"""Understand ECIS schedule wiring from the DB (real schema) + compare CLAUDE_EXCEL_IMPORT (5110, partial?)
against the proven product EXCEL_IMPORT_1/_2. Read-only. py -X utf8 this.
"""
import os
import oracledb

conn = oracledb.connect(user="ECKERNEL_EC", password="energy",
                        dsn=os.environ.get("EC_DB_DSN", "localhost:1521/ORCL"))
cur = conn.cursor()


def cols(tab):
    cur.execute("SELECT column_name FROM user_tab_columns WHERE table_name=:t ORDER BY column_id", t=tab)
    print(f"\n-- {tab} columns: {[r[0] for r in cur.fetchall()]}")


def dump(label, sql, **kw):
    try:
        cur.execute(sql, **kw)
        cnames = [d[0] for d in cur.description]
        rows = cur.fetchall()
        print(f"\n== {label} == ({len(rows)} rows) {cnames}")
        for r in rows[:50]:
            print("  ", r)
    except Exception as e:
        print(f"\n== {label} == ERROR {str(e)[:150]}")


for t in ("TV_ACTION_INSTANCE", "TV_ACTION_INSTANCE_PARAM", "ACTION_JOB_CONFIG"):
    cols(t)

dump("action instances (5110 CLAUDE vs 5079/5080)",
     "SELECT * FROM tv_action_instance WHERE schedule_no IN (5110,5079,5080) ORDER BY schedule_no")

dump("action-instance params (5110 vs 5079/5080)",
     """SELECT ai.schedule_no, p.* FROM tv_action_instance_param p
        JOIN tv_action_instance ai ON p.action_instance_no=ai.action_instance_no
        WHERE ai.schedule_no IN (5110,5079,5080) ORDER BY ai.schedule_no""")

conn.close()
print("\nDONE")
