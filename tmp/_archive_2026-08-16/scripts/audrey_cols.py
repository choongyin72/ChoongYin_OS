"""Get the actual 14.2.4 column names for the IMP_* and scheduler tables."""
import os

import oracledb

conn = oracledb.connect(user="ECKERNEL_EC", password="energy",
                        dsn=os.environ.get("EC_DB_DSN", "localhost:1521/ORCL"))
cur = conn.cursor()
for t in ["IMP_SOURCE_INTERFACE", "IMP_SOURCE_MAPPING", "IMP_SOURCE_PATH",
          "IMP_TARGET_MAPPING", "IMP_STAGING", "IMP_SOURCE_INTERFACE_FILE",
          "TV_SCHEDULE_LIST", "TV_SCHEDULE_DETAILS", "TV_JOB_SCHEDULE",
          "TV_ACTION_INSTANCE", "ACTION_JOB_CONFIG"]:
    cur.execute("""SELECT column_name FROM all_tab_columns
                   WHERE owner='ECKERNEL_EC' AND table_name=:t ORDER BY column_id""", t=t)
    cols = [r[0] for r in cur.fetchall()]
    print(f"{t} ({len(cols)}): {', '.join(cols[:24])}")
conn.close()
