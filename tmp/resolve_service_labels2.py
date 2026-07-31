import oracledb
def a(s): return str(s).encode("ascii","replace").decode("ascii")
con = oracledb.connect(user="ECKERNEL_EC", password="energy", dsn="localhost:1521/ORCL")
cur = con.cursor()
def q(label, sql, **kw):
    try:
        cur.execute(sql, kw); print(a("%-34s %s" % (label, cur.fetchall())))
    except Exception as e:
        print(a("%-34s ERR %s" % (label, repr(e)[:70])))
q("BU code TS3_BU1 ->", "select code, name from ov_business_unit where code='TS3_BU1'")
q("transport system TS3_SYSTEM ->", "select code, name from ov_transport_system where code='TS3_SYSTEM'")
q("service templates (any view) ->",
  """select table_name from all_tab_columns where column_name='OBJECT_CODE'
     and table_name like '%SERVICE_TEMPL%' and rownum<=5""")
q("template code from a real row ->",
  "select distinct template_code from ov_service where template_code is not null and rownum<=6")
cur.close(); con.close()
