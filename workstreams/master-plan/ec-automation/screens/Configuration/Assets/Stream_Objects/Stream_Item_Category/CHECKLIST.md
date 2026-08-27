# Stream Item Category - IUD Deliverable Checklist (vs docs/IUD-DELIVERABLE-CHECKLIST.md, 21 gates)

_Backfilled 2026-08-28 per `docs/lean-deliverable-backfill-workorder.md` (Batch 11) - Stream Item
Category was converted to the full Bank pattern in PR #473 (merged 2026-08-23, Batch 10 of the
Bank-pattern conversion project). Section H (2026-08-27) retired the 2026-08-23/26 lean waiver
except for items 4/5 (Playwright driver + investigation/), which stay permanently waived - the
Universal Screen Engine replaces that role. This checklist backfills the restored items; it does
not re-build or re-verify the RF automation itself (already proven at PR #473's merge, plus a
2026-08-25 alignment-fix note in the registry). **NOT** the same screen as "Stream Item Category
Split Key" (CD.0042, class `SPLIT_KEY`) - confirmed via `grep -ril "stream_item_category_page
.resource"` excluding any `split_key` hit before starting this backfill._

## Step 0 - check-existing gate
- [x] 0a. KB map exists (`ec-ui-knowledge/screens/stream_item_category.md`, refreshed by this
      backfill).
- [x] 0b. `grep -ril "stream_item_category_page.resource" workstreams/master-plan/ec-automation/
      {py,pageobjects,tests,screens}` -> existing impl found: `pageobjects/Configuration/Assets/
      Stream_Objects/stream_item_category_page.resource`, `tests/Configuration/Assets/
      Stream_Objects/stream_item_category_iud.robot`, `docs/ec_screen_registry.md` row. Reused/
      updated in PR #473, NOT duplicated. This backfill adds documentation only, no code path was
      re-derived.
- [x] 0c. Shared engine reused - RF suite calls the shared T2 `resources/manage_object.resource`
      keywords (`Apply Navigator`, `Insert/Update/Find Object From Properties`, `Find/Clear
      Object Row By Filter`, `Verify Object Removed`) + `libraries/DbVerify.py`; no per-screen
      plumbing added.

## A. Bundle artifacts
- [x] **1.** `stream_item_category_sow.md` - refreshed this backfill (was describing the
      pre-PR#473 4-TC/no-filter/generated-code shape; now reflects PR #473's Bank-pattern
      conversion).
- [x] **2.** `README.md` - refreshed this backfill with exact dryrun/live/DB-self-clean commands.
- [x] **3.** `JOURNAL.md` - refreshed this backfill: the 2026-07-26 original-build entry kept,
      2026-08-23 PR #473 conversion entry added from the real PR body, the 2026-08-25 alignment-
      fix entry added from the registry note, plus this backfill's own 2026-08-28 entry.
- [ ] **4.** Playwright driver - **N/A / permanently waived** (owner decision 2026-08-27,
      Universal Screen Engine replaces this role). Pre-existing `py/stream_item_category_iud.py`
      from the 2026-07-26 build is untouched by this backfill and by PR #473.
- [ ] **5.** `investigation/` - **N/A / permanently waived**, same reason as item 4. The
      pre-existing `investigation/` folder (recon.py from 2026-07-26) is left as-is.
- [x] **6.** `evidence/` - this backfill added `dryrun_output.xml` (5/5 pass), `live_output.xml`
      + `live_report.html` + `live_log.html` (5/5 pass, first attempt, no retry needed). The
      pre-existing `stream_item_category_0[1-5]_*.png` + `rf_report.html` from the 2026-07-26
      Playwright run are kept as historical evidence, not removed.
- [x] **7.** `CHECKLIST.md` - this file.

## B. RF files (pre-existing, verified not re-verified from scratch - already proven at PR #473)
- [x] **8.** T3 `pageobjects/Configuration/Assets/Stream_Objects/stream_item_category_page
      .resource` (label-driven, no hardcoded ids except the documented `objectdates` End Date
      constant - confirmed by reading the file, not touched by this backfill).
- [x] **9.** Suite `tests/Configuration/Assets/Stream_Objects/stream_item_category_iud.robot`
      (5 TCs, per-TC login/logout - confirmed by reading the file, not touched by this backfill).

## C. Verification gates (re-run once for this backfill's evidence capture, not a fresh build cycle)
- [x] **10.** robocop - `robocop check pageobjects/.../stream_item_category_page.resource
      tests/.../stream_item_category_iud.robot` -> **9 issues, all DOC02** (missing
      `[Documentation]` on TC02-05 plus a shared-file DOC02 hit, same baseline-noise class the
      Bank/Storage backfills already cite - no new issue class).
- [x] **11.** `--dryrun` - **5/5 PASS** (`evidence/dryrun_output.xml`, 2026-08-28).
- [x] **12.** LIVE headless run - **5/5 PASS on first attempt**, no retry needed
      (`evidence/live_output.xml`/`live_report.html`/`live_log.html`, 2026-08-28) - cited as this
      backfill's live evidence.
- [x] **13.** DB ground-truth - fresh `oracledb` connection (`ECKERNEL_EC`/`localhost:1521/ORCL`,
      via `libraries/DbVerify.py`'s default): `SELECT CODE, NAME FROM OV_STREAM_ITEM_CATEGORY
      WHERE CODE LIKE 'AUTOTEST%'` -> empty result set, both before and after the run (matching
      the same query cited in PR #473's own body).
- [x] **14.** FULL I-U-D scope - Insert (TC02) + Update (TC03) + Delete (TC05) all present and
      passed in this backfill's live run.
- [x] **15.** Self-clean confirmed - fresh-connection query above returned 0 residual rows after
      the run.
- [x] **16.** Hygiene PASS - `py scripts/check_bundle_hygiene.py` -> `RESULT: PASS` (no hardcoded
      creds / R16, pure ASCII / R20, no CHECKLIST/VERIFY-REPORT contradiction). The 2 WARN lines
      it reports belong to an unrelated screen (Contract_Area), not Stream Item Category.

## D. Delivery
- [x] **17.** Registry row - `docs/ec_screen_registry.md` Stream Item Category row already
      updated at PR #473's merge (2026-08-23) and the 2026-08-25 alignment-fix note; unchanged by
      this backfill.
- [x] **18.** Scorecard row - `docs/automation-scorecard.md` Stream Item Category row already
      updated at PR #473's merge; unchanged by this backfill.
- [x] **19.** PR - this backfill's own PR (docs/stream-item-category-backfill-artifacts), 6-field
      body, base = master, never self-merged.

## E. Knowledge base
- [x] **20.** KB selector map `ec-ui-knowledge/screens/stream_item_category.md` - refreshed this
      backfill from the pre-PR#473 shape (4-TC/generated-code) to reflect PR #473's fixed-code
      (`AUTOTEST_SIC`)/per-TC-login/explicit-grid-filter shape, pulled from
      `stream_item_category_page.resource`'s own Variables section.
- [x] **21.** Reuse clause - this IS a reuse/refresh run (screen already implemented, converted
      under PR #473): JOURNAL, evidence, and KB map are all refreshed/produced by this backfill,
      per the reuse-clause requirement - not just passing tests.
