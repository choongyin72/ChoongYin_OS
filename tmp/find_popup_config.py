# Find HOW EC flags a field as a pin/pinB popup picker in config, so picker screens can be enumerated (no guessing).
import oracledb
c=oracledb.connect(user="ECKERNEL_EC",password="energy",dsn="localhost:1521/ORCL");cur=c.cursor()
# 1) any config table/column mentioning popup / object_popup / pinB display type?
cur.execute("""select table_name, column_name from all_tab_columns where owner='ECKERNEL_EC'
   and (lower(column_name) like '%popup%' or lower(column_name) like '%display%type%' or lower(column_name) like '%widget%'
        or lower(column_name) like '%lookup%' or lower(column_name) like '%editor%')
   and table_name not like '%_JN' order by table_name""")
rows=cur.fetchall()
print("candidate config columns (display/widget/popup/lookup):")
for r in rows[:30]: print("  ", r[0], ".", r[1])
# 2) distinct values in class_property_cnfg that might mark a popup, e.g. a UI hint / display column
cur.execute("select column_name from all_tab_columns where owner='ECKERNEL_EC' and table_name='CLASS_PROPERTY_CNFG' order by column_id")
print("\nCLASS_PROPERTY_CNFG columns:", [r[0] for r in cur.fetchall()])
c.close()
