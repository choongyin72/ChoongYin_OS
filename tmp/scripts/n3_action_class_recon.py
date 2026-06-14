"""Pinpoint the ec-bpm setup fault: the scheduler fires the job but BusinessActionAdvancedConfig
.createAndInitBusinessAction -> getValidatedClass(name=null) throws. Find the business-action /
event-action config tables and which actions have a NULL/blank implementation CLASS. Read-only."""
import os
import oracledb
c = oracledb.connect(user="ECKERNEL_EC", password="energy",
                     dsn=os.environ.get("EC_DB_DSN", "localhost:1521/ORCL"), tcp_connect_timeout=15)
cur = c.cursor()

# 1. Find config tables that carry a CLASS / CLASS_NAME / IMPL column (business actions / events)
cur.execute(
    "SELECT table_name, column_name FROM all_tab_columns WHERE owner='ECKERNEL_EC' "
    "AND (column_name LIKE '%CLASS%' OR column_name LIKE '%IMPL%') "
    "AND (table_name LIKE '%ACTION%' OR table_name LIKE '%EVENT%' OR table_name LIKE '%BUSINESS%' "
    "OR table_name LIKE '%CONTROLLER%' OR table_name LIKE '%JOB%' OR table_name LIKE 'CTRL%') "
    "ORDER BY table_name, column_name"
)
rows = cur.fetchall()
print("config tables with CLASS/IMPL columns:")
for t, col in rows:
    print(f"  {t}.{col}")

# 2. For each such table+col, count NULL/blank class entries (the smoking gun)
print("\nNULL/blank class scan:")
seen = set()
for t, col in rows:
    if (t, col) in seen:
        continue
    seen.add((t, col))
    try:
        cur.execute(f"SELECT COUNT(*) total, SUM(CASE WHEN {col} IS NULL OR TRIM({col})='' THEN 1 ELSE 0 END) blank FROM {t}")
        tot, blank = cur.fetchone()
        flag = "  <<< has NULL/blank" if blank else ""
        print(f"  {t}.{col}: total={tot} blank={blank}{flag}")
    except Exception as e:
        print(f"  {t}.{col}: ERR {str(e)[:60]}")

cur.close(); c.close()
print("\nDONE")
