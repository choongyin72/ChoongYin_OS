"""ECSR-35333 read-only: trace WHY DEF_QTY_DER < 0 (negative auto deferments) for June 2026. Creds from env."""
import os, oracledb
c = oracledb.connect(user=os.environ['QDB_USER'], password=os.environ['QDB_PW'], dsn=os.environ['QDB_DSN'], tcp_connect_timeout=25)
cur = c.cursor()

print("=== columns of TV_ZWP_DEF_DAY_DETAIL ===")
cur.execute("""select column_name, data_type from all_tab_columns
               where table_name='TV_ZWP_DEF_DAY_DETAIL' order by column_id""")
cols = cur.fetchall()
print(", ".join(cn for cn,_ in cols))

print("\n=== sample NEGATIVE auto-deferment rows June 2026 (LNG Train2 / SCA) - key cols ===")
try:
    cur.execute("""select DAYTIME, ASSET_ID, LOSS_CATEGORY, VARIATION,
                          round(DEF_QTY,2) DEF_QTY, round(DEF_QTY_DER,2) DEF_QTY_DER, DEFERMENT_STATUS
                   from TV_ZWP_DEF_DAY_DETAIL
                   where DAYTIME >= DATE '2026-06-01' and DAYTIME <= LAST_DAY(DATE '2026-06-01')
                     and DEF_QTY_DER < 0 and VARIATION='Y'
                   order by DAYTIME fetch first 15 rows only""")
    print(" | ".join(d[0] for d in cur.description))
    for r in cur.fetchall(): print(" | ".join('' if v is None else str(v) for v in r))
except Exception as e:
    print("ERR:", str(e)[:200])
c.close(); print("\nDONE")
