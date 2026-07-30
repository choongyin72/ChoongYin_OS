import oracledb
c=oracledb.connect(user="ECKERNEL_EC",password="energy",dsn="localhost:1521/ORCL");cur=c.cursor()
cur.execute("""select t.class_name, count(*) n_popup_fields
  from class_attr_property_cnfg t
 where t.property_code = 'PopupURL'
   and t.property_value like '%/object_popup%'
   and t.class_name in (select class_name from class_cnfg where class_type = 'OBJECT')
 group by t.class_name order by t.class_name""")
rows=cur.fetchall()
print("OBJECT (OV) classes with a Pick-from-EC-Object popup field: %d" % len(rows))
for cn,n in rows: print("  %-34s %d popup field(s)" % (cn,n))
c.close()
