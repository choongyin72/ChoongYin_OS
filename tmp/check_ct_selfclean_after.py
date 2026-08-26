"""Independent DB self-clean check (fresh oracledb connection) after the live 5/5 run."""
import oracledb

conn = oracledb.connect(user="ECKERNEL_EC", password="energy", dsn="localhost:1521/ORCL")
cur = conn.cursor()
cur.execute("SELECT CODE, NAME FROM OV_CHEM_TANK WHERE CODE LIKE 'AUTOTEST%'")
rows = cur.fetchall()
print("AUTOTEST% residual rows in OV_CHEM_TANK:", rows)
cur.close()
conn.close()
