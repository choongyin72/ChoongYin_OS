"""ECPR-31011 — deep diff of DV_PWEL_DAY_STATUS vs DV_PWEL_DAY_STATUS_2 (read-only).

For every column in either view:
  - presence in each view, data type
  - source expression extracted from the generated view SQL
  - source classification: BASE column / ZWP_T extension / FUNCTION-computed / literal

Outputs (same folder):
  dv_view_diff.csv          full machine-readable table
  DV_VIEW_DIFF.md           full markdown table grouped: SHARED / ONLY-1 / ONLY-2
  view_DV_PWEL_DAY_STATUS.sql / view_DV_PWEL_DAY_STATUS_2.sql  raw view text
"""
import csv
import os
import re
import oracledb

HERE = os.path.dirname(os.path.abspath(__file__))
V1, V2 = 'DV_PWEL_DAY_STATUS', 'DV_PWEL_DAY_STATUS_2'

conn = oracledb.connect(user='ECKERNEL_EC', password='energy',
    dsn=oracledb.makedsn('db.plutodev.woodside-pluto.tieto-og.cloud', 1521,
                         service_name='plutodev'),
    tcp_connect_timeout=25)
cur = conn.cursor()

def cols_of(view):
    cur.execute("""
        SELECT column_name, data_type, data_length, data_precision, data_scale
        FROM all_tab_columns
        WHERE owner = 'ECKERNEL_EC' AND table_name = :t ORDER BY column_id""",
        {'t': view})
    out = {}
    for name, dtype, dlen, prec, scale in cur.fetchall():
        if dtype == 'NUMBER':
            t = 'NUMBER' if prec is None else f'NUMBER({prec},{scale or 0})'
        elif 'CHAR' in dtype:
            t = f'{dtype}({dlen})'
        else:
            t = dtype
        out[name] = t
    return out

def text_of(view):
    cur.execute("""SELECT text FROM all_views
                   WHERE owner = 'ECKERNEL_EC' AND view_name = :v""", {'v': view})
    row = cur.fetchone()
    txt = row[0] if row else ''
    if hasattr(txt, 'read'):
        txt = txt.read()
    return txt or ''

def select_items(view_sql):
    """Split the top-level SELECT list into (expression, alias) pairs."""
    s = view_sql
    m = re.search(r'\bselect\b', s, re.I)
    if not m:
        return {}
    i = m.end()
    depth = 0
    items, buf = [], []
    while i < len(s):
        ch = s[i]
        if ch == '(':
            depth += 1
        elif ch == ')':
            depth -= 1
        if depth == 0:
            if ch == ',':
                items.append(''.join(buf)); buf = []; i += 1; continue
            if re.match(r'\bfrom\b', s[i:i+5], re.I) and (not buf or s[i-1] in ' \n\t)'):
                items.append(''.join(buf)); break
        buf.append(ch)
        i += 1
    out = {}
    for it in items:
        it = it.strip()
        if not it:
            continue
        # alias = last identifier; expression = the rest
        m2 = re.search(r'(?:\bas\s+)?("?)([A-Z0-9_#$]+)\1\s*$', it, re.I)
        if not m2:
            continue
        alias = m2.group(2).upper()
        expr = it[:m2.start()].strip().rstrip()
        if not expr:               # plain column with no alias
            expr = alias
        out[alias] = ' '.join(expr.split())
    return out

def classify(expr, base_cols, ext_cols):
    e = expr.upper()
    bare = e.split('.')[-1].strip('"')
    if 'ZWP_T_PWEL_DAY_STATUS' in e or bare in ext_cols and 'ZWP_T' in e:
        return 'EXT (ZWP_T)'
    if '(' in e:
        return 'FUNCTION'
    if bare in base_cols:
        return 'BASE'
    if bare in ext_cols:
        return 'EXT (ZWP_T)'
    if e.startswith("'") or e.replace('.', '').isdigit() or e == 'NULL':
        return 'LITERAL'
    return 'OTHER'

c1, c2 = cols_of(V1), cols_of(V2)
t1, t2 = text_of(V1), text_of(V2)
e1, e2 = select_items(t1), select_items(t2)

cur.execute("""SELECT column_name FROM all_tab_columns
               WHERE owner='ECKERNEL_EC' AND table_name='PWEL_DAY_STATUS'""")
base_cols = {r[0] for r in cur.fetchall()}
cur.execute("""SELECT column_name FROM all_tab_columns
               WHERE owner='ECKERNEL_EC' AND table_name='ZWP_T_PWEL_DAY_STATUS'""")
ext_cols = {r[0] for r in cur.fetchall()}

for view, txt in ((V1, t1), (V2, t2)):
    with open(os.path.join(HERE, f'view_{view}.sql'), 'w', encoding='utf-8') as f:
        f.write(txt)

all_cols = sorted(set(c1) | set(c2))
rows = []
for col in all_cols:
    in1, in2 = col in c1, col in c2
    grp = 'SHARED' if in1 and in2 else ('ONLY DV_1' if in1 else 'ONLY DV_2')
    sub = []
    for inx, ex, cx in ((in1, e1, c1), (in2, e2, c2)):
        if inx:
            expr = ex.get(col, '?')
            sub.append((cx[col], expr))
        else:
            sub.append(('', ''))
    (t1c, x1), (t2c, x2) = sub
    src1 = classify(x1, base_cols, ext_cols) if in1 and x1 else ''
    src2 = classify(x2, base_cols, ext_cols) if in2 and x2 else ''
    rows.append({'column': col, 'group': grp,
                 'in_DV_1': 'Y' if in1 else '', 'in_DV_2': 'Y' if in2 else '',
                 'type_DV_1': t1c, 'type_DV_2': t2c,
                 'source_DV_1': src1, 'source_DV_2': src2,
                 'expr_DV_1': x1, 'expr_DV_2': x2})

with open(os.path.join(HERE, 'dv_view_diff.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader()
    w.writerows(rows)

def md_table(subset, show_both_exprs):
    lines = ['| # | Column | Type | Source | Expression |',
             '|---|--------|------|--------|------------|']
    for i, r in enumerate(subset, 1):
        if r['group'] == 'ONLY DV_2':
            t, s, x = r['type_DV_2'], r['source_DV_2'], r['expr_DV_2']
        else:
            t, s, x = r['type_DV_1'], r['source_DV_1'], r['expr_DV_1']
        x = (x[:90] + '…') if len(x) > 90 else x
        note = ''
        if show_both_exprs and r['group'] == 'SHARED' and r['expr_DV_1'] != r['expr_DV_2']:
            note = f'  ⚠ DV_2 differs: `{r["expr_DV_2"][:70]}`'
        lines.append(f'| {i} | {r["column"]} | {t} | {s} | `{x}`{note} |')
    return '\n'.join(lines)

shared = [r for r in rows if r['group'] == 'SHARED']
only1 = [r for r in rows if r['group'] == 'ONLY DV_1']
only2 = [r for r in rows if r['group'] == 'ONLY DV_2']
diff_shared = [r for r in shared if r['expr_DV_1'] != r['expr_DV_2']]

with open(os.path.join(HERE, 'DV_VIEW_DIFF.md'), 'w', encoding='utf-8') as f:
    f.write(f"""# DV_PWEL_DAY_STATUS vs DV_PWEL_DAY_STATUS_2 — full attribute diff
Generated read-only from plutodev on 2026-06-10 (script: dv_view_diff.py).

Totals: DV_1 = {len(c1)} cols | DV_2 = {len(c2)} cols | shared = {len(shared)} |
only DV_1 = {len(only1)} | only DV_2 = {len(only2)} |
shared-but-different-expression = {len(diff_shared)}

## 1. ONLY in DV_PWEL_DAY_STATUS_2 (must be added to class 1) — {len(only2)}

{md_table(only2, False)}

## 2. ONLY in DV_PWEL_DAY_STATUS — {len(only1)}

{md_table(only1, False)}

## 3. SHARED but DIFFERENT source expression — {len(diff_shared)}

{md_table(diff_shared, True)}

## 4. SHARED, identical — {len(shared) - len(diff_shared)}

{md_table([r for r in shared if r['expr_DV_1'] == r['expr_DV_2']], False)}
""")

print(f'DV_1={len(c1)} DV_2={len(c2)} shared={len(shared)} only1={len(only1)} '
      f'only2={len(only2)} shared_diff_expr={len(diff_shared)}')
print('files written: dv_view_diff.csv, DV_VIEW_DIFF.md, view_*.sql')

cur.close()
conn.close()
