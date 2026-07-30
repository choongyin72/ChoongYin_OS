# READ-ONLY: can we reach Oracle audit trail to find the client host for the 2026-07-21 14:23 change?
import oracledb
DSN="db.ec14151.woodside-pluto.tieto-og.cloud:1521/ec14151"
c=oracledb.connect(user="ECKERNEL_EC",password="energy",dsn=DSN); cur=c.cursor()

def try_q(label, sql):
    try:
        cur.execute(sql); rows=cur.fetchall()
        print(f"[{label}] OK - {len(rows)} row(s)")
        for r in rows[:15]: print("     ", " | ".join(str(x) for x in r))
    except Exception as e:
        print(f"[{label}] NO ACCESS / n/a: {str(e)[:90]}")

# 1) is unified auditing accessible + any rows in the window on CTRL_CHECK%?
try_q("UNIFIED_AUDIT_TRAIL",
  """select dbusername, os_username, userhost, terminal, client_program_name,
            to_char(event_timestamp,'YYYY-MM-DD HH24:MI:SS'), object_name, action_name
     from unified_audit_trail
     where event_timestamp between timestamp '2026-07-21 14:00:00' and timestamp '2026-07-21 14:45:00'
       and (object_name like 'CTRL_CHECK%' or sql_text like '%CTRL_CHECK_RULES%')
     order by event_timestamp fetch first 15 rows only""")

# 2) legacy DBA_AUDIT_TRAIL
try_q("DBA_AUDIT_TRAIL",
  """select username, os_username, userhost, terminal,
            to_char(timestamp,'YYYY-MM-DD HH24:MI:SS'), obj_name, action_name
     from dba_audit_trail
     where timestamp between date '2026-07-21' and date '2026-07-22' and obj_name like 'CTRL_CHECK%'
     order by timestamp fetch first 15 rows only""")

# 3) is ANY auditing even on? (can I see the param / policies)
try_q("V$OPTION unified", "select value from v$option where parameter='Unified Auditing'")
c.close()
