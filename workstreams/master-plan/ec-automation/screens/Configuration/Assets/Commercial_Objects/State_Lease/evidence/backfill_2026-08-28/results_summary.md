# State Lease backfill re-run — 2026-08-28

Re-run of the already-proven RF suite for the lean-deliverable backfill (Batch 7). No RF/page-object
files were modified for this run — this is evidence capture only.

## Dryrun (single suite)
```
robot --dryrun --outputdir Workplaces/state-lease-backfill/dryrun \
  tests/Configuration/Assets/Commercial_Objects/state_lease_iud.robot
```
Result: **5 tests, 5 passed, 0 failed** (TC01–TC05 all PASS).

## Live headless run
```
EC_HEADLESS=true robot --outputdir Workplaces/state-lease-backfill/live \
  tests/Configuration/Assets/Commercial_Objects/state_lease_iud.robot
```
Result: **5 tests, 5 passed, 0 failed** (TC01 Verify Clean State, TC02 Insert, TC03 Update,
TC04 Find, TC05 Delete — all PASS on first attempt, no retry needed).

## DB self-clean (fresh connection, post-run)
```
py Workplaces/state-lease-backfill/dbcheck.py
```
Output: `AUTOTEST_STL present in OV_STATE_LEASE (fresh connection): False`
— confirms 0 residual `AUTOTEST_STL` rows in `OV_STATE_LEASE` after TC05's delete, via a fresh
`oracledb` connection opened by `libraries/DbVerify.py::_connect()` (not a cached/session connection).

## Artifacts in this folder
- `output.xml`, `log.html`, `report.html` — full Robot Framework output for the live run above
  (screen-scoped, ~1.7 MB combined; well under the "full-tree dryrun" size concern this task's
  instructions flagged — this is a single-suite run, not a repo-wide dryrun).
- `*.png` — per-step screenshots captured by the suite's `Capture Step` keyword (login/open/action/
  verify/logout per TC).
