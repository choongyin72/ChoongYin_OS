import os, oracledb
dsn = os.environ.get("EC_DB_DSN", "localhost:1521/ORCL")
user = os.environ.get("EC_DB_USER", "ECKERNEL_EC")
pw = os.environ.get("EC_DB_PASS", "energy")
conn = oracledb.connect(user=user, password=pw, dsn=dsn, tcp_connect_timeout=15)
cur = conn.cursor()
cur.execute("SELECT COUNT(*) FROM FINANCIAL_ITEM_TEMPLATE WHERE TEMPLATE_CODE = 'AUTOTEST_FIT_001'")
print("AUTOTEST_FIT_001 present (should be 0, physically deleted):", cur.fetchone()[0])
cur.close(); conn.close()
