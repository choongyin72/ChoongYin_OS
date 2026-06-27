"""ECSR-35333 READ-ONLY: raw RAU monthly-event qty for C_PLU_LNG_1 vs C_PLU_LNG_2 (June 2026).
Shows Train1 has no ACT events; Train2 has ACT events with bad/NULL qty. Creds from ENV."""
import os, oracledb
con = oracledb.connect(user=os.environ["EC_DB_USER"], password=os.environ["EC_DB_PWD"], dsn=os.environ["EC_DB_DSN"])
cur = con.cursor()
for c in ('C_PLU_LNG_1', 'C_PLU_LNG_2'):
    print(f"\n=== {c} : RAU monthly events on 2026-06-01 (account_code, qty) ===")
    cur.execute("""SELECT account_code, qty
                   FROM dv_sctr_acc_mth_event
                   WHERE object_code = :c AND account_code LIKE 'RAU\\_%' ESCAPE '\\'
                     AND daytime = DATE '2026-06-01'
                   ORDER BY account_code""", [c])
    rows = cur.fetchall()
    if not rows:
        print("   (no RAU events)")
    for r in rows:
        print(f"   {r[0]:34} {r[1]}")
con.close()
