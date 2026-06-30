"""Verify B2 Part 2 persisted: find the class-key mapping table and count its rows for AUTOTEST_rCO2Rate.
Lists candidate CALC_VAR_* tables, then for each with a CALC_VAR_SIGNATURE column, counts rows for the var."""
import os, oracledb
def rd(v):
    try: return v.read() if hasattr(v,'read') else v
    except: return v
c=oracledb.connect(user=os.environ.get('EC_DB_USER','ECKERNEL_EC'),password=os.environ.get('EC_DB_PASS','energy'),dsn=os.environ.get('EC_DB_DSN','localhost:1521/ORCL'))
cur=c.cursor()
cur.execute("select calc_var_signature from calc_variable where name='AUTOTEST_rCO2Rate'")
row=cur.fetchone(); sig=row[0] if row else None
print("AUTOTEST_rCO2Rate signature:", sig)
if not sig:
    print("variable not found"); c.close(); raise SystemExit(0)
cur.execute("""select table_name from all_tables where owner='ECKERNEL_EC' and table_name like 'CALC_VAR%' order by table_name""")
tabs=[r[0] for r in cur.fetchall()]
print("CALC_VAR* tables:", tabs)
for t in tabs:
    cur.execute("select column_name from all_tab_columns where owner='ECKERNEL_EC' and table_name=:1 and column_name='CALC_VAR_SIGNATURE'",[t])
    if cur.fetchone():
        cur.execute(f"select count(*) from {t} where calc_var_signature=:1",[sig])
        n=cur.fetchone()[0]
        if n>0: print("   %-32s rows for var = %d" % (t, n))
# specifically dump the class-key/attr read mapping rows if a likely table exists
for t in tabs:
    if 'READ' in t and ('KEY' in t or 'ATTR' in t or 'DIM' in t):
        try:
            cur.execute(f"select * from {t} where calc_var_signature=:1",[sig])
            cols=[d[0] for d in cur.description]; rows=cur.fetchall()
            print("\n%s (%d rows):" % (t, len(rows)))
            for r in rows:
                d={cols[i]:rd(r[i]) for i in range(len(cols)) if rd(r[i]) is not None}
                # show the meaningful key/dimension columns only
                show={k:v for k,v in d.items() if any(x in k for x in ['KEY','ATTR','DIM','MAP','SYNTAX','CLS','TYPE','SEQ','VALUE'])}
                print("   ", show)
        except Exception as e: print("   (skip %s: %s)" % (t, str(e)[:50]))
c.close()
print("\nDONE verify_part2")
