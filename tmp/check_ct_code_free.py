"""Confirm a fixed AUTOTEST_CT code is free in OV_CHEM_TANK before wiring it into the
Area-pattern conversion (fresh oracledb connection, read-only)."""
import oracledb

conn = oracledb.connect(user="ECKERNEL_EC", password="energy",
                         dsn="localhost:1521/ORCL")
cur = conn.cursor()
cur.execute("SELECT CODE, NAME FROM OV_CHEM_TANK WHERE CODE LIKE 'AUTOTEST%'")
rows = cur.fetchall()
print("AUTOTEST% rows in OV_CHEM_TANK:", rows)
cur.execute("SELECT COUNT(*) FROM OV_CHEM_TANK WHERE CODE = 'AUTOTEST_CT'")
print("AUTOTEST_CT exact count:", cur.fetchone()[0])
cur.close()
conn.close()
