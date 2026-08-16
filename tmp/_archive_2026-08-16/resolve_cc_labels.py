import oracledb
def a(s): return str(s).encode("ascii","replace").decode("ascii")
con = oracledb.connect(user="ECKERNEL_EC", password="energy", dsn="localhost:1521/ORCL")
cur = con.cursor()
def q(label, sql, **kw):
    try:
        cur.execute(sql, kw); print(a("%-28s %s" % (label, cur.fetchall())))
    except Exception as e:
        print(a("%-28s ERR %s" % (label, repr(e)[:90])))
q("Contract TS5_FTR_SHB_01 ->", "select code, name, contract_area_code from ov_contract where code='TS5_FTR_SHB_01'")
q("Location TS5_DP_GP_GSP ->", """select column_name from all_tab_columns where table_name like 'OV_OPERATIONAL%'
                                   or table_name like 'OV_LOCATION%' order by table_name""")
cur.close(); con.close()
