"""Generic read-only context I/O trace: CTX_PREFIX -> per matching context: I/O by class (+ business LABEL)
+ sample equations from the top calc. Reusable for any EC calc context family."""
import os, oracledb, re
def say(m): print(m, flush=True)
def rd(v):
    try: return v.read() if hasattr(v,'read') else v
    except: return v
def sml(s):
    if not s: return ''
    s=rd(s); s=re.sub(r'<[^>]+>',' ',str(s)); s=re.sub(r'\s+',' ',s); return s.strip()
PREFIX=os.environ.get('CTX_PREFIX','EC_REVN')
c=oracledb.connect(user=os.environ.get('EC_DB_USER','ECKERNEL_EC'),password=os.environ.get('EC_DB_PASS','energy'),dsn=os.environ.get('EC_DB_DSN','localhost:1521/ORCL'))
cur=c.cursor()
def label(cl):
    cur.execute("select property_value from class_property_cnfg where class_name=:c and property_code='LABEL' and rownum=1",{'c':cl})
    r=cur.fetchone(); return rd(r[0]) if r else ''
cur.execute("select distinct object_id from calc_var_read_mapping union select distinct object_id from calc_var_write_mapping")
ctx=[]
for (oid,) in cur.fetchall():
    cur.execute("select ecdp_objects.GetObjCode(:o) from dual",{'o':oid}); code=rd(cur.fetchone()[0])
    if code and code.startswith(PREFIX): ctx.append((code,oid))
ctx.sort()
say("Contexts for %s: %s" % (PREFIX, [x[0] for x in ctx]))
for code,oid in ctx:
    cur.execute("select count(*) from calc_var_read_mapping where object_id=:o",{'o':oid}); nr=cur.fetchone()[0]
    cur.execute("select count(*) from calc_var_write_mapping where object_id=:o",{'o':oid}); nw=cur.fetchone()[0]
    say("\n===== %s (reads=%d writes=%d) =====" % (code,nr,nw))
    say("  READS:")
    cur.execute("select cls_name, count(*) n, min(sql_syntax) s from calc_var_read_mapping where object_id=:o group by cls_name order by n desc fetch first 8 rows only",{'o':oid})
    for cl,n,s in cur.fetchall(): say("     %-26s x%-2d [%s] e.g.%s" % (cl,n,label(cl),sml(s)[:24]))
    say("  WRITES:")
    cur.execute("select cls_name, count(*) n, min(sql_syntax) s from calc_var_write_mapping where object_id=:o group by cls_name order by n desc fetch first 8 rows only",{'o':oid})
    for cl,n,s in cur.fetchall(): say("     %-26s x%-2d [%s] e.g.%s" % (cl,n,label(cl),sml(s)[:24]))
    cur.execute("""select c.object_code from calculation c join calc_equation e on e.object_id=c.object_id
       where c.calc_context_id=:o group by c.object_code order by count(*) desc fetch first 1 rows only""",{'o':oid})
    t=cur.fetchone()
    if t:
        cur.execute("select object_id from calculation where object_code=:c",{'c':t[0]}); toid=cur.fetchone()[0]
        cur.execute("select exec_order, equation from calc_equation where object_id=:o order by exec_order fetch first 4 rows only",{'o':toid})
        say("  EQ sample (%s): %s" % (t[0], ' || '.join('[%s]%s'%(e[0],sml(e[1])[:55]) for e in cur.fetchall())))
c.close()
