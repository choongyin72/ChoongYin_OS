import os, oracledb
c = oracledb.connect(user="ECKERNEL_EC", password="energy", dsn="localhost:1521/ORCL")
cur = c.cursor()
for v in ("OV_PROD_SUB_UNIT",):
    try:
        cur.execute("select code, name, start_date from %s where code like 'AUTOTEST_PSU%%'" % v)
        rows = cur.fetchall()
        print(v, "->", len(rows), "AUTOTEST rows:", rows[:5])
    except Exception as e:
        print(v, "ERR", repr(e)[:120])
c.close()
