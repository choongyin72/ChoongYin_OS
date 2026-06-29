"""Transport contexts (EC_TRAN*): read/write I/O classes + attributes, grouped by class."""
import os, oracledb, re
def say(m): print(m, flush=True)
def rd(v):
    try: return v.read() if hasattr(v,'read') else v
    except: return v
def sml(s):
    if not s: return ''
    s=rd(s); s=re.sub(r'<[^>]+>',' ',str(s)); s=re.sub(r'\s+',' ',s); return s.strip()
c=oracledb.connect(user=os.environ.get('EC_DB_USER','ECKERNEL_EC'),password=os.environ.get('EC_DB_PASS','energy'),dsn=os.environ.get('EC_DB_DSN','localhost:1521/ORCL'))
cur=c.cursor()
# resolve EC_TRAN* context oids
cur.execute("select distinct object_id from calc_var_read_mapping union select distinct object_id from calc_var_write_mapping")
ctx=[]
for (oid,) in cur.fetchall():
    cur.execute("select ecdp_objects.GetObjCode(:o) from dual",{'o':oid}); code=rd(cur.fetchone()[0])
    if code and code.startswith('EC_TRAN'): ctx.append((code,oid))
ctx.sort()
say("Transport contexts: "+str([x[0] for x in ctx]))
for code,oid in ctx:
    cur.execute("select count(*) from calc_var_read_mapping where object_id=:o",{'o':oid}); nr=cur.fetchone()[0]
    cur.execute("select count(*) from calc_var_write_mapping where object_id=:o",{'o':oid}); nw=cur.fetchone()[0]
    say("\n===== %s  (reads=%d, writes=%d) =====" % (code, nr, nw))
    say("  READS by class:")
    cur.execute("select cls_name, count(*) n, min(sql_syntax) sample from calc_var_read_mapping where object_id=:o group by cls_name order by n desc",{'o':oid})
    for cl,n,s in cur.fetchall(): say("     %-26s x%-3d e.g. %s" % (cl, n, sml(s)[:32]))
    say("  WRITES by class:")
    cur.execute("select cls_name, count(*) n, min(sql_syntax) sample from calc_var_write_mapping where object_id=:o group by cls_name order by n desc",{'o':oid})
    for cl,n,s in cur.fetchall(): say("     %-26s x%-3d e.g. %s" % (cl, n, sml(s)[:32]))
c.close()
