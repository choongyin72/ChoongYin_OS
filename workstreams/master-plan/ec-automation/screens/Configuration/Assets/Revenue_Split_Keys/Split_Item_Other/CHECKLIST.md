# Split Item Other - IUD Deliverable Checklist (vs docs/IUD-DELIVERABLE-CHECKLIST.md, 21 gates)

_This bundle was originally built 2026-07-26, converted to the Bank pattern 2026-08-23 (PR #471),
and had its documentation/evidence retroactively backfilled 2026-08-28 per
`docs/lean-deliverable-backfill-workorder.md` (Batch 10, last screen) after Section H retired the
2026-08-23/26 lean waiver. Playwright driver (#4) and investigation/ (#5) stay waived per Section
H - the Universal Screen Engine is the owner-decided replacement for hand-written Playwright
drivers going forward._

## Step 0 - check-existing gate
- [x] **0a.** `ec-ui-knowledge/screens/split_item_other.md` existed (from the 2026-07-26 build) -
      refreshed in this backfill to reflect the 2026-08-23 Bank-pattern shape rather than
      re-scanned from scratch.
- [x] **0b.** `grep -ril "split_item_other" .../{py,pageobjects,tests,screens}` -> found: existing
      T3/suite/testdata/py driver/screens bundle (see README.md Artifacts) - REUSED/EXTENDED, no
      parallel copy built.
- [x] **0c.** Reused shared T2 (`manage_object.resource`) grid-filter keyword and `DbVerify.py` -
      zero engine/shared-file changes in PR #471 or this backfill.

## A. Bundle artifacts - `screens/Configuration/Assets/Revenue_Split_Keys/Split_Item_Other/`
- [x] **1.** `split_item_other_sow.md` - refreshed 2026-08-28 to describe the Bank-pattern shape
      (classification, nav/grid/cells, test data, dev story pulled from PR #471's real body).
- [x] **2.** `README.md` - refreshed 2026-08-28: bundle overview + exact dryrun/live/DB-self-clean
      commands.
- [x] **3.** `JOURNAL.md` - refreshed 2026-08-28: Built/Done well/Done wrong/Blockers/Decisions/
      Evidence per era (2026-07-26 build, 2026-08-23 PR #471 rebuild, 2026-08-28 backfill).
- [ ] **4.** Playwright bundle - **WAIVED** (Section H: superseded by the Universal Screen Engine;
      pre-existing `py/split_item_other_iud.py` untouched, not rebuilt).
- [ ] **5.** `investigation/` - **WAIVED** (Section H, same reasoning as #4); pre-existing
      `investigation/recon.py` from the 2026-07-26 build left as-is, not rebuilt.
- [x] **6.** `evidence/` - existing 2026-07-26 screenshots + `rf_report.html` kept; added
      `evidence/2026-08-28_live_output.xml` + `evidence/2026-08-28_live_log.html` from a fresh
      live re-run captured for this backfill (5/5 pass, both files <400KB).
- [x] **7.** `CHECKLIST.md` - this file.

## B. RF files (pre-existing, NOT modified by this backfill)
- [x] **8.** T3 `pageobjects/Configuration/Assets/Revenue_Split_Keys/split_item_other_page.resource`
      (properties-file-driven, T2-consolidated per PR #471; untouched by this task).
- [x] **9.** Suite `tests/Configuration/Assets/Revenue_Split_Keys/split_item_other_iud.robot`
      (5-TC: clean-state/insert/update/find/delete; untouched by this task).

## C. Verification gates - re-run 2026-08-28 for this backfill (evidence, not hand-typed)
- [x] **10.** robocop - `py -m robocop check pageobjects/.../split_item_other_page.resource
      tests/.../split_item_other_iud.robot` -> exit 1, 9 issues, all DOC02 (missing
      `[Documentation]` on TC03/TC04/TC05) - same baseline as the merged `berth_iud.robot`
      exemplar per PR #471's own citation; no new regression introduced by this backfill (no
      code was changed).
- [x] **11.** `--dryrun` - `python -m robot --dryrun tests/.../split_item_other_iud.robot` ->
      **5/5 pass, 0 fail** (`results/_dryrun_split_item_other/output.xml`, 2026-08-28).
- [x] **12.** LIVE run - `EC_HEADLESS=true python -m robot tests/.../split_item_other_iud.robot`
      -> **5/5 pass, 0 fail** (`evidence/2026-08-28_live_output.xml`/`_live_log.html`,
      2026-08-28). First attempt succeeded - no retry needed.
- [x] **13.** DB ground-truth - `Verify Object Insert Exists`/`Verify Object Form Record`/
      `Verify Object Found` (screen-only checks per Bank/Berth convention) + a direct fresh
      `oracledb` connection query `SELECT CODE, NAME FROM OV_SPLIT_ITEM_OTHER WHERE CODE LIKE
      'AUTOTEST%'` run independently before/after the 2026-08-28 live run - 0 rows both times
      until TC02 inserts, 0 rows again after TC05 deletes.
- [x] **14.** FULL I-U-D - TC02 Insert / TC03 Update / TC04 Find / TC05 Delete all present and
      passing in the live run.
- [x] **15.** Self-clean - fresh-connection re-read after the 2026-08-28 live run: 0 residual
      `AUTOTEST_SIO` rows in `OV_SPLIT_ITEM_OTHER`.
- [x] **16.** Hygiene - `py scripts/check_bundle_hygiene.py` -> `[hygiene] RESULT: PASS` (no
      hardcoded creds, pure ASCII, no CHECKLIST/VERIFY-REPORT contradiction for this bundle; one
      unrelated WARN reported for a different screen's, Contract Area's, recon script - not this
      one).

## D. Delivery
- [x] **17.** Registry row - already present and current in
      `workstreams/master-plan/ec-automation/docs/ec_screen_registry.md` (updated by PR #471,
      2026-08-23) - not re-added, not touched by this backfill.
- [x] **18.** Scorecard row - already present and current in `docs/automation-scorecard.md`
      (updated by PR #471, 2026-08-23) - not re-added, not touched by this backfill.
- [x] **19.** PR - this backfill's own PR uses the standard body (What was backfilled / Files
      added / Base branch = master); never self-merged.

## E. Knowledge base
- [x] **20.** KB map `ec-ui-knowledge/screens/split_item_other.md` - refreshed 2026-08-28 to
      describe the current Bank-pattern shape (properties-file-driven, explicit grid-filter,
      5-TC), replacing the stale 2026-07-26 label-driven/4-TC description.
- [x] **21.** Reuse clause - N/A in the original sense (screen already had a bundle); this
      backfill itself IS the reuse-clause deliverable - JOURNAL + evidence + KB map all
      refreshed, not just green tests re-cited.

_Gates 10-16 in this row were re-run live on 2026-08-28 specifically for this backfill; the
automation files themselves were not modified - see JOURNAL.md "2026-08-28" entry._
