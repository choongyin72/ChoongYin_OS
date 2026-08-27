"""Self-clean check: confirm 0 residual AUTOTEST% rows in OV_CHEM_STREAM.

Run before/after a live suite run to prove the fixed test code AUTOTEST_CHS
is free (TC05 Delete leaves it free for the next run).
"""
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parents[5] / "libraries"))
import DbVerify as db

conn = db._connect()
cur = conn.cursor()
cur.execute("SELECT CODE FROM OV_CHEM_STREAM WHERE CODE LIKE 'AUTOTEST%'")
rows = cur.fetchall()
print("AUTOTEST residual rows:", rows)
cur.close()
conn.close()
