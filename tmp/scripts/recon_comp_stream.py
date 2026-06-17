"""RECON (read-only): resolve OV_STREAM CODE + NAME for the target gas-comp stream, so Stream Finder
input + the G:5 Stream pick use the right strings. SELECT only."""
import os
import oracledb

conn = oracledb.connect(user="ECKERNEL_EC", password=os.environ.get("EC_DB_PWD", "energy"),
                        dsn=os.environ.get("EC_DB_DSN", "localhost:1521/ORCL"), tcp_connect_timeout=15)
cur = conn.cursor()
for r in cur.execute("""SELECT CODE, NAME FROM ECKERNEL_EC.OV_STREAM
                        WHERE NAME LIKE '%S038_AGA3_1985_AGA8_Y_1%' OR CODE LIKE '%S038_AGA3_1985_AGA8_Y_1%'
                        FETCH FIRST 5 ROWS ONLY""").fetchall():
    print("OV_STREAM:", r)
# OBJECT_CODE in the comp view is what the screen knows it by; show it too
for r in cur.execute("""SELECT DISTINCT OBJECT_CODE, OBJECT_ID FROM ECKERNEL_EC.DV_STRM_COMP_ANALYSIS
                        WHERE OBJECT_CODE LIKE '%S038_AGA3_1985_AGA8_Y_1%'""").fetchall():
    print("comp OBJECT_CODE/ID:", r)
cur.close()
conn.close()
print("DONE")
