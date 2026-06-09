"""
Issue_1052 - Unit Test: FROZEN-VALUE Check Rules (Layer 1, DB-level, COPS DEV)
Rules 1150-1155 (PHD_*_FROZEN_V1). Mirrors unit_test_check_rules.py structure.

Approach: discovery-based (read-only) for behaviour; idempotency + rollback self-restore.
- Wiring asserts (all 6): exists, WARNING, WHERE_FORMULA, FUNCTION_NAME, ConstBOOLEAN,
  5 func-params, ZWP_SCREEN_VAL, group link.
- Behavioural (one-row/day rules 1152/1153/1154/1155): find natural FROZEN (today==yesterday
  exact) + CHANGED (clearly different) rows, invoke ZWP_P_TOOLTIP.getValFrozenValue, assert.
  No natural case -> PENDING (data gap; seeding deferred - see report).
- Composition (1150/1151): demonstrate grain breakage (>1 row/object/day -> function SUMs
  across components) -> KNOWN_DEFECT (not pass/fail).
- Idempotency: re-run deploy, count stays 6.
- Rollback: group+rules rollback -> 0 -> restore -> 6 (self-restoring).
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
import re, oracledb
from pathlib import Path
from datetime import datetime

DB_DSN  = 'db.plutodev.woodside-pluto.tieto-og.cloud:1521/plutodev'
DB_USER, DB_PASS = 'ECKERNEL_EC', 'energy'
SQLDIR  = Path(r'C:\Projects\ChoongYin_OS\workstreams\production-stability\sql-scripts')
RESULTS = Path(r'C:\Projects\ChoongYin_OS\workstreams\production-stability\test-scripts\frozen_unit_test_results.txt')

LOG = []
def log(tc, scenario, expected, actual, detail=''):
    status = 'PASS' if expected == actual else ('INFO' if expected == 'INFO' else 'FAIL')
    if actual in ('KNOWN_DEFECT', 'PENDING', 'INFO'):
        status = actual
    LOG.append(dict(tc=tc, scenario=scenario, expected=expected, actual=actual, status=status, detail=detail))
    print(f"  [{status:12}] {tc:6} | {scenario:30} | {detail}")

# rule -> metadata
ONE_ROW = 'one_row'   # one row per object/day  (behaviour testable by discovery)
COMP    = 'comp'      # per-component (grain demo)
RULES = [
    dict(tc='F1150', name='PHD_STRM_COMP_MOL_PCT_FROZEN_V1',   view='RV_STRM_COMP_ANALYSIS',
         col='MOL_PCT',                 grp='V_PHD_STREAM_COMP',     sv='N', kind=COMP),
    dict(tc='F1151', name='PHD_STRM_COMP_WT_PCT_FROZEN_V1',    view='RV_STRM_COMP_ANALYSIS',
         col='WT_PCT',                  grp='V_PHD_STREAM_COMP',     sv='N', kind=COMP),
    dict(tc='F1152', name='PHD_STRM_ANALYSIS_DENSITY_FROZEN_V1', view='RV_STRM_ANALYSIS',
         col='DENSITY',                 grp='V_PHD_STREAM_ANALYSIS', sv='N', kind=ONE_ROW),
    dict(tc='F1153', name='PHD_STRM_ANALYSIS_GCV_FROZEN_V1',   view='RV_STRM_ANALYSIS',
         col='GCV_MJPERSM3',            grp='V_PHD_STREAM_ANALYSIS', sv='N', kind=ONE_ROW),
    dict(tc='F1154', name='PHD_STREAM_WATER_OILINWAT_FROZEN_V1', view='RV_STRM_DAY_STREAM_MEAS_WAT',
         col='ZWT_OILINWAT_MGPERLITER', grp='V_PHD_STREAM_WATER',    sv='N', kind=ONE_ROW),
    dict(tc='F1155', name='PHD_PWEL_AVG_GAS_RATE_FROZEN_V1',   view='RV_PWEL_DAY_STATUS',
         col='AVG_GAS_RATE_SM3',        grp='V_PHD_PWEL_STATUS',     sv='Y', kind=ONE_ROW),
]

def connect():
    return oracledb.connect(user=DB_USER, password=DB_PASS, dsn=DB_DSN, tcp_connect_timeout=25)

# ---- wiring asserts -----------------------------------------------------------
def test_wiring(cur, r):
    tc, name = r['tc'], r['name']
    cur.execute("""SELECT CHECK_ID, TABLE_ID, SEVERITY_LEVEL, WHERE_FORMULA, ZWP_SCREEN_VAL
                     FROM TV_CTRL_CHECK_RULES WHERE CHECK_NAME=:n""", n=name)
    row = cur.fetchone()
    if not row:
        log(tc, 'RULE_EXISTS', 'FOUND', 'NOT_FOUND', name); return None
    cid, tbl, sev, wf, sv = row
    log(tc, 'RULE_EXISTS', 'FOUND', 'FOUND', f'CHECK_ID={cid} TABLE={tbl}')
    log(tc, 'TABLE_ID', r['view'], tbl, tbl)
    log(tc, 'SEVERITY', 'WARNING', sev, f'sev={sev}')
    log(tc, 'WHERE_FORMULA', 'VALID',
        'VALID' if wf and 'FunctionFrozenValue' in wf and 'ConstBOOLEAN' in wf else 'INVALID', wf)
    log(tc, 'ZWP_SCREEN_VAL', r['sv'], sv, f'screen_val={sv}')
    # variables
    cur.execute("""SELECT VARIABLE_NAME, VARIABLE_TYPE, VARIABLE_VALUE, FUNCTION_NAME
                     FROM CTRL_CHECK_RULE_VARIABLE WHERE CHECK_ID=:c""", c=cid)
    vars = {x[0]: x for x in cur.fetchall()}
    f = vars.get('FunctionFrozenValue')
    if f:
        log(tc, 'VAR_FunctionFrozenValue', 'ZWP_P_TOOLTIP/getValFrozenValue',
            f'{f[2]}/{f[3]}',
            f'type={f[1]} value={f[2]} func={f[3]}')
    else:
        log(tc, 'VAR_FunctionFrozenValue', 'FOUND', 'MISSING', '')
    c = vars.get('ConstBOOLEAN')
    log(tc, 'VAR_ConstBOOLEAN', 'FROZEN', c[2] if c else 'MISSING', '')
    # func params
    cur.execute("""SELECT PARAMETER_NAME, POSITION, PARAMETER_TYPE, PARAMETER_VALUE
                     FROM CTRL_CHECK_RULE_FUNC_PARAM WHERE CHECK_ID=:c ORDER BY POSITION""", c=cid)
    fps = cur.fetchall()
    log(tc, 'FUNC_PARAMS', '5', str(len(fps)), ','.join(f'{p[0]}={p[3]}' for p in fps))
    # group link
    cur.execute("""SELECT COUNT(*) FROM CTRL_CHECK_COMBINATION WHERE CHECK_ID=:c AND CHECK_GROUP=:g""",
                c=cid, g=r['grp'])
    log(tc, 'GROUP_LINK', r['grp'], r['grp'] if cur.fetchone()[0] else 'MISSING', '')
    return cid

# ---- behavioural (discovery) --------------------------------------------------
def call_fn(cur, cls, obj, dt, val, attr):
    cur.execute("SELECT ZWP_P_TOOLTIP.getValFrozenValue(:c,:o,:d,:v,:a) FROM dual",
                c=cls, o=obj, d=dt, v=val, a=attr)
    return cur.fetchone()[0]

def find_candidate(cur, view, col, equal):
    op = '=' if equal else '<>'
    # exact-equal for frozen; clearly different (>1% apart) for changed -> avoid rounding boundary
    extra = '' if equal else f"AND ABS(t.{col}-y.{col}) > ABS(y.{col})*0.01 + 0.001"
    cur.execute(f"""SELECT t.OBJECT_ID, t.DATA_CLASS_NAME, t.DAYTIME, t.{col}, y.{col}
                      FROM {view} t JOIN {view} y
                        ON y.OBJECT_ID=t.OBJECT_ID AND y.DAYTIME=t.DAYTIME-1
                     WHERE t.{col} IS NOT NULL AND y.{col} IS NOT NULL
                       AND t.{col} {op} y.{col} {extra} AND ROWNUM<=1""")
    return cur.fetchone()

def test_behaviour(cur, r):
    tc, view, col, cls_attr = r['tc'], r['view'], r['col'], r['col']
    # positive (frozen)
    pos = find_candidate(cur, view, col, True)
    if pos:
        obj, cls, dt, v, pv = pos
        res = call_fn(cur, cls, obj, dt, v, cls_attr)
        log(tc, 'BEHAV_POSITIVE(frozen)', 'FROZEN', res, f'obj={obj[:8]} {dt:%Y-%m-%d} val={v}==prev')
    else:
        log(tc, 'BEHAV_POSITIVE(frozen)', 'INFO', 'PENDING', 'no natural frozen row - seeding deferred')
    # negative (changed)
    neg = find_candidate(cur, view, col, False)
    if neg:
        obj, cls, dt, v, pv = neg
        res = call_fn(cur, cls, obj, dt, v, cls_attr)
        log(tc, 'BEHAV_NEGATIVE(changed)', 'NOT_FROZEN', res, f'obj={obj[:8]} {dt:%Y-%m-%d} val={v}!=prev={pv}')
    else:
        log(tc, 'BEHAV_NEGATIVE(changed)', 'INFO', 'PENDING', 'no natural changed row - seeding deferred')

def test_composition_grain(cur, r):
    tc, view, col = r['tc'], r['view'], r['col']
    cur.execute(f"""SELECT MAX(c) FROM (SELECT COUNT(*) c FROM {view} GROUP BY OBJECT_ID, DAYTIME)""")
    maxrows = cur.fetchone()[0]
    log(tc, 'GRAIN_per_obj_day', 'KNOWN_DEFECT', 'KNOWN_DEFECT',
        f'{maxrows} rows/object/day (expected 1 for frozen fn) -> SUMs across components')
    log(tc, 'COMPOSITION_FROZEN', 'KNOWN_DEFECT', 'KNOWN_DEFECT',
        'function cannot do per-component frozen (grain mismatch) - escalate to Grant')

# ---- script integrity ---------------------------------------------------------
def plsql(path):
    return Path(path).read_text(encoding='utf-8').split('\n/', 1)[0].strip()

NAMES = [r['name'] for r in RULES]
def count_rules(cur):
    ph = ','.join(f':n{i}' for i in range(len(NAMES)))
    cur.execute(f"SELECT COUNT(*) FROM TV_CTRL_CHECK_RULES WHERE CHECK_NAME IN ({ph})",
                {f'n{i}': n for i, n in enumerate(NAMES)})
    return cur.fetchone()[0]

def test_idempotency(cur, conn):
    before = count_rules(cur)
    log('IDEM', 'COUNT_BEFORE', 6, before, f'rules={before}')
    cur.execute(plsql(SQLDIR/'Issue1052_PHD_Frozen_Checks.sql')); conn.commit()
    cur.execute(plsql(SQLDIR/'Issue1052_PHD_Frozen_Check_Group.sql')); conn.commit()
    after = count_rules(cur)
    log('IDEM', 'COUNT_AFTER_RERUN', before, after, f'rules={after} (no dupes)')

def test_rollback(cur, conn):
    cur.execute(plsql(SQLDIR/'Issue1052_PHD_Frozen_Check_Group_ROLLBACK.sql')); conn.commit()
    cur.execute(plsql(SQLDIR/'Issue1052_PHD_Frozen_Checks_ROLLBACK.sql')); conn.commit()
    gone = count_rules(cur)
    log('RBK', 'RULES_DELETED', 0, gone, f'remaining={gone}')
    # restore
    cur.execute(plsql(SQLDIR/'Issue1052_PHD_Frozen_Checks.sql')); conn.commit()
    cur.execute(plsql(SQLDIR/'Issue1052_PHD_Frozen_Check_Group.sql')); conn.commit()
    back = count_rules(cur)
    log('RBK', 'RULES_RESTORED', 6, back, f'restored={back}')

# ---- main ---------------------------------------------------------------------
if __name__ == '__main__':
    print('='*70); print('Issue_1052 FROZEN Check Rules - Layer-1 Unit Test'); print('='*70)
    conn = connect(); cur = conn.cursor()
    for r in RULES:
        print(f"\n--- {r['tc']} {r['name']} ---")
        cid = test_wiring(cur, r)
        if cid is None: continue
        if r['kind'] == COMP:
            test_composition_grain(cur, r)
        else:
            test_behaviour(cur, r)
    print("\n--- script integrity ---")
    test_idempotency(cur, conn)
    test_rollback(cur, conn)
    cur.close(); conn.close()

    # summary
    from collections import Counter
    c = Counter(x['status'] for x in LOG)
    print('\n'+'='*70)
    print(f"SUMMARY  PASS={c['PASS']} FAIL={c['FAIL']} INFO/PENDING={c['PENDING']+c['INFO']} "
          f"KNOWN_DEFECT={c['KNOWN_DEFECT']}  total={len(LOG)}")
    print('='*70)
    with open(RESULTS, 'w', encoding='utf-8') as f:
        f.write(f"Issue_1052 FROZEN Unit Test  |  {datetime.now()}  |  COPS DEV\n"+'='*90+'\n')
        for x in LOG:
            f.write(f"[{x['status']:12}] {x['tc']:6} | {x['scenario']:30} | {x['detail']}\n")
        f.write('='*90+f"\nPASS={c['PASS']} FAIL={c['FAIL']} PENDING={c['PENDING']+c['INFO']} "
                f"KNOWN_DEFECT={c['KNOWN_DEFECT']} total={len(LOG)}\n")
    print(f"results -> {RESULTS}")
