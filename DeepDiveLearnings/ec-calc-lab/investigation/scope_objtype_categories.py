import os, oracledb
def say(m): print(m, flush=True)
def rd(v):
    try: return v.read() if hasattr(v,'read') else v
    except: return v
c=oracledb.connect(user=os.environ.get('EC_DB_USER','ECKERNEL_EC'),password=os.environ.get('EC_DB_PASS','energy'),dsn=os.environ.get('EC_DB_DSN','localhost:1521/ORCL'))
cur=c.cursor()
say("=== DATABASE object types (category=DB) sample ===")
cur.execute("select object_type_code, data_type from calc_object_type where calc_obj_type_category='DB' and rownum<=14 order by object_type_code")
for r in cur.fetchall(): say("   %-22s %s" % (r[0], rd(r[1])))
say("\n=== PREDEFINED object types sample ===")
cur.execute("select object_type_code from calc_object_type where calc_obj_type_category='PREDEFINED' and rownum<=10 order by object_type_code")
for r in cur.fetchall(): say("   "+str(r[0]))
say("\n=== global/context attributes: any rows? DEFINED_BY values ===")
cur.execute("select count(*) from calc_context_attribute"); say("   CALC_CONTEXT_ATTRIBUTE total rows: %d" % cur.fetchone()[0])
cur.execute("select defined_by, count(*) from calc_context_attribute group by defined_by order by 2 desc")
for r in cur.fetchall(): say("   defined_by=%-12s %d" % (rd(r[0]), r[1]))
cur.execute("select distinct attribute_name from calc_context_attribute where rownum<=18 order by attribute_name")
say("   sample attrs: "+", ".join(rd(x[0]) for x in cur.fetchall()))
say("\n=== CALC_VARIABLE_META: access_mode distribution (read vs write) ===")
cur.execute("select access_mode, count(*) from calc_variable_meta group by access_mode order by 2 desc")
for r in cur.fetchall(): say("   access_mode=%-8s %d" % (rd(r[0]), r[1]))
c.close()
