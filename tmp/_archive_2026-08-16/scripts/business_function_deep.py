"""Deep-dive part 2: BUSINESS_FUNCTION profiled correctly + joined to class_cnfg => the coverage-ledger view.
READ-ONLY."""
import os, oracledb
cur = oracledb.connect(user="ECKERNEL_EC", password=os.environ.get("EC_DB_PWD", "energy"),
                       dsn=os.environ.get("EC_DB_DSN", "localhost:1521/ORCL"), tcp_connect_timeout=15).cursor()


def q(sql):
    cur.execute(sql); return cur.fetchall()


print("=== APP_SPACE_CNTX distribution (corrected) ===")
for r in q("SELECT NVL(APP_SPACE_CNTX,'(null)'), COUNT(*) FROM ECKERNEL_EC.BUSINESS_FUNCTION GROUP BY APP_SPACE_CNTX ORDER BY 2 DESC"):
    print(f"   {str(r[0]):16s} {r[1]}")

print("\n=== DEPRECATED_IND ===")
for r in q("SELECT NVL(DEPRECATED_IND,'(null)'), COUNT(*) FROM ECKERNEL_EC.BUSINESS_FUNCTION GROUP BY DEPRECATED_IND ORDER BY 2 DESC"):
    print(f"   {str(r[0]):8s} {r[1]}")

print("\n=== BF_CODE module prefixes (top 15) ===")
for r in q("""SELECT SUBSTR(BF_CODE,1,2) pfx, COUNT(*) FROM ECKERNEL_EC.BUSINESS_FUNCTION
              GROUP BY SUBSTR(BF_CODE,1,2) ORDER BY 2 DESC FETCH FIRST 15 ROWS ONLY"""):
    print(f"   {str(r[0]):4s} {r[1]}")

print("\n=== standard manage_object* BFs ⋈ class_cnfg → CLASS_TYPE / TIME_SCOPE (the IUD universe) ===")
for r in q("""SELECT c.class_type, c.time_scope_code, COUNT(*) bf
              FROM ECKERNEL_EC.BUSINESS_FUNCTION bf
              JOIN ECKERNEL_EC.CLASS_CNFG c ON c.class_name = bf.profile_class_name
              WHERE bf.url LIKE '%manage_object%' AND NVL(bf.deprecated_ind,'N') <> 'Y'
              GROUP BY c.class_type, c.time_scope_code ORDER BY 3 DESC"""):
    print(f"   class_type={str(r[0]):8s} time_scope={str(r[1]):10s} -> {r[2]} BFs")

print("\n=== how many DISTINCT classes are IUD-screen-backed (manage_object*, not deprecated) ===")
n = q("""SELECT COUNT(DISTINCT bf.profile_class_name) FROM ECKERNEL_EC.BUSINESS_FUNCTION bf
         WHERE bf.url LIKE '%manage_object%' AND bf.profile_class_name IS NOT NULL
           AND NVL(bf.deprecated_ind,'N') <> 'Y'""")[0][0]
print("  distinct IUD-backed classes:", n)

print("\n=== sample manage_object BFs (code | name | class | type) ===")
for r in q("""SELECT bf.bf_code, bf.name, bf.profile_class_name, c.class_type
              FROM ECKERNEL_EC.BUSINESS_FUNCTION bf
              JOIN ECKERNEL_EC.CLASS_CNFG c ON c.class_name=bf.profile_class_name
              WHERE bf.url LIKE '%manage_object_nav%' AND NVL(bf.deprecated_ind,'N')<>'Y'
              ORDER BY bf.bf_code FETCH FIRST 10 ROWS ONLY"""):
    print("    ", tuple(str(x)[:26] for x in r))
cur.close()
print("\nDONE")
