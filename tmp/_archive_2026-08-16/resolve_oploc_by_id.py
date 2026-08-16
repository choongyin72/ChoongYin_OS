import oracledb
def a(s): return str(s).encode("ascii","replace").decode("ascii")
con = oracledb.connect(user="ECKERNEL_EC", password="energy", dsn="localhost:1521/ORCL")
cur = con.cursor()
cur.execute("""select operational_locations_id from ov_contract_capacity
               where operational_locations_code='TS5_DP_GP_GSP' and rownum=1""")
oid = cur.fetchone()
print(a("OPERATIONAL_LOCATIONS_ID: %s" % (oid,)))
if oid:
    oid = oid[0]
    for t in ("OV_DELIVERY_POINT", "OV_RECEIPT_POINT", "OV_TRAN_ZONE", "OV_LOCATION"):
        try:
            cur.execute("select count(*) from all_views where view_name=:v", v=t)
            if cur.fetchone()[0]:
                cur.execute("select code, name from %s where object_id = :o" % t, o=oid)
                r = cur.fetchall()
                if r: print(a("%s -> %s" % (t, r)))
        except Exception as e:
            print(a("%s ERR %s" % (t, repr(e)[:60])))
cur.close(); con.close()
