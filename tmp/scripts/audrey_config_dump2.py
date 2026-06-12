"""Dump AUDREY config + AudreyExcelImport schedule with the REAL 14.2.4 columns."""
import os

import oracledb

conn = oracledb.connect(user="ECKERNEL_EC", password="energy",
                        dsn=os.environ.get("EC_DB_DSN", "localhost:1521/ORCL"))
cur = conn.cursor()

def q(title, sql, **kw):
    print(f"\n== {title} ==")
    try:
        cur.execute(sql, **kw)
        cols = [d[0] for d in cur.description]
        rows = cur.fetchall()
        if not rows:
            print("  (no rows)")
        for r in rows:
            print("  " + " | ".join(f"{c}={v}" for c, v in zip(cols, r) if v is not None))
    except Exception as e:
        print(f"  ERR {str(e)[:140]}")

q("ALL INTERFACES",
  "SELECT object_code, name, type, transaction_type, source_type, staging_validation_ind, ec_valid_level, ec_data_level, overwrite FROM imp_source_interface")
q("AUDREY SOURCE MAPPINGS",
  """SELECT m.code, m.sort_order, m.path_origin, m.type, m.value_type, m.ec_key,
            m.key_1, m.key_2, m.key_3
     FROM imp_source_mapping m JOIN imp_source_interface i ON i.object_id = m.imp_source_interface_id
     WHERE UPPER(i.object_code) LIKE '%AUDREY%' ORDER BY m.sort_order""")
q("AUDREY SOURCE PATHS",
  """SELECT m.code AS mapping, p.sort_order, p.type, p.path, p.path_param_1, p.path_param_2
     FROM imp_source_path p
     JOIN imp_source_mapping m ON m.object_id = p.imp_source_mapping_id
     JOIN imp_source_interface i ON i.object_id = m.imp_source_interface_id
     WHERE UPPER(i.object_code) LIKE '%AUDREY%' ORDER BY m.sort_order, p.sort_order""")
q("AUDREY TARGET MAPPINGS",
  """SELECT t.ec_key, t.class, t.attribute, t.class_key_1, t.class_key_2, t.class_key_3,
            t.constant_string_value, t.constant_number_value, t.constant_date_value
     FROM imp_target_mapping t
     LEFT JOIN imp_source_interface i ON i.object_id = t.imp_source_interface_id
     WHERE UPPER(NVL(i.object_code,'-')) LIKE '%AUDREY%'
        OR t.ec_key IN (SELECT m.ec_key FROM imp_source_mapping m
                        JOIN imp_source_interface i2 ON i2.object_id = m.imp_source_interface_id
                        WHERE UPPER(i2.object_code) LIKE '%AUDREY%' AND m.ec_key IS NOT NULL)""")
q("AUDREY SCHEDULE (TV_SCHEDULE_LIST)",
  "SELECT schedule_no, name, schedule_type, enabled, status, pin_to, func_name FROM tv_schedule_list WHERE UPPER(name) LIKE '%AUDREY%'")
q("SCHEDULE DETAILS",
  "SELECT name, username, log_level, retain_count, ignore_misfire FROM tv_schedule_details WHERE UPPER(name) LIKE '%AUDREY%'")
q("ACTION INSTANCES",
  """SELECT a.action_instance_no, a.business_action_no, a.business_action_name, a.exec_order, a.schedule_name
     FROM tv_action_instance a WHERE UPPER(a.schedule_name) LIKE '%AUDREY%' ORDER BY a.exec_order""")
q("ACTION JOB CONFIG (via JOB_ID like audrey OR business action join)",
  "SELECT job_id, job_action_no, job_action_class, param_name, param_value FROM action_job_config WHERE UPPER(job_id) LIKE '%AUDREY%' ORDER BY job_action_no, param_name")
q("BUSINESS ACTION rows referenced",
  """SELECT b.* FROM (SELECT business_action_no FROM tv_action_instance WHERE UPPER(schedule_name) LIKE '%AUDREY%') x
     JOIN business_action b ON b.business_action_no = x.business_action_no""")
conn.close()
