"""ECSR-35333 READ-ONLY: test the two ZWP_P_DEF_RAU_CALC triggers for the two LNG trains (June 2026):
(1) deferment-verified gate: TV_ZWP_DEF_DAY_DETAIL unverified count (APPROVAL_STATUS != 'V') per train asset;
(2) Techmax capacity reference stream (the LNG capacity source). Creds from ENV. SELECT-only."""
import os, oracledb
con = oracledb.connect(user=os.environ["EC_DB_USER"], password=os.environ["EC_DB_PWD"], dsn=os.environ["EC_DB_DSN"])
cur = con.cursor()

# deferment equipment object_ids for the two trains
cur.execute("""SELECT DISTINCT code, object_id FROM ov_eqpm
               WHERE eqpm_type='DEFERMENT' AND code IN ('LNG_TRAIN_1','LNG_TRAIN_2')""")
eqpm = cur.fetchall()
print("deferment equipment:", eqpm)

for code, oid in eqpm:
    print(f"\n=== {code}  (object_id={oid}) ===")
    # (1) verified gate
    cur.execute("""SELECT COUNT(*) total,
                          SUM(CASE WHEN NVL(APPROVAL_STATUS,'P')!='V' THEN 1 ELSE 0 END) unverified
                   FROM TV_ZWP_DEF_DAY_DETAIL
                   WHERE DAYTIME >= DATE '2026-06-01' AND DAYTIME <= LAST_DAY(DATE '2026-06-01')
                     AND asset_id = :oid""", [oid])
    tot, unv = cur.fetchone()
    print(f"  deferment-day-detail rows (June): total={tot}, UNVERIFIED(!='V')={unv}  -> gate {'TRIPS (skip actual)' if (unv or 0) >= 1 else 'passes'}")
    cur.execute("""SELECT NVL(APPROVAL_STATUS,'(null)'), COUNT(*) FROM TV_ZWP_DEF_DAY_DETAIL
                   WHERE DAYTIME >= DATE '2026-06-01' AND DAYTIME <= LAST_DAY(DATE '2026-06-01')
                     AND asset_id = :oid GROUP BY NVL(APPROVAL_STATUS,'(null)') ORDER BY 2 DESC""", [oid])
    print("    status breakdown:", cur.fetchall())
    # (2) Techmax capacity reference stream
    try:
        cur.execute("""SELECT ec_zwp_equipment.zwp_strm_ref_capacity(
                          ec_eqpm_version.rec_id(:oid, DATE '2026-06-01', '<=')) FROM dual""", [oid])
        print("  Techmax capacity reference stream:", cur.fetchone()[0])
    except Exception as e:
        print("  (capacity ref fn err:", str(e)[:80], ")")
con.close()
