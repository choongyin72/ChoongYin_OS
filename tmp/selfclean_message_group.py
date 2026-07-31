#!/usr/bin/env python3
"""SELF-CLEAN the AUTOTEST_MG001 row my driver persisted on Message Group (CO.0236).

Why a DB-level close rather than the UI: the screen's groupmodel is OFF, so the grid NEVER LISTS the row
(that is the blocker itself) - there is no row to select in the UI, so ec.closeObjectRecord cannot reach
it. EC's own delete semantics for a VERSIONED object are End Date = Start Date, so that is what this
applies, through the OV_ view (whose INSTEAD-OF trigger does the housekeeping) - NOT a raw base-table
DELETE.

Safety per feedback_no_destructive_write_on_assumption: log the FULL row first, touch exactly one code,
assert 1 row affected, then re-read to prove it left the view.
"""
import sys
from pathlib import Path

EC = Path(r"C:\Projects\ChoongYin_OS\workstreams\master-plan\ec-automation")
sys.path.insert(0, str(EC / "libraries"))
import DbVerify as db

CODE = "AUTOTEST_MG001"
VIEW = "OV_MESSAGE_GROUP"


def a(s):
    return str(s).encode("ascii", "replace").decode("ascii")


con = db._connect()
cur = con.cursor()

cur.execute("select * from %s where code = :c" % VIEW, c=CODE)
cols = [d[0] for d in cur.description]
rows = cur.fetchall()
print(a("rows found for %s: %d" % (CODE, len(rows))))
for r in rows:
    print(a("FULL ROW (logged before any write):"))
    for k, v in zip(cols, r):
        if v is not None:
            print(a("   %-28s %r" % (k, v)))

if not rows:
    print("nothing to clean")
    sys.exit(0)

cur.execute("update %s set object_end_date = object_start_date where code = :c" % VIEW, c=CODE)
print(a("rows updated: %d" % cur.rowcount))
assert cur.rowcount == 1, "expected exactly 1 row, got %d - NOT committing" % cur.rowcount
con.commit()

still = db._code_present(VIEW, CODE)
print(a("still present in %s after End=Start: %s" % (VIEW, still)))
cur.execute("select count(*) from %s where code like 'AUTOTEST%%'" % VIEW)
print(a("residual AUTOTEST rows in view: %d" % cur.fetchone()[0]))
cur.close()
con.close()
