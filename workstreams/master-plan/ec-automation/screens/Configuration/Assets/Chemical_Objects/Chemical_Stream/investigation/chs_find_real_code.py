import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parents[5] / "libraries"))
import DbVerify as db

conn = db._connect()
cur = conn.cursor()
cur.execute("SELECT CODE, NAME FROM OV_CHEM_STREAM WHERE ROWNUM <= 10")
for row in cur.fetchall():
    print(row)
cur.close()
conn.close()
