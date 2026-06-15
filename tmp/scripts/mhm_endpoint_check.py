import os, oracledb
con = oracledb.connect(user=os.environ.get("EC_DB_USER","ECKERNEL_EC"),
    password=os.environ.get("EC_DB_PASS","energy"),
    dsn=os.environ.get("EC_DB_DSN","localhost:1521/ORCL"), tcp_connect_timeout=15)
cur=con.cursor()
cur.execute("SELECT column_name FROM all_tab_columns WHERE table_name='ENDPOINT_CONFIG' ORDER BY column_id")
print("ENDPOINT_CONFIG cols:", ", ".join(r[0] for r in cur.fetchall()))
cur.execute("SELECT * FROM ENDPOINT_CONFIG")
cols=[d[0] for d in cur.description]
print("\nrows:")
for r in cur.fetchall():
    nn=[f"{cols[i]}={str(v)[:60]}" for i,v in enumerate(r) if v is not None]
    print("  "+" ; ".join(nn)); print("  -")
con.close(); print("DONE")
