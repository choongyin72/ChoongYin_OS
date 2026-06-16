import os, oracledb
con=oracledb.connect(user=os.environ.get("EC_DB_USER","ECKERNEL_EC"),
 password=os.environ.get("EC_DB_PASS","energy"),
 dsn=os.environ.get("EC_DB_DSN","localhost:1521/ORCL"),tcp_connect_timeout=15)
cur=con.cursor()
cur.execute("SELECT column_name FROM all_tab_columns WHERE table_name='FUNCTIONAL_AREA' ORDER BY column_id")
print("FUNCTIONAL_AREA cols:", ", ".join(r[0] for r in cur.fetchall()))
for sql in ["SELECT * FROM FUNCTIONAL_AREA WHERE OBJECT_ID='96D694768B3C0300E053020011AC7D49'",
            "SELECT * FROM FUNCTIONAL_AREA WHERE FUNC_AREA_ID='96D694768B3C0300E053020011AC7D49'"]:
    try:
        cur.execute(sql); cols=[d[0] for d in cur.description]
        rows=cur.fetchall()
        if rows:
            print("\n",sql[:50]); 
            for r in rows: print({cols[i]:str(v)[:30] for i,v in enumerate(r) if v is not None})
            break
    except Exception as e: print("x",str(e)[:80])
con.close();print("DONE")
