"""READ-ONLY: nail the message-type -> distribution wiring for the FRMW free text message, to know
exactly which config row controls the screen's recipients (for a precise, reversible safe-send option)."""
import os, oracledb
con=oracledb.connect(user=os.environ.get("EC_DB_USER","ECKERNEL_EC"),
 password=os.environ.get("EC_DB_PASS","energy"),
 dsn=os.environ.get("EC_DB_DSN","localhost:1521/ORCL"),tcp_connect_timeout=15)
cur=con.cursor()
def show(t,sql):
    print(f"\n=== {t} ===")
    cur.execute(sql);cols=[d[0] for d in cur.description]
    print(" | ".join(cols))
    for r in cur.fetchall()[:30]:
        print(" | ".join("" if v is None else str(v)[:34] for v in r))
# all MESSAGE_DISTRIBUTION rows with their key cols
show("MESSAGE_DISTRIBUTION (key cols)", """
 SELECT MESSAGE_DISTRIBUTION_NO, OBJECT_ID, DISTRIBUTION_SET_CODE, FORMAT_CODE, MSG_DISTR_CODE, RECORD_STATUS
 FROM MESSAGE_DISTRIBUTION ORDER BY MESSAGE_DISTRIBUTION_NO""")
# the freetext message def object id(s)
show("MESSAGE_DEFINITION freetext/FRMW", """
 SELECT OBJECT_ID, OBJECT_CODE FROM MESSAGE_DEFINITION
 WHERE UPPER(OBJECT_CODE) LIKE '%FREE%' OR UPPER(OBJECT_CODE) LIKE '%FRMW%' OR UPPER(OBJECT_CODE) LIKE '%MHM13%'""")
# does a separate msg-distr -> distribution-set join table exist? search tables
show("tables linking msg distr <-> distribution set", """
 SELECT table_name FROM all_tables WHERE owner='ECKERNEL_EC'
  AND (table_name LIKE 'MSG_DISTR%' OR table_name LIKE 'MESSAGE_DISTR%' OR table_name LIKE '%DISTR_SET%')
 ORDER BY 1""")
con.close();print("\nDONE")
