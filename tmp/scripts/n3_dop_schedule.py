import os, oracledb
c=oracledb.connect(user='ECKERNEL_EC',password='energy',dsn=os.environ.get('EC_DB_DSN','localhost:1521/ORCL'),tcp_connect_timeout=15)
cur=c.cursor()
def show(t,sql):
    print(f"\n=== {t} ===")
    try:
        cur.execute(sql); cols=[d[0] for d in cur.description]; print(" | ".join(cols))
        rows=cur.fetchall()
        if not rows: print("  (no rows)")
        for r in rows[:15]: print("  "+" | ".join("" if v is None else str(v)[:46] for v in r))
    except Exception as e: print("  ERR", str(e)[:150])

# schedule(s) that include the null-class business action 'Daily Offshore Process'
show("Schedules linked to 'Daily Offshore Process' action (auto-firing source)",
    "SELECT s.NAME sched_name, s.ENABLED_IND, s.RUN_AS_USER, ai.EXEC_ORDER "
    "FROM SCHEDULE s, ACTION_INSTANCE ai, BUSINESS_ACTION ba "
    "WHERE ai.SCHEDULE_NO=s.SCHEDULE_NO AND ai.BUSINESS_ACTION_NO=ba.BUSINESS_ACTION_NO "
    "AND ba.NAME='Daily Offshore Process'")

# is there a QRTZ trigger for it (actively scheduled)?
show("QRTZ job details mentioning Offshore (active schedule)",
    "SELECT JOB_NAME, JOB_GROUP FROM QRTZ_JOB_DETAILS WHERE UPPER(JOB_NAME) LIKE '%OFFSHORE%' FETCH FIRST 5 ROWS ONLY")

# which business action do the DAILY DATA STATUS processes use? (my N3 path) - has a class?
show("DailyDataStatusProcess action (the N3 status-process path)",
    "SELECT NAME, ACTION_CLASS_NAME, JBPM_PROCESS_NAME FROM BUSINESS_ACTION WHERE NAME IN ('DailyDataStatusProcess','MonthlyDataStatusProcess')")
cur.close(); c.close(); print("\nDONE")
