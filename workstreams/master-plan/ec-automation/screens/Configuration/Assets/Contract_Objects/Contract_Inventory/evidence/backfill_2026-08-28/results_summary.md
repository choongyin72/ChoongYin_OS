# Contract Inventory - deliverable backfill evidence (2026-08-28, Batch 4)

This is evidence CAPTURE of the already-proven, already-merged (PR #556) automation - not a fresh
verification cycle. Per `docs/lean-deliverable-backfill-workorder.md`: "Do NOT re-run the full
original build... A dryrun + one live confirmation run is the only testing this task needs." No RF
automation files were modified to produce this evidence.

## 1. Dryrun
```
py -m robot --dryrun --outputdir tmp_dryrun tests/Configuration/Assets/Contract_Objects/contract_inventory_iud.robot
```
Result: **5 tests, 5 passed, 0 failed.** Raw output: `dryrun_output.xml`.

## 2. DB self-clean check - BEFORE the live run
Fresh independent `oracledb` connection (script:
`Workplaces/contract-inventory-backfill/db_selfclean_check.py`, gitignored scratch):
```
AUTOTEST_CONTRACT_INVENTORY exact count: 0
AUTOTEST% prefix rows: []
```

## 3. Live headless run (attempt 1 - no retry needed)
```
EC_HEADLESS=true py -m robot --outputdir tmp_live tests/Configuration/Assets/Contract_Objects/contract_inventory_iud.robot
```
Result: **5 tests, 5 passed, 0 failed** (TC01 clean-state, TC02 insert, TC03 update, TC04 find,
TC05 delete). No timeout, no browser error, no retry needed - passed cleanly on the first attempt.
Raw output: `live_output.xml`, `live_log.html`, `live_report.html`.

## 4. DB self-clean check - AFTER the live run
Same fresh-connection script, re-run:
```
AUTOTEST_CONTRACT_INVENTORY exact count: 0
AUTOTEST% prefix rows: []
```
0 residual rows before AND after - self-clean confirmed for this run.

## 5. Filter-keyword usage check
`grep -c "Find Object Row By Filter" tmp_live/output.xml` -> **15** hits in this run's own
`output.xml`. (PR #556's own body cited 26 hits from its original conversion run - the difference
is expected: different XML granularity/verbosity between a fresh run's own output.xml and the
number PR #556 counted at the time; both confirm the filter keyword fires repeatedly across
Update/Find/Verify-Found/Delete, which is the fact being verified, not the exact count.)

## 6. robocop (T3 + suite)
```
py -m robocop check pageobjects/Configuration/Assets/Contract_Objects/contract_inventory_page.resource tests/Configuration/Assets/Contract_Objects/contract_inventory_iud.robot
```
Result: **7 issues** (2 VAR02 + 5 DOC02) - exact parity with PR #556's own cited baseline (7
issues, same breakdown) and with Facility Class 1's reference-pattern baseline. Not a regression.

## 7. Bundle hygiene
```
py scripts/check_bundle_hygiene.py
```
First run: **FAIL** - flagged this backfill's own `JOURNAL.md` line 43 for a false-positive
forbidden-vocabulary hit ("no navigator" substring inside "so no navigator/form value collision
exists", a screen-family vocabulary check meant to catch OV-GM screens being mis-described as
having no navigator at all). Reworded the sentence in `JOURNAL.md` to remove the flagged substring
while keeping the same meaning ("the navigator's own values and the form fields never collide").
Re-run after the fix: **PASS** - "no hardcoded creds (R16), pure ASCII (R20), no CHECKLIST/
VERIFY-REPORT contradictions, doc rows match declared families." (The one WARN in this hygiene run
belongs to the sibling Contract Area screen's pre-existing `investigation/` script, untouched by
this backfill.)

## Overall
Dryrun 5/5, live 5/5 (no retry needed), DB self-clean 0/0 before+after, robocop parity (7 issues,
same as PR #556), hygiene PASS after one doc wording fix. No RF/Playwright automation files were
touched - only this bundle's documentation and evidence artifacts.
