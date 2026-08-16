import os, oracledb
cur=oracledb.connect(user="ECKERNEL_EC",password=os.environ.get("EC_DB_PWD","energy"),dsn=os.environ.get("EC_DB_DSN","localhost:1521/ORCL"),tcp_connect_timeout=15).cursor()
comp=cur.execute("SELECT DISTINCT OBJECT_ID FROM ECKERNEL_EC.DV_WELL_COMP_ANALYSIS WHERE OBJECT_CODE='P1_W260_GP_COMP_GAS'").fetchall()
wv=cur.execute("SELECT OBJECT_ID FROM ECKERNEL_EC.WELL_VERSION WHERE NAME='P1 W260 GP Comp Gas' FETCH FIRST 2 ROWS ONLY").fetchall()
print("comp OBJECT_ID:",comp)
print("WELL_VERSION OBJECT_ID by NAME:",wv)
print("MATCH:", bool(comp and wv and comp[0][0]==wv[0][0]))
