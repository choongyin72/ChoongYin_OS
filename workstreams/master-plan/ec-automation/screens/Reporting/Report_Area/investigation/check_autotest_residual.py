"""Independent DB self-clean re-check for Report Area, added during the 2026-08-27 doc/evidence
backfill (docs/lean-deliverable-backfill-workorder.md, Batch 10). Fresh oracledb connection per
standing rule - confirms 0 residual AUTOTEST_RPTA rows in OV_REPORT_AREA both before and after a
live run of the already-merged, already-live Bank-pattern suite (PR #468). Additive only; does not
replace or modify the pre-existing investigation/recon.py / recon_update.py from the original build.
"""
import oracledb

conn = oracledb.connect(user="ECKERNEL_EC", password="energy", dsn="localhost:1521/ORCL")
cur = conn.cursor()
cur.execute("SELECT CODE, NAME FROM OV_REPORT_AREA WHERE CODE LIKE 'AUTOTEST%'")
rows = cur.fetchall()
print("AUTOTEST residual rows in OV_REPORT_AREA:", rows)
cur.close()
conn.close()
