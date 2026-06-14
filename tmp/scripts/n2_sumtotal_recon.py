"""N2 sum-to-total recon: is a clean conservation check feasible on existing 2021-10-01 data?
Need: (a) which network/wells produced the 22 PWEL_DAY_ALLOC rows, (b) a 'total' to conserve to
(STRM_DAY_*_ALLOC stream/field totals, or a measured source). Read-only."""
import os
import oracledb

conn = oracledb.connect(
    user=os.environ.get("EC_DB_USER", "ECKERNEL_EC"),
    password=os.environ.get("EC_DB_PASS", "energy"),
    dsn=os.environ.get("EC_DB_DSN", "localhost:1521/ORCL"),
    tcp_connect_timeout=15,
)
cur = conn.cursor()
DAY = "2021-10-01"

def show(title, sql, binds=None, limit=30):
    print(f"\n=== {title} ===")
    try:
        cur.execute(sql, binds or {})
        cols = [d[0] for d in cur.description]
        print(" | ".join(cols))
        for i, row in enumerate(cur.fetchall()):
            if i >= limit:
                print("  ...(truncated)"); break
            print("  " + " | ".join("" if v is None else str(v) for v in row))
    except Exception as e:
        print("  ERR:", str(e)[:200])

# 1. The 22 wells + their key alloc volumes on the day
show("PWEL_DAY_ALLOC wells on day (name + gas/oil/water vol)",
    """SELECT a.OBJECT_ID, w.NAME,
              ROUND(a.ALLOC_GAS_VOL,3) GAS, ROUND(a.ALLOC_NET_OIL_VOL,3) OIL,
              ROUND(a.ALLOC_WATER_VOL,3) WATER, ROUND(a.THEOR_GAS_VOL,3) THEOR_GAS
       FROM PWEL_DAY_ALLOC a LEFT JOIN WELL_VERSION w
         ON w.OBJECT_ID=a.OBJECT_ID AND TRUNC(a.DAYTIME) BETWEEN TRUNC(w.DAYTIME) AND NVL(w.END_DATE,DATE'9999-01-01')
       WHERE TRUNC(a.DAYTIME)=TO_DATE(:d,'YYYY-MM-DD') ORDER BY w.NAME""",
    {"d": DAY})

# 2. Sum of per-well alloc volumes (the 'allocated total')
show("SUM of per-well ALLOC volumes on day",
    """SELECT ROUND(SUM(ALLOC_GAS_VOL),3) SUM_GAS, ROUND(SUM(ALLOC_NET_OIL_VOL),3) SUM_OIL,
              ROUND(SUM(ALLOC_WATER_VOL),3) SUM_WATER, ROUND(SUM(THEOR_GAS_VOL),3) SUM_THEOR_GAS
       FROM PWEL_DAY_ALLOC WHERE TRUNC(DAYTIME)=TO_DATE(:d,'YYYY-MM-DD')""",
    {"d": DAY})

# 3. Stream-level allocation totals same day (candidate 'total to conserve to')
show("STRM_DAY_ALLOC on day (stream totals)",
    """SELECT s.OBJECT_ID, st.NAME, ROUND(s.ALLOC_GAS_VOL,3) GAS, ROUND(s.ALLOC_NET_OIL_VOL,3) OIL,
              ROUND(s.ALLOC_WATER_VOL,3) WATER
       FROM STRM_DAY_ALLOC s LEFT JOIN OV_STREAM st ON st.OBJECT_ID=s.OBJECT_ID
       WHERE TRUNC(s.DAYTIME)=TO_DATE(:d,'YYYY-MM-DD') ORDER BY st.NAME""",
    {"d": DAY})

# 4. Does STRM_DAY_ALLOC even have rows on this day? counts on nearby days
show("STRM_DAY_ALLOC row count on day + any data dates",
    """SELECT TO_CHAR(TRUNC(DAYTIME),'YYYY-MM-DD') d, COUNT(*) n FROM STRM_DAY_ALLOC
       GROUP BY TRUNC(DAYTIME) ORDER BY n DESC FETCH FIRST 6 ROWS ONLY""")

# 5. ALLOC_NETWORK_JOB_CONN structure (network<->job<->? mapping)
show("ALLOC_NETWORK_JOB_CONN columns",
    """SELECT column_name FROM all_tab_columns WHERE table_name='ALLOC_NETWORK_JOB_CONN' ORDER BY column_id""")

# 6. THEOR vs ALLOC: conservation often = sum(ALLOC)=measured total, ALLOC prorated from THEOR.
#    Check if per-well ALLOC sums relate to a field/stream measured total via PWEL ratios.
show("Per-well ALLOC vs THEOR ratio sanity (gas)",
    """SELECT ROUND(SUM(ALLOC_GAS_VOL),3) SUM_ALLOC_GAS, ROUND(SUM(THEOR_GAS_VOL),3) SUM_THEOR_GAS,
              ROUND(SUM(PREC_THEOR_GAS_VOL),3) SUM_PREC_THEOR_GAS
       FROM PWEL_DAY_ALLOC WHERE TRUNC(DAYTIME)=TO_DATE(:d,'YYYY-MM-DD')""",
    {"d": DAY})

cur.close(); conn.close()
print("\nDONE")
