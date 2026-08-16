"""Reverse the AUTOTEST_FREETEXT_INVALID distribution created earlier (it's unreachable from the screen,
so it's an orphan). Transactional: delete -> verify gone -> COMMIT. Reversible re-create via the .py."""
import os, oracledb
con=oracledb.connect(user=os.environ.get("EC_DB_USER","ECKERNEL_EC"),
 password=os.environ.get("EC_DB_PASS","energy"),
 dsn=os.environ.get("EC_DB_DSN","localhost:1521/ORCL"),tcp_connect_timeout=15)
cur=con.cursor()
DIST="AUTOTEST_FREETEXT_INVALID"; CODE="AUTOTEST_INVALID_RCV"
cur.execute("DELETE FROM DISTRIBUTION_SET_CONTACT WHERE DISTRIBUTION_SET_CODE=:d",{"d":DIST}); print("dsc deleted:",cur.rowcount)
cur.execute("DELETE FROM DISTRIBUTION_SET WHERE DISTRIBUTION_SET_CODE=:d",{"d":DIST}); print("dist deleted:",cur.rowcount)
cur.execute("DELETE FROM COMPANY_CONTACT_VERSION WHERE OBJECT_ID IN (SELECT OBJECT_ID FROM COMPANY_CONTACT WHERE OBJECT_CODE=:c)",{"c":CODE}); print("ccv deleted:",cur.rowcount)
cur.execute("DELETE FROM COMPANY_CONTACT WHERE OBJECT_CODE=:c",{"c":CODE}); print("cc deleted:",cur.rowcount)
cur.execute("SELECT COUNT(*) FROM DISTRIBUTION_SET WHERE DISTRIBUTION_SET_CODE=:d",{"d":DIST})
gone = cur.fetchone()[0]==0
cur.execute("SELECT COUNT(*) FROM COMPANY_CONTACT WHERE OBJECT_CODE=:c",{"c":CODE})
gone = gone and cur.fetchone()[0]==0
if gone:
    con.commit(); print("COMMITTED — orphan distribution + contact removed clean.")
else:
    con.rollback(); print("VERIFY FAILED -> ROLLED BACK.")
con.close(); print("DONE")
