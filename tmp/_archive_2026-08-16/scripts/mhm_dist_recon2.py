"""READ-ONLY: resolve each distribution's actual recipient email addresses + the message-type->distribution
wiring, to find any distribution that is ALREADY safe (no real deliverable domain) for the N-notify live
send. NO writes. Same connection contract as DbVerify."""
import os
import oracledb

con = oracledb.connect(
    user=os.environ.get("EC_DB_USER", "ECKERNEL_EC"),
    password=os.environ.get("EC_DB_PASS", "energy"),
    dsn=os.environ.get("EC_DB_DSN", "localhost:1521/ORCL"),
    tcp_connect_timeout=15,
)
cur = con.cursor()


def show(title, sql, binds=None):
    print(f"\n=== {title} ===")
    try:
        cur.execute(sql, binds or {})
        cols = [d[0] for d in cur.description]
        print(" | ".join(cols))
        for r in cur.fetchall()[:60]:
            print(" | ".join("" if v is None else str(v)[:40] for v in r))
    except Exception as e:
        print("ERR:", str(e)[:200])


def cols(title, table):
    print(f"\n=== {title} ({table}) cols ===")
    cur.execute(
        "SELECT column_name, data_type FROM all_tab_columns WHERE table_name=:t ORDER BY column_id",
        {"t": table},
    )
    print(", ".join(f"{c}:{d}" for c, d in cur.fetchall()))


cols("DISTRIBUTION_SET_CONTACT", "DISTRIBUTION_SET_CONTACT")
cols("RECIPIENT", "RECIPIENT")
cols("MESSAGE_DISTRIBUTION", "MESSAGE_DISTRIBUTION")

show("DISTRIBUTION_SET_CONTACT rows", "SELECT * FROM DISTRIBUTION_SET_CONTACT WHERE ROWNUM<=60")
show("RECIPIENT rows", "SELECT * FROM RECIPIENT WHERE ROWNUM<=60")
show(
    "MESSAGE_DISTRIBUTION rows (msg-type -> distribution wiring)",
    "SELECT * FROM MESSAGE_DISTRIBUTION WHERE ROWNUM<=60",
)

con.close()
print("\nDONE")
