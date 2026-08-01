#!/usr/bin/env python3
"""MANDATORY recon step for any OV-GM screen with a mandatory nav cascade or a form dropdown that ties to
scope (Contract, Transport System, Production Unit, Operator Route, Functional Area, ...).

WHY THIS EXISTS: the same defect was hit three separate times as three separate "screen bugs" needing a
fresh live-debugging session each time - Message Group (saved neighbouring functional area), Service
(saved a contract/transport system from outside the intended scope), and Collection Point (first-available
Production Unit's cascade children came back empty). All three are ONE recurring EC quirk: "first
available" in a dropdown or nav cascade is not guaranteed to be a scope that actually has usable data
underneath it. Each time I wrote a bespoke one-off DB script to find a working scope AFTER already hitting
the failure live. That is a process defect, not screen complexity - the fix is to run this BEFORE the
first live attempt, every time, as a required step, not a reminder in a doc I can skip.

WHAT IT DOES: queries the TARGET VIEW's own existing rows (ground truth, not a guess) and reports which
scope-code values actually recur - i.e. which Production Unit / Contract / Area / etc. already has real
data under it - so nav/dropdown values can be chosen from PROVEN scopes instead of "first available".

Usage:
    py scripts/find_populated_scope.py <VIEW_NAME>

Exit codes:
    0  - the view has data; scope candidates printed, pick from them.
    1  - the view has ZERO rows. There is nothing to learn from ground truth - this is a genuine unknown,
         not something to skip past. Probe the panels directly (see
         tmp/probe_service_panels.py-style scripts) or ask the owner, but do not default to __FIRST__ and
         hope. This exit code exists specifically so this case cannot be silently walked past.

Deliberately NOT fully automated: it does not pick a value for you, resolve every code to its display
label (that varies by cross-reference class and is safer done with one targeted query - see
tmp/resolve_service_labels.py for the pattern), or write a config. It replaces the AD-HOC DB QUERY step of
recon with ONE proven, reusable command - the judgment step (which scope to actually build against) stays
with whoever is building the screen.
"""
import sys

import oracledb

# columns that describe the object itself or audit metadata, never a SCOPE - excluded from candidates
EXCLUDE = {
    "CODE", "NAME", "DESCRIPTION", "CLASS_NAME", "OBJECT_ID", "REC_ID", "REV_NO", "REV_TEXT",
    "RECORD_STATUS", "CREATED_BY", "LAST_UPDATED_BY", "APPROVAL_BY", "APPROVAL_STATE",
}


def a(s):
    return str(s).encode("ascii", "replace").decode("ascii")


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    view = sys.argv[1].upper()

    con = oracledb.connect(user="ECKERNEL_EC", password="energy", dsn="localhost:1521/ORCL")
    cur = con.cursor()

    cur.execute("select count(*) from all_views where view_name = :v", v=view)
    if cur.fetchone()[0] == 0:
        print(a("ABORT: no view named %r (all_views). Check the name - OV_ views are case-sensitive-ish "
                "in this script; pass the exact name." % view))
        return 2

    cur.execute("select count(*) from %s" % view)
    total = cur.fetchone()[0]
    print(a("%s: %d row(s) total" % (view, total)))
    if total == 0:
        print(a("=" * 78))
        print(a("EXIT 1: this view has ZERO rows. There is NOTHING to learn from ground truth here."))
        print(a("Do not default to __FIRST__ and hope - probe the panels directly (a read-only script"))
        print(a("that opens the New-Object form and lists each dropdown's real options), or ask the owner."))
        print(a("=" * 78))
        return 1

    has_open = False
    try:
        cur.execute("select count(*) from %s where object_end_date is null" % view)
        open_n = cur.fetchone()[0]
        has_open = True
        print(a("  of which OPEN (object_end_date is null): %d" % open_n))
    except Exception:
        pass  # not every view is date-effective

    cur.execute("""select column_name from all_tab_columns where table_name = :v
                   and column_name like '%_CODE' order by column_id""", v=view)
    cols = [r[0] for r in cur.fetchall() if r[0] not in EXCLUDE]
    if not cols:
        print(a("no candidate scope columns found (only excluded/generic columns present)"))
        return 0

    print(a("\ncandidate SCOPE columns and their most-used values (ground truth, not a guess):"))
    for col in cols:
        where = " where %s is not null" % col
        if has_open:
            where += " and object_end_date is null"
        try:
            cur.execute("select %s, count(*) c from %s%s group by %s order by c desc "
                       "fetch first 5 rows only" % (col, view, where, col))
            rows = cur.fetchall()
        except Exception as e:
            print(a("   %-32s ERR %s" % (col, repr(e)[:100])))
            continue
        if not rows:
            print(a("   %-32s (no non-null values among open rows)" % col))
            continue
        print(a("   %-32s %s" % (col, rows)))

    print(a("\nPick a value from the TOP of each list you need - it is proven to have real data underneath."))
    print(a("Resolve CODE -> display LABEL with one targeted query before using it in the UI (dropdowns"))
    print(a("show labels, the DB stores codes - comparing the wrong one produces a false failure)."))
    cur.close()
    con.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
