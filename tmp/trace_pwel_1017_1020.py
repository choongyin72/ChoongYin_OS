# READ-ONLY: audit + formula of the 4 PWEL rules on ec14151, to compare vs OUR forward SQL.
import oracledb
DSN="db.ec14151.woodside-pluto.tieto-og.cloud:1521/ec14151"
c=oracledb.connect(user="ECKERNEL_EC",password="energy",dsn=DSN); cur=c.cursor()
def lob(v):
    try:
        import oracledb as o
        if isinstance(v,o.LOB): return v.read()
    except Exception: pass
    return v
cur.execute("""select check_id, check_name,
   to_char(created_date,'YYYY-MM-DD HH24:MI:SS') created,
   last_updated_by, to_char(last_updated_date,'YYYY-MM-DD HH24:MI:SS') updated,
   rev_no, rev_text, where_formula
   from ctrl_check_rules where check_id in (1017,1018,1019,1020) order by check_id""")
print("=== 1017-1020 audit + formula ===")
for r in cur.fetchall():
    print(f"[{r[0]}] {r[1]}")
    print(f"     created={r[2]}  last_updated_by={r[3]} updated={r[4]}  rev_no={r[5]}  rev_text={r[6]}")
    print(f"     where_formula: {lob(r[7])}")
# the OnStrmHrs variable these rules use (our script sets it ATTRIBUTE ON_STREAM_HRS_HRS)
cur.execute("""select check_id, variable_name, variable_type, variable_value,
   to_char(last_updated_date,'YYYY-MM-DD HH24:MI') upd, rev_text
   from tv_ctrl_check_rule_variable where check_id in (1017,1018,1019,1020) order by check_id, variable_name""")
print("\n=== their variables ===")
for r in cur.fetchall(): print("   ", " | ".join(str(x) for x in r))
c.close()
