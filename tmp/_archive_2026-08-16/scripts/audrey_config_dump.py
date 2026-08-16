"""Dump the AUDREY Advanced File Import configuration + AudreyExcelImport schedule
from the LOCAL EC DB (ground truth behind the Mapping Configuration / Schedules screens)."""
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
            pairs = [f"{c}={v}" for c, v in zip(cols, r) if v is not None]
            print("  " + " | ".join(pairs))
    except Exception as e:
        print(f"  ERR {str(e)[:140]}")

q("INTERFACES (all)", "SELECT interface_code, name, type, transaction_type, source_type, staging_validation_ind, ec_valid_level, ec_data_level, overwrite FROM imp_source_interface")
q("AUDREY SOURCE MAPPINGS",
  "SELECT code, sort_order, path_origin, type, value_type, ec_key, key_1, key_2, key_3 FROM imp_source_mapping WHERE UPPER(interface_code) LIKE '%AUDREY%' ORDER BY sort_order")
q("AUDREY SOURCE PATHS",
  """SELECT m.code, p.sort_order, p.type, p.path, p.path_param_1, p.path_param_2
     FROM imp_source_path p JOIN imp_source_mapping m ON m.imp_source_mapping_no = p.imp_source_mapping_no
     WHERE UPPER(m.interface_code) LIKE '%AUDREY%' ORDER BY m.code, p.sort_order""")
q("AUDREY TARGET MAPPINGS (by EC keys of the source mappings)",
  """SELECT t.ec_key, t.class, t.attribute, t.class_key_1, t.class_key_2, t.class_key_3,
            t.constant_string_value, t.constant_number_value, t.constant_date_value
     FROM imp_target_mapping t WHERE t.ec_key IN
       (SELECT ec_key FROM imp_source_mapping WHERE UPPER(interface_code) LIKE '%AUDREY%' AND ec_key IS NOT NULL)""")
q("SCHEDULES like AUDREY",
  "SELECT name, functional_area_id, enabled, start_date FROM tv_schedule_list WHERE UPPER(name) LIKE '%AUDREY%'")
q("SCHEDULE DETAILS",
  """SELECT l.name, d.username, d.log_level, d.retain_count
     FROM tv_schedule_list l JOIN tv_schedule_details d ON d.schedule_id = l.schedule_id
     WHERE UPPER(l.name) LIKE '%AUDREY%'""")
q("JOB SCHEDULE",
  """SELECT l.name, j.schedule_type, j.pin_to
     FROM tv_schedule_list l JOIN tv_job_schedule j ON j.schedule_id = l.schedule_id
     WHERE UPPER(l.name) LIKE '%AUDREY%'""")
q("ACTION INSTANCES",
  """SELECT l.name, a.business_action_id, a.exec_order, a.action_instance_id
     FROM tv_schedule_list l JOIN tv_action_instance a ON a.schedule_id = l.schedule_id
     WHERE UPPER(l.name) LIKE '%AUDREY%' ORDER BY a.exec_order""")
q("ACTION JOB CONFIG (params)",
  """SELECT c.name, c.parameter_value
     FROM tv_schedule_list l
     JOIN tv_action_instance a ON a.schedule_id = l.schedule_id
     JOIN action_job_config c ON c.action_instance_id = a.action_instance_id
     WHERE UPPER(l.name) LIKE '%AUDREY%' ORDER BY c.name""")
conn.close()
