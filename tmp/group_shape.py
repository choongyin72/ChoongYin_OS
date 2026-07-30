import oracledb
c=oracledb.connect(user="ECKERNEL_EC",password="energy",dsn="localhost:1521/ORCL"); cur=c.cursor()
cur.execute("""select column_name, nullable from all_tab_columns where owner='ECKERNEL_EC'
   and table_name='TV_CTRL_CHECK_GROUP' order by column_id""")
cols=cur.fetchall()
print("TV_CTRL_CHECK_GROUP cols (NN=mandatory):")
for cn,nn in cols: print(f"   {cn}{'  [NN]' if nn=='N' else ''}")
cur.execute("select count(*) from tv_ctrl_check_group"); print("local group count:", cur.fetchone()[0])
cur.execute("select * from tv_ctrl_check_group where rownum=1")
if cur.description:
    names=[d[0] for d in cur.description]; row=cur.fetchone()
    if row: print("sample group row:", dict(zip(names,[str(v)[:40] for v in row])))
c.close()
