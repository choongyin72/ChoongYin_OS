import oracledb
from datetime import datetime

conn = oracledb.connect(user='ECKERNEL_EC', password='energy', dsn='db.plutodev.woodside-pluto.tieto-og.cloud:1521/plutodev')
cur = conn.cursor()

RULES = [
    'PHD_STRM_COMP_MOL_PCT_VAL1',
    'PHD_STRM_COMP_WT_PCT_VAL1',
    'PHD_STRM_ANALYSIS_DENSITY_VAL1',
    'PHD_STRM_ANALYSIS_GCV_VAL1',
    'PHD_TANK_DIP_GRS_VOL_VAL1',
    'PHD_TANK_DIP_GRS_MASS_VAL1',
    'PHD_TANK_DIP_AVG_TEMP_VAL1',
    'PHD_TANK_DIP_STD_DENSITY_VAL1'
]

def verify(label):
    cur.execute("""
        SELECT cr.CHECK_ID, cr.CHECK_NAME, cr.TABLE_ID, cr.SEVERITY_LEVEL,
               crv.VARIABLE_NAME, crv.VARIABLE_VALUE, cr.REV_TEXT
          FROM TV_CTRL_CHECK_RULES cr
          LEFT JOIN TV_CTRL_CHECK_RULE_VARIABLE crv ON cr.CHECK_ID = crv.CHECK_ID
         WHERE cr.CHECK_NAME IN (
            'PHD_STRM_COMP_MOL_PCT_VAL1','PHD_STRM_COMP_WT_PCT_VAL1',
            'PHD_STRM_ANALYSIS_DENSITY_VAL1','PHD_STRM_ANALYSIS_GCV_VAL1',
            'PHD_TANK_DIP_GRS_VOL_VAL1','PHD_TANK_DIP_GRS_MASS_VAL1',
            'PHD_TANK_DIP_AVG_TEMP_VAL1','PHD_TANK_DIP_STD_DENSITY_VAL1'
         )
         ORDER BY cr.CHECK_ID
    """)
    rows = cur.fetchall()
    sep = '=' * 120
    print(f"\n{sep}")
    print(f"  {label}")
    print(f"  Timestamp : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  Rows found: {len(rows)}")
    print(sep)
    if rows:
        print(f"  {'CHECK_ID':<10} {'CHECK_NAME':<42} {'TABLE_ID':<32} {'SEV':<6} {'VAR':<15} {'VALUE':<25} {'REV_TEXT'}")
        print(f"  {'-'*115}")
        for r in rows:
            print(f"  {str(r[0]):<10} {str(r[1]):<42} {str(r[2]):<32} {str(r[3]):<6} {str(r[4] or '-'):<15} {str(r[5] or '-'):<25} {str(r[6] or '-')}")
    else:
        print("  >> NO ROWS FOUND")
    return len(rows)

# STEP 1: Before
before = verify("STEP 1 — BEFORE INSERT (Baseline)")

# STEP 2: Insert
sep = '=' * 120
print(f"\n{sep}")
print(f"  STEP 2 — RUNNING INSERT (Issue1052_PHD_Check_Rules.sql)")
print(f"  Timestamp : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(sep)

c_rev_text = 'ECPR-Issue1052'
inserts = [
    ('PHD_STRM_COMP_MOL_PCT_VAL1',     'RV_STRM_COMP_ANALYSIS',  '(${MolPct} IS NULL OR ${MolPct} < 0 OR ${MolPct} > 100)',  'Stream :STREAM_NAME component :COMPONENT_NO has invalid or missing Mol% for :DAYTIME',  'ERROR', 'MolPct',     'MOL_PCT'),
    ('PHD_STRM_COMP_WT_PCT_VAL1',      'RV_STRM_COMP_ANALYSIS',  '(${WtPct} IS NULL OR ${WtPct} < 0 OR ${WtPct} > 100)',    'Stream :STREAM_NAME component :COMPONENT_NO has invalid or missing Wt% for :DAYTIME',   'ERROR', 'WtPct',      'WT_PCT'),
    ('PHD_STRM_ANALYSIS_DENSITY_VAL1', 'RV_STRM_ANALYSIS',       '(${Density} IS NULL OR ${Density} <= 0)',                  'Stream :STREAM_NAME has invalid or missing Density value for :DAYTIME',                  'ERROR', 'Density',    'DENSITY'),
    ('PHD_STRM_ANALYSIS_GCV_VAL1',     'RV_STRM_ANALYSIS',       '(${Gcv} IS NULL OR ${Gcv} <= 0)',                          'Stream :STREAM_NAME has invalid or missing GCV value for :DAYTIME',                      'ERROR', 'Gcv',        'GCV_MJPERSM3'),
    ('PHD_TANK_DIP_GRS_VOL_VAL1',      'RV_TANK_DAY_DIP_STATUS', '(${GrsVol} IS NULL OR ${GrsVol} < 0)',                     'Tank :TANK_NAME has invalid or missing Gross Volume for :DAYTIME',                       'ERROR', 'GrsVol',     'GRS_VOL_SM3'),
    ('PHD_TANK_DIP_GRS_MASS_VAL1',     'RV_TANK_DAY_DIP_STATUS', '(${GrsMass} IS NULL OR ${GrsMass} < 0)',                   'Tank :TANK_NAME has invalid or missing Gross Mass for :DAYTIME',                         'ERROR', 'GrsMass',    'ZWP_GRS_MASS_TONNES'),
    ('PHD_TANK_DIP_AVG_TEMP_VAL1',     'RV_TANK_DAY_DIP_STATUS', '(${AvgTemp} IS NULL)',                                     'Tank :TANK_NAME has missing Average Temperature for :DAYTIME',                           'ERROR', 'AvgTemp',    'AVG_TEMP_C'),
    ('PHD_TANK_DIP_STD_DENSITY_VAL1',  'RV_TANK_DAY_DIP_STATUS', '(${StdDensity} IS NULL OR ${StdDensity} <= 0)',            'Tank :TANK_NAME has invalid or missing Standard Density for :DAYTIME',                   'ERROR', 'StdDensity', 'MEAS_STD_DENSITY_KGPERSM3'),
]

for check_name, table_id, where, message, severity, var_name, var_value in inserts:
    cur.execute("UPDATE TV_CTRL_CHECK_RULES SET TABLE_ID=:t, CLASS_OBJ_VALIDATION_IND='N', WHERE_FORMULA=:w, CHECK_MESSAGE=:m, SEVERITY_LEVEL=:s, REV_TEXT=:r WHERE CHECK_NAME=:n",
        t=table_id, w=where, m=message, s=severity, r=c_rev_text, n=check_name)
    if cur.rowcount > 0:
        cur.execute("SELECT CHECK_ID FROM CTRL_CHECK_RULES WHERE CHECK_NAME=:n", n=check_name)
        v_id = cur.fetchone()[0]
        action = 'UPDATED'
    else:
        cur.execute("SELECT NVL(MAX(CHECK_ID),0)+1 FROM CTRL_CHECK_RULES")
        v_id = cur.fetchone()[0]
        cur.execute("INSERT INTO TV_CTRL_CHECK_RULES (TABLE_CLASS_NAME,CHECK_ID,CHECK_NAME,SELECT_CLAUSE,TABLE_ID,CLASS_OBJ_VALIDATION_IND,WHERE_FORMULA,CHECK_MESSAGE,SEVERITY_LEVEL,REV_TEXT) VALUES ('CTRL_CHECK_RULES',:id,:n,'Count(*)',:t,'N',:w,:m,:s,:r)",
            id=v_id, n=check_name, t=table_id, w=where, m=message, s=severity, r=c_rev_text)
        action = 'INSERTED'
    cur.execute("UPDATE TV_CTRL_CHECK_RULE_VARIABLE SET VARIABLE_TYPE='ATTRIBUTE', VARIABLE_VALUE=:val, REV_TEXT=:r WHERE CHECK_ID=:id AND VARIABLE_NAME=:vn",
        val=var_value, r=c_rev_text, id=v_id, vn=var_name)
    if cur.rowcount == 0:
        cur.execute("INSERT INTO TV_CTRL_CHECK_RULE_VARIABLE (TABLE_CLASS_NAME,CHECK_ID,VARIABLE_NAME,VARIABLE_TYPE,VARIABLE_VALUE,REV_TEXT) VALUES ('CTRL_CHECK_RULE_VARIABLE',:id,:vn,'ATTRIBUTE',:val,:r)",
            id=v_id, vn=var_name, val=var_value, r=c_rev_text)
    print(f"  >> [{action}] {check_name} (CHECK_ID={v_id})")

conn.commit()
print("  >> COMMIT OK")

# STEP 3: Verify after insert
after_insert = verify("STEP 3 — AFTER INSERT VERIFY")

# STEP 4: Rollback
print(f"\n{sep}")
print(f"  STEP 4 — RUNNING ROLLBACK (Issue1052_PHD_Check_Rules_ROLLBACK.sql)")
print(f"  Timestamp : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(sep)

for check_name in RULES:
    cur.execute("SELECT COUNT(*) FROM CTRL_CHECK_RULES WHERE CHECK_NAME=:n", n=check_name)
    if cur.fetchone()[0] > 0:
        cur.execute("SELECT CHECK_ID FROM CTRL_CHECK_RULES WHERE CHECK_NAME=:n", n=check_name)
        v_id = cur.fetchone()[0]
        cur.execute("DELETE FROM TV_CTRL_CHECK_RULE_VARIABLE WHERE CHECK_ID=:id", id=v_id)
        vr = cur.rowcount
        cur.execute("DELETE FROM TV_CTRL_CHECK_RULE_FUNC_P WHERE CHECK_ID=:id", id=v_id)
        cur.execute("DELETE FROM TV_CTRL_CHECK_RULES WHERE CHECK_ID=:id", id=v_id)
        print(f"  >> [DELETED] {check_name} (CHECK_ID={v_id}, {vr} variable(s) removed)")

conn.commit()
print("  >> COMMIT OK")

# STEP 5: Final verify
after_rollback = verify("STEP 5 — AFTER ROLLBACK VERIFY")

# Summary
print(f"\n{sep}")
print(f"  TEST EVIDENCE SUMMARY")
print(sep)
print(f"  Script 1 : Issue1052_PHD_Check_Rules.sql")
print(f"  Script 2 : Issue1052_PHD_Check_Rules_ROLLBACK.sql")
print(f"  Database  : db.plutodev.woodside-pluto.tieto-og.cloud:1521/plutodev")
print(f"  Schema    : ECKERNEL_EC")
print(f"  Tested by : Choong-Yin Lee")
print(f"  Date      : {datetime.now().strftime('%Y-%m-%d')}")
print(f"  {'-'*80}")
print(f"  Step 1 — Before INSERT  : {before:>3} rows  (Expected: 0)   {'PASS' if before==0 else 'FAIL'}")
print(f"  Step 3 — After INSERT   : {after_insert:>3} rows  (Expected: 8)   {'PASS' if after_insert==8 else 'FAIL'}")
print(f"  Step 5 — After ROLLBACK : {after_rollback:>3} rows  (Expected: 0)   {'PASS' if after_rollback==0 else 'FAIL'}")
print(f"  {'-'*80}")
result = 'PASS' if before==0 and after_insert==8 and after_rollback==0 else 'FAIL'
print(f"  OVERALL RESULT: {result}")
print(sep)

cur.close()
conn.close()
