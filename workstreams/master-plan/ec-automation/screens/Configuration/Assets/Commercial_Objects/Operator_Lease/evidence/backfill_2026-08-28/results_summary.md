# Backfill evidence capture — Operator Lease — 2026-08-28

Batch 6 of `docs/lean-deliverable-backfill-workorder.md` (first Bank-pattern wave). This
folder captures a re-run of the already-proven `operator_lease_iud.robot` suite (rebuilt to
the Bank pattern by PR #436, merged 2026-08-23) — no automation files were modified by this
backfill.

## Commands run (from `workstreams/master-plan/ec-automation/`, worktree `C:/tmp/wt-operatorlease-backfill`)

```bash
# robocop
py -m robocop check pageobjects/Configuration/Assets/Commercial_Objects/operator_lease_page.resource \
    tests/Configuration/Assets/Commercial_Objects/operator_lease_iud.robot

# dryrun (this suite)
py -m robot --dryrun tests/Configuration/Assets/Commercial_Objects/operator_lease_iud.robot

# full-tree dryrun (parity check vs whole tests/ directory)
py -m robot --dryrun tests/

# live headless run
EC_HEADLESS=true py -m robot tests/Configuration/Assets/Commercial_Objects/operator_lease_iud.robot

# hygiene (from repo root)
py scripts/check_bundle_hygiene.py
```

## Results

| Gate | Result | Evidence file |
|---|---|---|
| Robocop | **9 issues** (4 VAR02 + 5 DOC02) — exact parity with the Bank/Country/State/Field Group baseline cited in PR #436's own body, not a regression | `robocop_output.txt` |
| Dryrun (this suite) | **5/5 PASS**, 0 failed | `dryrun_output.xml` |
| Full-tree dryrun | **883/883 PASS**, 0 failed | `fulltree_dryrun_summary.txt` (raw output.xml was ~51 MB, over GitHub's 50 MB recommended max, and was not committed) |
| Live headless run | **5/5 PASS on attempt 1** (TC01 Clean State, TC02 Insert, TC03 Update, TC04 Find, TC05 Delete) — no retry needed | `live_output.xml` / `live_log.html` / `live_report.html` |
| DB self-clean (BEFORE live run) | `SELECT COUNT(*) FROM OV_OPERATOR_LEASE WHERE CODE = 'AUTOTEST_OPERATOR_LEASE'` = **0**; `SELECT CODE FROM OV_OPERATOR_LEASE WHERE CODE LIKE 'AUTOTEST%'` = **no rows** | see below |
| DB self-clean (AFTER live run) | Same two queries, fresh `oracledb` connection = **0** / **no rows** — TC05 delete confirmed to have cleaned up | see below |
| Grid-filter wiring | `grep -c 'name="Find Operator Lease Row By Filter"' live_output.xml` = **5** (Update/Find/Verify-Insert-Exists/Verify-Found/Delete) | `live_output.xml` |
| Hygiene | `py scripts/check_bundle_hygiene.py` -> **RESULT: PASS** (exit 0). Only WARN is 2 pre-existing hardcoded-credential lines in **Contract Area's** `investigation/` recon script — a different screen, not touched by this backfill | `hygiene_output.txt` |

## DB self-clean raw output

Fresh `oracledb` connection (`ECKERNEL_EC`/`localhost:1521/ORCL`), run both before and after the live suite:

```
exact count: 0
AUTOTEST% rows: []
```
(identical output both times — confirmed via a throwaway scratch script,
`Workplaces/operator-lease-backfill/db_check.py`, gitignored, not part of this bundle)

## Scope confirmation

No file under `pageobjects/Configuration/Assets/Commercial_Objects/operator_lease_page.resource`,
`tests/Configuration/Assets/Commercial_Objects/operator_lease_iud.robot`, or
`testdata/operator_lease_*.properties` was modified by this backfill task — this folder is
evidence capture of the already-working, already-merged (PR #436) automation only.
