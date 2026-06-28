"""
ECSR-35236 Stage-2 behavioural UT (READ-ONLY on plutodev).
The EC check fires when  SELECT Count(*) FROM <target> WHERE <formula>  > 0.
For each of the 8 rules show, against LIVE data:
  - N_before = rows the ORIGINAL (value-only) check flags
  - N_after  = rows the SCOPED check flags (value-only AND method/on-stream criterion)
  - suppressed = N_before - N_after  (the false positives), broken down by the method column
Also VALIDATES every column the fix references actually exists on the target table
(catches e.g. a wrong method/on-stream column name that would break the deployed check).
No writes; safe regardless of apply/rollback state.
"""
import oracledb

con = oracledb.connect(user="ECKERNEL_EC", password="energy",
                       dsn="db.plutodev.woodside-pluto.tieto-og.cloud:1521/plutodev")
cur = con.cursor()

# rule -> (target table, value column, method criterion as raw SQL after the value test)
RULES = [
    ("PHD_TANK_DIP_GRS_MASS_VAL1",   "RV_TANK_DAY_DIP_STATUS", "ZWP_GRS_MASS_TONNES",      "GRS_MASS_METHOD = 'MEASURED'"),
    ("PHD_TANK_DIP_STD_DENSITY_VAL1","RV_TANK_DAY_DIP_STATUS", "MEAS_STD_DENSITY_KGPERSM3","STD_DENS_METHOD = 'MEASURED'"),
    ("PHD_STRM_ANALYSIS_DENSITY_VAL1","RV_STRM_ANALYSIS",      "DENSITY",                  "STD_DENSITY_METHOD = 'COMP_ANALYSIS'"),
    ("PHD_STRM_ANALYSIS_GCV_VAL1",   "RV_STRM_ANALYSIS",       "GCV_MJPERSM3",             "GCV_METHOD = 'COMP_ANALYSIS'"),
    ("PHD_PWEL_STATUS_NODATA_BHTEMP","RV_PWEL_DAY_STATUS",     "AVG_BH_TEMP_C",            "ON_STREAM_HRS_HRS > 0"),
    ("PHD_PWEL_STATUS_NODATA_WHTEMP","RV_PWEL_DAY_STATUS",     "AVG_WH_TEMP_C",            "ON_STREAM_HRS_HRS > 0"),
    ("PHD_PWEL_STATUS_NODATA_BHPRESS","RV_PWEL_DAY_STATUS",    "AVG_BH_PRESS_KPA",         "ON_STREAM_HRS_HRS > 0"),
    ("PHD_PWEL_STATUS_NODATA_WHPRESS","RV_PWEL_DAY_STATUS",    "AVG_WH_PRESS_KPA",         "ON_STREAM_HRS_HRS > 0"),
]


def cols_of(tbl):
    cur.execute("SELECT column_name FROM all_tab_columns WHERE table_name=:t", [tbl])
    return {r[0] for r in cur}


def count(sql):
    cur.execute(sql); return cur.fetchone()[0]


tbl_cols = {}
print("=" * 72)
for name, tbl, vcol, crit in RULES:
    if tbl not in tbl_cols:
        tbl_cols[tbl] = cols_of(tbl)
    cols = tbl_cols[tbl]
    method_col = crit.split()[0]
    col_ok = (vcol in cols) and (method_col in cols)
    print(f"\n[{name}]  target={tbl}")
    print(f"   value col {vcol:26} exists={vcol in cols} | criterion col {method_col:20} exists={method_col in cols}")
    if not col_ok:
        print(f"   *** COLUMN MISSING -> fix would break this check! ***")
        continue
    val_pred = f"({vcol} IS NULL OR {vcol} < 0)"
    nb = count(f"SELECT COUNT(*) FROM {tbl} a WHERE {val_pred}")
    na = count(f"SELECT COUNT(*) FROM {tbl} a WHERE {val_pred} AND {crit}")
    print(f"   N_before (original check flags) = {nb}")
    print(f"   N_after  (scoped check flags)   = {na}")
    print(f"   SUPPRESSED false-positives      = {nb - na}")
    # breakdown of the flagged rows by the method/on-stream column
    try:
        cur.execute(f"SELECT {method_col}, COUNT(*) FROM {tbl} a WHERE {val_pred} GROUP BY {method_col} ORDER BY 2 DESC")
        br = cur.fetchall()
        print(f"   flagged rows by {method_col}: " + ", ".join(f"{('NULL' if v is None else v)}={c}" for v, c in br))
    except Exception as e:
        print(f"   (breakdown err: {str(e)[:60]})")
con.close()
print("\n" + "=" * 72)
