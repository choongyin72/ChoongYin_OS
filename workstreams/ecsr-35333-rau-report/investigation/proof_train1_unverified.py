"""ECSR-35333 Issue-1 PROOF (READ-ONLY): list LNG Train 1's June deferment-day-detail rows that
are NOT Verified (APPROVAL_STATUS != 'V') - the exact rows the calc gate counts. Creds from ENV."""
import os, oracledb
con = oracledb.connect(user=os.environ["EC_DB_USER"], password=os.environ["EC_DB_PWD"], dsn=os.environ["EC_DB_DSN"])
cur = con.cursor()
OID = "45A9A31E13984198E0630100007F1329"  # LNG_TRAIN_1 deferment equipment object_id
WIN = "DAYTIME >= DATE '2026-06-01' AND DAYTIME <= LAST_DAY(DATE '2026-06-01') AND asset_id = :o"

print("=== (1) status breakdown (the gate counts NVL(APPROVAL_STATUS,'P')!='V') ===")
cur.execute(f"SELECT NVL(APPROVAL_STATUS,'(null)') st, COUNT(*) n FROM TV_ZWP_DEF_DAY_DETAIL WHERE {WIN} GROUP BY NVL(APPROVAL_STATUS,'(null)') ORDER BY 2 DESC", [OID])
for r in cur: print("   status", r[0], "=", r[1])

print("\n=== (2) unverified rows per day (P = Pending/not verified) ===")
cur.execute(f"""SELECT TO_CHAR(DAYTIME,'YYYY-MM-DD') dt, COUNT(*) rows_,
       SUM(CASE WHEN NVL(APPROVAL_STATUS,'P')!='V' THEN 1 ELSE 0 END) unverified
   FROM TV_ZWP_DEF_DAY_DETAIL WHERE {WIN} GROUP BY DAYTIME ORDER BY DAYTIME""", [OID])
for r in cur: print("   ", r)

print("\n=== (3) sample of the actual UNVERIFIED rows (proof) ===")
cur.execute(f"""SELECT TO_CHAR(DAYTIME,'YYYY-MM-DD') dt, APPROVAL_STATUS, DEF_QTY, DEF_QTY_DER, VARIATION
   FROM TV_ZWP_DEF_DAY_DETAIL WHERE {WIN} AND NVL(APPROVAL_STATUS,'P')!='V'
   ORDER BY DAYTIME FETCH FIRST 20 ROWS ONLY""", [OID])
print("   (daytime, approval_status, def_qty, def_qty_der, variation)")
for r in cur: print("   ", r)

print("\n=== (4) the gate result (mirrors the package: count unverified) ===")
cur.execute(f"SELECT COUNT(*) FROM TV_ZWP_DEF_DAY_DETAIL WHERE {WIN} AND NVL(APPROVAL_STATUS,'P')!='V'", [OID])
n = cur.fetchone()[0]
print(f"   unverified count = {n}  ->  IF {n} >= 1 THEN calc sets 'deferment events not verified' and SKIPS RAU Actual for PLU_LNG_TRAIN1")
con.close()
