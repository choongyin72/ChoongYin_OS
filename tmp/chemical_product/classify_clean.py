"""Classify Chemical Product's real time-scope/delete mechanism (fact, not assumption) + self-clean the
AUTOTEST_CP_001 residual on the LOCAL sandbox (my own test data). Verifies clean."""
import oracledb
c = oracledb.connect(user='ECKERNEL_EC', password='energy', dsn='localhost:1521/ORCL')
cur = c.cursor()
# time scope of the Chemical Product class (VERSIONED => End=Start delete applies)
for q, lbl in [
    ("select class_name, time_scope_code, class_type from class_cnfg where class_name='CHEM_PRODUCT'", "CHEM_PRODUCT class_cnfg"),
]:
    try:
        cur.execute(q); print(lbl, "->", cur.fetchall())
    except Exception as e:
        print(lbl, "ERR", repr(e)[:100])
# is the ov view updatable to close it? try end=start via the view (proper IUD-trigger path)
try:
    cur.execute("update OV_CHEM_PRODUCT set OBJECT_END_DATE = OBJECT_START_DATE where CODE='AUTOTEST_CP_001'")
    print("view update rowcount:", cur.rowcount)
    c.commit()
except Exception as e:
    print("view update ERR:", repr(e)[:150])
    c.rollback()
cur.execute("select count(*) from ov_chem_product where code like 'AUTOTEST%'")
print("residual in ov_chem_product after clean:", cur.fetchone()[0])
c.close()
