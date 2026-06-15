"""MHM SME recon step 2 (read-only): drill into the oracle candidates + config + fired-notification
tables. For MHM_MSG / MESSAGE_OUT / JBPM_NOTIFICATION: key columns + row count + newest sample. For
MESSAGE_DEFINITION + DISTRIBUTION_SET: does N_R_D_VALIDATION_REVIEW exist + the Pluto DLs. Establishes
which table is the Message Journal (MHM.0007) test oracle + whether the live notification has fired."""
import os, oracledb
c = oracledb.connect(user='ECKERNEL_EC', password=os.environ.get('EC_DB_PWD', 'energy'),
                     dsn=os.environ.get('EC_DB_DSN', 'localhost:1521/ORCL'), tcp_connect_timeout=15)
cur = c.cursor()


def cols(t):
    cur.execute("SELECT column_name FROM all_tab_columns WHERE table_name=:t AND owner='ECKERNEL_EC' ORDER BY column_id", t=t)
    return [r[0] for r in cur.fetchall()]


def show(t, sql, n=10):
    print(f"\n=== {t} ===")
    try:
        cur.execute(sql)
        d = [x[0] for x in cur.description]
        print("  " + " | ".join(d))
        for r in cur.fetchall()[:n]:
            print("  " + " | ".join("" if v is None else str(v)[:34] for v in r))
    except Exception as e:
        print("  ERR", str(e)[:150])


for t in ("MHM_MSG", "MESSAGE_OUT", "JBPM_NOTIFICATION", "MESSAGE_DEFINITION", "DISTRIBUTION_SET"):
    print(f"\n##### {t}: {len(cols(t))} cols -> {cols(t)[:18]}")
    try:
        cur.execute(f"SELECT COUNT(*) FROM {t}"); print(f"   row count: {cur.fetchone()[0]}")
    except Exception as e:
        print("   count ERR", str(e)[:80])

# Does the live notification message type exist? search message-definition-ish tables
show("MESSAGE_DEFINITION rows mentioning VALIDATION / N_R_D",
     "SELECT * FROM MESSAGE_DEFINITION WHERE UPPER(CODE) LIKE '%VALID%' OR UPPER(CODE) LIKE 'N_R_D%' "
     "OR UPPER(NAME) LIKE '%VALIDATION%' FETCH FIRST 10 ROWS ONLY")

# MHM_MSG newest rows (the journal) — key audit columns
mc = cols("MHM_MSG")
keyish = [x for x in mc if x in ('MSG_ID', 'MESSAGE_TYPE', 'MSG_TYPE', 'STATUS', 'SUBJECT', 'CREATED_DATE', 'SENT_DATE', 'TO_ADDRESS', 'RECIPIENT', 'MESSAGE_DEFINITION_CODE')]
if mc:
    sel = ", ".join(keyish) if keyish else "*"
    show(f"MHM_MSG newest rows ({keyish or 'all cols'})",
         f"SELECT {sel} FROM MHM_MSG ORDER BY {('CREATED_DATE' if 'CREATED_DATE' in mc else mc[0])} DESC FETCH FIRST 8 ROWS ONLY")

cur.close(); c.close(); print("\nDONE")
