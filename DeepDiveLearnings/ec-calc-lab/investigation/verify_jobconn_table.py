"""Read-only: check the REAL job-connection table tv_ALLOC_NETWORK_JOB_CONN (per user's query)."""
import os, oracledb
dsn=os.environ.get('EC_DB_DSN','localhost:1521/ORCL')
usr=os.environ.get('EC_DB_USER','ECKERNEL_EC'); pwd=os.environ.get('EC_DB_PASS','energy')
con=oracledb.connect(user=usr,password=pwd,dsn=dsn); cur=con.cursor()
q="""select ecdp_objects.GetObjCode(t.alloc_network_id) net,
            ecdp_objects.GetObjCode(t.job_id) job,
            to_char(nvl(t.LAST_UPDATED_date,t.CREATED_DATE),'YYYY-MM-DD HH24:MI') ts
     from tv_ALLOC_NETWORK_JOB_CONN t
     order by nvl(t.LAST_UPDATED_date,t.CREATED_DATE) desc"""
cur.execute(q); rows=cur.fetchall()
print("total rows in tv_ALLOC_NETWORK_JOB_CONN:", len(rows))
print("--- 15 most recent (network | job | last_change) ---")
for r in rows[:15]: print("  %-22s %-22s %s" % (r[0], r[1], r[2]))
auto=[r for r in rows if r[1] and 'AUTOTEST_CALC_TEST' in str(r[1])]
print("--- rows where job = AUTOTEST_CALC_TEST:", len(auto))
for r in auto: print("  %-22s %-22s %s" % (r[0], r[1], r[2]))
p1=[r for r in rows if r[0] and 'P1_DAY_ALLOC' in str(r[0])]
print("--- rows on network P1_DAY_ALLOC:", len(p1))
for r in p1[:15]: print("  %-22s %-22s %s" % (r[0], r[1], r[2]))
cur.close(); con.close()
