"""Find the physical table/view behind the gas-stream-measured data class (READ-ONLY)."""
import oracledb
c = oracledb.connect(user="ECKERNEL_EC", password="energy", dsn="localhost:1521/ORCL", tcp_connect_timeout=15).cursor()

def search(label, like_list):
    print(f"\n=== {label} ===")
    for owner_tab, kind in (("all_tables","TABLE"),("all_views","VIEW")):
        col = "table_name" if kind=="TABLE" else "view_name"
        conds = " OR ".join([f"{col} LIKE '{p}'" for p in like_list])
        c.execute(f"SELECT {col} FROM {owner_tab} WHERE owner='ECKERNEL_EC' AND ({conds}) ORDER BY {col}")
        rows=[r[0] for r in c.fetchall()]
        if rows: print(f"  [{kind}] {rows}")

search("stream-measured / stream-day candidates",
       ["%STRM%STREAM%","STRM_DAY%","%STREAM_MEAS%","%STREAM_DER%","STRM%MEAS%","STRM%GAS%"])
# also: EC often stores the data-class -> table mapping in a metadata table
print("\n=== does STRM_DAY_STREAM exist? + its cols if so ===")
c.execute("""SELECT table_name FROM all_tables WHERE owner='ECKERNEL_EC' AND table_name LIKE 'STRM_DAY%' ORDER BY table_name""")
print("  STRM_DAY* tables:", [r[0] for r in c.fetchall()])
