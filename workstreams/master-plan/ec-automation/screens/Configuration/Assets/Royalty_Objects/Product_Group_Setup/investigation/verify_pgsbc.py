import oracledb
cur = oracledb.connect(user="ECKERNEL_EC", password="energy", dsn="localhost:1521/ORCL").cursor()
print("=== PRODUCT_STRM_BAL_CAT columns ===")
for r in cur.execute("SELECT column_name,data_type FROM all_tab_columns WHERE owner='ECKERNEL_EC' AND table_name='PRODUCT_STRM_BAL_CAT' ORDER BY column_id").fetchall(): print("  ",r)
print("=== views over it (DV/RV/TV/V *PRODUCT_STRM_BAL*) ===")
for r in cur.execute("SELECT object_name,object_type FROM all_objects WHERE owner='ECKERNEL_EC' AND object_type IN('VIEW','TABLE') AND object_name LIKE '%PRODUCT_STRM_BAL%' ORDER BY object_name").fetchall(): print("  ",r)
print("=== sample rows (keyed by product group + product?) ===")
try:
    cur.execute("SELECT * FROM product_strm_bal_cat WHERE ROWNUM<=6")
    cols=[d[0] for d in cur.description]; print("  cols:",cols)
    for r in cur.fetchall(): print("  ",r)
    cur.execute("SELECT COUNT(*) FROM product_strm_bal_cat"); print("  total rows:",cur.fetchone()[0])
except Exception as e: print("  ERR",str(e)[:90])
