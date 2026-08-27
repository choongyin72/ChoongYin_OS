# JOURNAL - Meter Run (CO.0091) OV IUD

_Screen: Configuration > Assets > Stream_Objects > Meter Run (OV, date-effective, plain Bank-family,
no navigator). View `OV_METER_RUN`. This JOURNAL covers BOTH the 2026-07-26 original build and the
2026-08-23 Bank-pattern conversion (PR #462, Batch 8); the conversion section was backfilled
2026-08-27/28 per `docs/lean-deliverable-backfill-workorder.md` Batch 9 (Section H retired the
2026-08-23 lean waiver that had let the conversion ship without these artifacts)._

## 2026-07-26 (original build)
- **Branch:** `feature/meter_run-iud` (own branch, stacked so the shared-engine helpers are present).
  Check-existing gate: only this build; reused shared engine + T2 + DbVerify.
- **Recon** (`investigation/recon.py`, read-only): DB `CLASS_TYPE=OBJECT` => OV; treeview
  Configuration > Assets > Stream_Objects > Meter Run. Mandatory Code/Name/Start Date PLUS six
  extra mandatory fields (Type of Taps / Pipe Material / Location of Taps dropdowns, Pipe Diameter
  [mm] / Diameter Meas Temp [deg R] / All Calibration Factor). Plain Bank-layout OV, single
  Date+GO nav.
- **Label-driven** T3 (no hardcoded ids) on the shared `ec_object_iud.py` engine + T2, zero engine
  changes. Playwright driver -> 7/7; RF T3+suite (label-driven-only, no properties files, no
  explicit grid-filter) -> live 4/4.
- `verify_screen.py` -> **OVERALL PASS**: robocop 0, hygiene 0, dryrun 4/4, LIVE RF 4/4,
  Playwright 7/7.

## 2026-08-23 (PR #462, Batch 8 of the Bank-pattern conversion project)
- Rebuilt `meter_run_page.resource` from the label-driven-only shape to the full Bank-pattern
  shape (properties-file-driven insert/update/verify + explicit grid-filter wiring), matching
  `bank_page.resource`/`berth_page.resource` exactly - part of a 5-screen parallel batch
  (`tmp/batch8_shared_findings.md`).
- Rebuilt `meter_run_iud.robot` to the 5-TC fixed-code business narrative (Verify Clean State /
  Insert / Update / Find / Delete), per-TC Login/Logout.
- New: `testdata/meter_run_insert.properties`, `meter_run_update.properties`,
  `meter_run_form_verify.properties`, `meter_run_grid_verify.properties`; new credential pair
  `METER_RUN_EC_USER`/`METER_RUN_EC_PASS` (additive) in `resources/credentials.py`.
- No shared T1/T2 (`manage_object.resource`/`common.resource`) edits.
- Evidence cited in the PR body: live **5/5**, filter keyword (`Find/Clear Object Row By Filter`)
  fired 15/15, full-`tests/`-tree dryrun 758/758, robocop 9 issues (parity with the accepted
  `berth_iud.robot` baseline, not a regression), fresh-connection DB self-clean 0 residual
  (`AUTOTEST_METER_RUN` in `OV_METER_RUN`).
- Explicitly flagged in the PR body that it **MODIFIES** the existing registry/scorecard rows
  (added 2026-07-26) rather than adding new ones - called out per the Batch 7 merge-conflict lesson
  (PR #458/#459) so a concurrent sibling Batch 8 PR touching the same doc files could be watched
  for a duplicate-row artifact.

## 2026-08-27/28 (this backfill)
- Section H of `docs/IUD-DELIVERABLE-CHECKLIST.md` retired the 2026-08-23 lean waiver that had let
  the PR #462 conversion ship without a refreshed SOW/JOURNAL/evidence/KB map. This entry, the
  updated `meter_run_sow.md`/`README.md`/`CHECKLIST.md`/`ec-ui-knowledge/screens/meter_run.md`, and
  the evidence in `evidence/` close that gap - built from PR #462's real body (via `gh pr view 462`)
  and a fresh re-run, not invented.
- Re-ran the suite once for evidence capture: dryrun 5/5, live RF 5/5 (first attempt, no retry
  needed), filter keyword fired 15/15, robocop 9 issues (same as PR #462's cited baseline, not a
  regression), hygiene PASS, DB self-clean 0 residual (fresh oracledb connection, checked both
  before and after the run).
- No RF automation files were modified - this is documentation/evidence backfill only.

## Done well
- Full I-U-D DB-verified vs `OV_METER_RUN` (insert Code/Name, update Name, delete via End
  Date=Start Date); self-clean 0 residual, confirmed via a fresh connection both before and after
  the live run, across both the 2026-08-23 conversion and this backfill's re-run.
- Mandatory field set (6 extras beyond Code/Name/Start Date) taken as-is from the already-proven
  driver/page object, not extrapolated from Bank/Berth's simpler 3-field baseline - avoided the
  "shape resembles a known case" trap this project has hit on other screens.
- Delete End Date field id confirmed live via a **read-only** recon that selected an existing
  production row and inspected the DOM, never saved - same convention as Bank/Berth's
  `*_DEL_ENDDATE` constant, not assumed.

## Done wrong / lessons
- The original 2026-07-26 build shipped without the properties-file-driven pattern or explicit
  grid-filter wiring that later became the Bank/Berth standard, requiring the full Batch 8 rebuild
  rather than an incremental patch.
- The 2026-08-23 conversion shipped clean, DB-verified automation but, under the since-retired
  Section G lean waiver, skipped the SOW/JOURNAL/evidence/KB refresh - "done" (green tests) is not
  the same as "fully documented"; this backfill closes that specific gap.

## Blockers -> resolution
- None during the 2026-08-23 conversion - live 5/5 on the recorded run, no retries needed.
- None during this backfill's evidence-capture re-run (2026-08-28) - dryrun 5/5 and live 5/5 both
  passed on the first attempt.

## Decisions
- Playwright driver (`py/meter_run_iud.py`) stays as-is, unmaintained going forward - the Universal
  Screen Engine (`py/engine.py`) is the owner-decided replacement for hand-written Playwright
  drivers (Section H, `docs/IUD-DELIVERABLE-CHECKLIST.md`); no new Playwright work was done for the
  conversion or this backfill.
- `investigation/recon.py` and the 2026-07-26 evidence set are kept as historical record; the
  2026-08-28 backfill evidence-capture run's artifacts are added alongside, not overwriting them.

## Evidence
- **2026-07-26 (original build):** `evidence/meter_run_0[1-5]_*.png` + `evidence/rf_report.html`
  (Playwright 7/7 + RF 4/4).
- **2026-08-23 (PR #462 conversion):** cited in the PR body - live 5/5, filter keyword fired
  15/15, full-tree dryrun 758/758, robocop 9 issues (parity baseline), fresh-connection DB
  self-clean 0 residual.
- **2026-08-28 (this backfill's evidence-capture re-run):** `evidence/tmp_live_meterrun_*` (log/
  report/screenshots) - dryrun 5/5, live RF 5/5, filter keyword fired 15/15, robocop 9 issues
  (same baseline as PR #462, not a regression), hygiene PASS, DB self-clean 0 residual (fresh
  connection, before and after).
