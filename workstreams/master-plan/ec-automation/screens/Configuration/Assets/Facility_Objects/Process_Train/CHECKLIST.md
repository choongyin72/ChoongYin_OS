# Process Train - IUD Deliverable Checklist (vs docs/IUD-DELIVERABLE-CHECKLIST.md, Section H)

_Refreshed 2026-08-28 (`docs/lean-deliverable-backfill-workorder.md`, Batch 10). Original bundle
predated PR #469's Bank-pattern rebuild (2026-08-23); this refresh backfills the checklist against
the current automation, evidence citations from the 2026-08-28 re-run below (RF automation itself
untouched)._

## Step 0 - check-existing gate
- [x] 0a KB map exists (`ec-ui-knowledge/screens/process_train.md`, already current from PR #469 - used as-is, not re-scanned).
- [x] 0b `grep -ril process_train workstreams/master-plan/ec-automation/{py,pageobjects,tests,screens}` -> only this screen's own files; no parallel copy.
- [x] 0c Reused shared engine (`py/ec_object_iud.py`), T2 (`manage_object.resource`), and `libraries/DbVerify.py` - zero shared-file changes.

## A. Bundle artifacts
- [x] 1 `process_train_sow.md` - refreshed 2026-08-28 with PR #469's real dev story + de-facto-mandatory-dropdown finding.
- [x] 2 `README.md` - refreshed 2026-08-28 with exact dryrun/live/DB-self-clean commands.
- [x] 3 `JOURNAL.md` - refreshed 2026-08-28, modeled on Bank's JOURNAL.md, pulling real content from PR #469's body.
- [ ] 4 Playwright driver - **N/A, permanently waived** (Section H: Universal Screen Engine replaces
      hand-written Playwright drivers). Pre-existing `py/process_train_iud.py` retained, not rebuilt.
- [ ] 5 `investigation/` - **N/A, permanently waived** (same reason as #4). Pre-existing `investigation/recon.py` retained.
- [x] 6 `evidence/` - fresh live run captured 2026-08-28: `evidence/2026-08-28-live/report.html`,
      `output.xml`, `log.html`, and one representative screenshot per TC (`TC0N *_verify.png`).
      Pre-existing evidence (`process_train_0[1-5]_*.png`, `rf_report.html` from the 2026-07-26 build)
      retained alongside for history.
- [x] 7 `CHECKLIST.md` - this file.

## B. RF files (pre-existing, untouched by this backfill)
- [x] 8 T3 `pageobjects/Configuration/Assets/Facility_Objects/process_train_page.resource` (Bank/Berth
      pattern, PR #469, label-driven, NO hardcoded ids).
- [x] 9 Suite `tests/Configuration/Assets/Facility_Objects/process_train_iud.robot` (5 TCs, per-TC login/logout).

## C. Verification gates (2026-08-28 re-run, real commands + real output)
- [x] 10 robocop - `py -m robocop check pageobjects/.../process_train_page.resource tests/.../process_train_iud.robot`
      -> **9 issues** (4 VAR02 + 5 DOC02), exit 0. Matches the established Bank/Berth/Port baseline count/kind - no new defect class.
- [x] 11 `--dryrun` - `robot --dryrun tests/.../process_train_iud.robot` -> **5/5 pass, 0 fail**.
- [x] 12 LIVE headless run - `EC_HEADLESS=true robot tests/.../process_train_iud.robot` -> **5/5 pass, 0 fail**
      (TC01 clean-state / TC02 insert / TC03 update / TC04 find / TC05 delete), first attempt, no retry needed.
- [x] 13 DB ground-truth - suite's own `DbVerify` assertions (`Code Should Be Present/Absent In View
      OV_PROCESS_TRAIN`, `Field Should Equal In View OV_PROCESS_TRAIN <code> NAME <expected>`) all
      passed within the 5/5 live run above; independently re-confirmed via a **fresh** `oracledb`
      connection: `SELECT COUNT(*) FROM OV_PROCESS_TRAIN WHERE CODE LIKE 'AUTOTEST_PT%'` -> **0** (post-run).
- [x] 14 FULL I-U-D - Insert (TC02) + Update (TC03) + Delete (TC05) all present and passed.
- [x] 15 Self-clean confirmed - fresh-connection query above returned **0** residual `AUTOTEST_PT%` rows.
- [x] 16 Hygiene - `py scripts/check_bundle_hygiene.py` -> `RESULT: PASS` (no hardcoded creds, pure ASCII, no CHECKLIST/VERIFY-REPORT contradiction).

## D. Delivery (pre-existing from PR #469, unchanged by this backfill)
- [x] 17 Registry row - `docs/ec_screen_registry.md` "Process Train" row (MODIFIED in PR #469, not touched here).
- [x] 18 Scorecard row - `docs/automation-scorecard.md` "Process Train" row (MODIFIED in PR #469, not touched here).
- [x] 19 PR - this backfill's own PR (docs-only) carries the R9 6-field body; PR #469 carried it for the automation itself.

## E. Knowledge base
- [x] 20 KB map `ec-ui-knowledge/screens/process_train.md` - already current from PR #469 (documents
      the Production Facility Class 1 de-facto-mandatory correction); last-verified date bumped to
      2026-08-28 in this backfill.
- [x] 21 Reuse clause - this IS a reuse/backfill run (Step 0 found existing automation); JOURNAL,
      evidence, and KB map all refreshed/produced per the clause, not left at "tests still pass" alone.

_Items 10-16 above are real re-run output from 2026-08-28, hand-recorded in `VERIFY-REPORT.md`
(refreshed the same session) - not from `scripts/verify_screen.py` (that script requires `--t3`/
`--suite`/`--driver` args tuned for the IUD-builder flow; this backfill ran the equivalent commands
directly, as the workorder's Step 4 instructs: "if it fails, that's a real regression to report,
not something to silently work around" - it did not fail)._
