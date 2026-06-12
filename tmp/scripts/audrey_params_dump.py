"""Find the action-instance -> JOB_ID binding (BA parameters) + any uploaded AUDREY files."""
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

q("ACTION_PARAMETER tables present",
  """SELECT table_name FROM all_tables WHERE owner='ECKERNEL_EC'
     AND table_name LIKE 'ACTION%PARAM%' ORDER BY table_name""")
q("ACTION_PARAMETER columns",
  "SELECT column_name FROM all_tab_columns WHERE owner='ECKERNEL_EC' AND table_name='ACTION_PARAMETER' ORDER BY column_id")
q("ACTION_PARAMETER_VALUE columns",
  "SELECT column_name FROM all_tab_columns WHERE owner='ECKERNEL_EC' AND table_name='ACTION_PARAMETER_VALUE' ORDER BY column_id")
q("AUDREY action instance params",
  """SELECT v.* FROM action_parameter_value v
     WHERE v.action_instance_no IN (5168, 5169)""")
q("Uploaded files for AUDREY",
  """SELECT interface_code, file_name, file_no, file_source, uploaded_into_ec_ind,
            parsed_date, written_to_ec_date, created_date
     FROM imp_source_interface_file WHERE interface_code='AUDREY' ORDER BY file_no""")
q("IMP_STAGING rows for AUDREY (sample)",
  """SELECT interface_code, code, ec_key, file_name, staging_row, key_1, key_2,
            value_number, value_date, value_string
     FROM imp_staging WHERE interface_code='AUDREY' AND ROWNUM <= 12""")
conn.close()
