"""RECON (read-only): resolve the navigator scope (PU / Area / Facility Class 1) for the oil-comp target
stream 'P1 Alloc S001 M OIL' so the PO.0019 grid can be navigated to it. Inspect OV_STREAM hierarchy
columns, then read this stream's values. SELECT only."""
import os
import oracledb

conn = oracledb.connect(user="ECKERNEL_EC", password=os.environ.get("EC_DB_PWD", "energy"),
                        dsn=os.environ.get("EC_DB_DSN", "localhost:1521/ORCL"), tcp_connect_timeout=15)
cur = conn.cursor()


def q(sql, *a):
    cur.execute(sql, a); return cur.fetchall()


print("=== OV_STREAM columns hinting at PU/Area/Facility hierarchy ===")
cols = [c[0] for c in q("""SELECT column_name FROM all_tab_columns WHERE owner='ECKERNEL_EC'
        AND table_name='OV_STREAM'
        AND (column_name LIKE '%PRODUCTIONUNIT%' OR column_name LIKE '%PROD_UNIT%'
             OR column_name LIKE '%AREA%' OR column_name LIKE '%FACILITY%' OR column_name LIKE '%FCTY%'
             OR column_name LIKE 'OP_%' OR column_name LIKE '%PARENT%') ORDER BY column_id""")]
print("  ", cols)

print("\n=== full OV_STREAM row for the oil target (key hierarchy cols) ===")
sel = ", ".join(["NAME", "CODE"] + cols) if cols else "NAME, CODE"
for r in q(f"""SELECT {sel} FROM ECKERNEL_EC.OV_STREAM
              WHERE NAME='P1 Alloc S001 M OIL' FETCH FIRST 3 ROWS ONLY"""):
    print("  ", dict(zip(["NAME", "CODE"] + cols, r)))

print("\n=== cross-check: which Facility Class 1 / Area / PU does this stream sit under? (via STREAM table) ===")
# Try the production-structure: many EC builds expose the hierarchy on STREAM_VERSION / a stream-facility map
for t in ("STREAM", "STREAM_VERSION"):
    hc = [c[0] for c in q("""SELECT column_name FROM all_tab_columns WHERE owner='ECKERNEL_EC'
            AND table_name=:t AND (column_name LIKE '%FACILITY%' OR column_name LIKE '%AREA%'
            OR column_name LIKE '%PRODUCTIONUNIT%' OR column_name LIKE 'OP_%') ORDER BY column_id""", t)]
    if hc:
        print(f"  {t} hierarchy cols: {hc}")

cur.close(); conn.close()
print("\nDONE")
