import os, oracledb
def say(m): print(m, flush=True)
def rd(v):
    try: return v.read() if hasattr(v,'read') else v
    except: return v
c=oracledb.connect(user=os.environ.get('EC_DB_USER','ECKERNEL_EC'),password=os.environ.get('EC_DB_PASS','energy'),dsn=os.environ.get('EC_DB_DSN','localhost:1521/ORCL'))
cur=c.cursor()
EC_PROD='96D6E0ED1D5A0571E053020011ACE2E9'
say("=== object types by category (DATABASE vs SIMPLE) ===")
cur.execute("select calc_obj_type_category, count(*) from calc_object_type group by calc_obj_type_category order by 2 desc")
for r in cur.fetchall(): say("   %-14s %d" % (rd(r[0]), r[1]))
say("\n=== sample DATABASE object types (code, data_type) ===")
cur.execute("select object_type_code, data_type from calc_object_type where calc_obj_type_category='DATABASE' and rownum<=8 order by object_type_code")
for r in cur.fetchall(): say("   %-22s %s" % (r[0], rd(r[1])))
say("=== sample SIMPLE object types ===")
cur.execute("select object_type_code, data_type from calc_object_type where calc_obj_type_category='SIMPLE' and rownum<=8 order by object_type_code")
for r in cur.fetchall(): say("   %-22s %s" % (r[0], rd(r[1])))
say("\n=== CALC_VARIABLE total + sample (name, datatype, objtype, dims) ===")
cur.execute("select count(*) from calc_variable"); say("   total variable defs: %d" % cur.fetchone()[0])
cur.execute("select name, calc_var_data_type, calc_object_type_code, dim1_object_type_code, dim2_object_type_code from calc_variable where name is not null and rownum<=10 order by name")
for r in cur.fetchall(): say("   %-24s type=%-7s of=%-10s dims=[%s,%s]" % (rd(r[0]), rd(r[1]), rd(r[2]), rd(r[3]), rd(r[4])))
say("\n=== EC_PROD global attributes (CALC_CONTEXT_ATTRIBUTE) ===")
cur.execute("select attribute_name, defined_by from calc_context_attribute where object_id=:o order by attribute_name",{'o':EC_PROD})
for r in cur.fetchall(): say("   %-26s defined_by=%s" % (rd(r[0]), rd(r[1])))
say("\n=== how variables link to a context? CALC_VARIABLE_META cols ===")
cur.execute("select column_name from all_tab_columns where owner='ECKERNEL_EC' and table_name='CALC_VARIABLE_META' order by column_id")
say("   "+", ".join(x[0] for x in cur.fetchall()))
c.close()
