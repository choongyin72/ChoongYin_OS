"""Recon to extend N3 into the V->A (approval) transition (complete the P->V->A lifecycle).
Enumerate STATUS_PROCESS with decoded record-status levels (CTRL_RECORD_STATUS_LEVEL), flag the
processes that target Approved ('A') and whether they're DAY or MTH grain + reverse. Then assess
data: the sandbox day-status family is all 'P' (I cleaned V), so a V->A test must CHAIN P->V then
V->A. Confirm a daily forward (P->V) + a daily approve (V->A) pair exists, and that both appear
runnable. Read-only."""
import os, oracledb
c = oracledb.connect(user='ECKERNEL_EC', password='energy', dsn=os.environ.get('EC_DB_DSN', 'localhost:1521/ORCL'), tcp_connect_timeout=15)
cur = c.cursor()


def show(t, sql, binds=None):
    print(f"\n=== {t} ===")
    try:
        cur.execute(sql, binds or {})
        cols = [d[0] for d in cur.description]
        print("  " + " | ".join(cols))
        for r in cur.fetchall()[:40]:
            print("  " + " | ".join("" if v is None else str(v)[:34] for v in r))
    except Exception as e:
        print("  ERR", str(e)[:160])


show("CTRL_RECORD_STATUS_LEVEL (decode the level codes)",
     "SELECT * FROM CTRL_RECORD_STATUS_LEVEL ORDER BY 1")

show("ALL STATUS_PROCESS rows (PROCESS_ID, text, FROM->TO level, interval, reverse, parent)",
     "SELECT PROCESS_ID, PROCESS_TEXT, FROM_RS_LEVEL, TO_RS_LEVEL, PROCESS_INTERVAL, REVERSE_FLAG, "
     "PARENT_PROCESS_ID, PROD_FCTY_ID FROM STATUS_PROCESS ORDER BY PROCESS_INTERVAL, PROCESS_ID")

# specifically: processes that target 'A' (approval) and their grain
show("processes targeting APPROVED ('A')",
     "SELECT PROCESS_ID, PROCESS_TEXT, FROM_RS_LEVEL, TO_RS_LEVEL, PROCESS_INTERVAL, REVERSE_FLAG "
     "FROM STATUS_PROCESS WHERE TO_RS_LEVEL='A' ORDER BY PROCESS_INTERVAL")

# processes that lift to V (forward) on DAY grain — the P->V step to chain before V->A
show("DAY processes targeting VERIFIED ('V') — the forward step to stage V rows",
     "SELECT PROCESS_ID, PROCESS_TEXT, FROM_RS_LEVEL, TO_RS_LEVEL, REVERSE_FLAG "
     "FROM STATUS_PROCESS WHERE TO_RS_LEVEL='V' AND PROCESS_INTERVAL='DAY' ORDER BY PROCESS_ID")

cur.close(); c.close(); print("\nDONE")
