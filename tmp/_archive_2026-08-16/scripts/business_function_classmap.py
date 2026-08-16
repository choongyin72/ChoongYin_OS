"""Deep-dive part 3: derive the managed class from the BF URL's last segment (not PROFILE_CLASS_NAME),
join to class_cnfg -> the real OV/TV IUD universe. ASCII-only console (R18). READ-ONLY."""
import os, oracledb
cur = oracledb.connect(user="ECKERNEL_EC", password=os.environ.get("EC_DB_PWD", "energy"),
                       dsn=os.environ.get("EC_DB_DSN", "localhost:1521/ORCL"), tcp_connect_timeout=15).cursor()


def q(sql):
    cur.execute(sql); return cur.fetchall()


print("=== what does PROFILE_CLASS_NAME actually hold? (top non-null) ===")
for r in q("""SELECT NVL(profile_class_name,'(null)'), COUNT(*) FROM ECKERNEL_EC.BUSINESS_FUNCTION
              GROUP BY profile_class_name ORDER BY 2 DESC FETCH FIRST 8 ROWS ONLY"""):
    print(f"   {str(r[0]):28s} {r[1]}")

# class = last '/'-segment of the URL
URLCLASS = "REGEXP_SUBSTR(bf.url, '[^/]+$')"

print("\n=== manage_object* BFs: managed class (from URL) JOIN class_cnfg -> CLASS_TYPE / TIME_SCOPE ===")
for r in q(f"""SELECT c.class_type, c.time_scope_code, COUNT(*) n
               FROM ECKERNEL_EC.BUSINESS_FUNCTION bf
               JOIN ECKERNEL_EC.CLASS_CNFG c ON c.class_name = {URLCLASS}
               WHERE bf.url LIKE '%manage_object%'
               GROUP BY c.class_type, c.time_scope_code ORDER BY 3 DESC"""):
    print(f"   class_type={str(r[0]):8s} time_scope={str(r[1]):10s} -> {r[2]}")

print("\n=== distinct managed classes behind manage_object* screens ===")
print("  ", q(f"""SELECT COUNT(DISTINCT {URLCLASS}) FROM ECKERNEL_EC.BUSINESS_FUNCTION bf
                  WHERE bf.url LIKE '%manage_object%'""")[0][0])

print("\n=== sample: BF -> managed class -> type (manage_object_nav) ===")
for r in q(f"""SELECT bf.bf_code, bf.name, {URLCLASS} cls, c.class_type
               FROM ECKERNEL_EC.BUSINESS_FUNCTION bf
               JOIN ECKERNEL_EC.CLASS_CNFG c ON c.class_name = {URLCLASS}
               WHERE bf.url LIKE '%manage_object_nav%'
               ORDER BY bf.bf_code FETCH FIRST 12 ROWS ONLY"""):
    print("    ", tuple(str(x)[:24] for x in r))
cur.close()
print("\nDONE")
