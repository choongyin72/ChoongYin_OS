import os, oracledb
def say(m): print(m, flush=True)
def rd(v):
    try: return v.read() if hasattr(v,'read') else v
    except: return v
c=oracledb.connect(user=os.environ.get('EC_DB_USER','ECKERNEL_EC'),password=os.environ.get('EC_DB_PASS','energy'),dsn=os.environ.get('EC_DB_DSN','localhost:1521/ORCL'))
cur=c.cursor()
EC_PROD='96D6E0ED1D5A0571E053020011ACE2E9'

say("=== BASELINE counts (for self-clean diff later) ===")
for t in ['CALC_OBJECT_TYPE','CALC_VARIABLE','CALC_VAR_READ_MAPPING','CALC_VAR_WRITE_MAPPING']:
    cur.execute("select count(*) from "+t); say("   %-26s %d" % (t, cur.fetchone()[0]))

say("\n=== any AUTOTEST_ residue already present? (should be 0) ===")
cur.execute("select count(*) from calc_object_type where upper(object_type_code) like 'AUTOTEST%'"); say("   obj_type AUTOTEST: %d" % cur.fetchone()[0])
cur.execute("select count(*) from calc_variable where upper(name) like 'AUTOTEST%'"); say("   variable AUTOTEST: %d" % cur.fetchone()[0])

say("\n=== CALC_OBJECT_TYPE columns (what the New form will need) ===")
cur.execute("select column_name, nullable, data_type from all_tab_columns where owner='ECKERNEL_EC' and table_name='CALC_OBJECT_TYPE' order by column_id")
for r in cur.fetchall(): say("   %-28s null=%s %s" % (r[0], rd(r[1]), rd(r[2])))

say("\n=== CALC_VARIABLE key columns ===")
cur.execute("select column_name, nullable from all_tab_columns where owner='ECKERNEL_EC' and table_name='CALC_VARIABLE' order by column_id")
for r in cur.fetchall(): say("   %-28s null=%s" % (r[0], rd(r[1])))

say("\n=== CALC_VAR_READ_MAPPING columns ===")
cur.execute("select column_name from all_tab_columns where owner='ECKERNEL_EC' and table_name='CALC_VAR_READ_MAPPING' order by column_id")
say("   "+", ".join(x[0] for x in cur.fetchall()))

say("\n=== sample EC_PROD read mappings to a _DATA class (copy this pattern) ===")
cur.execute("""select cls_name, count(*) from calc_var_read_mapping
               where cls_name like '%\\_DATA' escape '\\' group by cls_name order by 2 desc""")
for r in cur.fetchall()[:10]: say("   %-26s used_by=%d vars" % (rd(r[0]), r[1]))

say("\n=== one concrete read mapping example (cls + sql_syntax) ===")
cur.execute("""select cls_name, sql_syntax from calc_var_read_mapping
               where cls_name like 'PWEL_DAY_DATA' and rownum<=3""")
for r in cur.fetchall(): say("   %s  ::  %s" % (rd(r[0]), str(rd(r[1]))[:80]))
c.close()
say("\nDONE phase0_db_recon")
