"""Fully self-clean AUTOTEST_CP_001 (local sandbox, my artifact) whose date-close is blocked by a child
FK. Identify FK child table/col, delete my object's children, then end=start via the view. Verify 0."""
import oracledb
c = oracledb.connect(user='ECKERNEL_EC', password='energy', dsn='localhost:1521/ORCL')
cur = c.cursor()
# what does FK_CHEM_USAGE_REPORT_CONF_1 constrain (child table + columns + referenced)?
cur.execute("""select a.table_name, a.column_name, a.position
               from all_cons_columns a where a.constraint_name='FK_CHEM_USAGE_REPORT_CONF_1' order by a.position""")
print("FK child cols:", cur.fetchall())
cur.execute("""select r.table_name, rc.column_name from all_constraints ac
               join all_constraints r on ac.r_constraint_name=r.constraint_name
               join all_cons_columns rc on r.constraint_name=rc.constraint_name
               where ac.constraint_name='FK_CHEM_USAGE_REPORT_CONF_1'""")
print("FK references (parent):", cur.fetchall())
# object id(s) for my code in base table
cur.execute("select object_id from chem_product where code='AUTOTEST_CP_001'")
ids = [r[0] for r in cur.fetchall()]
print("chem_product object_id(s):", ids)
# children referencing it (assume child col CHEM_PRODUCT_ID)
for col in ("CHEM_PRODUCT_ID", "OBJECT_ID"):
    try:
        cur.execute("select count(*) from CHEM_USAGE_REPORT_CONF where %s in (select object_id from chem_product where code='AUTOTEST_CP_001')" % col)
        n = cur.fetchone()[0]
        print("CHEM_USAGE_REPORT_CONF via %s:" % col, n)
        if n:
            cur.execute("delete from CHEM_USAGE_REPORT_CONF where %s in (select object_id from chem_product where code='AUTOTEST_CP_001')" % col)
            print("  deleted children:", cur.rowcount); c.commit()
    except Exception as e:
        print("  col %s err:" % col, str(e)[:90])
# now end=start via view
try:
    cur.execute("update OV_CHEM_PRODUCT set OBJECT_END_DATE=OBJECT_START_DATE where CODE='AUTOTEST_CP_001'")
    print("end=start rowcount:", cur.rowcount); c.commit()
except Exception as e:
    c.rollback(); print("end=start still ERR:", str(e)[:120])
cur.execute("select count(*) from ov_chem_product where code like 'AUTOTEST%'")
print("FINAL residual ov_chem_product:", cur.fetchone()[0])
c.close()
