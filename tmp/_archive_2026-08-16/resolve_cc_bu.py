import oracledb
def a(s): return str(s).encode("ascii","replace").decode("ascii")
con = oracledb.connect(user="ECKERNEL_EC", password="energy", dsn="localhost:1521/ORCL")
cur = con.cursor()
cur.execute("select code, name, business_unit_id, business_unit_code from ov_contract_area where code='TS5_CA'")
print(a(cur.fetchall()))
cur.execute("select code, name from ov_business_unit where code=(select business_unit_code from ov_contract_area where code='TS5_CA')")
print(a(cur.fetchall()))
cur.close(); con.close()
