"""Get the exact ORA error for end=start, then self-clean AUTOTEST_CP_001 (local sandbox, my data):
try view DELETE (proper IUD-trigger path); if unsupported, end=start+1day (past -> leaves current view)."""
import oracledb, datetime
c = oracledb.connect(user='ECKERNEL_EC', password='energy', dsn='localhost:1521/ORCL')
cur = c.cursor()
def resid():
    cur.execute("select count(*) from ov_chem_product where code like 'AUTOTEST%'"); return cur.fetchone()[0]
# 1) exact error on end=start
try:
    cur.execute("update OV_CHEM_PRODUCT set OBJECT_END_DATE=OBJECT_START_DATE where CODE='AUTOTEST_CP_001'")
    c.commit(); print("end=start OK (unexpected)")
except Exception as e:
    c.rollback(); print("end=start ERROR:", str(e)[:160])
# 2) try view DELETE
try:
    cur.execute("delete from OV_CHEM_PRODUCT where CODE='AUTOTEST_CP_001'")
    print("view delete rowcount:", cur.rowcount); c.commit()
except Exception as e:
    c.rollback(); print("view delete ERROR:", str(e)[:160])
# 3) if still present, end = start + 1 day (satisfies end>start; past date leaves current view)
if resid():
    try:
        cur.execute("update OV_CHEM_PRODUCT set OBJECT_END_DATE=OBJECT_START_DATE+1 where CODE='AUTOTEST_CP_001'")
        print("end=start+1 rowcount:", cur.rowcount); c.commit()
    except Exception as e:
        c.rollback(); print("end=start+1 ERROR:", str(e)[:160])
print("residual in ov_chem_product now:", resid())
c.close()
