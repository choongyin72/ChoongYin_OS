"""Confirm root cause: BUSINESS_ACTION.ACTION_CLASS_NAME is NULL for the jBPM-backed status-process
actions (the value the scheduler reads as the null 'class'). Read-only."""
import os, oracledb
c=oracledb.connect(user='ECKERNEL_EC',password='energy',dsn=os.environ.get('EC_DB_DSN','localhost:1521/ORCL'),tcp_connect_timeout=15)
cur=c.cursor()
def show(t,sql,binds=None):
    print(f"\n=== {t} ===")
    try:
        cur.execute(sql,binds or {}); cols=[d[0] for d in cur.description]; print(" | ".join(cols))
        rows=cur.fetchall()
        if not rows: print("  (no rows)")
        for r in rows[:25]: print("  "+" | ".join("" if v is None else str(v)[:42] for v in r))
    except Exception as e: print("  ERR", str(e)[:160])

show("BUSINESS_ACTION: class-name NULL vs set (the smoking gun)",
    "SELECT CASE WHEN ACTION_CLASS_NAME IS NULL THEN 'NULL_CLASS' ELSE 'has_class' END k, "
    "CASE WHEN JBPM_PROCESS_NAME IS NULL THEN 'no_jbpm' ELSE 'jbpm_backed' END j, COUNT(*) n "
    "FROM BUSINESS_ACTION GROUP BY CASE WHEN ACTION_CLASS_NAME IS NULL THEN 'NULL_CLASS' ELSE 'has_class' END, "
    "CASE WHEN JBPM_PROCESS_NAME IS NULL THEN 'no_jbpm' ELSE 'jbpm_backed' END ORDER BY 1,2")

show("Business actions with NULL ACTION_CLASS_NAME (name + jbpm fields)",
    "SELECT NAME, ACTION_CLASS_NAME, JBPM_PROCESS_NAME, JBPM_DEPLOYMENT_ID, JBPM_PROCESS_VERSION "
    "FROM BUSINESS_ACTION WHERE ACTION_CLASS_NAME IS NULL ORDER BY NAME")

show("The 'Daily Offshore Process' action specifically",
    "SELECT NAME, ACTION_CLASS_NAME, JBPM_PROCESS_NAME, JBPM_DEPLOYMENT_ID, JBPM_PROCESS_VERSION "
    "FROM BUSINESS_ACTION WHERE UPPER(NAME) LIKE '%OFFSHORE%' OR UPPER(NAME) LIKE '%PROCESS%' OR UPPER(NAME) LIKE '%STATUS%' ORDER BY NAME")

show("For comparison: a few actions WITH a class set",
    "SELECT NAME, ACTION_CLASS_NAME FROM BUSINESS_ACTION WHERE ACTION_CLASS_NAME IS NOT NULL "
    "FETCH FIRST 8 ROWS ONLY")

# Are jBPM processes actually deployed? (deployment id populated?)
show("jbpm_deployment_id populated? (deployment registered?)",
    "SELECT CASE WHEN JBPM_DEPLOYMENT_ID IS NULL THEN 'no_deployment_id' ELSE 'has_deployment_id' END k, COUNT(*) n "
    "FROM BUSINESS_ACTION WHERE JBPM_PROCESS_NAME IS NOT NULL GROUP BY CASE WHEN JBPM_DEPLOYMENT_ID IS NULL THEN 'no_deployment_id' ELSE 'has_deployment_id' END")

cur.close(); c.close(); print("\nDONE")
