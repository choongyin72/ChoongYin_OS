"""Inspect PWEL_DAY_ALLOC structure + a 2021-10-01 sample (READ-ONLY) to see if existing allocation
results support a conservation check (no-neg / sum-to-total) without running a fresh calc."""
import oracledb
c = oracledb.connect(user="ECKERNEL_EC", password="energy", dsn="localhost:1521/ORCL", tcp_connect_timeout=15).cursor()
print("=== PWEL_DAY_ALLOC columns ===")
c.execute("""SELECT column_name, data_type FROM all_tab_columns WHERE owner='ECKERNEL_EC'
             AND table_name='PWEL_DAY_ALLOC' ORDER BY column_id""")
cols=c.fetchall()
for n,dt in cols: print(f"   {n:26} {dt}")
print("\n=== sample 2021-10-01 rows (non-null fields) ===")
c.execute("SELECT * FROM ECKERNEL_EC.PWEL_DAY_ALLOC WHERE TRUNC(DAYTIME)=DATE '2021-10-01' AND ROWNUM<=3")
names=[d[0] for d in c.description]
for r in c.fetchall():
    print("  ", {n:str(v)[:22] for n,v in zip(names,r) if v is not None})
print("\n=== any negative allocated values on 2021-10-01? (conservation no-neg check) ===")
# build a check over NUMBER columns
numcols=[n for n,dt in cols if dt=='NUMBER' and n not in ('REV_NO',)]
checks=" OR ".join([f'"{n}" < 0' for n in numcols[:60]])
try:
    c.execute(f"SELECT COUNT(*) FROM ECKERNEL_EC.PWEL_DAY_ALLOC WHERE TRUNC(DAYTIME)=DATE '2021-10-01' AND ({checks})")
    print("   rows with a negative allocated value:", c.fetchone()[0])
except Exception as e: print("   ERR:", str(e)[:120])
