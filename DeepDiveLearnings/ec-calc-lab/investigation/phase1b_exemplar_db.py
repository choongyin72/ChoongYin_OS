"""Find a known-good EXEMPLAR variable that already has a READ MAPPING to PWEL_DAY_DATA, and
dump its definition (name, data type, precision, DIM1..5 object types) + the mapping detail
(cls_name, sql_syntax, date handling). Read-only - this is the pattern I will clone for Var B."""
import os, oracledb
def rd(v):
    try: return v.read() if hasattr(v,'read') else v
    except: return v
c=oracledb.connect(user=os.environ.get('EC_DB_USER','ECKERNEL_EC'),password=os.environ.get('EC_DB_PASS','energy'),dsn=os.environ.get('EC_DB_DSN','localhost:1521/ORCL'))
cur=c.cursor()
print("=== variables with a READ mapping to PWEL_DAY_DATA (name, datatype, precision, dims) ===")
cur.execute("""select v.name, v.calc_var_data_type, v.default_precision,
                      v.dim1_object_type_code, v.dim2_object_type_code, v.dim3_object_type_code,
                      m.sql_syntax, m.calc_date_handling
               from calc_variable v
               join calc_var_read_mapping m on m.calc_var_signature=v.calc_var_signature
               where m.cls_name='PWEL_DAY_DATA' and rownum<=8 order by v.name""")
for r in cur.fetchall():
    print("   name=%-20s type=%-7s prec=%s dims=[%s,%s,%s] sql=%-16s dateh=%s" % (
        rd(r[0]), rd(r[1]), rd(r[2]), rd(r[3]), rd(r[4]), rd(r[5]), str(rd(r[6]))[:16], rd(r[7])))
print("\n=== the production-well object type used as dim1 (so Var B uses the right dimension) ===")
cur.execute("""select distinct v.dim1_object_type_code, ot.calc_obj_type_category
               from calc_variable v join calc_var_read_mapping m on m.calc_var_signature=v.calc_var_signature
               left join calc_object_type ot on ot.object_type_code=v.dim1_object_type_code
               where m.cls_name='PWEL_DAY_DATA' and v.dim1_object_type_code is not null""")
for r in cur.fetchall(): print("   dim1 object type:", rd(r[0]), " category:", rd(r[1]))
print("\n=== available attributes on PWEL_DAY_DATA class (candidates for SQL_SYNTAX) ===")
cur.execute("""select distinct sql_syntax from calc_var_read_mapping where cls_name='PWEL_DAY_DATA' and sql_syntax is not null and rownum<=12 order by 1""")
for r in cur.fetchall(): print("   ", str(rd(r[0]))[:40])
c.close()
print("\nDONE exemplar_db")
