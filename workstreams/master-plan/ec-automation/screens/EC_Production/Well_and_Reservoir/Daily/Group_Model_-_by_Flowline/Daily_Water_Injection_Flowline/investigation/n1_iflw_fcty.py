import os, oracledb
con=oracledb.connect(user=os.environ.get("EC_DB_USER","ECKERNEL_EC"),password=os.environ.get("EC_DB_PASS","energy"),dsn=os.environ.get("EC_DB_DSN","localhost:1521/ORCL"),tcp_connect_timeout=15)
cur=con.cursor()
# the 3 data-bearing P1 flowlines + their facility code/id
cur.execute("""SELECT CODE, NAME, OP_FCTY_1_CODE, OP_FCTY_1_ID FROM OV_FLOWLINE WHERE OBJECT_ID IN ('96D7FD4F173A0217E053020011AC1940','96D7FD4F175E0217E053020011AC1940','96D7FD4F17700217E053020011AC1940')""")
print("data flowlines:", cur.fetchall())
# resolve facility display name for P1_FCTY_1
for t in ('OV_FACILITY','OV_OP_FACILITY','OV_FCTY'):
    try:
        cur.execute(f"SELECT CODE, NAME FROM {t} WHERE CODE='P1_FCTY_1' OR NAME LIKE '%P1%Facility%1%' FETCH FIRST 5 ROWS ONLY")
        r=cur.fetchall()
        if r: print(f"{t}:", r); break
    except Exception as e: pass
con.close()
