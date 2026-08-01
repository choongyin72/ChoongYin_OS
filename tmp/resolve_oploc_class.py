import oracledb
def a(s): return str(s).encode("ascii","replace").decode("ascii")
con = oracledb.connect(user="ECKERNEL_EC", password="energy", dsn="localhost:1521/ORCL")
cur = con.cursor()
cur.execute("""select property_code, property_value from class_property_cnfg
               where class_name='OPERATIONAL_LOCATIONS' and property_code in
               ('DB_OBJECT_NAME','DB_OBJECT_ATTRIBUTE','LABEL')""")
print(a(cur.fetchall()))
# try the base table directly if named per convention
for t in ("OPERATIONAL_LOCATIONS", "OPER_LOCATION", "OPLOC"):
    cur.execute("select count(*) from all_tables where table_name = :t", t=t)
    if cur.fetchone()[0]:
        cur.execute("select code, name from %s where code='TS5_DP_GP_GSP'" % t)
        print(a("%s -> %s" % (t, cur.fetchall())))
cur.close(); con.close()
