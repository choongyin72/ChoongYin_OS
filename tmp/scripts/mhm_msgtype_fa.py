import os, oracledb
con=oracledb.connect(user=os.environ.get("EC_DB_USER","ECKERNEL_EC"),
 password=os.environ.get("EC_DB_PASS","energy"),
 dsn=os.environ.get("EC_DB_DSN","localhost:1521/ORCL"),tcp_connect_timeout=15)
cur=con.cursor()
def show(t,sql,b=None):
    print(f"\n=== {t} ===")
    try:
        cur.execute(sql,b or {});cols=[d[0] for d in cur.description]
        print(" | ".join(cols))
        for r in cur.fetchall()[:30]:
            print(" | ".join("" if v is None else str(v)[:40] for v in r))
    except Exception as e: print("ERR:",str(e)[:160])
# message definition table cols
cur.execute("SELECT column_name FROM all_tab_columns WHERE table_name='MESSAGE_DEFINITION' ORDER BY column_id")
print("MESSAGE_DEFINITION cols:", ", ".join(r[0] for r in cur.fetchall()))
show("MHM13 / freetext message types + their functional area", """
 SELECT OBJECT_CODE, NAME, FUNCTIONAL_AREA_ID, DIRECTION, FORMAT_CODE, DISTRIBUTION_SET_CODE
 FROM MESSAGE_DEFINITION
 WHERE UPPER(OBJECT_CODE) LIKE '%FREE%' OR UPPER(OBJECT_CODE) LIKE '%MHM13%' OR UPPER(NAME) LIKE '%FREE%'""")
# resolve FA id -> name for the FRMW free text FA
show("functional area name for the freetext FA", """
 SELECT FUNCTIONAL_AREA_ID, NAME FROM FUNCTIONAL_AREA
 WHERE FUNCTIONAL_AREA_ID='96D694768B3C0300E053020011AC7D49'""")
con.close();print("DONE")
