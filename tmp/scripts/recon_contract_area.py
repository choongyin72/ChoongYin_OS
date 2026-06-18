"""RECON (read-only): identify 'Contract Area' — its OV view / base table, whether it's OV (manage-object,
date-effective) or TV (table-class), and row count — to anchor the spec-template worked example. SELECT only."""
import os
import oracledb

cur = oracledb.connect(user="ECKERNEL_EC", password=os.environ.get("EC_DB_PWD", "energy"),
                       dsn=os.environ.get("EC_DB_DSN", "localhost:1521/ORCL"), tcp_connect_timeout=15).cursor()


def q(sql, *a):
    cur.execute(sql, a); return cur.fetchall()


print("=== objects matching CONTRACT_AREA / CONTRACT%AREA ===")
for r in q("""SELECT object_name, object_type FROM all_objects WHERE owner='ECKERNEL_EC'
              AND object_type IN ('TABLE','VIEW')
              AND (object_name LIKE '%CONTRACT_AREA%' OR object_name LIKE 'OV_CONTRACT%'
                   OR object_name LIKE '%CNTR_AREA%' OR object_name LIKE '%CONTRACTAREA%')
              AND object_name NOT LIKE '%JN' ORDER BY 2,1 FETCH FIRST 25 ROWS ONLY"""):
    try:
        cur.execute(f"SELECT COUNT(*) FROM ECKERNEL_EC.{r[0]}"); n = cur.fetchone()[0]
    except Exception:
        n = "?"
    print(f"  {r[1][0]} {r[0]:38s} rows={n}")

# columns + date-effective check on the most likely OV view
for cand in ("OV_CONTRACT_AREA", "OV_CNTR_AREA", "OV_CONTRACTAREA"):
    cols = [c[0] for c in q("SELECT column_name FROM all_tab_columns WHERE owner='ECKERNEL_EC' AND table_name=:t ORDER BY column_id", cand)]
    if cols:
        deff = [c for c in cols if c in ("START_DATE", "END_DATE", "OBJECT_ID", "OBJECT_START_DATE")]
        print(f"\n=== {cand} cols ({len(cols)}) ===\n  {', '.join(cols[:25])}")
        print("  date-effective markers:", deff, "->", "OV/Manage-Object (date-effective)" if deff else "likely TV/table-class")
        try:
            print("  sample rows:", q(f"SELECT * FROM ECKERNEL_EC.{cand} FETCH FIRST 2 ROWS ONLY"))
        except Exception:
            pass
        break
cur.close()
print("\nDONE")
