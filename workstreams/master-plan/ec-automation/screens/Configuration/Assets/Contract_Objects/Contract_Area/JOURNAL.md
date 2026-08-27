# JOURNAL — Contract Area IUD

_Screen: Configuration > Assets > Contract Objects > Contract Area (OV-GM groupmodel,
Business-Unit-gated). View `OV_CONTRACT_AREA`. This JOURNAL was backfilled 2026-08-27 under the
retired-lean-waiver work order (`docs/lean-deliverable-backfill-workorder.md`, Batch 2; Section H
of `docs/IUD-DELIVERABLE-CHECKLIST.md`) — the bundle's SOW/README/evidence/playwright/
investigation predated the JOURNAL rule; PR #542 (the Area-pattern conversion) is the source of
the "Built" and "Done well" content below, pulled from its real PR body and the reviewer's real
merge comment, not invented._

## Built

### Original build (2026-06-18)
- Playwright reference `playwright/ec_iud_contract_area.py`, full recon trail in
  `investigation/` (`db_recon_contract_area.py`, `live_recon_contract_area.py`,
  `bu_distribution.py`, `treeview_path.py`, `grid_columns.py`).
- RF suite (4 TC, suite-level login, bespoke inline navigator) — `contract_area_page.resource` +
  `contract_area_iud.robot`.

### Area-pattern conversion (PR #542, merged 2026-08-26)
- Converted the RF IUD suite from the OLD bespoke-navigator/4-TC/suite-level-login pattern to the
  full Area-pattern structure, mirroring `area_page.resource`/`area_iud.robot` exactly:
  properties-file-driven navigator via the shared `Apply Navigator From Properties` T2 keyword
  (`resources/manage_object.resource`, added 2026-08-26), per-TC login/logout, 5 TCs (added TC04
  Find), a fixed test code (`AUTOTEST_CONTRACT_AREA`, confirmed 0 rows before use, replacing the
  old timestamped code), a dedicated credentials pair (`CONTRACT_AREA_EC_USER`/
  `CONTRACT_AREA_EC_PASS` in `resources/credentials.py`), explicit grid-filter wiring (`Find/Clear
  Contract Area Row By Filter`), and zero inline DB-verify calls left in the `.robot` file (the
  old screen-local `Contract Area Should Exist/Not Exist In DB` wrappers were removed — DB proof
  now comes solely from the shared T2 `Verify Object Removed` + the mandatory live-run self-clean
  check).
- New test-data files: `testdata/contract_area_{navigator,insert,update,form_verify,
  grid_verify}.properties`.
- The screen's genuine Business Unit navigator + GO gesture was KEPT unchanged — this was a
  structural conversion, not a reclassification of the screen as plain Bank-shaped.
- Registry (`docs/ec_screen_registry.md`) and scorecard (`docs/automation-scorecard.md`) rows
  MODIFIED in place (not new rows).

### This backfill (2026-08-27)
- Added `contract_area_sow.md` §3.2 (real PR #542 dev story, including the branch-collision
  incident below), this `JOURNAL.md`, `CHECKLIST.md`, the KB selector map
  `ec-ui-knowledge/screens/contract_area.md`, and `evidence/backfill_2026-08-27/` (fresh dryrun +
  live re-run captured as evidence of the already-proven suite — no automation code touched).

## Done well
- Full I-U-D DB-verified vs `OV_CONTRACT_AREA` (insert Contract Area Code/Name, update Contract
  Area Name, delete End=Start absent); self-clean 0 residual, confirmed via a FRESH oracledb
  connection both before and after the live run (PR #542 body: pre-run check found the fixed test
  code free, independent post-run self-clean check found 0 residual `AUTOTEST%` rows).
- Screen-prefixed labels confirmed live, not assumed: PR #542's page object documents that
  `objectForm`/`updateAttributes` use "Contract Area Code"/"Contract Area Name" (SCREEN-PREFIXED,
  like Area's own "Area Code"/"Area Name"), NOT the generic "Code"/"Name" that Bank/Object List
  use — confirmed against this screen's own screenshot evidence
  (`ca_04_insert_filled.png`/`ca_06_update_result.png`) before wiring the T2 `code_label`
  parameter.
- Full-tree dryrun stayed 100% pass (851/851) before the live run (per PR #542 body); this
  backfill's own fresh dryrun re-confirmed the Contract Area suite alone: 5/5 PASS.
- `resources/manage_object.resource` (shared T2) was NOT modified for this conversion beyond the
  addition (2026-08-26, same day, shared across the batch) of `Apply Navigator From Properties` —
  no Contract-Area-specific gap found.
- Robocop parity check performed and passed: 7 issues (2x VAR02 + 5x DOC02) on the 2 changed
  files, identical count/kind to Area's own established baseline — confirmed independently again
  during this backfill.

## Done wrong / lessons
- **Real branch-name collision incident, disclosed at merge, NOT smoothed over here:** PR #542
  was raised from `feature/contract-area-pattern-conversion`. A separate, parallel task
  converting the sibling **Contract** screen (PR #546) was independently assigned the SAME branch
  name. That agent's worktree was created from a point that already contained Contract Area's
  commit, and pushing there silently appended the Contract commit on top of Contract Area's own
  commit on this shared branch/PR. PR #546's own body disclosed the collision and stated its
  attempted force-push cleanup was blocked by the environment's own safety guardrail (no
  destructive rewrite of an already-published PR branch without explicit authorization) — leaving
  a human/owner decision needed on how to clean it up. The reviewer's merge comment on PR #542
  confirms the resolution before merge: *"Before merging, I verified the branch-collision cleanup
  #546 disclosed: this branch is back at its clean single Contract Area commit (`1b0c874`), own 10
  files only — the accidental Contract-commit append was fully undone on the remote before
  review."* Contract Area's own conversion content and RF suite were never at issue — only the
  shared branch/PR was transiently affected by a naming collision between two independently
  dispatched agents, and it was clean again before this PR was reviewed and merged.
- No other regressions or wrong turns disclosed in PR #542's body for this specific conversion.
- Backfill-specific: none — the dryrun, live run, DB self-clean, filter-fired grep, robocop
  parity check, and hygiene check all reproduced PR #542's cited results on the first attempt
  during this backfill session.

## Blockers -> resolution
- **Branch-name collision** (see above) — resolved by the sibling PR #546's own cherry-pick +
  disclosure, and confirmed clean by the reviewer before PR #542 was merged. No data loss: Contract
  Area's commit (`1b0c874`) and its 10 own files were preserved; only a transient double-commit on
  the shared branch, undone before review.
- No other hard blockers during the original conversion or this backfill; the dryrun, live run,
  DB self-clean, and hygiene check all passed on the first real attempt.

## Decisions
- Playwright bundle stays waived permanently for this backfill (owner decision 2026-08-27,
  `docs/IUD-DELIVERABLE-CHECKLIST.md` Section H) — the existing `playwright/ec_iud_contract_area.py`
  from the 2026-06-18 build is preserved as-is and was NOT touched, re-verified, or regenerated.
  The Universal Screen Engine is the owner-decided replacement for hand-written Playwright drivers
  going forward.
- The RF suite remains the maintained/live test; the Playwright driver is historical reference
  only (README.md updated to say so explicitly).
- Code lives in `ec-automation`; `ec-ui-knowledge/` stays MD-only.

## Evidence
- Original build (2026-06-18): `evidence/ca_0[1-9]_*.png` (9 screenshots) +
  `evidence/ec_iud_contract_area_result.json` (4-TC Playwright/RF run, `results/ca_live2/`).
- PR #542 conversion (2026-08-26): live run `5 tests, 5 passed, 0 failed` (TC01-TC05), 15 `Find
  Object Row By Filter` hits in output.xml, robocop 7 issues (parity with Area), full-tree dryrun
  851/851 — all cited in the PR body; not re-captured as new screenshots at conversion time (RF
  run, not Playwright).
- This backfill (2026-08-27): `evidence/backfill_2026-08-27/` — `dryrun/` (5/5 PASS,
  `log.html`/`report.html`/`output.xml`) and `live/` (5/5 PASS headless,
  `log.html`/`report.html`/`output.xml`), plus a DB self-clean result (`OV_CONTRACT_AREA`: 0 rows
  for `AUTOTEST_CONTRACT_AREA`, 0 residual `AUTOTEST%`, fresh connection, both pre- and post-run),
  a re-confirmed 15-hit filter-fired grep, a re-confirmed 7-issue robocop parity check against
  Area's own baseline, and `py scripts/check_bundle_hygiene.py` → `RESULT: PASS`.
