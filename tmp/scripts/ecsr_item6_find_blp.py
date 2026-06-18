import os
"""ECSR-35331 item 6 - locate where 'Daily BLP Allocation <OBSOLETE>' (a Proxy calc job on the Daily
Allocation screen) is defined, so it can be removed. Read-only. Probes name/desc columns across calc/
proxy/process/jbpm/business-action config tables for 'BLP' / 'OBSOLETE' / 'Mass Balance'. SELECT only."""
import oracledb, sys

con = oracledb.connect(user="ECKERNEL_EC", password=os.environ.get("EC_DB_PWD",""),
                       dsn="dev.db.non-prod.plp.wde.ecaas.cloud:1521/QDB", tcp_connect_timeout=20)
cur = con.cursor()


def q(sql, a=None):
    try:
        cur.execute(sql, a or []); return cur.fetchall()
    except Exception as e:
        return []


pats = ("PROXY", "CALC", "ALLOC", "PROCESS", "JBPM", "BUSINESS", "JOB", "TASK", "ACTION", "DEFIN", "ECPD", "PROC")
where_tbl = " OR ".join(f"table_name LIKE '%{p}%'" for p in pats)
cands = q(f"""SELECT table_name, column_name FROM all_tab_columns
              WHERE owner='ECKERNEL_EC' AND data_type IN ('VARCHAR2','NVARCHAR2','CHAR') AND char_length>=10
                AND table_name NOT LIKE '%\\_JN' ESCAPE '\\'
                AND (column_name LIKE '%NAME%' OR column_name LIKE '%DESC%' OR column_name LIKE '%TITLE%'
                     OR column_name LIKE '%LABEL%')
                AND ({where_tbl})
              ORDER BY table_name, column_name""")
print(f"candidate columns: {len(cands)}", flush=True)

found = False
for t, c in cands:
    hit = q(f"""SELECT DISTINCT {c} FROM {t}
                WHERE UPPER({c}) LIKE '%BLP ALLOCATION%' OR UPPER({c}) LIKE '%OBSOLETE%'
                   OR UPPER({c}) LIKE '%DAILY MASS BALANCE%' OR UPPER({c}) LIKE '%ONSHORE DAILY ALLOCATION%'""")
    if hit:
        found = True
        print(f"\n>>> {t}.{c}", flush=True)
        for h in hit[:25]:
            print("    ", h[0], flush=True)

if not found:
    print("\nNo match in calc/proxy/process tables. Trying ANY name/desc column for 'BLP Allocation'...", flush=True)
    allc = q("""SELECT table_name, column_name FROM all_tab_columns
                WHERE owner='ECKERNEL_EC' AND data_type='VARCHAR2' AND char_length>=15
                  AND table_name NOT LIKE '%\\_JN' ESCAPE '\\'
                  AND (column_name LIKE '%NAME%' OR column_name LIKE '%DESCR%' OR column_name LIKE '%TITLE%')""")
    print(f"  scanning {len(allc)} columns...", flush=True)
    for t, c in allc:
        hit = q(f"SELECT DISTINCT {c} FROM {t} WHERE UPPER({c}) LIKE '%BLP ALLOCATION%' OR UPPER({c}) LIKE '%<OBSOLETE>%'")
        if hit:
            print(f"\n>>> {t}.{c}", flush=True)
            for h in hit[:25]:
                print("    ", h[0], flush=True)

con.close()
print("\nDONE (read-only).", flush=True)
