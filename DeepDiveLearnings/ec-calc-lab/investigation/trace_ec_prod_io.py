import os, oracledb, re
def say(m): print(m, flush=True)
def rd(v):
    try: return v.read() if hasattr(v,'read') else v
    except: return v
def sml(s):
    if not s: return ''
    s=rd(s); s=re.sub(r'<[^>]+>',' ',str(s)); s=re.sub(r'\s+',' ',s); return s.strip()
EC_PROD='96D6E0ED1D5A0571E053020011ACE2E9'
c=oracledb.connect(user=os.environ.get('EC_DB_USER','ECKERNEL_EC'),password=os.environ.get('EC_DB_PASS','energy'),dsn=os.environ.get('EC_DB_DSN','localhost:1521/ORCL'))
cur=c.cursor()
cur.execute("select count(*) from calc_var_read_mapping where object_id=:o",{'o':EC_PROD})
cur.execute("select count(*) from calc_var_read_mapping where object_id=:o",{'o':EC_PROD}); say("EC_PROD read maps: "+str(cur.fetchone()[0]))
cur.execute("select count(*) from calc_var_write_mapping where object_id=:o",{'o':EC_PROD}); say("EC_PROD write maps: "+str(cur.fetchone()[0]))
say("\n=== EC_PROD READ: classes it reads from (cls_name + sample sql) ===")
cur.execute("select cls_name, sql_syntax from calc_var_read_mapping where object_id=:o fetch first 12 rows only",{'o':EC_PROD})
for cls,sq in cur.fetchall(): say("   %-26s %s" % (cls, sml(sq)[:55]))
say("\n=== EC_PROD WRITE: classes it writes to (cls_name + sample sql) ===")
cur.execute("select cls_name, sql_syntax from calc_var_write_mapping where object_id=:o fetch first 12 rows only",{'o':EC_PROD})
for cls,sq in cur.fetchall(): say("   %-26s %s" % (cls, sml(sq)[:55]))
c.close()
