# County backfill evidence — 2026-08-28

Re-run of the already-proven, already-merged Bank-pattern RF suite (PR #429 + #489), captured for the
lean-deliverable backfill work order (Batch 12, final screen). No automation files were modified for
this run.

## Commands run
```bash
# full-tree dryrun (collision check)
py -m robot --dryrun --outputdir results/_dryrun_full tests
# -> 883 tests, 883 passed, 0 failed

# County-only dryrun
py -m robot --dryrun --outputdir results/_dryrun_county tests/Configuration/Assets/Basic_Objects/county_iud.robot
# -> 5 tests, 5 passed, 0 failed

# live headless run
EC_HEADLESS=true py -m robot --outputdir results/_live_county tests/Configuration/Assets/Basic_Objects/county_iud.robot
# -> 5 tests, 5 passed, 0 failed (TC01 Verify Clean State, TC02 Insert, TC03 Update, TC04 Find, TC05 Delete)
```

## DB self-clean (fresh oracledb connection, run after the live suite)
```sql
SELECT CODE FROM OV_COUNTY WHERE CODE LIKE 'AUTOTEST%';
```
Result: **0 rows** (`Residual AUTOTEST% rows in OV_COUNTY: 0`).

## Evidence in this folder
- `output.xml`, `log.html` — full Robot Framework result set for the live run above.
- `TC0*_*.png` — per-step screenshots (login / open_screen / action / verify / logout) for all 5 TCs,
  captured by the suite's own `Capture Step` calls (pre-existing mechanism, unchanged).
- All files individually well under the 2MB single-file guidance (largest is `log.html` at ~332KB).

## Scope note
This is evidence CAPTURE of an already-verified, already-merged suite — not a new verification cycle.
The automation itself (`county_page.resource`, `county_iud.robot`, `testdata/county_*.properties`) was
read-only for this task; nothing in `pageobjects/`, `tests/`, or `testdata/` was modified.
