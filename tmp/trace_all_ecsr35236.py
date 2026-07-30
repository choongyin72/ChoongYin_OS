# READ-ONLY: all check rules on ec14151 stamped REV_TEXT='ECSR-35236'. SELECT only.
import oracledb
DSN="db.ec14151.woodside-pluto.tieto-og.cloud:1521/ec14151"
c=oracledb.connect(user="ECKERNEL_EC",password="energy",dsn=DSN); cur=c.cursor()
cur.execute("""select check_id, check_name, created_by,
   to_char(created_date,'YYYY-MM-DD HH24:MI') cwhen,
   last_updated_by, to_char(last_updated_date,'YYYY-MM-DD HH24:MI') uwhen, rev_no
   from ctrl_check_rules where rev_text='ECSR-35236' order by created_date, check_id""")
rows=cur.fetchall()
print("=== ctrl_check_rules with REV_TEXT=ECSR-35236 : %d ===" % len(rows))
print("ID | NAME | CREATED_BY | CREATED | LAST_UPD_BY | UPDATED | REV")
for r in rows: print(" | ".join(str(x) for x in r))
# also the rule-variable table (our script added variables too)
try:
    cur.execute("""select count(*), min(to_char(created_date,'YYYY-MM-DD HH24:MI')),
       max(to_char(created_date,'YYYY-MM-DD HH24:MI')) from tv_ctrl_check_rule_variable where rev_text='ECSR-35236'""")
    print("\ntv_ctrl_check_rule_variable REV_TEXT=ECSR-35236:", cur.fetchone())
except Exception as e: print("var table:", str(e)[:80])
c.close()
