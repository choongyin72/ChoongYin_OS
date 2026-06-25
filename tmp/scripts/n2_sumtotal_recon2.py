"""N2 sum-to-total feasibility v2 (read-only). Get the REAL columns of the alloc result tables, the
allocation networks + which have calc jobs, and whether any date has CO-PRESENT member (PWEL_DAY_ALLOC)
+ stream-total (STRM_DAY_ALLOC) data for the same network (the prerequisite for a sum-to-total check).
Also: the richest PWEL_DAY_ALLOC dates (candidate run outputs)."""
import os, oracledb
c = oracledb.connect(user='ECKERNEL_EC', password='energy', dsn=os.environ.get('EC_DB_DSN', 'localhost:1521/ORCL'), tcp_connect_timeout=15)
cur = c.cursor()


def show(t, sql, n=25):
    print(f"\n=== {t} ===")
    try:
        cur.execute(sql)
        cols = [d[0] for d in cur.description]
        print("  " + " | ".join(cols))
        for r in cur.fetchall()[:n]:
            print("  " + " | ".join("" if v is None else str(v)[:34] for v in r))
    except Exception as e:
        print("  ERR", str(e)[:160])


show("PWEL_DAY_ALLOC ALLOC_* numeric columns",
     "SELECT column_name FROM all_tab_columns WHERE table_name='PWEL_DAY_ALLOC' "
     r"AND column_name LIKE 'ALLOC\_%' ESCAPE '\' ORDER BY column_id")
show("STRM_DAY_ALLOC numeric columns (the 'total' side)",
     "SELECT column_name FROM all_tab_columns WHERE table_name='STRM_DAY_ALLOC' "
     "AND data_type='NUMBER' ORDER BY column_id")
show("richest PWEL_DAY_ALLOC dates (member results)",
     "SELECT TO_CHAR(TRUNC(DAYTIME),'YYYY-MM-DD') d, COUNT(*) n, COUNT(DISTINCT OBJECT_ID) wells "
     "FROM PWEL_DAY_ALLOC GROUP BY TRUNC(DAYTIME) ORDER BY n DESC FETCH FIRST 6 ROWS ONLY")
show("dates with BOTH PWEL_DAY_ALLOC and STRM_DAY_ALLOC (co-present member+total)",
     "SELECT TO_CHAR(TRUNC(p.DAYTIME),'YYYY-MM-DD') d, COUNT(DISTINCT p.OBJECT_ID) wells, "
     "(SELECT COUNT(*) FROM STRM_DAY_ALLOC s WHERE TRUNC(s.DAYTIME)=TRUNC(p.DAYTIME)) strm_rows "
     "FROM PWEL_DAY_ALLOC p GROUP BY TRUNC(p.DAYTIME) "
     "HAVING (SELECT COUNT(*) FROM STRM_DAY_ALLOC s WHERE TRUNC(s.DAYTIME)=TRUNC(p.DAYTIME))>0 ORDER BY d")
show("allocation networks (name + id)",
     "SELECT OBJECT_ID, NAME FROM OV_ALLOC_NETWORK ORDER BY NAME FETCH FIRST 20 ROWS ONLY")
show("networks that HAVE a calc job wired (runnable)",
     "SELECT DISTINCT n.NAME FROM ALLOC_NETWORK_JOB_CONN jc JOIN OV_ALLOC_NETWORK n "
     "ON n.OBJECT_ID=jc.ALLOC_NETWORK_ID ORDER BY n.NAME FETCH FIRST 20 ROWS ONLY")

cur.close(); c.close(); print("\nDONE")
