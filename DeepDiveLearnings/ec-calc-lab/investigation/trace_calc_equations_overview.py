import os, oracledb, re
def say(m): print(m, flush=True)
def rd(v):
    try: return v.read() if hasattr(v,'read') else v
    except: return v
def strip_ml(s):
    if not s: return ''
    s=rd(s); s=re.sub(r'<[^>]+>',' ',str(s)); s=re.sub(r'\s+',' ',s); return s.strip()
c=oracledb.connect(user=os.environ.get('EC_DB_USER','ECKERNEL_EC'),password=os.environ.get('EC_DB_PASS','energy'),dsn=os.environ.get('EC_DB_DSN','localhost:1521/ORCL'))
cur=c.cursor()
for tbl,lbl in [('calc_equation','equations'),('calc_var_read_mapping','read maps'),('calc_var_write_mapping','write maps'),('calc_variable_local','local vars')]:
    cur.execute("select count(*), count(distinct object_id) from "+tbl); n,d=cur.fetchone()
    say("%s: %d rows across %d object_ids" % (lbl, n, d))
say("\n=== top calcs by equation count ===")
cur.execute("select object_id, count(*) n from calc_equation group by object_id order by n desc fetch first 6 rows only")
tops=cur.fetchall()
for oid,n in tops:
    cur.execute("select object_code, calc_type from calculation where object_id=:o",{'o':oid}); cc=cur.fetchone()
    say("  %-22s type=%-9s eqs=%d" % ((cc[0] if cc else oid[:14]+'..'), (cc[1] if cc else '?'), n))
say("\n=== sample equations of the top calc ===")
oid=tops[0][0]
cur.execute("select object_code from calculation where object_id=:o",{'o':oid}); say("  calc: "+str((cur.fetchone() or ['?'])[0]))
cur.execute("select exec_order, description, condition, equation from calc_equation where object_id=:o order by exec_order",{'o':oid})
for e in cur.fetchall()[:8]:
    cond=strip_ml(e[2]); eq=strip_ml(e[3])
    say("   [%s] %s%s=> %s" % (e[0], (rd(e[1]) or '')[:30], (' COND('+cond[:40]+') ' if cond else ' '), eq[:130]))
c.close()
