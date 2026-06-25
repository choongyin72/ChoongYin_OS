"""READ-ONLY: determine whether the sandbox actually TRANSMITS messages or only journals them.
Check MHM_MSG status distribution + the SMTP/email endpoint config. NO writes."""
import os, oracledb
con = oracledb.connect(user=os.environ.get("EC_DB_USER","ECKERNEL_EC"),
    password=os.environ.get("EC_DB_PASS","energy"),
    dsn=os.environ.get("EC_DB_DSN","localhost:1521/ORCL"), tcp_connect_timeout=15)
cur=con.cursor()
def show(t,sql):
    print(f"\n=== {t} ===")
    try:
        cur.execute(sql); cols=[d[0] for d in cur.description]
        print(" | ".join(cols))
        for r in cur.fetchall()[:40]:
            print(" | ".join("" if v is None else str(v)[:48] for v in r))
    except Exception as e: print("ERR:",str(e)[:160])

show("MHM_MSG status x direction", """
  SELECT DIRECTION, STATUS, COUNT(*) FROM MHM_MSG GROUP BY DIRECTION, STATUS ORDER BY 1,2""")
show("MHM_MSG recent outbound (status/sent date)", """
  SELECT MSG_TYPE, DIRECTION, STATUS, SENDER, RECIPIENT, CREATED_DATE, SENT_DATE
  FROM (SELECT m.*, ROW_NUMBER() OVER (ORDER BY CREATED_DATE DESC) rn FROM MHM_MSG m WHERE DIRECTION='O')
  WHERE rn<=15""")
# endpoint / smtp config tables
show("endpoint-ish tables", """
  SELECT table_name FROM all_tables WHERE owner='ECKERNEL_EC'
   AND (table_name LIKE '%ENDPOINT%' OR table_name LIKE '%SMTP%' OR table_name LIKE '%EMAIL%'
        OR table_name LIKE '%MAIL%' OR table_name LIKE '%COMM_CHANNEL%') ORDER BY 1""")
con.close(); print("\nDONE")
