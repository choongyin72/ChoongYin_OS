"""Deep-dive: find + profile the table behind the EC 'Business Function' screen
(/com.ec.frmw.co.screens/business_function). Columns / count / app-space distribution / URL-pattern
breakdown (manage_object_nav=OV, manage_object_groupmodel_nav=OV-GM, custom). READ-ONLY."""
import os, oracledb
cur = oracledb.connect(user="ECKERNEL_EC", password=os.environ.get("EC_DB_PWD", "energy"),
                       dsn=os.environ.get("EC_DB_DSN", "localhost:1521/ORCL"), tcp_connect_timeout=15).cursor()


def q(sql, *a):
    try:
        cur.execute(sql, a); return cur.fetchall()
    except Exception as e:
        return [("ERR", str(e)[:80])]


print("=== candidate tables (BUSINESS_FUNCTION / BUS_FUNC / BF_*) ===")
for r in q("""SELECT table_name FROM all_tables WHERE owner='ECKERNEL_EC'
              AND (table_name LIKE '%BUSINESS_FUNC%' OR table_name LIKE '%BUS_FUNC%'
                   OR table_name LIKE 'BF\\_%' ESCAPE '\\' OR table_name LIKE '%BUSINESS_FUNCTION%')
              AND table_name NOT LIKE '%JN' ORDER BY 1 FETCH FIRST 25 ROWS ONLY"""):
    print("  ", r[0])

# profile the most likely table
for t in ("BUSINESS_FUNCTION", "BUS_FUNCTION", "BUSINESS_FUNC", "EC_BUSINESS_FUNCTION"):
    cols = q("SELECT column_name FROM all_tab_columns WHERE owner='ECKERNEL_EC' AND table_name=:t ORDER BY column_id", t)
    if cols and cols[0][0] != "ERR":
        print(f"\n=== {t} columns ({len(cols)}) ===\n  ", ", ".join(c[0] for c in cols))
        n = q(f"SELECT COUNT(*) FROM ECKERNEL_EC.{t}")[0][0]
        print("  total rows:", n)
        # find code/name/appspace/url-ish columns
        cnames = [c[0] for c in cols]
        appcol = next((c for c in cnames if "SPACE" in c or "CNTX" in c or "APP" in c), None)
        urlcol = next((c for c in cnames if "URL" in c), None)
        codecol = next((c for c in cnames if c in ("BF_CODE", "CODE", "BUSINESS_FUNCTION_CODE")), cnames[0])
        if appcol:
            print(f"\n  app-space distribution ({appcol}):")
            for r in q(f"SELECT {appcol}, COUNT(*) FROM ECKERNEL_EC.{t} GROUP BY {appcol} ORDER BY 2 DESC"):
                print(f"     {str(r[0]):16s} {r[1]}")
        if urlcol:
            print(f"\n  URL-pattern breakdown ({urlcol}):")
            for r in q(f"""SELECT CASE
                    WHEN {urlcol} LIKE '%manage_object_groupmodel_nav%' THEN 'OV-GM (groupmodel)'
                    WHEN {urlcol} LIKE '%manage_object_nav%' THEN 'OV (manage_object)'
                    WHEN {urlcol} LIKE '%manage_object_object_list%' THEN 'OV (object_list)'
                    ELSE 'custom / other' END AS kind, COUNT(*)
                    FROM ECKERNEL_EC.{t} GROUP BY CASE
                    WHEN {urlcol} LIKE '%manage_object_groupmodel_nav%' THEN 'OV-GM (groupmodel)'
                    WHEN {urlcol} LIKE '%manage_object_nav%' THEN 'OV (manage_object)'
                    WHEN {urlcol} LIKE '%manage_object_object_list%' THEN 'OV (object_list)'
                    ELSE 'custom / other' END ORDER BY 2 DESC"""):
                print(f"     {str(r[0]):22s} {r[1]}")
        print(f"\n  sample rows ({codecol}, name, app, url):")
        sel = [c for c in (codecol, "NAME", appcol, urlcol) if c]
        for r in q(f"SELECT {','.join(sel)} FROM ECKERNEL_EC.{t} FETCH FIRST 6 ROWS ONLY"):
            print("    ", tuple(str(x)[:34] for x in r))
        break
cur.close()
print("\nDONE")
