"""Scope the allocation data model for HA.0002 (READ-ONLY DB): allocation-network + calc-job
tables, the *_DAY_ALLOC result tables, and dates/networks that already have allocation data
(=> a safe, input-backed test case to run + verify the conservation oracle)."""
import oracledb
c = oracledb.connect(user="ECKERNEL_EC", password="energy", dsn="localhost:1521/ORCL", tcp_connect_timeout=15).cursor()

def q(label, sql, n=15):
    print(f"\n=== {label} ===")
    try:
        c.execute(sql); rows=c.fetchall()
        for r in rows[:n]: print("  ", tuple(str(v)[:34] for v in r))
        if not rows: print("   (none)")
    except Exception as e:
        print("   ERR:", str(e)[:130])

q("allocation-network / calc-job tables",
  """SELECT table_name FROM all_tables WHERE owner='ECKERNEL_EC'
     AND (table_name LIKE '%ALLOC_NET%' OR table_name LIKE '%ALLOCATION_NET%'
          OR table_name LIKE 'CALC_JOB%' OR table_name LIKE '%CALC_JOB%'
          OR table_name LIKE 'CALCULATION%' OR table_name LIKE 'CTRL_CALC%'
          OR table_name LIKE '%ALLOC_NETWORK%') ORDER BY table_name""", 40)

q("PWEL_DAY_ALLOC row count + recent dates",
  """SELECT TO_CHAR(DAYTIME,'YYYY-MM-DD') d, COUNT(*) n FROM ECKERNEL_EC.PWEL_DAY_ALLOC
     GROUP BY TO_CHAR(DAYTIME,'YYYY-MM-DD') ORDER BY d DESC FETCH FIRST 12 ROWS ONLY""")

q("STRM_DAY_ALLOC row count + recent dates",
  """SELECT TO_CHAR(DAYTIME,'YYYY-MM-DD') d, COUNT(*) n FROM ECKERNEL_EC.STRM_DAY_ALLOC
     GROUP BY TO_CHAR(DAYTIME,'YYYY-MM-DD') ORDER BY d DESC FETCH FIRST 12 ROWS ONLY""")

# the allocation network objects (name -> for the nav dd)
q("OV_ALLOC_NETWORK (if exists) sample",
  """SELECT * FROM (SELECT OBJECT_CODE, NAME FROM ECKERNEL_EC.OV_ALLOC_NETWORK) WHERE ROWNUM<=15""")
q("alloc-network-ish views",
  """SELECT view_name FROM all_views WHERE owner='ECKERNEL_EC'
     AND (view_name LIKE 'OV_%ALLOC%NET%' OR view_name LIKE 'OV_%NETWORK%') ORDER BY view_name FETCH FIRST 20 ROWS ONLY""")
print("\nDONE")
