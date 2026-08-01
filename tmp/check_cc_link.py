import oracledb
def a(s): return str(s).encode("ascii","replace").decode("ascii")
con = oracledb.connect(user="ECKERNEL_EC", password="energy", dsn="localhost:1521/ORCL")
cur = con.cursor()
cur.execute("""select contract_code, operational_locations_code, count(*) c
               from ov_contract_capacity group by contract_code, operational_locations_code
               order by c desc fetch first 8 rows only""")
for r in cur.fetchall(): print(a(str(r)))
cur.close(); con.close()
