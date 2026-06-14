"""Get equipment nav-scope NAMES: list OV_EQPM *NAME* hierarchy cols, then dump the PU/Area/Facility
names for offshore equipment that has data on 2024-02-06 (to drive the nav cascade). Read-only."""
import os, oracledb
c=oracledb.connect(user='ECKERNEL_EC',password='energy',dsn=os.environ.get('EC_DB_DSN','localhost:1521/ORCL'),tcp_connect_timeout=15);cur=c.cursor()
cur.execute("SELECT column_name FROM all_tab_columns WHERE table_name='OV_EQPM' AND column_name LIKE '%NAME%' ORDER BY column_id")
namecols=[r[0] for r in cur.fetchall()]
print("OV_EQPM *NAME* cols:", namecols)
# pick hierarchy-ish name cols
hier=[c2 for c2 in namecols if any(k in c2 for k in ('FCTY','FACIL','AREA','UNIT','CLASS'))]
print("hierarchy name cols:", hier)
sel=", ".join(['NAME']+hier) if hier else "NAME"
cur.execute(f"SELECT {sel} FROM OV_EQPM WHERE OBJECT_ID IN "
            f"(SELECT OBJECT_ID FROM EQPM_DAY_STATUS WHERE TRUNC(DAYTIME)=TO_DATE('2024-02-06','YYYY-MM-DD')) "
            f"FETCH FIRST 10 ROWS ONLY")
cols=[d[0] for d in cur.description]; print("\n"+" | ".join(cols))
for r in cur.fetchall(): print("  "+" | ".join("" if v is None else str(v)[:34] for v in r))
cur.close();c.close();print("DONE")
