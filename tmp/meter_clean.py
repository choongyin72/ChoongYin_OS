import oracledb
c=oracledb.connect(user="ECKERNEL_EC",password="energy",dsn="localhost:1521/ORCL");cur=c.cursor()
# find meter-ish views + check for AUTOTEST_MTR leftovers
cur.execute("select view_name from all_views where owner='ECKERNEL_EC' and view_name like 'OV_%METER%' order by view_name")
views=[r[0] for r in cur.fetchall()]
print("meter views:",views)
for v in views:
    try:
        cur.execute(f"select code from {v} where code like 'AUTOTEST_MTR%'")
        rows=[r[0] for r in cur.fetchall()]
        if rows:
            print(f"  {v}: LEFTOVER {rows}")
            cur.execute(f"update {v} set object_end_date=object_start_date where code like 'AUTOTEST_MTR%' and object_end_date is null")
            print(f"    cleaned rowcount={cur.rowcount}"); c.commit()
        else:
            print(f"  {v}: 0 AUTOTEST_MTR (clean)")
    except Exception as e: print(f"  {v}: {str(e)[:60]}")
c.close()
