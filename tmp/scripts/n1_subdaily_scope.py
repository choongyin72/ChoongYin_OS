"""Resolve the nav scope (well name + PU/Area/FacilityClass1/WellHookup cascade) for the clean
sub-daily test well AEBC774296CE11E6E053020011ACFD on 2024-10-01, plus the 2nd well that day, and
the SUMMER_TIME values present. Feeds the live grid-crack (recon3). Read-only."""
import os, oracledb
c = oracledb.connect(user='ECKERNEL_EC', password='energy',
                     dsn=os.environ.get('EC_DB_DSN', 'localhost:1521/ORCL'), tcp_connect_timeout=15)
cur = c.cursor()


def show(t, sql):
    print(f"\n=== {t} ===")
    try:
        cur.execute(sql)
        cols = [d[0] for d in cur.description]
        print("  " + " | ".join(cols))
        for r in cur.fetchall()[:10]:
            print("  " + " | ".join("" if v is None else str(v)[:40] for v in r))
    except Exception as e:
        print("  ERR", str(e)[:160])


show("wells with P sub-daily rows on 2024-10-01 + their names",
     "SELECT s.OBJECT_ID, wv.NAME, COUNT(*) rows_, MIN(TO_CHAR(s.DAYTIME,'HH24:MI')) first_t, "
     "MAX(TO_CHAR(s.DAYTIME,'HH24:MI')) last_t, COUNT(DISTINCT s.SUMMER_TIME) st_vals "
     "FROM PWEL_SUB_DAY_STATUS s LEFT JOIN WELL_VERSION wv ON wv.OBJECT_ID=s.OBJECT_ID "
     "WHERE s.RECORD_STATUS='P' AND TRUNC(s.DAYTIME)=TO_DATE('2024-10-01','YYYY-MM-DD') "
     "GROUP BY s.OBJECT_ID, wv.NAME")

show("SUMMER_TIME distinct values present (DST flag domain)",
     "SELECT DISTINCT SUMMER_TIME FROM PWEL_SUB_DAY_STATUS WHERE TRUNC(DAYTIME)=TO_DATE('2024-10-01','YYYY-MM-DD')")

# one well, one hour: confirm a single row + its ON_STREAM_HRS / AVG_WH_PRESS values (cell targets)
show("sample measured values for well AEBC...ACFD @ 2024-10-01 00:00:00",
     "SELECT TO_CHAR(DAYTIME,'YYYY-MM-DD HH24:MI:SS') dt, SUMMER_TIME, ON_STREAM_HRS, AVG_WH_PRESS, AVG_WH_TEMP "
     "FROM PWEL_SUB_DAY_STATUS WHERE OBJECT_ID='AEBC774296CE11E6E053020011ACFD' "
     "AND TRUNC(DAYTIME)=TO_DATE('2024-10-01','YYYY-MM-DD') ORDER BY DAYTIME FETCH FIRST 5 ROWS ONLY")

# the well's asset cascade: which PU/Area/Facility does this well hang under?
show("well -> hookup -> facility/area/PU cascade (for the navigator)",
     "SELECT wv.NAME well, wh.NAME hookup, fc.NAME facility, ar.NAME area, pu.NAME pu "
     "FROM WELL_VERSION wv "
     "LEFT JOIN WELL_HOOKUP_VERSION wh ON wh.WELL_ID=wv.OBJECT_ID "
     "LEFT JOIN OV_FACILITY_CLASS_1 fc ON fc.OBJECT_ID=wh.OP_FCTY_1_ID "
     "LEFT JOIN OV_AREA ar ON ar.OBJECT_ID=wh.OP_AREA_ID "
     "LEFT JOIN OV_PRODUCTIONUNIT pu ON pu.OBJECT_ID=wh.OP_PROD_UNIT_ID "
     "WHERE wv.OBJECT_ID='AEBC774296CE11E6E053020011ACFD' FETCH FIRST 5 ROWS ONLY")

cur.close(); c.close(); print("\nDONE")
