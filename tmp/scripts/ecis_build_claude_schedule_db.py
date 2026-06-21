"""Finish the CLAUDE_EXCEL_IMPORT schedule (5110) action chain by CLONING the proven product wiring in the DB
(the Flyway-style delivery path). Mirrors EXCEL_IMPORT_1/_2 exactly, only swapping INTERFACE_CODE ->
CLAUDE_WELL_TEST. Non-destructive (INSERTs only); prints every new PK so it is fully reversible.

Builds:
  ACTION_JOB_CONFIG  job_id 'CLAUDE_JOB'      = clone of EXCEL_IMPORT_1 (AdvancedExcel -> StagingTarget)
  ACTION_JOB_CONFIG  job_id 'CLAUDE_STAGE2EC' = clone of EXCEL_IMPORT_2 (StagingSource -> TargetMapping)
  TV_ACTION_INSTANCE x2 on schedule 5110 (exec_order 10 -> CLAUDE_JOB, 20 -> CLAUDE_STAGE2EC)
  TV_ACTION_INSTANCE_PARAM x2 (jobid = CLAUDE_JOB / CLAUDE_STAGE2EC)
py -X utf8 this.
"""
import os
import oracledb

conn = oracledb.connect(user="ECKERNEL_EC", password="energy",
                        dsn=os.environ.get("EC_DB_DSN", "localhost:1521/ORCL"))
cur = conn.cursor()
NEW = {"action_job_config": [], "tv_action_instance": [], "tv_action_instance_param": []}


def colnames(tab):
    cur.execute(f"SELECT * FROM {tab} WHERE 1=0")
    return [d[0] for d in cur.description]


def clone_select(tab, where, overrides):
    """INSERT INTO tab (...) SELECT ... FROM tab WHERE where, with per-column SQL-expression overrides."""
    cols = colnames(tab)
    exprs = [overrides.get(c, c) for c in cols]
    sql = f"INSERT INTO {tab} ({', '.join(cols)}) SELECT {', '.join(exprs)} FROM {tab} WHERE {where}"
    cur.execute(sql)
    return cur.rowcount


# guard: don't double-build
cur.execute("SELECT COUNT(*) FROM action_job_config WHERE job_id IN ('CLAUDE_JOB','CLAUDE_STAGE2EC')")
if cur.fetchone()[0] > 0:
    print("CLAUDE job config already present - aborting to avoid duplicates. Clean first if rebuilding.")
    raise SystemExit

# 1) ACTION_JOB_CONFIG clones (multi-row; unique PK via MAX+ROWNUM)
n1 = clone_select("action_job_config", "job_id='EXCEL_IMPORT_1'", {
    "JOB_CONFIG_NO": "(SELECT MAX(job_config_no) FROM action_job_config)+ROWNUM",
    "JOB_ID": "'CLAUDE_JOB'",
    "PARAM_VALUE": "CASE WHEN param_name='INTERFACE_CODE' THEN 'CLAUDE_WELL_TEST' ELSE param_value END",
    "REC_ID": "RAWTOHEX(SYS_GUID())",
})
n2 = clone_select("action_job_config", "job_id='EXCEL_IMPORT_2'", {
    "JOB_CONFIG_NO": "(SELECT MAX(job_config_no) FROM action_job_config)+ROWNUM",
    "JOB_ID": "'CLAUDE_STAGE2EC'",
    "PARAM_VALUE": "CASE WHEN param_name='INTERFACE_CODE' THEN 'CLAUDE_WELL_TEST' ELSE param_value END",
    "REC_ID": "RAWTOHEX(SYS_GUID())",
})
print(f"ACTION_JOB_CONFIG: CLAUDE_JOB {n1} rows, CLAUDE_STAGE2EC {n2} rows")

# 2) TV_ACTION_INSTANCE x2 (compute literal PKs so the two rows are unique + ordered)
cur.execute("SELECT NVL(MAX(action_instance_no),0) FROM tv_action_instance")
ai0 = cur.fetchone()[0]
ai_1, ai_2 = ai0 + 1, ai0 + 2
clone_select("tv_action_instance", "action_instance_no=5214", {
    "ACTION_INSTANCE_NO": str(ai_1), "SCHEDULE_NO": "5110", "ISOLATED_TX_IND": "'N'",
    "SCHEDULE_NAME": "'CLAUDE_EXCEL_IMPORT'", "EXEC_ORDER": "10", "REC_ID": "RAWTOHEX(SYS_GUID())",
})
clone_select("tv_action_instance", "action_instance_no=5215", {
    "ACTION_INSTANCE_NO": str(ai_2), "SCHEDULE_NO": "5110", "ISOLATED_TX_IND": "'N'",
    "SCHEDULE_NAME": "'CLAUDE_EXCEL_IMPORT'", "EXEC_ORDER": "20", "REC_ID": "RAWTOHEX(SYS_GUID())",
})
print(f"TV_ACTION_INSTANCE: new nos {ai_1} (exec 10), {ai_2} (exec 20) on schedule 5110")

# 3) TV_ACTION_INSTANCE_PARAM x2 (jobid -> CLAUDE_JOB / CLAUDE_STAGE2EC)
cur.execute("SELECT NVL(MAX(action_parameter_no),0) FROM tv_action_instance_param")
ap0 = cur.fetchone()[0]
ap_1, ap_2 = ap0 + 1, ap0 + 2


def insert_jobid_param(ap_no, ai_no, jobid):
    cur.execute(
        """INSERT INTO tv_action_instance_param
             (table_class_name, action_parameter_no, name, action_instance_no, functional_area_code,
              schedule_name, exec_order, parameter_value, parameter_subtype, parameter_type, record_status,
              created_by, created_date, rev_no, rec_id)
           VALUES ('ACTION_INSTANCE_PARAM', :ap, 'jobid', :ai, 'ECIS', 'CLAUDE_EXCEL_IMPORT', 10,
              :val, 'STRING', 'BASIC_TYPE', 'P', 'ECKERNEL_EC', SYSDATE, 0, RAWTOHEX(SYS_GUID()))""",
        ap=ap_no, ai=ai_no, val=jobid)


insert_jobid_param(ap_1, ai_1, "CLAUDE_JOB")
insert_jobid_param(ap_2, ai_2, "CLAUDE_STAGE2EC")
print(f"TV_ACTION_INSTANCE_PARAM: new nos {ap_1}, {ap_2}")

conn.commit()
print("COMMITTED.")
print(f"REVERT KEYS -> action_instance_no IN ({ai_1},{ai_2}); action_parameter_no IN ({ap_1},{ap_2}); "
      f"action_job_config job_id IN ('CLAUDE_JOB','CLAUDE_STAGE2EC')")

# verify
cur.execute("""SELECT ai.exec_order, ai.business_action_name, p.parameter_value AS jobid
               FROM tv_action_instance ai JOIN tv_action_instance_param p ON p.action_instance_no=ai.action_instance_no
               WHERE ai.schedule_no=5110 ORDER BY ai.exec_order""")
print("\nVERIFY instances on 5110:", cur.fetchall())
cur.execute("""SELECT job_id, job_action_no, job_action_class, param_name, param_value
               FROM action_job_config WHERE job_id IN ('CLAUDE_JOB','CLAUDE_STAGE2EC')
               AND (param_name='INTERFACE_CODE' OR param_name IS NULL) ORDER BY job_id, job_action_no""")
print("VERIFY job actions (interface code + chain):")
for r in cur.fetchall():
    print("  ", r)
conn.close()
print("\nDONE")
