"""RECON (read-only): map the Laboratory / Sample-Analysis lineage in the sandbox DB. Find the
SAMPLE / LAB / ANALYSIS / SAMPLING_POINT tables+views, their row counts, and how they chain toward the
composition analysis (DV_STRM_COMP_ANALYSIS) we automated. SELECT only."""
import os
import oracledb

conn = oracledb.connect(user="ECKERNEL_EC", password=os.environ.get("EC_DB_PWD", "energy"),
                        dsn=os.environ.get("EC_DB_DSN", "localhost:1521/ORCL"), tcp_connect_timeout=15)
cur = conn.cursor()


def q(sql, *a):
    cur.execute(sql, a)
    return cur.fetchall()


print("=== Tables/views matching SAMPLE / LAB / ANALYSIS / SAMPLING (with row counts) ===")
objs = q("""SELECT object_name, object_type FROM all_objects
            WHERE owner='ECKERNEL_EC' AND object_type IN ('TABLE','VIEW')
              AND ( object_name LIKE '%SAMPLE%' OR object_name LIKE '%SAMPLING%'
                    OR object_name LIKE 'LAB%' OR object_name LIKE '%_LAB_%'
                    OR object_name LIKE '%ANALYSIS%' OR object_name LIKE '%COMP_ANALYS%' )
              AND object_name NOT LIKE '%JN'
            ORDER BY object_type, object_name""")
for name, otype in objs:
    try:
        cur.execute(f"SELECT COUNT(*) FROM ECKERNEL_EC.{name}")
        n = cur.fetchone()[0]
    except Exception:
        n = "?"
    if (isinstance(n, int) and n > 0) or otype == 'TABLE':
        print(f"  {otype[0]} {name:42s} rows={n}")

print("\n=== Columns of the core lab/sample tables (if present) ===")
for t in ("SAMPLE", "SAMPLE_VERSION", "SAMPLING_POINT", "SAMPLING_POINT_VERSION", "LAB_ANALYSIS",
          "SAMPLE_ANALYSIS", "ANALYSIS", "STRM_COMP_ANALYSIS", "WELL_FLUID_ANALYSIS",
          "DV_SAMPLE", "OV_SAMPLING_POINT"):
    cols = [c[0] for c in q("""SELECT column_name FROM all_tab_columns
            WHERE owner='ECKERNEL_EC' AND table_name=:t ORDER BY column_id""", t)]
    if cols:
        print(f"  {t} ({len(cols)}): {', '.join(cols[:28])}")

print("\n=== FK relationships into/out of *ANALYSIS* and *SAMPLE* tables (lineage edges) ===")
for r in q("""SELECT ac.table_name child, ac.constraint_name, acp.table_name parent
              FROM all_constraints ac
              JOIN all_constraints acp ON ac.r_constraint_name=acp.constraint_name AND ac.r_owner=acp.owner
              WHERE ac.owner='ECKERNEL_EC' AND ac.constraint_type='R'
                AND ( ac.table_name LIKE '%ANALYSIS%' OR ac.table_name LIKE '%SAMPLE%'
                      OR acp.table_name LIKE '%ANALYSIS%' OR acp.table_name LIKE '%SAMPLE%' )
              ORDER BY 1 FETCH FIRST 40 ROWS ONLY"""):
    print(f"  {r[0]} --FK--> {r[2]}")

cur.close()
conn.close()
print("\nDONE (read-only)")
