# Meter Run - IUD Deliverable Checklist (vs docs/IUD-DELIVERABLE-CHECKLIST.md)

_Backfilled 2026-08-28 per `docs/lean-deliverable-backfill-workorder.md` Batch 9 (Section H
retired the 2026-08-23 lean waiver for Bank-pattern conversions). Screen: Configuration > Assets >
Stream_Objects > Meter Run (CO.0091), plain Bank-pattern OV, no navigator. RF automation was
rebuilt to the Bank pattern in PR #462 (2026-08-23, Batch 8) and was NOT modified by this backfill -
this checklist documents that existing, already-verified automation._

## Step 0 - check-existing gate
- [x] **0a** KB map `ec-ui-knowledge/screens/meter_run.md` existed (from the 2026-07-26 original
      build) - read and updated in place for this backfill, not re-scanned from scratch.
- [x] **0b** `grep -ril "meter_run" workstreams/master-plan/ec-automation/{py,pageobjects,tests,screens,testdata}`
      -> existing impl found: `py/meter_run_iud.py`, `pageobjects/.../meter_run_page.resource`,
      `tests/.../meter_run_iud.robot`, this `screens/.../Meter_Run/` bundle, 4
      `testdata/meter_run_*.properties` files. REUSED/EXTENDED (documentation backfill only), no
      parallel copy created.
- [x] **0c** Shared engine/T2 reused (`manage_object.resource`, `libraries/DbVerify.py`,
      `libraries/PropertiesReader.py`) - no changes.

## A. Bundle artifacts
- [x] **1** `meter_run_sow.md` - updated to cover both the 2026-07-26 original build and the
      2026-08-23 Bank-pattern conversion (PR #462).
- [x] **2** `README.md` - updated with exact dryrun/live/DB-self-clean commands.
- [x] **3** `JOURNAL.md` - built/done-well/done-wrong/blockers/decisions/evidence, sourced from
      PR #462's real body (`gh pr view 462`) plus this backfill's own re-run.
- [ ] **4** Playwright driver - **N/A / pre-existing, untouched.** `py/meter_run_iud.py` was built
      2026-07-26, is unmaintained going forward (Universal Screen Engine is the owner-decided
      replacement per Section H of `docs/IUD-DELIVERABLE-CHECKLIST.md`), and was not touched by
      this backfill or by PR #462.
- [ ] **5** `investigation/` - **N/A / pre-existing, untouched.** `investigation/recon.py`
      (2026-07-26) kept as historical record; item 4/5 stay permanently waived for Bank-/
      Area-pattern work per Section H.
- [x] **6** `evidence/` - `evidence/2026-08-28_backfill/` (log.html, report.html, output.xml,
      screenshots from a fresh live 5/5 run) added alongside the pre-existing 2026-07-26
      evidence (`evidence/meter_run_0[1-5]_*.png`, `evidence/rf_report.html`), not overwriting it.
- [x] **7** `CHECKLIST.md` - this file.

## B. RF files (pre-existing, verified not modified by this backfill)
- [x] **8** T3 `pageobjects/Configuration/Assets/Stream_Objects/meter_run_page.resource` -
      properties-file-driven, T2-consolidated, explicit grid-filter wiring (rebuilt PR #462,
      2026-08-23). `git diff` against `origin/master` for this file: none (backfill touched only
      `screens/`, `ec-ui-knowledge/` and this doc set).
- [x] **9** Suite `tests/Configuration/Assets/Stream_Objects/meter_run_iud.robot` - 5-TC (Verify
      Clean State / Insert / Update / Find / Delete), per-TC Login/Logout. Not modified.

## C. Verification gates (this backfill's own re-run, 2026-08-28, plus PR #462's original citation)
- [x] **10** robocop clean - `py -m robocop check pageobjects/.../meter_run_page.resource
      tests/.../meter_run_iud.robot` -> **9 issues** (8x DOC02 missing-test-doc + 1x VAR02) -
      same count/shape PR #462 cited as parity with the accepted `berth_iud.robot` baseline, not
      a regression.
- [x] **11** `--dryrun` - `py -m robot --dryrun tests/Configuration/Assets/Stream_Objects/meter_run_iud.robot`
      -> **5/5 PASS, 0 failed** (2026-08-28 re-run).
- [x] **12** LIVE headless run - `EC_HEADLESS=true py -m robot tests/Configuration/Assets/Stream_Objects/meter_run_iud.robot`
      -> **5/5 PASS, 0 failed** (2026-08-28 re-run, first attempt, no retry needed). Original
      PR #462 citation: live 5/5 (2026-08-23).
- [x] **13** DB ground-truth - `DbVerify.fetch_object("OV_METER_RUN", "AUTOTEST_METER_RUN")` via a
      fresh oracledb connection returned `None` both BEFORE and AFTER the 2026-08-28 live run.
      Suite-internal assertions (unchanged): `Field Should Equal In View OV_METER_RUN
      AUTOTEST_METER_RUN NAME "AUTOTEST Meter Run UPDATED"` (TC03 update) + `Code Should Be
      Present/Absent In View OV_METER_RUN` (TC02 insert / TC05 delete) via T2's `Verify Object
      Insert Exists`/`Verify Object Removed`.
- [x] **14** FULL I-U-D - TC02 Insert, TC03 Update, TC05 Delete all present and passing.
- [x] **15** Self-clean confirmed - fresh-connection DB re-read after the 2026-08-28 live run =
      0 residual `AUTOTEST_METER_RUN` rows in `OV_METER_RUN`.
- [x] **16** Hygiene PASS - `py scripts/check_bundle_hygiene.py --path
      workstreams/master-plan/ec-automation/screens/Configuration/Assets/Stream_Objects/Meter_Run`
      -> `RESULT: PASS` (no hardcoded creds / R16, pure ASCII / R20, no CHECKLIST/VERIFY-REPORT
      contradiction).

## D. Delivery
- [x] **17** Registry row - already present in `docs/ec_screen_registry.md` (added 2026-07-26,
      modified by PR #462 2026-08-23 to reflect the Bank-pattern conversion) - not touched by this
      backfill (documentation/evidence only, no registry re-append needed).
- [x] **18** Scorecard row - already present in `docs/automation-scorecard.md` (same history as
      #17) - not touched by this backfill.
- [x] **19** PR - this backfill's own PR uses the standard body (What was backfilled / Files
      added / Base branch = master); never self-merged.

## E. Knowledge base
- [x] **20** KB selector map `ec-ui-knowledge/screens/meter_run.md` - updated for this backfill to
      reflect the 2026-08-23 Bank-pattern conversion (was stale, still describing the 2026-07-26
      label-driven-only shape and live 4/4).
- [x] **21** Reuse clause - the screen was already implemented (Step 0 found it); this backfill
      produces exactly the reuse-clause deliverables (#3 JOURNAL, #6 evidence, #20 KB map) plus
      the restored #1/#2/#7 per Section H, without rebuilding tests.

_No RF automation file (T3/suite/testdata/py driver) was modified by this backfill - verified via
`git status`/`git diff` in the isolated worktree before committing._
