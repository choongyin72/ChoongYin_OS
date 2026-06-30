"""Final self-clean verify: AUTOTEST residue across object types, variables, and mappings = 0;
counts back to baseline (232/1022/484/527)."""
import os, oracledb
c=oracledb.connect(user=os.environ.get('EC_DB_USER','ECKERNEL_EC'),password=os.environ.get('EC_DB_PASS','energy'),dsn=os.environ.get('EC_DB_DSN','localhost:1521/ORCL'))
cur=c.cursor()
cur.execute("select count(*) from calc_object_type where upper(object_type_code) like 'AUTOTEST%'"); print("AUTOTEST obj_types:", cur.fetchone()[0])
cur.execute("select count(*) from calc_variable where upper(name) like 'AUTOTEST%'"); print("AUTOTEST variables:", cur.fetchone()[0])
cur.execute("""select count(*) from calc_var_read_mapping m join calc_variable v on v.calc_var_signature=m.calc_var_signature where upper(v.name) like 'AUTOTEST%'"""); print("AUTOTEST read mappings:", cur.fetchone()[0])
for t in ['CALC_OBJECT_TYPE','CALC_VARIABLE','CALC_VAR_READ_MAPPING','CALC_VAR_WRITE_MAPPING']:
    cur.execute("select count(*) from "+t); print("   %-24s %d" % (t, cur.fetchone()[0]))
c.close()
