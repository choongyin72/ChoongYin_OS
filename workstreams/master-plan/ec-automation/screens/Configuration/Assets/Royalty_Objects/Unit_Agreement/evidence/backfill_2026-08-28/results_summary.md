# Unit Agreement - deliverable backfill evidence (2026-08-28, Batch 8)

This is evidence CAPTURE of the already-proven, already-merged (PR #446) automation - not a fresh
verification cycle. Per `docs/lean-deliverable-backfill-workorder.md`: "Do NOT re-run the full
original build... A dryrun + one live confirmation run is the only testing this task needs." No RF
automation files were modified to produce this evidence.

## 1. Dryrun
```
py -m robot --dryrun --outputdir tmp_dryrun tests/Configuration/Assets/Royalty_Objects/unit_agreement_iud.robot
```
Result: **5 tests, 5 passed, 0 failed.** Raw output: `dryrun_output.xml`.

## 2. DB self-clean check - BEFORE the live run
Fresh independent `oracledb` connection (script:
`Workplaces/unit-agreement-backfill/db_selfclean_check.py`, gitignored scratch):
```
AUTOTEST_UA exact count: 0
AUTOTEST% prefix rows: []
```

## 3. Live headless run (attempt 1 - no retry needed)
```
EC_HEADLESS=true py -m robot --outputdir tmp_live tests/Configuration/Assets/Royalty_Objects/unit_agreement_iud.robot
```
Result: **5 tests, 5 passed, 0 failed** (TC01 clean-state, TC02 insert, TC03 update, TC04 find,
TC05 delete). No timeout, no browser error, no retry needed - passed cleanly on the first attempt.
Raw output: `live_output.xml`, `live_log.html`, `live_report.html`.

## 4. DB self-clean check - AFTER the live run
Same fresh-connection script, re-run:
```
AUTOTEST_UA exact count: 0
AUTOTEST% prefix rows: []
```
0 residual rows before AND after - self-clean confirmed for this run.

## 5. Filter-keyword usage check
`grep -c "Find Object Row By Filter" tmp_live/output.xml` -> **15** hits in this run's own
`output.xml`. (PR #446's own body cited 5 `Find Unit Agreement Row By Filter` hits from its own
conversion run - the difference is expected: different XML granularity between a fresh run's own
output.xml (which also counts the underlying shared T2 keyword's internal log entries) and the
narrower screen-specific keyword count PR #446 cited; both confirm the filter keyword fires
repeatedly across Insert/Update/Find/Delete, which is the fact being verified, not the exact count.)

## 6. robocop (T3 + suite)
```
py -m robocop check pageobjects/Configuration/Assets/Royalty_Objects/unit_agreement_page.resource tests/Configuration/Assets/Royalty_Objects/unit_agreement_iud.robot
```
Result: **11 issues** - 6 VAR02 (unused variables `TEST_CODE`/`OBJ_NAME`/`END_DATE`/`OBJ_COMMENTS`/
`OBJ_NAME_UPD`/`OBJ_COMMENTS_UPD` in the suite, each used only as robot's built-in `${TEST_CODE}`-
style test-level variables consumed by keyword defaults rather than referenced directly in the
`.robot` file body) + 5 DOC02 (missing `[Documentation]` on TC01-TC05). Full output:
`robocop_output.txt`. Not compared against a PR #446-cited robocop baseline - PR #446's own body
does not cite a robocop number for this screen, so this is the first robocop reading on file for
Unit Agreement's current T3/suite, not a regression check.

## 7. Bundle hygiene
```
py scripts/check_bundle_hygiene.py
```
Result: **PASS** - "no hardcoded creds (R16), pure ASCII (R20), no CHECKLIST/VERIFY-REPORT
contradictions, doc rows match declared families." One pre-existing WARN unrelated to this screen
(2 hardcoded-credential lines in the sibling Contract Area screen's `investigation/` recon script -
not touched by this backfill). Full output: `hygiene_output.txt`.

## Overall
Dryrun 5/5, live 5/5 (no retry needed), DB self-clean 0/0 before+after, robocop 11 issues (6 VAR02
+ 5 DOC02, first reading on file - no prior baseline cited by PR #446), hygiene PASS. No RF/
Playwright automation files were touched - only this bundle's documentation and evidence artifacts.
