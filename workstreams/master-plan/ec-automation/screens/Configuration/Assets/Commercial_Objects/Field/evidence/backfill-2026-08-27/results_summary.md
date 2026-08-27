# Field backfill evidence — 2026-08-27

## Full-tree dryrun
`py -m robot --dryrun tests/` -> **883 tests, 883 passed, 0 failed**

## Live suite run
`EC_HEADLESS=true py -m robot tests/Configuration/Assets/Commercial_Objects/field_iud.robot`
-> **5 tests, 5 passed, 0 failed** (TC01 Verify Clean State, TC02 Insert Field Data,
TC03 Update Field Data, TC04 Find Field Data, TC05 Delete Field Data)

Artifacts: `live_log.html`, `live_output.xml`, `live_report.html` (this run).

## DB self-clean (fresh oracledb connection, localhost:1521/ORCL, ECKERNEL_EC)
`SELECT COUNT(*) FROM OV_FIELD WHERE CODE LIKE 'AUTOTEST%'` -> **0**

## Filter-keyword wiring (grep on live_output.xml)
- `Find Field Row By Filter` -> 14
- `Find Object Row By Filter` -> 15
- `Clear Field Row Filter` -> 5
- `Clear Object Row Filter` -> 15

## Hygiene
`py scripts/check_bundle_hygiene.py` (repo root) -> **RESULT: PASS** (167 bundles + 271 recon
scripts scanned; no hardcoded creds in Field's own files; ASCII-clean; no CHECKLIST/
VERIFY-REPORT contradictions; doc rows match declared families). One unrelated WARN noted for
Contract Area's investigation script — not a Field issue.
