import oracledb
c=oracledb.connect(user="ECKERNEL_EC",password="energy",dsn="localhost:1521/ORCL");cur=c.cursor()
for v in ("OV_FORECAST_GROUP","OV_FORECAST"):
    try:
        cur.execute(f"select count(*) from {v}"); print(v,"exists, rows=",cur.fetchone()[0])
    except Exception as e: print(v,"->",str(e)[:60])
# columns of the real one
for v in ("OV_FORECAST_GROUP","OV_FORECAST"):
    try:
        cur.execute(f"select column_name from all_tab_columns where owner='ECKERNEL_EC' and table_name='{v}' and column_name in ('CODE','NAME')")
        print(v,"CODE/NAME cols:",[r[0] for r in cur.fetchall()])
    except Exception: pass
c.close()
