# JOURNAL - Well Hookup (CO.0108) OV-GM IUD

_Screen: Configuration > Assets > Facility_Objects > Well Hookup (OV-GM, groupmodel manage-object,
navigator-GATED, date-effective). View `OV_WELL_HOOKUP`. This JOURNAL originally covered only the
2026-07-30 base build; the 2026-08-26 Area-pattern conversion (PR #539) and 2026-08-27 backfill pass
are appended below, per `docs/lean-deliverable-backfill-workorder.md`._

## Built

### 2026-07-30 - base OV-GM IUD build
- **Branch:** `feature/ov-gm-well-hookup` (stacked on the gated-navigator capability, PR #244).
  Check-existing gate: grep ec-automation -> only this build; reused shared engine
  (`ec_object_iud.py`) + T2 + `DbVerify`.
- **Recon** (`investigation/recon.py`, read-only + `tmp/well_hookup/config.json` scan): OV-GM
  (grid `manageObject:form:T_data`), navigator cascade Production Unit -> Area -> Facility Class 1.
  Mandatory Well Hookup Code / Well Hookup Name / Start Date.
- **Built** (generator `tmp/gen_ovgm.py` -> proven Node/Chemical-Tank template): label-driven T3
  (no hardcoded ids); Playwright driver + RF T3/suite (4 TCs). Op Production Unit set
  first-available for grid visibility.
- `verify_screen.py` -> **OVERALL PASS**: robocop 0, hygiene 0, dryrun 4/4, LIVE RF 4/4 pass,
  Playwright 8/8. DB residual 0.

### 2026-08-26 - Area-pattern conversion (PR #539)
- **Branch:** `feature/well-hookup-area-pattern`, isolated git worktree (many sibling screens were
  being converted in parallel; confirmed via `git status --short` that only Well-Hookup-scoped
  paths plus the additive `credentials.py` line changed).
- **Trigger:** owner standing rule (2026-08-26) - any EC screen with a navigator matching Area's
  layout must be upgraded to Area's FULL pattern, not just get the shared navigator-fill piece.
- **Converted:** old bespoke-inline-navigator / 4-TC / single-suite-login / generated-code shape ->
  Area's full pattern: 5 TCs (Verify Clean State / Insert / Update / Find / Delete), per-TC
  Login/Logout, fixed test code `AUTOTEST_WH` (replacing the old timestamped code), properties-file-
  driven insert/update/verify via the shared T2 keywords, explicit `Find/Clear Well Hookup Row By
  Filter` grid-filter wiring, navigator filled via the shared `Apply Navigator From Properties`
  keyword with EXPLICIT values captured live (`Op Production Unit=AS1 EC Exploration Norway`,
  `Op Area=AS1_Area`, `Op Facility Class 1=AS1_Facility_01`), and zero inline DB-verify calls in the
  `.robot` file. The screen's genuine 3-level Production Unit -> Area -> Facility Class 1 navigator
  cascade was kept unchanged (structural conversion, not a reclassification). No changes to the
  shared `resources/manage_object.resource` T2 file.
- Additive-only `WELL_HOOKUP_EC_USER`/`WELL_HOOKUP_EC_PASS` credential pair added to
  `resources/credentials.py`.

### 2026-08-27 - deliverable backfill (this task, `docs/lean-deliverable-backfill-workorder.md`)
- Owner retired the 2026-08-23/26 lean waiver (`docs/IUD-DELIVERABLE-CHECKLIST.md` Section H,
  2026-08-27): SOW/README/JOURNAL/evidence/CHECKLIST.md/KB map are restored requirements for every
  screen converted under the old lean rule, Well Hookup included. This session backfilled those
  artifacts around the ALREADY-WORKING, ALREADY-MERGED PR #539 automation - no RF file was rebuilt
  or re-verified from scratch, only re-run once for fresh evidence.
- Re-ran the existing suite: `robot --dryrun` 5/5 PASS, `EC_HEADLESS=true robot` live run 5/5 PASS,
  grid-filter wiring fired 15x, fresh-connection DB self-clean 0 residual `AUTOTEST%` rows in
  `OV_WELL_HOOKUP`, robocop 7 issues (2 VAR02 + 5 DOC02, same as PR #539's own accepted baseline),
  hygiene PASS.

## Done well
- Full I-U-D DB-verified vs `OV_WELL_HOOKUP` across both builds; self-clean 0 residual confirmed
  independently each time (2026-07-30, 2026-08-26, and again in this 2026-08-27 backfill pass).
- The Area-pattern conversion kept the genuine 3-level navigator cascade unchanged rather than
  forcing it into a simpler shape it doesn't actually have - PR #539 explicitly called this out as
  "a structural conversion, not a reclassification."
- No shared T1/T2 files (`resources/manage_object.resource`) were touched by the conversion -
  reused the existing shared keywords as-is.

## Done wrong / lessons
- The original 2026-08-23/26 lean-deliverable waiver let this screen (and 81 others) merge without
  SOW/README/JOURNAL/evidence/CHECKLIST.md/KB map - only the RF suite and registry/scorecard rows
  were produced at conversion time. The owner judged this too thin and retired the waiver
  2026-08-27, requiring the retroactive backfill this JOURNAL entry itself is part of. Lesson: a
  structurally-correct, DB-verified, merged suite is still not "done" by this project's own
  21-item standard without its documentation/evidence bundle alongside it.

## Blockers -> resolution
- No blockers in either the 2026-08-26 conversion or this 2026-08-27 backfill pass - the RF suite
  was already proven; this task's only live activity was one dryrun + one live confirmation run,
  both green on the first attempt.

## Decisions
- Playwright bundle (`py/well_hookup_iud.py`, and this bundle's original `investigation/`/
  `evidence/` artifacts from the 2026-07-30 base build) is left untouched and NOT refreshed by this
  backfill - Section H of `docs/IUD-DELIVERABLE-CHECKLIST.md` keeps items 4/5 permanently waived
  for Bank-/Area-pattern work since the Universal Screen Engine (`py/engine.py`) is the owner-decided
  replacement going forward.
- `ec-ui-knowledge/screens/well_hookup.md` ALREADY EXISTED from the 2026-07-30 base build
  (describing the pre-conversion 4-TC, first-available-navigator shape) - updated in this backfill
  pass to reflect PR #539's Area-pattern conversion, not re-created from scratch. Selectors
  transcribed from `well_hookup_page.resource`'s own Variables section, not re-discovered live.

## Evidence
- 2026-07-30 base build: `evidence/wh_0[1-5]_*.png` + `evidence/results.json` (Playwright 8/8).
- 2026-08-26 conversion (PR #539): live RF 5/5, DB self-clean 0 residual, filter fired 15x,
  full-tree dryrun 850/850 - cited in the PR body, not re-captured as files in this bundle at the
  time.
- 2026-08-27 backfill: `evidence/rf_live_run_2026-08-27/` - `output.xml`, `log.html`, `report.html`
  from a fresh live headless run (5/5 PASS), plus `results_summary.md` citing the dryrun/live/
  filter/DB-self-clean/robocop/hygiene numbers above.
