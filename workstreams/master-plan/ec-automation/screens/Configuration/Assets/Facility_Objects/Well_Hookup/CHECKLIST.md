# Well Hookup - IUD Deliverable Checklist (vs docs/IUD-DELIVERABLE-CHECKLIST.md, restored per Section H, 2026-08-27)

_Screen already has a fully working, merged RF suite (Area-pattern conversion, PR #539, merged
2026-08-26). This checklist backfills the documentation/evidence bundle Section H restored; it does
NOT represent a rebuild. Evidence cited below is from a fresh re-run performed 2026-08-27 in an
isolated worktree, plus real facts pulled from PR #539's own body._

## Step 0 - check-existing gate
- [x] **0a.** `ec-ui-knowledge/screens/well_hookup.md` ALREADY EXISTED (from the 2026-07-30 base
      build, describing the pre-conversion 4-TC first-available-navigator shape) - read first, then
      updated in this pass to reflect PR #539's Area-pattern conversion, transcribed from
      `well_hookup_page.resource`'s own Variables section (not re-discovered live).
- [x] **0b.** `grep -ril "well_hookup" workstreams/master-plan/ec-automation/{pageobjects,tests,testdata}`
      -> found the existing, merged RF suite (see file list in `README.md`). REUSED/DOCUMENTED, not
      rebuilt, per this task's own scope.
- [x] **0c.** Confirmed the RF suite already uses the shared T2 `resources/manage_object.resource`
      keywords (`Apply Navigator From Properties`, `Insert/Update Object From Properties`,
      `Verify Object Removed`) - no new plumbing added.

## A. Bundle artifacts
- [x] **1.** `well_hookup_sow.md` - updated to cover the Area-pattern conversion + PR #539 dev story.
- [x] **2.** `README.md` - updated with exact dryrun/live/DB-self-clean commands.
- [x] **3.** `JOURNAL.md` - updated: original 2026-07-30 entry preserved, PR #539 conversion entry
      and this 2026-08-27 backfill entry appended (Built/Done well/Done wrong/Blockers/Decisions/
      Evidence sections).
- [ ] **4.** Playwright flow - **N/A, waived.** Section H (2026-08-27) keeps items 4/5 permanently
      waived for Bank-/Area-pattern work; the Universal Screen Engine (`py/engine.py`) supersedes
      hand-written Playwright drivers. Legacy `py/well_hookup_iud.py` and this bundle's original
      2026-07-30 evidence/investigation left untouched.
- [ ] **5.** `investigation/` - **N/A, waived** (same reason as item 4). Original 2026-07-30
      `investigation/recon.py` left in place, not refreshed.
- [x] **6.** `evidence/` - added `evidence/rf_live_run_2026-08-27/` (`output.xml`, `log.html`,
      `report.html`, `results_summary.md`) from a real live headless run, 2026-08-27. Original
      2026-07-30 `evidence/wh_0[1-5]_*.png` + `results.json` left in place.
- [x] **7.** `CHECKLIST.md` - this file.

## B. RF files (pre-existing, unmodified by this backfill)
- [x] **8.** T3 `pageobjects/Configuration/Assets/Facility_Objects/well_hookup_page.resource`
      (label-driven; docstring documents the Area-pattern conversion).
- [x] **9.** Suite `tests/Configuration/Assets/Facility_Objects/well_hookup_iud.robot` - 5 TCs
      (Verify Clean State / Insert / Update / Find / Delete).

## C. Verification gates - fresh re-run 2026-08-27, isolated worktree `C:/tmp/wt-wellhookup-backfill`
- [x] **10.** robocop - `py -m robocop check` on the T3 + suite -> **7 issues** (2 VAR02 + 5 DOC02).
      Same kind/count as PR #539's own accepted baseline (matches Facility Class 1's/Area's own
      accepted Area-pattern shape - not a regression, not claimed "clean").
- [x] **11.** `robot --dryrun --test "*Well Hookup*" tests/` -> **5/5 PASS**, 0 failed.
- [x] **12.** `EC_HEADLESS=true robot tests/.../well_hookup_iud.robot` -> **5/5 PASS**, 0 failed
      (TC01 Verify Clean State, TC02 Insert, TC03 Update, TC04 Find, TC05 Delete).
- [x] **13.** DB ground-truth - `Verify Object Removed` (shared T2) asserts absence in
      `OV_WELL_HOOKUP`; independently re-checked via a fresh `oracledb` connection:
      `SELECT COUNT(*) FROM OV_WELL_HOOKUP WHERE CODE LIKE 'AUTOTEST%'` -> **0**.
- [x] **14.** FULL I-U-D - Insert (TC02) + Update (TC03) + Delete (TC05) all present and PASS.
- [x] **15.** Self-clean confirmed - fresh-connection re-read above = 0 residual `AUTOTEST%` rows.
- [x] **16.** Hygiene - `py scripts/check_bundle_hygiene.py` (repo-wide) ->
      `[hygiene] RESULT: PASS - no hardcoded creds (R16), pure ASCII (R20), no CHECKLIST/
      VERIFY-REPORT contradictions, doc rows match declared families`.

## D. Delivery (already done at PR #539's merge, 2026-08-26 - not re-done here)
- [x] **17.** Registry row - `docs/ec_screen_registry.md` Well Hookup row already reflects the
      Area-pattern conversion (5 TCs, `AUTOTEST_WH`, live 5/5, self-clean 0, filter fired 15x,
      full-tree dryrun 850/850).
- [x] **18.** Scorecard row - `docs/automation-scorecard.md` Well Hookup row already updated at
      PR #539's merge.
- [x] **19.** PR - this backfill's own PR uses the standard body (What backfilled / Files added /
      Base branch = master); never self-merged.

## E. Knowledge base
- [x] **20.** KB map `ec-ui-knowledge/screens/well_hookup.md` - already existed (2026-07-30 base
      build); updated in this backfill pass to reflect PR #539's Area-pattern conversion (navigator
      now explicit not first-available, 5 TCs not 4, screen-prefixed labels, del-enddate exception
      documented). Transcribed from `well_hookup_page.resource`'s Variables section, not
      re-discovered live.
- [x] **21.** Reuse clause - the screen was ALREADY implemented (Step 0 confirmed); this backfill
      produces exactly what the clause requires: refreshed **#3 JOURNAL**, fresh **#6 evidence**,
      and new **#20 KB map** - "done" is not just the already-passing tests.

_Gates 10-16 above are from a fresh manual re-run in this backfill session (not `verify_screen.py`,
since that script targets new builds; commands and raw output are recorded in
`evidence/rf_live_run_2026-08-27/results_summary.md`). See `VERIFY-REPORT.md` for the
originally-auto-generated 2026-07-30 report (kept for history, now superseded in scope by this
CHECKLIST's own Section C)._
