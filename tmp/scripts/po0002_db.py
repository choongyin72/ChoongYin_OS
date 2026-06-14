"""PO.0002 DB recon (READ-ONLY): describe STRM_DAY_STREAM_MEAS_GAS (the editable measured gas
stream table), key columns, row count, and a data-bearing sample on 2003-01-01."""
import oracledb
c = oracledb.connect(user="ECKERNEL_EC", password="energy", dsn="localhost:1521/ORCL", tcp_connect_timeout=15).cursor()

print("=== STRM_DAY_STREAM_MEAS_GAS columns ===")
c.execute("""SELECT column_name, data_type FROM all_tab_columns
             WHERE owner='ECKERNEL_EC' AND table_name='STRM_DAY_STREAM_MEAS_GAS' ORDER BY column_id""")
cols = c.fetchall()
for n, dt in cols:
    print(f"   {n:28} {dt}")

try:
    c.execute("SELECT COUNT(*) FROM ECKERNEL_EC.STRM_DAY_STREAM_MEAS_GAS")
    print("\nrow count:", c.fetchone()[0])
except Exception as e:
    print("count err:", str(e)[:120])

print("\n=== sample row WITH data on 2003-01-01 (non-null measured cols) ===")
try:
    c.execute("""SELECT * FROM ECKERNEL_EC.STRM_DAY_STREAM_MEAS_GAS
                 WHERE TRUNC(DAYTIME)=DATE '2003-01-01' AND ROWNUM<=3""")
    names = [d[0] for d in c.description]
    for r in c.fetchall():
        d = {n: v for n, v in zip(names, r) if v is not None}
        print("  ", d)
except Exception as e:
    print("sample err:", str(e)[:140])
