"""Fresh-connection check: is AUTOTEST_WH free in OV_WELL_HOOKUP before wiring it in as the
fixed test code for the Well Hookup Area-pattern conversion?"""
import oracledb

conn = oracledb.connect(user="ECKERNEL_EC", password="energy", dsn="localhost:1521/ORCL", tcp_connect_timeout=15)
cur = conn.cursor()
cur.execute("SELECT COUNT(*) FROM OV_WELL_HOOKUP WHERE UPPER(CODE) LIKE 'AUTOTEST%'")
print("AUTOTEST% rows in OV_WELL_HOOKUP:", cur.fetchone()[0])
cur.execute("SELECT COUNT(*) FROM OV_WELL_HOOKUP WHERE UPPER(CODE) = 'AUTOTEST_WH'")
print("AUTOTEST_WH exact rows:", cur.fetchone()[0])
cur.close()
conn.close()
