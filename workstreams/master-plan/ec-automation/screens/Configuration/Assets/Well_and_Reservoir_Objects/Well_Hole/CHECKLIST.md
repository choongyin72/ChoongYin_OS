# Well Hole - IUD Deliverable Checklist (vs docs/IUD-DELIVERABLE-CHECKLIST.md, 21 gates)

_Backfilled 2026-08-28 (Batch 4, `docs/lean-deliverable-backfill-workorder.md`) for the
Area-pattern STRUCTURE conversion (PR #543, merged 2026-08-26). Items 4/5 (Playwright driver +
investigation/) are N/A per Section H of `docs/IUD-DELIVERABLE-CHECKLIST.md` - the Universal
Screen Engine supersedes new hand-written Playwright bundles for Bank-/Area-pattern work; Well
Hole's existing `py/well_hole_iud.py` driver was left untouched by PR #543 and is not re-verified
here. This bundle already had a base-build (2026-07-31) SOW/README/JOURNAL/CHECKLIST/evidence/
investigation/VERIFY-REPORT from before the lean-waiver era - this backfill REFRESHES it to cover
PR #543's conversion, it does not create a duplicate bundle._

## Step 0 - check-existing gate
- [x] 0a - `ec-ui-knowledge/screens/well_hole.md` already existed (from the 2026-07-31 base
      build); refreshed this backfill (item 20 below) rather than re-scanned live - selectors
      transcribed from the current `well_hole_page.resource`.
- [x] 0b - `grep -ril well_hole_page.resource workstreams/master-plan/ec-automation` -> only this
      screen's own files (`pageobjects/.../well_hole_page.resource`,
      `tests/.../well_hole_iud.robot`, `py/well_hole_iud.py`,
      `screens/.../Well_Hole/investigation/recon.py`, `resources/credentials.py`); existing impl
      reused, not duplicated.
- [x] 0c - RF suite reuses the shared T2 `Apply Navigator From Properties`
      (`resources/manage_object.resource`) and T1 `common.resource`/`manage_object.resource`
      keywords throughout; no new shared plumbing added by this backfill.

## A. Bundle artifacts
- [x] **1.** `well_hole_sow.md` - refreshed this backfill: classification, navigator shape (3-level
      SAME-ROW cascade, SPECIFIC "P1" scope), grid, mandatory fields, test data, dev story pulled
      from PR #543's real body (original 2026-07-31 text retained below it for history, not
      deleted).
- [x] **2.** `README.md` - refreshed this backfill: bundle overview + exact dryrun/live-headless/
      live-headed/DB-check commands.
- [x] **3.** `JOURNAL.md` - refreshed this backfill: added the PR #543 conversion entry (Built /
      real gotcha / files touched / cited evidence) and this backfill's own entry (Built / Done
      well / Lessons / Blockers->resolution / Decisions / Evidence), on top of the pre-existing
      2026-07-31 base-build entry (kept, not overwritten).
- [ ] **4.** Playwright driver - **N/A (Section H waiver)**: `py/well_hole_iud.py` pre-exists (live
      8/8, 2026-07-31), unchanged by PR #543; no new driver built for this backfill.
- [ ] **5.** `investigation/` - **N/A (Section H waiver)**: pre-existing `investigation/recon.py`
      folder left as-is; no new recon scripts needed for a documentation-only backfill.
- [x] **6.** `evidence/` - refreshed this backfill: added `output.xml`/`log.html`/`report.html`
      from a real live headless RF run (2026-08-28, 5/5 PASS, first attempt) alongside the
      pre-existing base-build Playwright screenshots (`whl_0[1-5]_*.png`, `results.json`) - both
      kept.
- [x] **7.** `CHECKLIST.md` - this file.

## B. RF files (pre-existing, unmodified by this backfill)
- [x] **8.** T3 `pageobjects/Configuration/Assets/Well_and_Reservoir_Objects/well_hole_page.resource`
      - navigator delegates to shared T2 `Apply Navigator From Properties`; SCREEN-PREFIXED labels
      ("Well Hole Code"/"Well Hole Name"); the `objectdates` End Date cell is the one documented
      hardcoded id.
- [x] **9.** Suite `tests/Configuration/Assets/Well_and_Reservoir_Objects/well_hole_iud.robot` - 5
      TCs (Verify Clean State / Insert / Update / Find / Delete), per-TC login/logout, fixed test
      code `AUTOTEST_WELL_HOLE`.

## C. Verification gates (re-run 2026-08-28 for this backfill, no automation changes made)
- [x] **10.** robocop clean-equivalent - `py -m robocop check pageobjects/.../well_hole_page.resource
      tests/.../well_hole_iud.robot` -> **7 issues** (2x VAR02 unused-var + 5x DOC02
      missing-TC-doc), this session. Cross-checked `py -m robocop check
      pageobjects/.../area_page.resource tests/.../area_iud.robot` (the Area-pattern role model)
      -> also **7 issues**, same VAR02/DOC02 categories - parity confirmed independently, matches
      PR #543's own citation, no regression.
- [x] **11.** `--dryrun` PASS - `py -m robot --dryrun tests/.../well_hole_iud.robot` -> **5 tests,
      5 passed, 0 failed** (2026-08-28 re-run, this backfill).
- [x] **12.** LIVE headless run PASS - `EC_HEADLESS=true py -m robot tests/.../well_hole_iud.robot`
      -> **5 tests, 5 passed, 0 failed** (2026-08-28 re-run, this backfill; FIRST attempt, no retry
      needed; output in `evidence/`).
- [x] **13.** DB ground-truth - fresh oracledb connection (`localhost:1521/ORCL`, `ECKERNEL_EC`,
      via `Workplaces/well-hole-backfill/dbcheck_selfclean.py`), 2026-08-28: `SELECT COUNT(*) FROM
      OV_WELL_HOLE WHERE CODE='AUTOTEST_WELL_HOLE'` -> **0** (post-run); `SELECT CODE, NAME FROM
      OV_WELL_HOLE WHERE UPPER(CODE) LIKE 'AUTOTEST%' OR UPPER(NAME) LIKE 'AUTOTEST%'` -> **[]**
      (no rows). `grep -c "Find Well Hole Row By Filter\|Find Object Row By Filter"` on this
      session's `output.xml` -> **29** (grid-filter keyword confirmed firing, matches PR #543's own
      citation).
- [x] **14.** FULL I-U-D scope - TC02 Insert, TC03 Update, TC04 Find, TC05 Delete all present and
      passing (not I/D only).
- [x] **15.** Self-clean confirmed - independent fresh-connection re-read (item 13) = 0 residual
      `AUTOTEST_WELL_HOLE`/`AUTOTEST%` rows in `OV_WELL_HOLE`.
- [x] **16.** Hygiene PASS - `py scripts/check_bundle_hygiene.py` (repo root, this session) ->
      `RESULT: PASS - no hardcoded creds (R16), pure ASCII (R20), no CHECKLIST/VERIFY-REPORT
      contradictions, doc rows match declared families` (one pre-existing WARN unrelated to Well
      Hole, in Contract Area's `investigation/` scripts).

## D. Delivery
- [x] **17.** Registry row - `docs/ec_screen_registry.md` line 315 for "Well Hole" already reflects
      the Area-pattern conversion (updated in place by PR #543 itself: "converted to Area's full
      pattern 2026-08-26 ... live RF 5/5, DB-verified, self-clean"). This backfill does not
      re-append or re-edit it (append-only / no-duplicate-edit, R23).
- [x] **18.** Scorecard row - `docs/automation-scorecard.md` Well Hole row already updated in place
      by PR #543 ("OK Done 2026-08-26 - converted to Area's full RF pattern ..."); not duplicated
      by this backfill.
- [x] **19.** PR - this backfill's own PR (branch `docs/well-hole-backfill-artifacts`), 6-field
      body, base branch master, isolated worktree, sync-before-push, never self-merge.

## E. Knowledge base
- [x] **20.** KB selector map `ec-ui-knowledge/screens/well_hole.md` - refreshed this backfill
      (existed since the 2026-07-31 base build, describing the OLD first-available-nav/4-TC
      shape): now documents the 3-level SAME-ROW cascade with the SPECIFIC "P1" scope, the shared
      T2 `Apply Navigator From Properties` fill mechanism, SCREEN-PREFIXED field labels, and the
      5-TC structure - transcribed from the current `well_hole_page.resource`'s own
      Variables/Documentation section, not re-scanned live via a fresh DOM probe.
- [x] **21.** Reuse clause - this IS a reuse/backfill run (RF suite already built and merged via PR
      #543): JOURNAL, evidence, and KB map are all freshly refreshed by this backfill, not just
      passing tests alone.

---

## Deviations from the standard 21-item list (stated explicitly, per R-no-silent-deviation)
- Items 4/5 (Playwright driver + investigation/) are marked N/A per the PERMANENT waiver
  (`docs/IUD-DELIVERABLE-CHECKLIST.md` Section H). Well Hole's existing driver/recon folder from
  the 2026-07-31 base build were left completely untouched by both PR #543 and this backfill.
- Items 17/18 (registry/scorecard rows) are NOT re-appended by this backfill - PR #543 itself
  already updated them in place for the conversion, and appending a second row for the same screen
  would violate the append-only, no-duplicate convention (R23).
- The pre-existing `VERIFY-REPORT.md` (2026-07-31, auto-generated by `scripts/verify_screen.py`
  against the OLD 4-TC shape) is kept as a historical record rather than deleted or overwritten
  with a fabricated re-run against a structure it no longer describes; fresh evidence for the
  CURRENT 5-TC suite lives in `evidence/` and this CHECKLIST's own citations instead - same
  approach as the Well backfill (Batch 2).

_Gates 10-16 re-run manually for this backfill (not via `scripts/verify_screen.py`, which targets
the older 4-TC bundle shape) - see JOURNAL.md "Evidence" section and this file's own citations
above for the exact commands and output._
