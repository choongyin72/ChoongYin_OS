"""READ-ONLY round 2: actual IMP_* schema on COPSDEV + full dump of the
existing interfaces and ONE complete worked example (interface -> source
mappings -> source paths -> target mappings)."""
import oracledb

conn = oracledb.connect(user="ECKERNEL_EC", password="energy",
                        dsn="db.plutodev.woodside-pluto.tieto-og.cloud:1521/plutodev",
                        tcp_connect_timeout=20)
cur = conn.cursor()


def cols(t):
    cur.execute("SELECT column_name FROM all_tab_columns WHERE table_name=:t ORDER BY column_id", t=t)
    return [r[0] for r in cur.fetchall()]


print("IMP_SOURCE_INTERFACE cols:", cols("IMP_SOURCE_INTERFACE")[:18])
print("IMP_SOURCE_MAPPING cols  :", cols("IMP_SOURCE_MAPPING")[:18])
print("IMP_SOURCE_PATH cols     :", cols("IMP_SOURCE_PATH")[:12])
print("IMP_TARGET_MAPPING cols  :", cols("IMP_TARGET_MAPPING")[:14])

print("\n=== ALL interfaces ===")
cur.execute("SELECT * FROM IMP_SOURCE_INTERFACE")
ic = [d[0] for d in cur.description]
rows = cur.fetchall()
for r in rows:
    d = dict(zip(ic, r))
    print(" ", {k: d.get(k) for k in ic[:12] if d.get(k) is not None})

print("\n=== source mappings per interface ===")
cur.execute("SELECT OBJECT_ID, COUNT(*) FROM IMP_SOURCE_MAPPING GROUP BY OBJECT_ID" if "OBJECT_ID" in cols("IMP_SOURCE_MAPPING") else "SELECT CODE, COUNT(*) FROM IMP_SOURCE_MAPPING GROUP BY CODE")
for r in cur.fetchall()[:15]:
    print(" ", r)

cur.close()
conn.close()
print("done (READ-ONLY)")
