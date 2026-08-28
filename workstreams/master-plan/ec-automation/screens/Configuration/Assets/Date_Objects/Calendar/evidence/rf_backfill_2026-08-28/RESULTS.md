# Calendar RF backfill evidence run - 2026-08-28

Batch 8 doc/evidence backfill (`docs/lean-deliverable-backfill-workorder.md`). No RF automation
files were modified; this is a fresh evidence capture of the already-merged, already-working
suite built in PR #451 (2026-08-23, Batch 6 Bank-pattern conversion, final of the 23-screen
conversion pool).

## Dryrun
`robot --dryrun tests/Configuration/Assets/Date_Objects/calendar_iud.robot`
-> **5 tests, 5 passed, 0 failed.**

## Live headless run
`EC_HEADLESS=true robot --outputdir <this folder> tests/Configuration/Assets/Date_Objects/calendar_iud.robot`
-> **5 tests, 5 passed, 0 failed.** First attempt, no retry needed.

| TC | Result |
|---|---|
| TC01 Verify Clean State | PASS |
| TC02 Insert Calendar Data | PASS |
| TC03 Update Calendar Data | PASS |
| TC04 Find Calendar Data | PASS |
| TC05 Delete Calendar Data | PASS |

## DB self-clean (independent fresh connection, separate from the suite's own in-run `DbVerify`)
```
SELECT COUNT(*) FROM OV_CALENDAR WHERE CODE = 'AUTOTEST_CALENDAR'  -> 0
SELECT COUNT(*) FROM OV_CALENDAR                                   -> 6  (unchanged pre-existing rows)
```

## Other gates re-run this session
- `robocop check` on `pageobjects/.../calendar_page.resource` + `tests/.../calendar_iud.robot`
  -> 9 issues (4x VAR02 + 5x DOC02), same count PR #451 itself cited as its established baseline.
- Full-tree `robot --dryrun tests/` -> 883/883 pass (repo has grown since PR #451's own
  749/750 baseline check; no regression from this suite).
- `py scripts/check_bundle_hygiene.py` (repo-wide) -> RESULT: PASS. Sole WARN in the scan is
  unrelated (Contract Area's `investigation/live_recon_contract_area.py`).
- `output.xml` grep on `Find Calendar Row By Filter` -> 15 hits across TC02-TC05.

## Files in this folder
- `output.xml` (364 KB) -- full Robot Framework result for this run.
- 24 step screenshots (one set of `login`/`open_screen`/`action`/`verify`/`logout` per TC,
  captured by the suite's own `Capture Step` calls) -- total folder size ~1.4 MB.
- This `RESULTS.md`.

(`log.html`/`report.html`/`playwright-log.txt` from the run were NOT committed -- they are
derivable from `output.xml` via `rebot` and are not needed as static evidence; keeps this folder
small per the size guidance in the backfill work order.)
