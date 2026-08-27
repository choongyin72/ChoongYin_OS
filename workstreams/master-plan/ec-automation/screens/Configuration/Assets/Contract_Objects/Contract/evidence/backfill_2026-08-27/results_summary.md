# Contract backfill evidence — 2026-08-27

Deliverable-backfill task (`docs/lean-deliverable-backfill-workorder.md`, Batch 3). Re-runs the
ALREADY-PROVEN Area-pattern suite from PR #546 (2026-08-26) to capture evidence artifacts; the RF
automation itself was NOT modified by this task.

## 1. Dryrun (structure only)
`robot --dryrun tests/Configuration/Assets/Contract_Objects/contract_iud.robot` -> **5/5 PASS**
(TC01-TC05), 0 failed. No dryrun log saved separately (dryrun writes no browser/DB artifacts worth
keeping beyond the console summary, which is quoted here verbatim):
```
5 tests, 5 passed, 0 failed
```

## 2. Live headless run — attempt 1 (FLAKE, disclosed per workorder instruction)
`EC_HEADLESS=true robot tests/Configuration/Assets/Contract_Objects/contract_iud.robot` ->
**0/5, TC02-TC05 failed** with `Error: Could not find active page` (TC01 passed). This is the same
class of transient UI-timing flakiness the original PR #546 body disclosed (that conversion needed
3 live attempts for the same reason). Retried ONCE per the workorder's instruction, not ground
into further attempts. This attempt's artifacts were not kept (superseded by the clean rerun
below); the failure mode is captured here in this summary for honesty.

## 3. Live headless run — attempt 2 (kept as evidence)
`EC_HEADLESS=true robot tests/Configuration/Assets/Contract_Objects/contract_iud.robot` ->
**5/5 PASS** (TC01 Verify Clean State, TC02 Insert, TC03 Update, TC04 Find, TC05 Delete). Artifacts
in this folder: `log.html`, `report.html`, `output.xml`.
- `Find Contract Row By Filter` fired 5x (`grep -c 'kw name="Find Contract Row By Filter"' output.xml` = 5),
  confirming explicit grid-filter wiring is exercised on every TC that touches the grid.

## 4. DB ground-truth self-clean (fresh connection, read-only)
`py Workplaces/contract-backfill/db_selfclean_check.py` (uses the same connection resolution as
`libraries/DbVerify.py`) -> `db_selfclean_check_output.txt`:
```
AUTOTEST_CONTRACT exact count = 0
AUTOTEST% prefix count = 0
```
Run AFTER the clean 5/5 live run above — confirms TC05's delete left 0 residual rows in
`OV_CONTRACT` and no other `AUTOTEST%` test data leaked.

## 5. Robocop (parity check, not a regression)
`robocop check pageobjects/Configuration/Assets/Contract_Objects/contract_page.resource tests/Configuration/Assets/Contract_Objects/contract_iud.robot`
-> `robocop_output.txt`: **7 issues** (2x VAR02 unused-variable, 5x DOC02 missing-test-doc) — exact
match to the count PR #546's body cited as "exact parity with Area's own baseline, not a
regression."

## 6. Hygiene
`py scripts/check_bundle_hygiene.py` -> `RESULT: PASS` — no hardcoded creds (R16), pure ASCII
(R20), no CHECKLIST/VERIFY-REPORT contradictions across the whole `screens/` tree (the only WARN
in the run is 2 pre-existing hardcoded-credential lines in **Contract_Area's** `investigation/`
recon script, a different screen, not touched by this task).
