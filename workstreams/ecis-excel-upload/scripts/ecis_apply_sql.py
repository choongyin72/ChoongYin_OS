"""Prove create_CLAUDE_WELL_TEST_interface.sql works + is re-runnable. Deletes the UI-built CLAUDE_WELL_TEST
config (child-first), runs the SQL block, runs it AGAIN (idempotency), then verifies counts + rev_text.
Recovery if the SQL fails after delete: re-run build_claude_interface.py + build_claude_children.py.
py -X utf8 this.
"""
import os
import oracledb

SQL_FILE = r"c:/Projects/ChoongYin_OS/workstreams/ecis-excel-upload/sql/create_CLAUDE_WELL_TEST_interface.sql"
conn = oracledb.connect(user="ECKERNEL_EC", password="energy", dsn=os.environ.get("EC_DB_DSN", "localhost:1521/ORCL"))
cur = conn.cursor()


def counts(tag):
    cur.execute("SELECT object_id FROM imp_source_interface WHERE object_code='CLAUDE_WELL_TEST'")
    r = cur.fetchone()
    iid = r[0] if r else None
    rev = None
    nm = npa = nt = 0
    if iid:
        cur.execute("SELECT rev_text FROM imp_source_interface WHERE object_id=:i", i=iid); rev = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM imp_source_mapping WHERE imp_source_interface_id=:i", i=iid); nm = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM imp_source_path WHERE imp_source_mapping_id IN (SELECT object_id FROM imp_source_mapping WHERE imp_source_interface_id=:i)", i=iid); npa = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM imp_target_mapping WHERE imp_source_interface_id=:i", i=iid); nt = cur.fetchone()[0]
    print(f"  [{tag}] iface={'Y' if iid else 'N'} rev_text={rev!r} mappings={nm} paths={npa} targets={nt}")
    return iid


print("BEFORE:")
iid = counts("before")

# delete child-first
if iid:
    cur.execute("DELETE FROM imp_source_path WHERE imp_source_mapping_id IN (SELECT object_id FROM imp_source_mapping WHERE imp_source_interface_id=:i)", i=iid)
    cur.execute("DELETE FROM imp_source_mapping WHERE imp_source_interface_id=:i", i=iid)
    cur.execute("DELETE FROM imp_target_mapping WHERE imp_source_interface_id=:i", i=iid)
    cur.execute("DELETE FROM imp_source_interface WHERE object_id=:i", i=iid)
    conn.commit()
    print("deleted UI-built config.")
counts("after delete")

# load SQL block (strip trailing slash line)
with open(SQL_FILE, encoding="utf-8") as f:
    raw = f.read()
block = "\n".join(l for l in raw.splitlines() if l.strip() != "/")

print("RUN 1 (create) ...")
cur.execute(block)
counts("after run1")

print("RUN 2 (re-run = idempotency) ...")
cur.execute(block)
counts("after run2")

conn.close()
print("DONE (expect: iface=Y, rev_text='ECPR-DEMO', mappings=3, paths=6, targets=1 after BOTH runs)")
