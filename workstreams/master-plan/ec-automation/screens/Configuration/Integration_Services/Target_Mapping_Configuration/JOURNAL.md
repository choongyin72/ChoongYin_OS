# JOURNAL — Target Mapping Configuration (Find-only)

_Screen: Configuration > Integration Services > Import > Target Mapping Configuration (IS.0002).
View `OV_IMP_TARGET_MAPPING`. This JOURNAL was backfilled 2026-08-28 (Batch 12,
`docs/lean-deliverable-backfill-workorder.md`) — the bundle was skipped when the screen was
originally built (PR #488, merged 2026-08-24) under the 2026-08-23/26 lean-waiver rule, which the
owner retired 2026-08-27 (`docs/IUD-DELIVERABLE-CHECKLIST.md` Section H). No RF automation was
touched in this backfill — this JOURNAL documents the original build (from PR #488's real body)
plus this session's re-run for fresh evidence._

## Built (original, PR #488, 2026-08-24)
- `pageobjects/Configuration/Integration_Services/target_mapping_configuration_page.resource` (T3,
  114 lines, new) — Find/read-only keywords only, non-standard navigator/GO ids for this screen.
- `tests/Configuration/Integration_Services/target_mapping_configuration_find.robot` (new suite,
  65 lines, named `_find` not `_iud` since it never inserts/updates/deletes) — TC01 (clean-load)
  + TC04 (find).
- `resources/credentials.py` — additive `TARGET_MAPPING_CONFIGURATION_EC_USER`/`_PASS` (no existing
  lines touched).
- `docs/ec_screen_registry.md` + `docs/automation-scorecard.md` — new registry/scorecard rows.
- No shared T1/T2 file edits — `manage_object.resource`'s Insert/Update/Delete keywords do not
  apply to this screen.

## Done well
- Live DOM recon before writing any test code independently corroborated the owner's own
  statement that this screen has no Insert/Update/Delete — Insert/Delete toolbar `<li>` both
  `ui-submenu-state-disabled`, no Update icon at all (count=0). Two independent sources agreeing,
  not one substituting for the other.
- Reduced-scope suite named honestly (`_find.robot`, not `_iud.robot`) rather than padding out a
  5-TC suite with dead/no-op test cases to match the tree's usual shape.
- Row-identity check applied even though nothing is ever saved: `Row Should Be Found` asserts all
  5 fields match, not just a substring — same spirit as the standing "verify row identity before
  save" rule, extended to a read-only context.

## Done wrong / lessons
- None identified in the original PR — no live-test failures, no wrong-classification, no
  shared-file regression reported. The only disclosed deviation was procedural, not a defect (see
  Decisions below).
- This backfill found no defects either: dryrun, live run, robocop, and hygiene all reproduce the
  same clean result as the original PR.

## Blockers -> resolution
- None. The screen's Find-only nature could have looked like a build blocker (toolbar icons
  visually appear enabled), but the owner's direct statement plus this session's live DOM probe
  resolved it before any test code was written — never escalated as a blocker.

## Decisions
- **Find-only is a permanent scope decision, not a build limitation.** Confirmed by the owner
  directly, then independently re-confirmed via live DOM probe (Insert/Delete `<li>`
  `ui-submenu-state-disabled`; Update icon count=0). This backfill's own re-run (below) reproduces
  the same DB-row-count-unchanged evidence, consistent with that decision — nothing here needed
  revisiting.
- No self-clean check in the usual sense applies (nothing is ever inserted). The equivalent proof
  is a fresh-connection DB row count unchanged across the live run.
- Original build deviated from the prompt's ask for an isolated sparse-checkout clone under
  `Workplaces/`, building instead directly on the feature branch in the main worktree — disclosed
  in the PR body as matching recent practice (PRs #486/#487), not silently diverged.

## Evidence
### Original (PR #488, 2026-08-24)
- Live run: 2/2 pass (TC01 + TC04), `EC_HEADLESS=true`.
- Full `tests/` tree `--dryrun`: 792/792 pass (before and after the live run).
- Robocop: clean (0 issues) on both new files.
- DB row count unchanged: 117 -> 117 (`tmp/tmc_rowcount_check.py`).

### This backfill's re-run (2026-08-28)
- Suite dryrun: 2/2 pass (`Workplaces/target-mapping-configuration-backfill/dryrun/output.xml`).
- Full `tests/` tree dryrun: **883/883 pass** (tree has grown since PR #488's 792, from later
  batches — no collisions), `Workplaces/target-mapping-configuration-backfill/dryrun_tree/output.xml`.
- Live headless run: **2/2 pass** — `screens/Configuration/Integration_Services/
  Target_Mapping_Configuration/evidence/` (`log.html`, `report.html`, `output.xml`,
  `tmc_tc01_clean_load.png`, `tmc_tc04_found.png`, `playwright-log.txt`).
- Robocop on both existing files: `No issues found.`
- Fresh-connection DB row count on `OV_IMP_TARGET_MAPPING`: **117 before -> 117 after** the live
  run — the table is provably untouched, matching the original build's evidence exactly.
- `py scripts/check_bundle_hygiene.py`: `RESULT: PASS` (repo-wide scan; the one WARN reported is
  pre-existing in Contract Area's `investigation/`, unrelated to this screen).
