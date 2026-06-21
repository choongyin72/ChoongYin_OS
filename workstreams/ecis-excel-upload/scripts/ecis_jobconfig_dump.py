"""Dump the exact wiring template to clone for CLAUDE_EXCEL_IMPORT: EXCEL_IMPORT_1/_2 action-instance rows,
their params, and their ACTION_JOB_CONFIG chains (all columns), plus PK/sequence info. Read-only.
py -X utf8 this.
"""
import os
import oracledb

conn = oracledb.connect(user="ECKERNEL_EC", password="energy",
                        dsn=os.environ.get("EC_DB_DSN", "localhost:1521/ORCL"))
cur = conn.cursor()


def dump(label, sql, **kw):
    cur.execute(sql, **kw)
    cnames = [d[0] for d in cur.description]
    rows = cur.fetchall()
    print(f"\n== {label} == ({len(rows)} rows)\n   cols={cnames}")
    for r in rows:
        print("   ", r)


# job ids the product instances point at
dump("ACTION_JOB_CONFIG for EXCEL_IMPORT_1 / EXCEL_IMPORT_2",
     "SELECT job_config_no, job_id, job_action_no, job_action_class, param_name, param_value, transport_component_ind, record_status FROM action_job_config WHERE job_id IN ('EXCEL_IMPORT_1','EXCEL_IMPORT_2') ORDER BY job_id, job_action_no, param_name")

dump("TV_ACTION_INSTANCE rows for 5079/5080 (full)",
     "SELECT * FROM tv_action_instance WHERE schedule_no IN (5079,5080) ORDER BY schedule_no")

dump("TV_ACTION_INSTANCE_PARAM rows for those instances (full)",
     "SELECT * FROM tv_action_instance_param WHERE action_instance_no IN (5214,5215) ORDER BY action_instance_no")

# current CLAUDE schedule shell
dump("CLAUDE schedule shell (5110)",
     "SELECT schedule_no, name, enabled, status FROM tv_schedule_list WHERE schedule_no=5110")

# PK / sequence info
dump("max PKs",
     "SELECT (SELECT MAX(job_config_no) FROM action_job_config) mx_jc, (SELECT MAX(action_instance_no) FROM tv_action_instance) mx_ai, (SELECT MAX(action_parameter_no) FROM tv_action_instance_param) mx_ap FROM dual")

dump("sequences for these tables?",
     "SELECT sequence_name FROM user_sequences WHERE sequence_name LIKE '%ACTION%' OR sequence_name LIKE '%JOB_CONFIG%' OR sequence_name LIKE '%INSTANCE%'")

conn.close()
print("\nDONE")
