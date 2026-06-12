"""Find the OV_* view names + a CODE-like column for the Dispatching Objects screens."""
import os

import oracledb

dsn = os.environ.get("EC_DB_DSN", "localhost:1521/ORCL")
user = os.environ.get("EC_DB_USER", "ECKERNEL_EC")
pw = os.environ.get("EC_DB_PASS", "energy")

conn = oracledb.connect(user=user, password=pw, dsn=dsn)
cur = conn.cursor()

PATTERNS = ["%DELIVERY_POINT%", "%DELIVERY_STREAM%", "%METER%", "%NOMINATION%",
            "%PIPELINE%", "%TRANSPORT_SYSTEM%", "%TRANSPORT_ZONE%", "%NOM_CYCLE%", "%CYCLE%"]
for p in PATTERNS:
    cur.execute("""SELECT object_name, object_type FROM all_objects
                   WHERE owner = 'ECKERNEL_EC' AND object_type IN ('VIEW','TABLE')
                   AND (object_name LIKE 'OV_' || :p OR object_name LIKE :p2)
                   ORDER BY object_type, object_name""",
                p=p.strip("%"), p2=p)
    rows = [r for r in cur.fetchall() if not r[0].endswith("_JN")]
    print(f"{p}:")
    for name, typ in rows[:10]:
        print(f"   {typ:5s} {name}")

# code columns of the likely OV views
for v in ["OV_DELIVERY_POINT", "OV_DELIVERY_STREAM", "OV_METER", "OV_NOMINATION_POINT",
          "OV_PIPELINE", "OV_PIPELINE_SEGMENT", "OV_TRANSPORT_SYSTEM", "OV_TRANSPORT_ZONE"]:
    cur.execute("""SELECT column_name FROM all_tab_columns
                   WHERE owner='ECKERNEL_EC' AND table_name=:t
                   AND (column_name LIKE '%CODE%' OR column_name='NAME') ORDER BY column_id""", t=v)
    cols = [r[0] for r in cur.fetchall()]
    print(f"{v}: {cols[:6] if cols else 'NOT FOUND'}")
conn.close()
