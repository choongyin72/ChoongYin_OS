"""Find the stream version table that resolves 'AS2_Flare Gas 001' -> OBJECT_ID (READ-ONLY)."""
import oracledb
c = oracledb.connect(user="ECKERNEL_EC", password="energy", dsn="localhost:1521/ORCL", tcp_connect_timeout=15).cursor()
EXPECT = "96D7FD4CB6770217E053020011AC1940"
for tbl in ("STREAM_VERSION", "STREAM", "OV_STREAM"):
    try:
        c.execute(f"SELECT OBJECT_ID FROM ECKERNEL_EC.{tbl} WHERE NAME=:n FETCH FIRST 1 ROWS ONLY", n="AS2_Flare Gas 001")
        r = c.fetchone()
        print(f"{tbl:16} NAME='AS2_Flare Gas 001' -> {r[0] if r else None}  (match={r and r[0]==EXPECT})")
    except Exception as e:
        print(f"{tbl:16} ERR: {str(e)[:70]}")
# also: which tables even have a NAME col + an OBJECT_ID col for streams
c.execute("""SELECT table_name FROM all_tables WHERE owner='ECKERNEL_EC'
   AND table_name LIKE 'STREAM%' ORDER BY table_name""")
print("STREAM* tables:", [r[0] for r in c.fetchall()])
