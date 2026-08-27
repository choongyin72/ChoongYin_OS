# Well - IUD Deliverable Checklist (vs docs/IUD-DELIVERABLE-CHECKLIST.md, 21 gates)

_Backfilled 2026-08-27 (Batch 2, `docs/lean-deliverable-backfill-workorder.md`) for the
Area-pattern STRUCTURE conversion (PR #540, merged 2026-08-26). Items 4/5 (Playwright driver +
investigation/) are N/A per Section H of `docs/IUD-DELIVERABLE-CHECKLIST.md` - the Universal
Screen Engine supersedes new hand-written Playwright bundles for Bank-/Area-pattern work; Well's
existing `py/well_iud.py` driver was left untouched by PR #540 and is not re-verified here._

## Step 0 - check-existing gate
- [x] 0a - `ec-ui-knowledge/screens/well.md` did not exist before this backfill; created now (item
      20 below), no re-scan needed - selectors transcribed from the live `well_page.resource`.
- [x] 0b - `grep -ril well_page.resource workstreams/master-plan/ec-automation` (excluding
      well_bore/well_hole/well_hookup/well_bore_interval) -> only this screen's own files;
      existing impl reused, not duplicated.
- [x] 0c - RF suite reuses the shared T2 `Apply Navigator From Properties`
      (`resources/manage_object.resource`) and T1 `common.resource`/`manage_object.resource`
      keywords throughout; no new shared plumbing added.

## A. Bundle artifacts
- [x] **1.** `well_sow.md` - refreshed this backfill: classification, navigator shape, grid,
      mandatory fields, test data, dev story (base build + PR #540 conversion + canary role).
- [x] **2.** `README.md` - refreshed this backfill: bundle overview + exact dryrun/live/DB-check
      commands.
- [x] **3.** `JOURNAL.md` - refreshed this backfill: Built / Done well / Done wrong-lessons /
      Blockers->resolution / Decisions / Evidence, covering both the base build and PR #540,
      including the regression-canary role not disclosed in PR #540's own body.
- [ ] **4.** Playwright driver - **N/A (Section H waiver)**: `py/well_iud.py` pre-exists,
      unchanged by PR #540; no new driver built for this backfill.
- [ ] **5.** `investigation/` - **N/A (Section H waiver)**: pre-existing `investigation/` folder
      left as-is; no new recon scripts needed for a documentation-only backfill.
- [x] **6.** `evidence/` - refreshed this backfill: added `output.xml`/`log.html`/`report.html`
      from a real live headless RF run (2026-08-27, 5/5 PASS) alongside the pre-existing base-build
      Playwright screenshots (`we_0[1-5]*.png`, `results.json`).
- [x] **7.** `CHECKLIST.md` - this file.

## B. RF files (pre-existing, unmodified by this backfill)
- [x] **8.** T3 `pageobjects/Configuration/Assets/Well_and_Reservoir_Objects/well_page.resource`
      (navigator delegates to shared T2 `Apply Navigator From Properties`; label-driven, no
      hardcoded field ids except the documented `objectdates` End Date cell).
- [x] **9.** Suite `tests/Configuration/Assets/Well_and_Reservoir_Objects/well_iud.robot` - 5 TCs
      (Verify Clean State / Insert / Update / Find / Delete), per-TC login/logout.

## C. Verification gates (re-run 2026-08-27 for this backfill, no automation changes made)
- [x] **10.** robocop clean-equivalent - `robocop check pageobjects/.../well_page.resource
      tests/.../well_iud.robot` -> **7 issues** (2 VAR02 + 5 DOC02), identical categories/count to
      Area's own baseline (parity, no regression) - matches PR #540's own citation.
- [x] **11.** `--dryrun` PASS - `robot --dryrun tests/.../well_iud.robot` -> **5 tests, 5 passed, 0
      failed** (2026-08-27 re-run, this backfill).
- [x] **12.** LIVE headless run PASS - `EC_HEADLESS=true robot tests/.../well_iud.robot` -> **5
      tests, 5 passed, 0 failed** (2026-08-27 re-run, this backfill; output in `evidence/`).
- [x] **13.** DB ground-truth - fresh oracledb connection (`localhost:1521/ORCL`, `ECKERNEL_EC`):
      `SELECT COUNT(*) FROM OV_WELL WHERE CODE='AUTOTEST_WELL'` -> **0** (post-run, 2026-08-27).
      Insert/Update/Delete each verified live via the shared T2's pure-screen checks plus this
      DB self-clean read; PR #540 additionally cited `grep -c "Find Well Row By Filter"
      output.xml` = 14 (grid-filter keyword confirmed firing).
- [x] **14.** FULL I-U-D scope - TC02 Insert, TC03 Update, TC04 Find, TC05 Delete all present and
      passing (not I/D only).
- [x] **15.** Self-clean confirmed - independent fresh-connection re-read (above) = 0 residual
      `AUTOTEST_WELL` rows.
- [x] **16.** Hygiene PASS - `py scripts/check_bundle_hygiene.py` (repo root) -> `RESULT: PASS - no
      hardcoded creds (R16), pure ASCII (R20), no CHECKLIST/VERIFY-REPORT contradictions` (one
      pre-existing WARN unrelated to Well, in Contract Area's `investigation/` scripts).

## D. Delivery
- [x] **17.** Registry row - `docs/ec_screen_registry.md` line 310 for "Well" exists and its
      OV-GM classification/view/navigator facts are still correct, but its narrative text was NOT
      updated by PR #540 (that PR's own "Files touched" list only names
      `docs/automation-scorecard.md`, not the registry) - it still reads "verify_screen PASS
      2026-07-30 - RF 4/4 pass + Playwright 8/8" without mentioning the 5-TC conversion. This is a
      real, disclosed gap, not claimed as fixed: `docs/lean-deliverable-backfill-workorder.md`'s
      per-screen task list (items 1-6) does not include a registry-row update, so it is left
      out-of-scope for this docs/evidence backfill rather than silently edited.
- [x] **18.** Scorecard row - `docs/automation-scorecard.md` Well row updated in place by PR #540
      (cited in that PR's "Files touched" list).
- [x] **19.** PR - this backfill's own PR (docs-only, standard 6-field body, base branch master,
      never self-merged).

## E. Knowledge base
- [x] **20.** KB selector map `ec-ui-knowledge/screens/well.md` - created this backfill (did not
      exist before): nav path, DB view, grid id, selectors incl. the shared `Apply Navigator From
      Properties` call + Well's own testdata properties files, mandatory-yellow fields, quirks,
      last-verified date 2026-08-27.
- [x] **21.** Reuse clause - this IS a reuse/backfill run (RF suite already built and merged via PR
      #540): JOURNAL, evidence, and KB map are all freshly produced/refreshed by this backfill, not
      just passing tests alone.

_Gates 10-16 re-run manually for this backfill (not via `scripts/verify_screen.py`, which targets
the older 4-TC bundle shape) - see JOURNAL.md "Evidence" section and this file's own citations
above for the exact commands and output. The original 2026-07-30 `VERIFY-REPORT.md` in this folder
is kept as a historical record of the base build's own auto-generated gate run; it predates and
does not describe the current 5-TC structure._
