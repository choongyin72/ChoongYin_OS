"""Find data-rich N1 targets: scan *_DAY_STATUS + STRM_DAY_STREAM tables for row counts, RECORD_STATUS
distribution, and a seed date with abundant editable (P) rows. Picks the next N1 screen reliably.
Read-only."""
import os, oracledb
c=oracledb.connect(user='ECKERNEL_EC',password='energy',dsn=os.environ.get('EC_DB_DSN','localhost:1521/ORCL'),tcp_connect_timeout=15)
cur=c.cursor()

cur.execute("SELECT table_name FROM all_tables WHERE owner='ECKERNEL_EC' AND "
            "(table_name LIKE '%\\_DAY\\_STATUS' ESCAPE '\\' OR table_name='STRM_DAY_STREAM') "
            "AND table_name NOT LIKE '%\\_JN' ESCAPE '\\' ORDER BY table_name")
tables=[r[0] for r in cur.fetchall()]
print("day-status tables (%d):" % len(tables))
for t in tables:
    try:
        cur.execute(f"SELECT COUNT(*) FROM {t}")
        total=cur.fetchone()[0]
        if total==0:
            print(f"  {t:32s} EMPTY"); continue
        # P count + a top data day
        cur.execute(f"SELECT COUNT(*) FROM {t} WHERE RECORD_STATUS='P'")
        pc=cur.fetchone()[0]
        cur.execute(f"SELECT TO_CHAR(TRUNC(DAYTIME),'YYYY-MM-DD') d, COUNT(*) n FROM {t} "
                    f"WHERE RECORD_STATUS='P' GROUP BY TRUNC(DAYTIME) ORDER BY n DESC FETCH FIRST 1 ROWS ONLY")
        row=cur.fetchone()
        topday = f"{row[0]}({row[1]})" if row else "-"
        print(f"  {t:32s} total={total:<7} P={pc:<7} topP_day={topday}")
    except Exception as e:
        print(f"  {t:32s} ERR {str(e)[:50]}")
cur.close(); c.close(); print("DONE")
