# Evidence capture — Batch 8 backfill (2026-08-28)

Re-run of the ALREADY-MERGED PR #449 Bank-pattern RF suite, one live pass, for the
lean-deliverable-backfill work order (`docs/lean-deliverable-backfill-workorder.md`). No RF
automation files were modified for this capture.

## Commands run
```
robot --dryrun --outputdir /tmp/cc_dryrun tests/Configuration/Assets/Date_Objects/calendar_collection_iud.robot
EC_HEADLESS=true robot --outputdir /tmp/cc_live tests/Configuration/Assets/Date_Objects/calendar_collection_iud.robot
```

## Results
- **Dryrun:** 5 tests, 5 passed, 0 failed.
- **Live headless:** 5 tests, 5 passed, 0 failed (first attempt, no retry needed).
  - TC01 Verify Clean State — PASS
  - TC02 Insert Calendar Collection Data — PASS
  - TC03 Update Calendar Collection Data — PASS
  - TC04 Find Calendar Collection Data — PASS
  - TC05 Delete Calendar Collection Data — PASS
- **robocop** (`calendar_collection_page.resource` + `calendar_collection_iud.robot`): 9 issues
  (5x VAR02 unused-variable-style + 4x DOC02 missing test-case documentation) — matches the
  baseline PR #449 itself reported ("robocop (9 issues, matches established baseline)"). Not
  fixed here — doc-only backfill task, automation files untouched.
- **DB self-clean** (independent fresh `oracledb` connection, local sandbox DSN
  `localhost:1521/ORCL`, separate from the RF suite's own in-run connection):
  - `SELECT COUNT(*) FROM OV_CALENDAR_COLLECTION WHERE CODE = 'AUTOTEST_CALENDAR_COLLECTION'` -> **0**
  - `SELECT COUNT(*) FROM OV_CALENDAR_COLLECTION` -> **7** (unchanged pre-existing rows, matches
    the SOW's original recon count)
- **Hygiene** (`py scripts/check_bundle_hygiene.py`, repo-wide): RESULT PASS. Sole WARN in the
  full-repo scan is a pre-existing, unrelated hardcoded-credential line in Contract Area's
  `investigation/` recon script — not this screen.

## Files in this folder
- `output.xml` — full live-run Robot Framework output (368 KB, screen-scoped single suite, well
  under the 2MB full-tree-dryrun risk this task's instructions warned about).
- `TC0*_*.png` (20 screenshots) — per-TC login/open_screen/action/verify/logout captures from
  T1/T2's built-in `Capture Step` calls, produced by the existing automation unmodified.
- This `RESULTS.md`.

Pre-existing `evidence/cc_0*.png` + `evidence/results.json` (outside this subfolder) are the
ORIGINAL PR #144 Playwright reference-flow evidence, predating the Bank-pattern conversion —
left as-is, not overwritten, since they document a different (still valid) artifact class.
