import oracledb
c=oracledb.connect(user="ECKERNEL_EC",password="energy",dsn="localhost:1521/ORCL"); cur=c.cursor()
# 1) any sequence that looks check-rule related?
cur.execute("""select sequence_name from all_sequences where sequence_owner='ECKERNEL_EC'
   and (sequence_name like '%CHECK%' or sequence_name like '%CTRL_CHECK%')""")
print("check-related sequences:", [r[0] for r in cur.fetchall()])
# 2) current max check_id locally
cur.execute("select nvl(max(check_id),0), count(*) from ctrl_check_rules")
print("local MAX(check_id), count:", cur.fetchone())
# 3) does the trigger reference a sequence / GetNextId? peek at source
cur.execute("""select text from all_source where owner='ECKERNEL_EC' and name='IUD_CTRL_CHECK_RULES'
   and (upper(text) like '%CHECK_ID%' or upper(text) like '%NEXTVAL%' or upper(text) like '%SEQ%'
        or upper(text) like '%GETNEXT%' or upper(text) like '%MAX(%') order by line""")
print("--- trigger lines mentioning id assignment ---")
for r in cur.fetchall(): print("  ", r[0].rstrip())
c.close()
