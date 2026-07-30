import oracledb
DSN="db.ec14151.woodside-pluto.tieto-og.cloud:1521/ec14151"
c=oracledb.connect(user="ECKERNEL_EC",password="energy",dsn=DSN); cur=c.cursor()
cur.execute("""select column_name from all_tab_columns where owner='ECKERNEL_EC'
   and table_name='CTRL_CHECK_RULES' order by column_id""")
allcols=[r[0] for r in cur.fetchall()]
print("CTRL_CHECK_RULES columns:", allcols)
want=[x for x in ("CHECK_ID","CHECK_NAME","DATA_CLASS_NAME","CLASS","SELECT_CLAUSE","WHERE_FORMULA","WHERE_CLAUSE","SEVERITY_LEVEL","CHECK_MESSAGE","MESSAGE") if x in allcols]
cur.execute(f"select {', '.join(want)} from ctrl_check_rules where check_id in (1147,1148,1149,1150) order by check_id")
print("\n=== 1147-1150 ===")
for r in cur.fetchall():
    for k,v in zip(want,r): print(f"   {k}: {v}")
    print("   ---")
for tbl in ("flyway_schema_history","schema_version"):
    try:
        cur.execute(f"select version, script, installed_by, to_char(installed_on,'YYYY-MM-DD HH24:MI'), success from {tbl} where installed_on between date '2026-07-20' and date '2026-07-23' order by installed_on")
        rows=cur.fetchall(); print(f"\n=== {tbl} 07-20..23: {len(rows)} ===")
        for r in rows: print("   "," | ".join(str(x) for x in r))
    except Exception as e: print(f"\n{tbl}: {str(e)[:60]}")
c.close()
