# READ-ONLY: WHERE_FORMULA of 1147-1150 + Flyway history around 2026-07-21. SELECT only.
import oracledb
DSN="db.ec14151.woodside-pluto.tieto-og.cloud:1521/ec14151"
c=oracledb.connect(user="ECKERNEL_EC",password="energy",dsn=DSN); cur=c.cursor()

# 1) what the 4 new rules actually check
cur.execute("""select check_id, check_name, class_name, select_clause, where_formula, severity_level, check_message
   from ctrl_check_rules where check_id in (1147,1148,1149,1150) order by check_id""")
print("=== 1147-1150 definitions ===")
for r in cur.fetchall():
    print(f"[{r[0]}] {r[1]} | class={r[2]} | sev={r[5]}")
    print(f"     formula: {r[4]}")
    print(f"     msg: {r[6]}")

# 2) Flyway history around 2026-07-21 (try both table names)
for tbl in ("flyway_schema_history","schema_version"):
    try:
        cur.execute(f"""select version, description, script, installed_by,
            to_char(installed_on,'YYYY-MM-DD HH24:MI') ins, success
            from {tbl} where installed_on between date '2026-07-20' and date '2026-07-23'
            order by installed_on""")
        rows=cur.fetchall()
        print(f"\n=== {tbl} 2026-07-20..23 : {len(rows)} ===")
        for r in rows: print("   ", " | ".join(str(x) for x in r))
    except Exception as e:
        print(f"\n{tbl}: {str(e)[:70]}")
c.close()
