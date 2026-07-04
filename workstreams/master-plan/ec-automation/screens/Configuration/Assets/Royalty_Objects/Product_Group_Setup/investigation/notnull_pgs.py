import oracledb
cur=oracledb.connect(user="ECKERNEL_EC",password="energy",dsn="localhost:1521/ORCL").cursor()
for t in ("PRODUCT_GROUP_SETUP","PRODUCT_GROUP_COST","PRODUCT_STRM_BAL_CAT"):
    print(f"=== {t} NOT NULL columns ===")
    for r in cur.execute("SELECT column_name FROM all_tab_columns WHERE owner='ECKERNEL_EC' AND table_name=:t AND nullable='N' ORDER BY column_id",[t]).fetchall():
        print("  ",r[0])
