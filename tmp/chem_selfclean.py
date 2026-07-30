import oracledb
c=oracledb.connect(user="ECKERNEL_EC",password="energy",dsn="localhost:1521/ORCL");cur=c.cursor()
# object_id of the leftover parent
cur.execute("select object_id from OV_CHEM_PRODUCT where code='AUTOTEST_CHP_RECON1'")
row=cur.fetchone()
if not row: print("parent already gone"); raise SystemExit
oid=row[0]; print("parent object_id:", oid)
# CHEM_USAGE_REPORT_CONF columns -> find FK to chem product
cur.execute("select column_name from all_tab_columns where owner='ECKERNEL_EC' and table_name='CHEM_USAGE_REPORT_CONF' order by column_id")
cols=[r[0] for r in cur.fetchall()]; print("child cols:", cols)
fk=next((x for x in cols if 'CHEM' in x and 'ID' in x) or 'OBJECT_ID' in cols, None)
fk=next((x for x in cols if x in ('CHEM_PRODUCT_ID','OBJECT_ID','CHEM_PROD_ID','PRODUCT_ID')), None)
print("using child FK col:", fk)
if fk:
    cur.execute(f"delete from CHEM_USAGE_REPORT_CONF where {fk}=:o", {"o":oid}); print("child rows deleted:", cur.rowcount)
# End=Start the parent via the OV view
cur.execute("update OV_CHEM_PRODUCT set OBJECT_END_DATE=OBJECT_START_DATE where code='AUTOTEST_CHP_RECON1' and OBJECT_END_DATE is null")
print("parent end=start rows:", cur.rowcount)
c.commit()
cur.execute("select count(*) from OV_CHEM_PRODUCT where code like 'AUTOTEST_CHP%'"); print("AUTOTEST_CHP still visible:", cur.fetchone()[0])
c.close()
