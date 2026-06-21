"""Dump the live CLAUDE_WELL_TEST ECIS config from the 4 config tables (+ object types + columns) so we can
generate accurate, idempotent upsert SQL. Read-only. py -X utf8 this.
"""
import os
import oracledb

conn = oracledb.connect(user="ECKERNEL_EC", password="energy", dsn=os.environ.get("EC_DB_DSN", "localhost:1521/ORCL"))
cur = conn.cursor()
TABLES = ["IMP_SOURCE_INTERFACE", "IMP_SOURCE_MAPPING", "IMP_SOURCE_PATH", "IMP_TARGET_MAPPING"]

print("=== object types (TABLE vs VIEW = trigger risk) ===")
for t in TABLES:
    cur.execute("SELECT object_type FROM user_objects WHERE object_name=:t", t=t)
    r = cur.fetchone()
    print(f"  {t}: {r[0] if r else 'NOT FOUND'}")

print("\n=== columns ===")
cols = {}
for t in TABLES:
    cur.execute("SELECT column_name, nullable FROM user_tab_columns WHERE table_name=:t ORDER BY column_id", t=t)
    cols[t] = cur.fetchall()
    print(f"  {t}: {[c[0] for c in cols[t]]}")


def rows(label, sql, **kw):
    cur.execute(sql, **kw)
    cn = [d[0] for d in cur.description]
    rs = cur.fetchall()
    print(f"\n== {label} == ({len(rs)} rows)")
    for r in rs:
        print("  " + " | ".join(f"{c}={v!r}" for c, v in zip(cn, r)))
    return cn, rs


# interface
cn, ir = rows("IMP_SOURCE_INTERFACE (CLAUDE_WELL_TEST)",
              "SELECT * FROM imp_source_interface WHERE object_code='CLAUDE_WELL_TEST'")
oid = None
if ir:
    oid = ir[0][cn.index("OBJECT_ID")]
    print("interface object_id =", oid)

rows("IMP_SOURCE_MAPPING",
     "SELECT * FROM imp_source_mapping WHERE imp_source_interface_id=:o ORDER BY 1", o=oid)
rows("IMP_SOURCE_PATH (commands)",
     "SELECT p.* FROM imp_source_path p JOIN imp_source_mapping m ON p.imp_source_mapping_id=m.imp_source_mapping_id "
     "WHERE m.imp_source_interface_id=:o ORDER BY 1", o=oid)
rows("IMP_TARGET_MAPPING",
     "SELECT * FROM imp_target_mapping WHERE imp_source_interface_id=:o OR imp_source_interface_id IS NULL ORDER BY 1", o=oid)

conn.close()
print("\nDONE")
