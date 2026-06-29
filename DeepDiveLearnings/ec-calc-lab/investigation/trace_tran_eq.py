"""Sample equations from calcs in each EC_TRAN* context."""
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
# EC_TRAN* context oids
cur.execute("select distinct object_id from calc_var_read_mapping union select distinct object_id from calc_var_write_mapping")
ctx=[]
for (oid,) in cur.fetchall():
    cur.execute("select ecdp_objects.GetObjCode(:o) from dual",{'o':oid}); code=rd(cur.fetchone()[0])
    if code and code.startswith('EC_TRAN'): ctx.append((code,oid))
ctx.sort()
for code,oid in ctx:
    say("\n===== %s : calcs with equations =====" % code)
    cur.execute("""select c.object_code, c.calc_type, count(e.object_id) ne
       from calculation c left join calc_equation e on e.object_id=c.object_id
       where c.calc_context_id=:o group by c.object_code, c.calc_type
       having count(e.object_id)>0 order by ne desc fetch first 4 rows only""",{'o':oid})
    calcs=cur.fetchall()
    if not calcs: say("   (no direct-equation calcs in this context)"); continue
    for cc,ct,ne in calcs: say("   %-30s %-9s eqs=%d" % (cc,ct,ne))
    # show sample equations of the top one
    top=calcs[0][0]
    cur.execute("select object_id from calculation where object_code=:c",{'c':top}); toid=cur.fetchone()[0]
    cur.execute("select exec_order, equation from calc_equation where object_id=:o order by exec_order fetch first 5 rows only",{'o':toid})
    say("   -- sample equations of %s --" % top)
    for eo,eq in cur.fetchall(): say("      [%s] %s" % (eo, sml(eq)[:120]))
c.close()
