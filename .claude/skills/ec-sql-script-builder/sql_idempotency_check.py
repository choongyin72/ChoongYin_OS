"""Re-runnability / idempotency harness for EC config SQL scripts (see SKILL.md, step 5).

Runs:  delete -> create -> (count A) -> create AGAIN -> (count B)  and asserts A == B with no error
=> proves the create script is idempotent (re-run = same end state, no duplicates) and the delete teardown works.

Usage (always via the `py` launcher):
  py -X utf8 .claude/skills/ec-sql-script-builder/sql_idempotency_check.py \
     --create workstreams/ecis-excel-upload/sql/create_CLAUDE_WELL_TEST_interface.sql \
     --delete workstreams/ecis-excel-upload/sql/delete_CLAUDE_WELL_TEST_interface_ov.sql \
     --count "SELECT COUNT(*) FROM ov_imp_source_mapping WHERE imp_source_interface_code='CLAUDE_WELL_TEST'" \
     --count "SELECT COUNT(*) FROM ov_imp_source_path    WHERE imp_source_interface_code='CLAUDE_WELL_TEST'" \
     --count "SELECT COUNT(*) FROM ov_imp_target_mapping WHERE imp_source_interface_code='CLAUDE_WELL_TEST'"

DSN/creds via env (defaults = local sandbox): EC_DB_DSN, EC_DB_USER, EC_DB_PASS.
NOTE: this MUTATES whatever the scripts target -> point it at a THROWAWAY code, never the shared live config
(see SKILL.md step 5/6). It does NOT prove the config functionally works end-to-end (do that separately).
"""
import argparse
import os
import sys

import oracledb


def run_block(cur, path):
    with open(path, encoding="utf-8") as f:
        raw = f.read()
    cur.execute("\n".join(l for l in raw.splitlines() if l.strip() != "/"))


def counts(cur, queries):
    out = []
    for q in queries:
        cur.execute(q)
        out.append(cur.fetchone()[0])
    return out


def main():
    ap = argparse.ArgumentParser(description="EC SQL idempotency / re-runnability check")
    ap.add_argument("--create", required=True, help="path to the create_*.sql script")
    ap.add_argument("--delete", required=True, help="path to the delete_*.sql teardown")
    ap.add_argument("--count", action="append", default=[], required=True,
                    help="a COUNT(*) SQL to assert (repeat for several); compared run1 vs run2")
    args = ap.parse_args()

    con = oracledb.connect(
        user=os.environ.get("EC_DB_USER", "ECKERNEL_EC"),
        password=os.environ.get("EC_DB_PASS", "energy"),
        dsn=os.environ.get("EC_DB_DSN", "localhost:1521/ORCL"),
    )
    cur = con.cursor()
    ok = True
    try:
        run_block(cur, args.delete); con.commit(); print("deleted (clean slate)")
        run_block(cur, args.create); con.commit(); a = counts(cur, args.count); print("RUN 1 counts:", a)
        run_block(cur, args.create); con.commit(); b = counts(cur, args.count); print("RUN 2 counts:", b)
        if a != b:
            ok = False; print("FAIL: counts differ between run 1 and run 2 (NOT idempotent):", a, "vs", b)
        elif any(v == 0 for v in a):
            ok = False; print("FAIL: a count is 0 after create — create did not produce the expected rows:", a)
        else:
            print("PASS: idempotent — identical counts both runs, no duplicates, no error.")
    except Exception as e:
        ok = False; print("FAIL: error while running scripts ->", str(e).splitlines()[0])
    finally:
        con.close()
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
