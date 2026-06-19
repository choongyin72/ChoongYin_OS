"""DB recon for the Alarms event log: DV_ALARMS + FCTY_DAY_ALARM columns + sample rows, so the IUD oracle
can identify a test alarm by a Reason marker (or count-delta). READ-ONLY."""
import os, oracledb
cur = oracledb.connect(user="ECKERNEL_EC", password=os.environ.get("EC_DB_PWD", "energy"),
                       dsn=os.environ.get("EC_DB_DSN", "localhost:1521/ORCL"), tcp_connect_timeout=15).cursor()


def cols(t):
    cur.execute("""SELECT column_name, data_type FROM all_tab_columns WHERE owner='ECKERNEL_EC'
                   AND table_name=:t ORDER BY column_id""", [t])
    return cur.fetchall()


for t in ("DV_ALARMS", "FCTY_DAY_ALARM"):
    c = cols(t)
    print(f"=== {t} columns ({len(c)}) ===")
    for name, dt in c:
        print(f"   {name:28s} {dt}")
    try:
        cur.execute(f"SELECT COUNT(*) FROM ECKERNEL_EC.{t}"); print("   row count:", cur.fetchone()[0])
    except Exception as e:
        print("   count err:", str(e)[:60])
    print()

print("=== DV_ALARMS sample rows (any) ===")
try:
    cur.execute("SELECT * FROM ECKERNEL_EC.DV_ALARMS FETCH FIRST 3 ROWS ONLY")
    names = [d[0] for d in cur.description]
    for r in cur.fetchall():
        print("  ", dict(zip(names, [str(x)[:22] for x in r])))
except Exception as e:
    print("  err:", str(e)[:80])

print("\n=== any AUTOTEST residue in DV_ALARMS (reason-like cols)? ===")
rc = [n for n, d in cols("DV_ALARMS") if d in ("VARCHAR2", "CHAR", "NVARCHAR2")]
print("  text columns:", rc)
cur.close()
print("\nDONE")
