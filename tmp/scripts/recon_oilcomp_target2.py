"""RECON: is there a NAVIGABLE oil-comp target with adequate multi-component WT_PCT data? Join
STRM_OIL_COMP analyses to OV_STREAM (real stream NAME = the G:5 dropdown label) and rank by component
count + wt% population. Also list each candidate's facility scope + date. Read-only."""
import os
import oracledb

conn = oracledb.connect(user="ECKERNEL_EC", password=os.environ.get("EC_DB_PWD", "energy"),
                        dsn=os.environ.get("EC_DB_DSN", "localhost:1521/ORCL"), tcp_connect_timeout=15)
cur = conn.cursor()


def q(sql, *a):
    cur.execute(sql, a); return cur.fetchall()


print("=== STRM_OIL_COMP analyses joined to OV_STREAM (NAME = dropdown label) ===")
for r in q("""SELECT a.OBJECT_CODE, s.NAME stream_name, TRUNC(a.DAYTIME) D, MAX(a.RECORD_STATUS) st,
                     MAX(a.SAMPLING_METHOD) samp, COUNT(*) ncomp, COUNT(a.WT_PCT) nwt, COUNT(a.MOL_PCT) nmol
              FROM ECKERNEL_EC.DV_STRM_COMP_ANALYSIS a
              LEFT JOIN ECKERNEL_EC.OV_STREAM s ON s.OBJECT_ID = a.OBJECT_ID
              WHERE a.ANALYSIS_TYPE='STRM_OIL_COMP'
              GROUP BY a.OBJECT_CODE, s.NAME, TRUNC(a.DAYTIME)
              ORDER BY COUNT(a.WT_PCT) DESC, ncomp DESC FETCH FIRST 25 ROWS ONLY"""):
    print("  ", r)

print("\n=== For the navigable streams seen in G:5 (S008/S0156/S0157/S093), any oil comp on ANY date? ===")
for nm in ("P1 S008 M OIL PO.0001", "P1 S0156 OIL PO.0001", "P1 S0157 OIL PO.0001", "P1 S093 M OIL PO.0095"):
    rows = q("""SELECT TRUNC(a.DAYTIME) D, COUNT(*) ncomp, COUNT(a.WT_PCT) nwt
                FROM ECKERNEL_EC.DV_STRM_COMP_ANALYSIS a JOIN ECKERNEL_EC.OV_STREAM s ON s.OBJECT_ID=a.OBJECT_ID
                WHERE a.ANALYSIS_TYPE='STRM_OIL_COMP' AND s.NAME=:n
                GROUP BY TRUNC(a.DAYTIME) ORDER BY 1""", nm)
    print(f"  {nm}: {rows}")

print("\n=== ALSO: is the rich 12-comp 'P1 Alloc S001 M OIL' a navigable OV_STREAM? facility scope? ===")
for r in q("""SELECT s.NAME, s.CODE, fc.NAME facility FROM ECKERNEL_EC.OV_STREAM s
              LEFT JOIN ECKERNEL_EC.OV_FACILITY_CLASS_1 fc ON 1=0
              WHERE s.NAME LIKE '%Alloc S001%OIL%' OR s.CODE LIKE '%ALLOC S001 OIL%' FETCH FIRST 5 ROWS ONLY"""):
    print("  ", r)
cur.close(); conn.close()
print("\nDONE")
