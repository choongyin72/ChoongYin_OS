import oracledb
c=oracledb.connect(user="ECKERNEL_EC",password="energy",dsn="localhost:1521/ORCL");cur=c.cursor()
cur.execute("""select column_name, data_type, data_length, nullable from all_tab_columns
   where owner='ECKERNEL_EC' and table_name='OV_FORECAST_GROUP'
   and nullable='N' order by column_id""")
print("NOT NULL cols in OV_FORECAST_GROUP:")
for r in cur.fetchall(): print("  ",r)
c.close()
