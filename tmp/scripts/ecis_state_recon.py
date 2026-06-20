"""Recon current ECIS state on the local sandbox DB before rebuilding the demo: is the CLAUDE_WELL_TEST
interface + its mappings present, is the CLAUDE_EXCEL_IMPORT schedule present, do the demo wells exist, and
what's the baseline dv_pwel_day_status for the test date. Read-only. py -X utf8 this.
"""
import os
import oracledb

dsn = os.environ.get("EC_DB_DSN", "localhost:1521/ORCL")
conn = oracledb.connect(user=os.environ.get("EC_DB_USER", "ECKERNEL_EC"),
                        password=os.environ.get("EC_DB_PWD", "energy"), dsn=dsn)
cur = conn.cursor()


def q(label, sql, **kw):
    try:
        cur.execute(sql, **kw)
        rows = cur.fetchall()
        print(f"{label}: {rows}")
    except Exception as e:
        print(f"{label}: ERROR {str(e)[:120]}")


print("DSN:", dsn)
q("interface CLAUDE_WELL_TEST",
  "SELECT object_code, name, type, transaction_type, overwrite FROM imp_source_interface WHERE object_code='CLAUDE_WELL_TEST'")
q("source mappings count",
  "SELECT COUNT(*) FROM imp_source_mapping m JOIN imp_source_interface i ON m.imp_source_interface_id=i.object_id WHERE i.object_code='CLAUDE_WELL_TEST'")
q("target mappings count",
  "SELECT COUNT(*) FROM imp_target_mapping t JOIN imp_source_interface i ON t.imp_source_interface_id=i.object_id WHERE i.object_code='CLAUDE_WELL_TEST'")
q("schedule CLAUDE_EXCEL_IMPORT",
  "SELECT schedule_no, name, enabled, status FROM tv_schedule_list WHERE name='CLAUDE_EXCEL_IMPORT'")
q("demo wells AS1_Well_001..003",
  "SELECT object_code FROM well WHERE object_code IN ('AS1_Well_001','AS1_Well_002','AS1_Well_003') ORDER BY object_code")
q("baseline dv_pwel_day_status 2003-01-05",
  "SELECT object_code, avg_bh_press FROM dv_pwel_day_status WHERE daytime=DATE '2003-01-05' AND object_code IN ('AS1_Well_001','AS1_Well_002','AS1_Well_003') ORDER BY object_code")
q("EXCEL_IMPORT product interface (reference exists?)",
  "SELECT object_code FROM imp_source_interface WHERE object_code IN ('EXCEL_IMPORT','AUDREY')")
conn.close()
print("DONE")
