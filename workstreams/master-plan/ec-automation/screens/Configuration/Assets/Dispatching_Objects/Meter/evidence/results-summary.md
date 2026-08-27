# Evidence — Meter backfill live run (2026-08-27)

Captured for the lean-deliverable backfill (Batch 3), documenting an already-proven suite —
no automation was modified to produce this run.

## Live run
```
EC_HEADLESS=true robot --outputdir results/meter_backfill_live tests/Configuration/Assets/Dispatching_Objects/meter_iud.robot
```
Result: **5/5 pass** (TC01 Verify Clean State, TC02 Insert, TC03 Update, TC04 Find, TC05 Delete).

## Dryrun (screen suite)
```
robot --dryrun --outputdir results/meter_backfill_dryrun tests/Configuration/Assets/Dispatching_Objects/meter_iud.robot
```
Result: 5/5 pass.

## Dryrun (full tests/ tree — regression parity check)
```
robot --dryrun --outputdir results/meter_backfill_dryrun_full tests/
```
Result: 883/883 pass, 0 failed.

## DB self-clean (fresh oracledb connection, run AFTER the live run above)
```sql
SELECT COUNT(*) FROM OV_METER WHERE CODE LIKE 'AUTOTEST_METER%';
```
Result: **0** residual rows.

## robocop (changed screen files only)
```
py -m robocop check pageobjects/Configuration/Assets/Dispatching_Objects/meter_page.resource tests/Configuration/Assets/Dispatching_Objects/meter_iud.robot
```
Result: 7 issues (2 VAR02 + 5 DOC02) — exact parity with `area_page.resource`/`area_iud.robot`'s
own 7-issue baseline, matching PR #554's original citation.

## Hygiene
```
py scripts/check_bundle_hygiene.py
```
Result: PASS (Meter is not part of the one unrelated pre-existing WARN, which concerns
`Contract_Area/investigation/live_recon_contract_area.py`).

## Note on a transient environment flake during this evidence run
Two live-run attempts before the successful one above failed with Browser-library
`ConnectionError: Playwright process has been terminated` / `Could not find active page` /
`WSAGetOverlappedResult: Connection reset` errors before even reaching the EC login form. This
was preceded by ~20 stray `chrome-headless-shell.exe`/`chrome-native-host.exe` processes already
running on the machine from earlier work in this session, force-killed before this run per the
session's standing instruction to check for stray Chrome processes on any live-run timeout. A
plain re-run (no code change, same command) then passed cleanly 5/5. Treated as a local
environment flake, not a regression in Meter's automation — no automation file was touched to
"fix" it.

## Files
- `TC0*_*.png` — per-step screenshots (login, open_screen, action, verify, logout) for each TC.
- `output.xml` / `log.html` / `report.html` — the full RF run artifacts from `results/meter_backfill_live/`.
