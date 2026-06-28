import oracledb
cur=oracledb.connect(user="ECKERNEL_EC",password="energy",dsn="localhost:1521/ORCL").cursor()
print("products already in ALL_GENERAL:")
for r in cur.execute("SELECT product_code FROM dv_product_group_setup WHERE object_code='ALL_GENERAL' ORDER BY product_code").fetchall(): print("  ",r[0])
print("\ncandidate test products (in OV_PRODUCT, NOT in ALL_GENERAL):")
for r in cur.execute("""SELECT code FROM ov_product WHERE code NOT IN
   (SELECT product_code FROM dv_product_group_setup WHERE object_code='ALL_GENERAL') AND ROWNUM<=8 ORDER BY code""").fetchall(): print("  ",r[0])
print("\nsentinel baseline (must be 0 everywhere):")
for s,v in (("DV_PRODUCT_GROUP_SETUP","comments"),("DV_PRODUCT_GROUP_COST","comments"),("PRODUCT_STRM_BAL_CAT","comments")):
    n=cur.execute(f"SELECT COUNT(*) FROM {s} WHERE {v} LIKE 'AUTOTEST_PGS%'").fetchone()[0]; print(f"  {s}: {n}")
