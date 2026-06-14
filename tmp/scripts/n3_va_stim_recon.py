"""Confirm STIM_DAY_VALUE (target of the daily Stream Item V->A pair) is testable: keys
(OBJECT_ID/DAYTIME/RECORD_STATUS present?), RECORD_STATUS distribution, and dates with Provisional
('P') rows = candidate test scope for the daily P->V->A chain. Read-only."""
import os, oracledb
c = oracledb.connect(user='ECKERNEL_EC', password='energy', dsn=os.environ.get('EC_DB_DSN', 'localhost:1521/ORCL'), tcp_connect_timeout=15)
cur = c.cursor()


def show(t, sql, n=20):
    print(f"\n=== {t} ===")
    try:
        cur.execute(sql)
        cols = [d[0] for d in cur.description]
        print("  " + " | ".join(cols))
        for r in cur.fetchall()[:n]:
            print("  " + " | ".join("" if v is None else str(v)[:38] for v in r))
    except Exception as e:
        print("  ERR", str(e)[:160])


show("STIM_DAY_VALUE key-ish columns",
     "SELECT column_name, data_type FROM all_tab_columns WHERE table_name='STIM_DAY_VALUE' "
     "AND (column_name IN ('OBJECT_ID','DAYTIME','RECORD_STATUS') OR column_name LIKE '%VALUE%' "
     "OR column_name LIKE '%ITEM%') ORDER BY column_id")

show("RECORD_STATUS distribution",
     "SELECT RECORD_STATUS, COUNT(*) FROM STIM_DAY_VALUE GROUP BY RECORD_STATUS ORDER BY 1")

show("dates with the most Provisional (P) rows (candidate test scope)",
     "SELECT TO_CHAR(TRUNC(DAYTIME),'YYYY-MM-DD') day, COUNT(*) n, COUNT(DISTINCT OBJECT_ID) objs "
     "FROM STIM_DAY_VALUE WHERE RECORD_STATUS='P' GROUP BY TRUNC(DAYTIME) ORDER BY n DESC FETCH FIRST 6 ROWS ONLY")

cur.close(); c.close(); print("\nDONE")
