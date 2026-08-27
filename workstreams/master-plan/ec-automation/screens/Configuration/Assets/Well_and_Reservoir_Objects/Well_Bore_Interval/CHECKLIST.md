# Well Bore Interval - IUD Deliverable Checklist (vs docs/IUD-DELIVERABLE-CHECKLIST.md, 21 gates)

_Backfilled 2026-08-28 (Batch 5, `docs/lean-deliverable-backfill-workorder.md`) for the
Area-pattern STRUCTURE conversion (PR #563, merged 2026-08-27). Items 4/5 (Playwright driver +
investigation/) are N/A per Section H of `docs/IUD-DELIVERABLE-CHECKLIST.md` - the Universal
Screen Engine supersedes new hand-written Playwright bundles for Bank-/Area-pattern work; Well
Bore Interval's existing `py/well_bore_interval_iud.py` driver was left untouched by PR #563 and
is not re-verified here. This bundle already had a base-build (2026-07-31)
SOW/README/JOURNAL/CHECKLIST/evidence/investigation/VERIFY-REPORT from before the lean-waiver era
- this backfill REFRESHES it to cover PR #563's conversion, it does not create a duplicate
bundle._

## Step 0 - check-existing gate
- [x] 0a - `ec-ui-knowledge/screens/well_bore_interval.md` already existed (from the 2026-07-31
      base build); refreshed this backfill (item 20 below) rather than re-scanned live - selectors
      transcribed from the current `well_bore_interval_page.resource`.
- [x] 0b - `grep -rli well_bore_interval workstreams/master-plan/ec-automation` -> only this
      screen's own files (`pageobjects/.../well_bore_interval_page.resource`,
      `tests/.../well_bore_interval_iud.robot`, `testdata/well_bore_interval_*.properties`,
      `py/well_bore_interval_iud.py`, `screens/.../Well_Bore_Interval/investigation/*.py`,
      `resources/credentials.py`); existing impl reused, not duplicated.
- [x] 0c - RF suite uses a BESPOKE screen-local T3 navigator keyword
      (`Apply Well Bore Interval Navigator`) because the shared T2 `Apply Navigator From
      Properties` (`resources/manage_object.resource`) genuinely does not support this screen's
      per-field-groups navigator shape (confirmed live, twice) - `manage_object.resource` was NOT
      touched by PR #563 or this backfill; everything else (Find/Clear filter, Insert/Update
      Object From Properties, Verify Object * family) reuses the shared T2/T1 keywords.

## A. Bundle artifacts
- [x] **1.** `well_bore_interval_sow.md` - refreshed this backfill: classification, navigator
      shape (genuine PER-FIELD groups G:1-G:4 + G:6, skip G:5), grid, mandatory fields, test data,
      dev story pulled from PR #563's real body (original 2026-07-31 text retained below it for
      history, not deleted), including why a bespoke T3 keyword was used instead of the shared
      one.
- [x] **2.** `README.md` - refreshed this backfill: bundle overview + exact dryrun/live-headless/
      live-headed/DB-check commands.
- [x] **3.** `JOURNAL.md` - refreshed this backfill: added the PR #563 conversion entry (Built /
      real gotcha / files touched / cited evidence) and this backfill's own entry (Built / Done
      well / Lessons / Blockers->resolution / Decisions / Evidence), on top of the pre-existing
      2026-07-31 base-build entry (kept, not overwritten).
- [ ] **4.** Playwright driver - **N/A (Section H waiver)**: `py/well_bore_interval_iud.py`
      pre-exists (live 8/8, 2026-07-31), unchanged by PR #563; no new driver built for this
      backfill.
- [ ] **5.** `investigation/` - **N/A (Section H waiver)**: pre-existing `investigation/recon.py` /
      `investigation/recon_wbi.py` folder left as-is; no new recon scripts needed for a
      documentation-only backfill.
- [x] **6.** `evidence/` - refreshed this backfill: added `output.xml`/`log.html`/`report.html`
      from a real live headless RF run (2026-08-28, 5/5 PASS, first attempt) alongside the
      pre-existing base-build Playwright screenshots (`wbi_0[1-5]_*.png`/`wbi_01b_*.png`,
      `results.json`) - both kept.
- [x] **7.** `CHECKLIST.md` - this file.

## B. RF files (pre-existing, unmodified by this backfill)
- [x] **8.** T3
      `pageobjects/Configuration/Assets/Well_and_Reservoir_Objects/well_bore_interval_page.resource`
      - BESPOKE `Apply Well Bore Interval Navigator` keyword (per-field groups G:1/G:2/G:3/G:4/G:6
      via `Select Nav Group Value`, one GO), screen-local `Pick Well Bore Popup` (list grid
      `Objects:form:T_data`), SCREEN-PREFIXED labels ("Well Bore Interval Code"/"Well Bore
      Interval Name"); the `objectdates` End Date cell is the one documented hardcoded id.
- [x] **9.** Suite
      `tests/Configuration/Assets/Well_and_Reservoir_Objects/well_bore_interval_iud.robot` - 5 TCs
      (Verify Clean State / Insert / Update / Find / Delete), per-TC login/logout, fixed test code
      `AUTOTEST_WBI`.

## C. Verification gates (re-run 2026-08-28 for this backfill, no automation changes made)
- [x] **10.** robocop clean-equivalent - `py -m robocop check pageobjects/.../well_bore_interval_page.resource
      tests/.../well_bore_interval_iud.robot` -> **7 issues** (2x VAR02 unused-var + 5x DOC02
      missing-TC-doc), this session. Cross-checked
      `py -m robocop check pageobjects/Configuration/Assets/Basic_Objects/area_page.resource
      tests/Configuration/Assets/Basic_Objects/area_iud.robot` (the Area-pattern role model) ->
      also **7 issues**, same VAR02/DOC02 categories - parity confirmed independently, matches
      PR #563's own citation, no regression.
- [x] **11.** `--dryrun` PASS - `py -m robot --dryrun tests/.../well_bore_interval_iud.robot` ->
      **5 tests, 5 passed, 0 failed** (2026-08-28 re-run, this backfill).
- [x] **12.** LIVE headless run PASS - `EC_HEADLESS=true py -m robot
      tests/.../well_bore_interval_iud.robot` -> **5 tests, 5 passed, 0 failed** (2026-08-28
      re-run, this backfill; FIRST attempt, no retry needed; output in `evidence/`).
- [x] **13.** DB ground-truth - fresh oracledb connection (`localhost:1521/ORCL`, `ECKERNEL_EC`,
      via `Workplaces/well-bore-interval-backfill/dbcheck_selfclean.py`), 2026-08-28: `SELECT
      COUNT(*) FROM OV_WELL_BORE_INTERVAL WHERE CODE='AUTOTEST_WBI'` -> **0** (post-run); `SELECT
      CODE, NAME FROM OV_WELL_BORE_INTERVAL WHERE UPPER(CODE) LIKE 'AUTOTEST%' OR UPPER(NAME) LIKE
      'AUTOTEST%'` -> **[]** (no rows). `grep -c "Find Well Bore Interval Row By Filter\|Find
      Object Row By Filter"` on this session's `output.xml` -> **27** (grid-filter keyword
      confirmed firing; PR #563's own separate-run citation was 15, both non-zero/consistent).
- [x] **14.** FULL I-U-D scope - TC02 Insert, TC03 Update, TC04 Find, TC05 Delete all present and
      passing (not I/D only).
- [x] **15.** Self-clean confirmed - independent fresh-connection re-read (item 13) = 0 residual
      `AUTOTEST_WBI`/`AUTOTEST%` rows in `OV_WELL_BORE_INTERVAL`.
- [x] **16.** Hygiene PASS - `py scripts/check_bundle_hygiene.py` (repo root, this session) ->
      `RESULT: PASS - no hardcoded creds (R16), pure ASCII (R20), no CHECKLIST/VERIFY-REPORT
      contradictions, doc rows match declared families` (one pre-existing WARN unrelated to Well
      Bore Interval, in Contract Area's `investigation/` scripts).

## D. Delivery
- [x] **17.** Registry row - `docs/ec_screen_registry.md` line 316 for "Well Bore Interval" already
      reflects the Area-pattern conversion (updated in place by PR #563 itself: "converted to
      Area's full pattern 2026-08-27 ... live RF 5/5, DB self-clean, BESPOKE screen-local T3
      navigator keyword"). This backfill does not re-append or re-edit it (append-only /
      no-duplicate-edit, R23).
- [x] **18.** Scorecard row - `docs/automation-scorecard.md` Well Bore Interval row already updated
      in place by PR #563 ("OK Done 2026-07-31 (base IUD, Playwright 8/8) - MODIFIED 2026-08-27:
      FULL Area-pattern structural conversion ..."); not duplicated by this backfill.
- [x] **19.** PR - this backfill's own PR (branch
      `docs/well-bore-interval-backfill-artifacts`), 6-field body, base branch master, isolated
      worktree, sync-before-push, never self-merge.

## E. Knowledge base
- [x] **20.** KB selector map `ec-ui-knowledge/screens/well_bore_interval.md` - refreshed this
      backfill (existed since the 2026-07-31 base build, describing the OLD 4-TC shape): now
      documents the BESPOKE `Apply Well Bore Interval Navigator` T3 keyword's group sequence
      (G:1/G:2/G:3/G:4/G:6, skip G:5), the screen-local `Pick Well Bore Popup`, and the 5-TC
      structure - transcribed from the current `well_bore_interval_page.resource`'s own
      Variables/Documentation section, not re-scanned live via a fresh DOM probe.
- [x] **21.** Reuse clause - this IS a reuse/backfill run (RF suite already built and merged via PR
      #563): JOURNAL, evidence, and KB map are all freshly refreshed by this backfill, not just
      passing tests alone.

---

## Deviations from the standard 21-item list (stated explicitly, per R-no-silent-deviation)
- Items 4/5 (Playwright driver + investigation/) are marked N/A per the PERMANENT waiver
  (`docs/IUD-DELIVERABLE-CHECKLIST.md` Section H). Well Bore Interval's existing driver/recon
  folder from the 2026-07-31 base build were left completely untouched by both PR #563 and this
  backfill.
- Items 17/18 (registry/scorecard rows) are NOT re-appended by this backfill - PR #563 itself
  already updated them in place for the conversion, and appending a second row for the same screen
  would violate the append-only, no-duplicate convention (R23).
- The pre-existing `VERIFY-REPORT.md` (2026-07-31, auto-generated by `scripts/verify_screen.py`
  against the OLD 4-TC shape) is kept as a historical record rather than deleted or overwritten
  with a fabricated re-run against a structure it no longer describes; fresh evidence for the
  CURRENT 5-TC suite lives in `evidence/` and this CHECKLIST's own citations instead - same
  approach as the Well/Well Hole backfills (Batches 2/4).

_Gates 10-16 re-run manually for this backfill (not via `scripts/verify_screen.py`, which targets
the older 4-TC bundle shape) - see JOURNAL.md "Evidence" section and this file's own citations
above for the exact commands and output._
