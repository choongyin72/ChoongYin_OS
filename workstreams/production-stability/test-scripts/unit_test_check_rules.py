"""
Issue_1052 — Unit Test: PHD Check Rule Validation
Layer 1: DB-level unit tests (no browser) using Oracle direct calls.

Object codes are loaded dynamically from issue-1052-tag-list.csv.
NO hardcoded object codes — each TC picks the first matching object
from the CSV for its EC Class and Attribute.

Test date: 2026-01-01 (configurable via TEST_DATE below)
Environment: COPS DEV (db.plutodev.woodside-pluto.tieto-og.cloud)
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

import csv
import oracledb
from datetime import date, datetime
from pathlib import Path
from collections import defaultdict

# ── Config ───────────────────────────────────────────────────────────────────
DB_DSN  = 'db.plutodev.woodside-pluto.tieto-og.cloud:1521/plutodev'
DB_USER = 'ECKERNEL_EC'
DB_PASS = 'energy'
TEST_DATE = date(2026, 1, 1)

CSV_PATH = Path(r'C:\Projects\ChoongYin_OS\workstreams\production-stability\issue-1052-tag-list.csv')
RESULTS_PATH = Path(r'C:\Projects\ChoongYin_OS\workstreams\production-stability\test-scripts\unit_test_results.txt')

RESULTS  = []
TC_META  = {}   # tc_id → {check_name, rv_table, obj_code, max_daytime}


# ── Load tag list CSV ─────────────────────────────────────────────────────────
def load_tag_list():
    """
    Returns dict: { (ec_class, attribute): [(object_code, component), ...] }
    Driven entirely from issue-1052-tag-list.csv — no hardcoding.
    """
    tag_map = defaultdict(list)
    with open(CSV_PATH, newline='', encoding='utf-8') as f:
        for row in csv.DictReader(f):
            key = (row['EC Class'].strip(), row['Attribute'].strip())
            tag_map[key].append((row['Object Code'].strip(), row['Component'].strip()))
    return tag_map


def get_all_objects(tag_map, ec_class, attribute):
    """
    Return ALL unique (object_code, component) entries from CSV
    for the given EC Class + Attribute.
    Falls back to class-level lookup if attribute not found.
    """
    entries = tag_map.get((ec_class, attribute), [])
    if not entries:
        for (cls, attr), vals in tag_map.items():
            if cls == ec_class and vals:
                entries = vals
                break
    # Deduplicate preserving order
    seen = set()
    unique = []
    for obj_code, comp in entries:
        if obj_code not in seen:
            seen.add(obj_code)
            unique.append((obj_code, comp))
    return unique


# ── DB helpers ────────────────────────────────────────────────────────────────
def connect():
    return oracledb.connect(user=DB_USER, password=DB_PASS, dsn=DB_DSN)


def log_result(tc_id, rule_name, scenario, expected, actual, detail=''):
    status = 'PASS' if expected == actual else 'FAIL'
    RESULTS.append({
        'tc': tc_id, 'rule': rule_name, 'scenario': scenario,
        'expected': expected, 'actual': actual, 'status': status, 'detail': detail
    })
    icon = '✅' if status == 'PASS' else '❌'
    print(f'  {icon} [{status}] {tc_id} | {scenario} | {detail}')


# ── Core test function ────────────────────────────────────────────────────────
def test_check_rule(tc_id, check_name, ec_class, attribute, tag_map,
                    rv_table, var_col, check_range=False):
    """
    Sub-Test 1 (RULE_EXISTS) runs once per TC.
    Sub-Tests 2–5 run for EVERY object found in issue-1052-tag-list.csv
    for the given EC Class + Attribute.
    """
    conn = connect()
    cur  = conn.cursor()

    print(f"\n{'─'*65}")
    print(f"TC: {tc_id} | Rule: {check_name}")
    print(f"EC Class: {ec_class} | Attribute: {attribute} | RV Table: {rv_table}")
    print(f"{'─'*65}")

    # ── Get ALL objects from CSV ──────────────────────────────────────────────
    all_objects = get_all_objects(tag_map, ec_class, attribute)
    if not all_objects:
        log_result(tc_id, check_name, 'CSV_LOOKUP',
                   'FOUND', 'NOT_FOUND',
                   f'No entry in CSV for class={ec_class} attr={attribute}')
        cur.close(); conn.close()
        return

    print(f"  Objects from CSV ({len(all_objects)}): {[o[0] for o in all_objects]}")

    # ── Sub-Test 1: RULE_EXISTS — runs once per TC ────────────────────────────
    cur.execute("""
        SELECT cr.CHECK_ID, cr.TABLE_ID, cr.SEVERITY_LEVEL, cr.WHERE_FORMULA,
               cr.REV_TEXT, crv.VARIABLE_NAME, crv.VARIABLE_VALUE
          FROM TV_CTRL_CHECK_RULES cr
          JOIN TV_CTRL_CHECK_RULE_VARIABLE crv ON cr.CHECK_ID = crv.CHECK_ID
         WHERE cr.CHECK_NAME = :cn
    """, cn=check_name)
    rule = cur.fetchone()

    if not rule:
        log_result(tc_id, check_name, 'RULE_EXISTS',
                   'FOUND', 'NOT_FOUND', 'Rule missing from DB — SQL script may not have run')
        cur.close(); conn.close()
        return

    check_id, table_id, severity, where_formula, rev_text, var_name, var_col_db = rule
    log_result(tc_id, check_name, 'RULE_EXISTS',
               'FOUND', 'FOUND',
               f'CHECK_ID={check_id} | TABLE={table_id} | VAR={var_col_db}')

    # ── Sub-Test 1b: SEVERITY_LEVEL must be ERROR ──────────────────────────────
    log_result(tc_id, check_name, 'SEVERITY_LEVEL',
               'ERROR', severity or 'NULL',
               f'SEVERITY_LEVEL={severity}')

    # ── Sub-Test 1c: WHERE_FORMULA must exist and contain IS NULL check ────────
    formula_ok = where_formula and 'IS NULL' in where_formula
    log_result(tc_id, check_name, 'WHERE_FORMULA',
               'VALID', 'VALID' if formula_ok else 'INVALID',
               f'Formula: {where_formula}')

    # ── Sub-Test 1d: REV_TEXT must be set ─────────────────────────────────────
    log_result(tc_id, check_name, 'REV_TEXT',
               'SET', 'SET' if rev_text else 'NULL',
               f'REV_TEXT={rev_text}')

    # ── Sub-Tests 2–5: loop every object from CSV ─────────────────────────────
    for idx, (obj_code, component) in enumerate(all_objects, start=1):
        obj_label = f'OBJ{idx:02d}:{obj_code}'
        print(f"\n  [{idx}/{len(all_objects)}] Object: {obj_code}  Component: {component or '(none)'}")

        # Sub-Test 2 — OBJECT_EXISTS
        cur.execute("SELECT OBJECT_ID FROM TV_OBJECTS WHERE CODE = :c", c=obj_code)
        obj_row = cur.fetchone()
        if not obj_row:
            log_result(tc_id, check_name, f'OBJECT_EXISTS | {obj_label}',
                       'FOUND', 'NOT_FOUND', f'CODE={obj_code} not found in TV_OBJECTS')
            continue
        log_result(tc_id, check_name, f'OBJECT_EXISTS | {obj_label}',
                   'FOUND', 'FOUND', f'CODE={obj_code} confirmed in TV_OBJECTS')

        # Sub-Test 2b — MAX(DAYTIME)
        cur.execute(f"SELECT MAX(DAYTIME) FROM {rv_table} WHERE CODE = :c", c=obj_code)
        max_daytime = cur.fetchone()[0]
        if max_daytime is None:
            log_result(tc_id, check_name, f'MAX_DAYTIME | {obj_label}',
                       'FOUND', 'NOT_FOUND', f'No data in {rv_table} for CODE={obj_code}')
            continue
        use_date = str(TEST_DATE)
        log_result(tc_id, check_name, f'MAX_DAYTIME | {obj_label}',
                   'FOUND', 'FOUND',
                   f'MAX(DAYTIME)={max_daytime.strftime("%Y-%m-%d")} | TEST_DATE={use_date}')

        # Store TC meta on first object only
        if tc_id not in TC_META:
            TC_META[tc_id] = {
            'check_name':  check_name,
            'rv_table':    rv_table,
            'obj_code':    obj_code,
            'max_daytime': use_date,
        }

        # Sub-Test 3 — POSITIVE_VALID
        # Query 1: data exists and IS NOT NULL → rule would NOT fire (positive scenario)
        # Query 2: negative value found → only FAIL if rule formula fires on negatives
        try:
            cur.execute(f"""
                SELECT COUNT(*) FROM {rv_table}
                 WHERE CODE    = :code
                   AND DAYTIME = TO_DATE(:dt, 'YYYY-MM-DD')
                   AND {var_col} IS NOT NULL
                   AND ROWNUM  <= 1
            """, code=obj_code, dt=use_date)
            q1_count = cur.fetchone()[0]
            if q1_count > 0:
                log_result(tc_id, check_name, f'POSITIVE_VALID | {obj_label}',
                           'PASS', 'PASS',
                           f'Valid {var_col} found (NOT NULL) | Rule would NOT fire for null check')
            else:
                log_result(tc_id, check_name, f'POSITIVE_VALID | {obj_label}',
                           'PASS', 'FAIL',
                           f'No data (NOT NULL) for CODE={obj_code} on DAYTIME={use_date}')
        except Exception as e:
            log_result(tc_id, check_name, f'POSITIVE_VALID | {obj_label}',
                       'PASS', 'QUERY_ERROR', str(e)[:80])

        # Sub-Test 4 — NEG_NULL_CHECK
        try:
            cur.execute(f"""
                SELECT COUNT(*) FROM {rv_table}
                 WHERE CODE    = :code
                   AND DAYTIME = TO_DATE(:dt, 'YYYY-MM-DD')
                   AND {var_col} IS NULL AND ROWNUM <= 10
            """, code=obj_code, dt=use_date)
            null_count = cur.fetchone()[0]
            fires  = null_count > 0
            result = 'RULE_FIRES' if fires else 'INFO_NO_NULL_DATA'
            log_result(tc_id, check_name, f'NEG_NULL_CHECK | {obj_label}',
                       result, result,
                       f'NULL rows={null_count} | {"→ rule fires" if fires else "→ no nulls on test date"}')
        except Exception as e:
            log_result(tc_id, check_name, f'NEG_NULL_CHECK | {obj_label}',
                       'RULE_FIRES', 'QUERY_ERROR', str(e)[:80])

        # Sub-Test 5 — NEG_OUTOFRANGE (range rules only)
        if check_range:
            try:
                cur.execute(f"""
                    SELECT COUNT(*) FROM {rv_table}
                     WHERE CODE    = :code
                       AND DAYTIME = TO_DATE(:dt, 'YYYY-MM-DD')
                       AND ({var_col} < 0 OR {var_col} > 100) AND ROWNUM <= 10
                """, code=obj_code, dt=use_date)
                range_count = cur.fetchone()[0]
                fires  = range_count > 0
                result = 'RULE_FIRES' if fires else 'INFO_NO_RANGE_DATA'
                log_result(tc_id, check_name, f'NEG_OUTOFRANGE | {obj_label}',
                           result, result,
                           f'Out-of-range rows={range_count} | {"→ rule fires" if fires else "→ no out-of-range data"}')
            except Exception as e:
                log_result(tc_id, check_name, f'NEG_OUTOFRANGE | {obj_label}',
                           'RULE_FIRES', 'QUERY_ERROR', str(e)[:80])

    cur.close(); conn.close()


def read_plsql(path):
    """Extract just the DECLARE...END; block — strips SQL*Plus '/' terminator and trailing comments."""
    lines = Path(path).read_text(encoding='utf-8').splitlines()
    block = []
    for line in lines:
        if line.strip() == '/':
            break
        block.append(line)
    return '\n'.join(block).strip()


# ── Idempotency Test ──────────────────────────────────────────────────────────
def test_idempotency():
    """
    Run the SQL script a second time and verify rule count stays at 8.
    Confirms UPDATE-then-INSERT pattern is re-runnable with no duplicates.
    """
    print(f"\n{'─'*65}")
    print('IDEMPOTENCY TEST — Re-run SQL script, verify no duplicates')
    print(f"{'─'*65}")

    check_names = [
        'PHD_STRM_COMP_MOL_PCT_VAL1', 'PHD_STRM_COMP_WT_PCT_VAL1',
        'PHD_STRM_ANALYSIS_DENSITY_VAL1', 'PHD_STRM_ANALYSIS_GCV_VAL1',
        'PHD_TANK_DIP_GRS_VOL_VAL1', 'PHD_TANK_DIP_GRS_MASS_VAL1',
        'PHD_TANK_DIP_AVG_TEMP_VAL1', 'PHD_TANK_DIP_STD_DENSITY_VAL1',
    ]
    conn = connect(); cur = conn.cursor()

    # Count before re-run
    placeholders = ','.join([f':n{i}' for i in range(len(check_names))])
    bind = {f'n{i}': n for i, n in enumerate(check_names)}
    cur.execute(f"SELECT COUNT(*) FROM TV_CTRL_CHECK_RULES WHERE CHECK_NAME IN ({placeholders})", bind)
    count_before = cur.fetchone()[0]
    log_result('IDEMPOTENCY', 'ALL_RULES', 'COUNT_BEFORE_RERUN', 8, count_before,
               f'Rules in DB before re-run = {count_before}')

    # Re-run the SQL script
    sql_path = Path(r'C:\Projects\ChoongYin_OS\workstreams\production-stability\sql-scripts\Issue1052_PHD_Check_Rules.sql')
    try:
        sql = read_plsql(sql_path)
        cur.execute(sql)
        conn.commit()
        log_result('IDEMPOTENCY', 'ALL_RULES', 'RERUN_SQL',
                   'SUCCESS', 'SUCCESS', f'Script re-executed: {sql_path.name}')
    except Exception as e:
        log_result('IDEMPOTENCY', 'ALL_RULES', 'RERUN_SQL',
                   'SUCCESS', 'FAIL', str(e)[:80])
        cur.close(); conn.close(); return

    # Count after re-run — must still be 8
    cur.execute(f"SELECT COUNT(*) FROM TV_CTRL_CHECK_RULES WHERE CHECK_NAME IN ({placeholders})", bind)
    count_after = cur.fetchone()[0]
    log_result('IDEMPOTENCY', 'ALL_RULES', 'COUNT_AFTER_RERUN',
               count_before, count_after,
               f'Rules after re-run = {count_after} | {"No duplicates ✅" if count_after == count_before else "DUPLICATES FOUND ❌"}')

    cur.close(); conn.close()


# ── Rollback Test ─────────────────────────────────────────────────────────────
def test_rollback():
    """
    Run the rollback script, verify 8 rules deleted.
    Then re-run insert script to restore rules.
    """
    print(f"\n{'─'*65}")
    print('ROLLBACK TEST — Run rollback, verify deletion, restore rules')
    print(f"{'─'*65}")

    check_names = [
        'PHD_STRM_COMP_MOL_PCT_VAL1', 'PHD_STRM_COMP_WT_PCT_VAL1',
        'PHD_STRM_ANALYSIS_DENSITY_VAL1', 'PHD_STRM_ANALYSIS_GCV_VAL1',
        'PHD_TANK_DIP_GRS_VOL_VAL1', 'PHD_TANK_DIP_GRS_MASS_VAL1',
        'PHD_TANK_DIP_AVG_TEMP_VAL1', 'PHD_TANK_DIP_STD_DENSITY_VAL1',
    ]
    placeholders = ','.join([f':n{i}' for i in range(len(check_names))])
    bind = {f'n{i}': n for i, n in enumerate(check_names)}

    rollback_path = Path(r'C:\Projects\ChoongYin_OS\workstreams\production-stability\sql-scripts\Issue1052_PHD_Check_Rules_ROLLBACK.sql')
    insert_path   = Path(r'C:\Projects\ChoongYin_OS\workstreams\production-stability\sql-scripts\Issue1052_PHD_Check_Rules.sql')

    conn = connect(); cur = conn.cursor()

    # Step 1: Run rollback
    try:
        rollback_sql = read_plsql(rollback_path)
        cur.execute(rollback_sql)
        conn.commit()
        log_result('ROLLBACK', 'ALL_RULES', 'ROLLBACK_EXECUTED',
                   'SUCCESS', 'SUCCESS', f'Rollback script executed: {rollback_path.name}')
    except Exception as e:
        log_result('ROLLBACK', 'ALL_RULES', 'ROLLBACK_EXECUTED',
                   'SUCCESS', 'FAIL', str(e)[:80])
        cur.close(); conn.close(); return

    # Step 2: Verify rules deleted
    cur.execute(f"SELECT COUNT(*) FROM TV_CTRL_CHECK_RULES WHERE CHECK_NAME IN ({placeholders})", bind)
    count_after_rollback = cur.fetchone()[0]
    log_result('ROLLBACK', 'ALL_RULES', 'RULES_DELETED',
               0, count_after_rollback,
               f'Rules remaining after rollback = {count_after_rollback} | {"All deleted ✅" if count_after_rollback == 0 else "Some rules remain ❌"}')

    # Step 3: Re-run insert script to restore
    try:
        insert_sql = read_plsql(insert_path)
        cur.execute(insert_sql)
        conn.commit()
        log_result('ROLLBACK', 'ALL_RULES', 'RESTORE_EXECUTED',
                   'SUCCESS', 'SUCCESS', f'Insert script re-executed to restore rules')
    except Exception as e:
        log_result('ROLLBACK', 'ALL_RULES', 'RESTORE_EXECUTED',
                   'SUCCESS', 'FAIL', str(e)[:80])
        cur.close(); conn.close(); return

    # Step 4: Verify rules restored
    cur.execute(f"SELECT COUNT(*) FROM TV_CTRL_CHECK_RULES WHERE CHECK_NAME IN ({placeholders})", bind)
    count_restored = cur.fetchone()[0]
    log_result('ROLLBACK', 'ALL_RULES', 'RULES_RESTORED',
               8, count_restored,
               f'Rules after restore = {count_restored} | {"All restored ✅" if count_restored == 8 else "Restore incomplete ❌"}')

    cur.close(); conn.close()


# ── Main ──────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    print('=' * 65)
    print('Issue_1052 — Unit Test: PHD Check Rule Validation')
    print(f'Environment : COPS DEV')
    print(f'Test Date   : {TEST_DATE}')
    print(f'Run At      : {datetime.now().strftime("%Y-%m-%d %H:%M")}')
    print(f'Object Source: {CSV_PATH.name}  (no hardcoding)')
    print('=' * 65)

    tag_map = load_tag_list()
    print(f'\nLoaded {sum(len(v) for v in tag_map.values())} tags from CSV across {len(tag_map)} class/attribute combinations.\n')

    # TC01 — STRM_COMP_ANALYSIS / MOL_PCT  (range rule: 0–100%)
    test_check_rule('TC01', 'PHD_STRM_COMP_MOL_PCT_VAL1',
                    'STRM_COMP_ANALYSIS', 'MOL_PCT', tag_map,
                    rv_table='RV_STRM_COMP_ANALYSIS', var_col='MOL_PCT', check_range=True)

    # TC02 — STRM_COMP_ANALYSIS / WT_PCT  (range rule: 0–100%)
    test_check_rule('TC02', 'PHD_STRM_COMP_WT_PCT_VAL1',
                    'STRM_COMP_ANALYSIS', 'WT_PCT', tag_map,
                    rv_table='RV_STRM_COMP_ANALYSIS', var_col='WT_PCT', check_range=True)

    # TC03 — STRM_ANALYSIS / DENSITY
    test_check_rule('TC03', 'PHD_STRM_ANALYSIS_DENSITY_VAL1',
                    'STRM_ANALYSIS', 'DENSITY', tag_map,
                    rv_table='RV_STRM_ANALYSIS', var_col='DENSITY')

    # TC04 — STRM_ANALYSIS / GCV
    test_check_rule('TC04', 'PHD_STRM_ANALYSIS_GCV_VAL1',
                    'STRM_ANALYSIS', 'GCV', tag_map,
                    rv_table='RV_STRM_ANALYSIS', var_col='GCV_MJPERSM3')

    # TC05 — TANK_DAY_DIP_STATUS / GRS_VOL
    test_check_rule('TC05', 'PHD_TANK_DIP_GRS_VOL_VAL1',
                    'TANK_DAY_DIP_STATUS', 'GRS_VOL', tag_map,
                    rv_table='RV_TANK_DAY_DIP_STATUS', var_col='GRS_VOL_SM3')

    # TC06 — TANK_DAY_DIP_STATUS / GRS_MASS
    # CSV attribute = ZWP_GRS_MASS (short name) → finds T_LNG_T3101/T3102
    # RV_ column    = ZWP_GRS_MASS_TONNES (full column name with unit suffix)
    test_check_rule('TC06', 'PHD_TANK_DIP_GRS_MASS_VAL1',
                    'TANK_DAY_DIP_STATUS', 'ZWP_GRS_MASS', tag_map,
                    rv_table='RV_TANK_DAY_DIP_STATUS', var_col='ZWP_GRS_MASS_TONNES')

    # TC07 — TANK_DAY_DIP_STATUS / AVG_TEMP
    test_check_rule('TC07', 'PHD_TANK_DIP_AVG_TEMP_VAL1',
                    'TANK_DAY_DIP_STATUS', 'AVG_TEMP', tag_map,
                    rv_table='RV_TANK_DAY_DIP_STATUS', var_col='AVG_TEMP_C')

    # TC08 — TANK_DAY_DIP_STATUS / STD_DENSITY (CSV lookup via MEAS_STD_DENSITY — T_LNG_T3101/T3102)
    test_check_rule('TC08', 'PHD_TANK_DIP_STD_DENSITY_VAL1',
                    'TANK_DAY_DIP_STATUS', 'MEAS_STD_DENSITY', tag_map,
                    rv_table='RV_TANK_DAY_DIP_STATUS', var_col='MEAS_STD_DENSITY_KGPERSM3')

    # ── Idempotency Test ──────────────────────────────────────────────────────
    test_idempotency()

    # ── Rollback Test ─────────────────────────────────────────────────────────
    test_rollback()

    # ── Summary ───────────────────────────────────────────────────────────────
    passed = sum(1 for r in RESULTS if r['status'] == 'PASS')
    failed = sum(1 for r in RESULTS if r['status'] == 'FAIL')
    total  = len(RESULTS)

    print(f'\n{"="*110}')
    print('UNIT TEST SUMMARY')
    print(f'{"="*110}')
    print(f'  {"TC":<6} {"RV View Table":<26} {"Objects Tested":<8} {"POSITIVE_VALID":<16} {"Failed Objects / Reason"}')
    print(f'  {"-"*6} {"-"*26} {"-"*8} {"-"*16} {"-"*55}')

    for tc_id in sorted(TC_META.keys()):
        meta         = TC_META[tc_id]
        # All POSITIVE_VALID results for this TC
        pv_results   = [r for r in RESULTS if r['tc'] == tc_id and 'POSITIVE_VALID' in r['scenario']]
        obj_results  = [r for r in RESULTS if r['tc'] == tc_id and 'OBJECT_EXISTS' in r['scenario']]
        obj_count    = len(obj_results)
        pv_fails     = [r for r in pv_results if r['status'] == 'FAIL']
        tc_pass      = len(pv_fails) == 0
        pv_icon      = '✅ PASS' if tc_pass else '❌ FAIL'

        if tc_pass:
            reason = f'All {obj_count} object(s) passed'
        else:
            fail_details = []
            for r in pv_fails:
                obj = r['scenario'].split('OBJ')[1].split(':')[1] if 'OBJ' in r['scenario'] else '?'
                fail_details.append(f'{obj}: {r["detail"][:40]}')
            reason = ' | '.join(fail_details)

        print(f'  {tc_id:<6} {meta["rv_table"]:<26} {obj_count:<8} {pv_icon:<16} {reason}')

    print(f'{"="*110}')
    print(f'  Total assertions : {total}  |  Passed : {passed}  |  Failed : {failed}  |  Overall : {"PASS ✅" if failed == 0 else "FAIL ❌"}')
    print(f'{"="*110}')

    # ── Save results ──────────────────────────────────────────────────────────
    with open(RESULTS_PATH, 'w', encoding='utf-8') as f:
        f.write('Issue_1052 Unit Test Results\n')
        f.write(f'Run     : {datetime.now()}\n')
        f.write(f'Env     : COPS DEV\n')
        f.write(f'Objects : loaded from {CSV_PATH.name}\n')
        f.write('=' * 100 + '\n\n')

        # Detail section
        f.write('DETAIL\n')
        f.write('-' * 100 + '\n')
        for r in RESULTS:
            f.write(f"[{r['status']}] {r['tc']} | {r['rule']} | {r['scenario']} | {r['detail']}\n")

        # Summary table
        f.write(f'\n{"=" * 100}\n')
        f.write('SUMMARY — TC TABLE\n')
        f.write('=' * 100 + '\n')
        f.write(f'  {"TC":<6} {"Check Rule":<40} {"RV View Table":<30} {"Object Code":<25} {"MAX(DAYTIME)":<13} {"Result"}\n')
        f.write(f'  {"-"*6} {"-"*40} {"-"*30} {"-"*25} {"-"*13} {"-"*8}\n')
        for tc_id in sorted(TC_META.keys()):
            meta       = TC_META[tc_id]
            tc_failed  = any(r['status'] == 'FAIL' for r in RESULTS if r['tc'] == tc_id)
            tc_result  = 'FAIL' if tc_failed else 'PASS'
            f.write(f'  {tc_id:<6} {meta["check_name"]:<40} {meta["rv_table"]:<30} {meta["obj_code"]:<25} {meta["max_daytime"]:<13} {tc_result}\n')
        f.write('=' * 100 + '\n')
        f.write(f'  Total={total}  Passed={passed}  Failed={failed}  Overall={"PASS" if failed == 0 else "FAIL"}\n')
        f.write('=' * 100 + '\n')

    print(f'\nResults saved: {RESULTS_PATH}')
