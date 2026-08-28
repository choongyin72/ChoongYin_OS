# JOURNAL - Process Train (CO.0120) OV IUD

_Screen: Configuration > Assets > Facility_Objects > Process Train (OV, date-effective). View
`OV_PROCESS_TRAIN`. Modeled on `screens/Configuration/Assets/Financial_Objects/Bank/JOURNAL.md`
(the golden OV exemplar). This entry structure was backfilled 2026-08-28
(`docs/lean-deliverable-backfill-workorder.md`, Batch 10) - the bundle predated the current
JOURNAL/SOW/evidence rule (retired 2026-08-27, Section H of
`docs/IUD-DELIVERABLE-CHECKLIST.md`)._

## 2026-07-26 (original build)
- **Branch:** `feature/process_train-iud`. Check-existing gate: only this build; reused shared
  engine + T2 + DbVerify.
- **Recon** (`investigation/recon.py`, read-only): DB `CLASS_TYPE=OBJECT` -> OV; treeview
  Configuration > Assets > Facility_Objects > Process Train. Mandatory Code/Name/Start Date
  (as first scanned); optional dropdowns skipped.
- Label-driven T3 (no hardcoded ids). Playwright driver -> 7/7; RF T3+suite -> live 4/4.
- `verify_screen.py` -> OVERALL PASS: robocop 0, hygiene 0, dryrun 4/4, LIVE RF 4/4,
  Playwright 7/7.

## 2026-08-23 (Batch 9 Bank-pattern conversion, PR #469, merged)

### Built
- Rebuilt `process_train_page.resource` (T3) + `process_train_iud.robot` (suite) from the
  original label-driven-but-fixed-argument shape to the full **Bank/Berth pattern**:
  properties-file-driven insert/update/verify (`testdata/process_train_{insert,update,
  form_verify,grid_verify}.properties`), per-TC Login/Logout, fixed test code `AUTOTEST_PT`
  (replacing a per-run generated code), and explicit `Find/Clear Process Train Row By Filter`
  grid-filter wiring using the shared T2 `Find Object Row By Filter`.
- Added `PROCESS_TRAIN_EC_USER`/`PROCESS_TRAIN_EC_PASS` to `resources/credentials.py`
  (additive - Process Train gets its own dedicated credential pair, per the owner's
  2026-08-22 standing decision that every EC screen has its own login).

### Done well
- Full I-U-D DB-verified vs `OV_PROCESS_TRAIN` (insert Name, update Name, delete
  End=Start absent); live RF **5/5** (TC01 clean-state / TC02 insert / TC03 update / TC04
  find / TC05 delete). Fresh-connection self-clean: 0 residual `AUTOTEST_PT` rows.
- Grid-filter keyword confirmed actually fired via `output.xml` grep (non-zero occurrences
  across TC02-TC05) - not just wired but proven to execute.
- No shared T1/T2 (`manage_object.resource`/`common.resource`) files touched - every
  consolidated T2 keyword reused as-is.

### Done wrong / lessons
- **Silent Save failure, live-repro'd:** the screen's own KB doc (2026-07-26 scan) said
  "no mandatory dropdowns." A first live RF attempt with only Process Train Code / Process
  Train Name / Start Date clicked Save successfully (button enabled, click succeeded) but the
  row never reached `OV_PROCESS_TRAIN` (0 rows) and left EC's own unsaved-changes confirmation
  modal (`#confirmationForm:confirmation_modal`) open, stalling every subsequent click
  (4/5 fail that attempt). Root-caused via the repo's own "deep-dive first" standing order:
  re-ran the already-proven, unmodified `py/process_train_iud.py` (which fills
  `Production Facility Class 1 = __FIRST__`) and it passed 7/7 cleanly - confirming that
  dropdown is de-facto required for Save to actually commit, despite carrying no CSS
  mandatory-flag. Fixed by adding it to `testdata/process_train_insert.properties`, deliberately
  excluded from the round-trip form-label compare list (`__FIRST__` never matches the resolved
  literal text on reload - a documented Batch 9 gotcha shared with sibling screens).
- Lesson for future screens: a static field/CSS scan is not sufficient to establish "no
  mandatory fields" - a business rule can silently gate persistence without a visible
  mandatory flag. Live-repro the full round trip, don't trust the KB doc's field inventory
  alone once behavior contradicts it (matches the repo's External Location lesson on the
  same theme - stop and verify live, don't keep guessing).

### Blockers -> resolution
- Confirmation-modal stall (above) -> resolved by adding the de-facto-mandatory dropdown to
  the insert testdata, not by any T2/T1 change. No data damage; the stalled attempt never
  reached the DB (0 rows), so no cleanup was needed beyond closing the modal.

### Decisions
- Registry (`docs/ec_screen_registry.md`) and scorecard (`docs/automation-scorecard.md`) rows
  MODIFIED in place (not new rows) - this is a re-conversion of an existing screen, not a
  brand-new build.
- KB doc `ec-ui-knowledge/screens/process_train.md` corrected in the same PR (write-after),
  not left stale for a future session to rediscover.

### Evidence
- Live RF: 5/5 (2026-08-23), cited in PR #469 body; robocop 9 issues (4 VAR02 + 5 DOC02,
  baseline-matching); full `tests/` dryrun 766/766 post-merge with the other 4 Batch 9
  screens.

## 2026-08-28 (documentation/evidence backfill, this session)
- Owner decision 2026-08-27 (Section H) retired the 2026-08-23/26 lean-deliverable waiver for
  Bank-/Area-pattern work; SOW/README/JOURNAL/evidence/CHECKLIST/KB map must be backfilled for
  every screen converted since 2026-08-23, Process Train included (Batch 10 of
  `docs/lean-deliverable-backfill-workorder.md`).
- **Did NOT rebuild, modify, or re-verify the RF automation itself** - `process_train_page.
  resource` and `process_train_iud.robot` are unchanged from PR #469.
- Re-ran the already-proven suite once for fresh evidence: `--dryrun` 5/5, live headless
  5/5 (first attempt, no retry needed), fresh-connection DB self-clean 0 residual
  `AUTOTEST_PT%` rows, robocop 9 issues (same baseline), hygiene PASS.
- Refreshed `process_train_sow.md`, `README.md`, this `JOURNAL.md`, `CHECKLIST.md`, and
  `VERIFY-REPORT.md` to reflect the PR #469 rebuild (they still described the 2026-07-26
  pre-Bank-pattern shape). `ec-ui-knowledge/screens/process_train.md` was already current
  (corrected in PR #469 itself) - only its last-verified date was bumped.
