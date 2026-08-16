"""MHM/Notification SME recon (read-only). Discover the actual MHM tables in the sandbox — esp. the
Message Journal (the test oracle), Message Type, Distribution List, Message Distribution, Actor —
their schemas + row counts + sample rows, and whether N_R_D_VALIDATION_REVIEW exists + any journal
entries. Grounds Phase-1 SME knowledge in ground truth."""
import os, oracledb
c = oracledb.connect(user='ECKERNEL_EC', password=os.environ.get('EC_DB_PWD', 'energy'),
                     dsn=os.environ.get('EC_DB_DSN', 'localhost:1521/ORCL'), tcp_connect_timeout=15)
cur = c.cursor()


def show(t, sql, n=15):
    print(f"\n=== {t} ===")
    try:
        cur.execute(sql)
        cols = [d[0] for d in cur.description]
        print("  " + " | ".join(cols))
        for r in cur.fetchall()[:n]:
            print("  " + " | ".join("" if v is None else str(v)[:40] for v in r))
    except Exception as e:
        print("  ERR", str(e)[:150])


# 1. discover candidate MHM/message tables by name
show("candidate MHM/message tables (by name)",
     "SELECT table_name FROM all_tables WHERE owner='ECKERNEL_EC' AND table_name NOT LIKE '%JN' "
     "AND (table_name LIKE '%MESSAGE%' OR table_name LIKE '%MSG%' OR table_name LIKE 'MHM%' "
     "OR table_name LIKE '%JOURNAL%' OR table_name LIKE '%DISTRIB%' OR table_name LIKE '%ACTOR%' "
     "OR table_name LIKE '%NOTIF%' OR table_name LIKE '%TODO%') ORDER BY table_name", n=60)

cur.close(); c.close(); print("\nDONE")
