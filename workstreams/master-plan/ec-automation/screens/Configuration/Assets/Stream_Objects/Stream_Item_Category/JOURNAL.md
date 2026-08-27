# JOURNAL - Stream Item Category (CD.0016) OV IUD

## 2026-07-26 (original build)
- **Branch:** `feature/stream_item_category-iud` (own branch, stacked so the shared-engine helpers are present).
  Check-existing gate: only this build; reused shared engine + T2 + DbVerify.
- **Recon** (`investigation/recon.py`, read-only): DB `CLASS_TYPE=OBJECT` -> OV; treeview
  Configuration > Assets > Stream_Objects > Stream Item Category. Mandatory Code/Name/Start Date; optional dropdowns skipped.
  Plain Bank-layout OV (single Date+GO nav, no mandatory dropdowns).
- **Label-driven** T3 (no hardcoded ids). Playwright driver -> 7/7; RF T3+suite -> live 4/4.
- `verify_screen.py` -> **OVERALL PASS**: robocop 0, hygiene 0, dryrun 4/4, LIVE RF 4/4, Playwright 7/7.

## 2026-08-23 - PR #473: full Bank-pattern structural conversion (Batch 10)
- **Built:** rebuilt the existing (already label-driven) page object + test suite to add
  properties-file-driven insert/update/verify and explicit grid-filter wiring, replacing the
  older 4-TC no-filter/no-properties pattern with the same full shape as `bank_page.resource`/
  `berth_page.resource`. GENERIC "Code"/"Name" labels (NOT screen-prefixed), mandatory fields
  Code/Name/Start Date only - confirmed against the already-proven Playwright driver
  `py/stream_item_category_iud.py`.
- **Files touched:** `pageobjects/.../stream_item_category_page.resource` (rebuilt: added
  properties-file-driven Insert/Update/Verify wrappers, explicit `Find/Clear Stream Item
  Category Row By Filter` wired into Update/Find/Verify-Found/Delete), `tests/.../
  stream_item_category_iud.robot` (rebuilt from 4-TC to 5-TC: clean-state/insert/update/find/
  delete, per-TC login/logout, fixed test code `AUTOTEST_SIC`), `resources/credentials.py`
  (additive `STREAM_ITEM_CATEGORY_EC_USER`/`STREAM_ITEM_CATEGORY_EC_PASS`), 4 new
  `testdata/stream_item_category_{insert,update,form_verify,grid_verify}.properties`,
  `docs/ec_screen_registry.md` + `docs/automation-scorecard.md` (MODIFIED the existing rows
  from the 2026-07-26 generator-scaffolded build, not new rows), `docs/bank-pattern-conversion-
  checklist.md` + `docs/grid-filter-standardization-checklist.md` (appended this screen's row
  under the pre-merged "Batch 10 additions" header). No changes to `resources/manage_object
  .resource` or `resources/common.resource`.
- **Verified at PR time:** live run (EC_HEADLESS=true) 5/5 TC pass; `robot --dryrun` on the
  full `tests/` tree 767/767 pass; `robocop check` on changed files - 0 new issues beyond the
  same baseline DOC02/VAR02 noise `bank_iud.robot`/`bank_insert.properties` already carry, one
  real LEN32 hit (2 variable names 43/40 chars) fixed by shortening `*_PROPERTIES` -> `*_PROPS`;
  grid-filter keyword confirmed fired via `output.xml` grep (`Find Object Row By Filter`/`Find
  Stream Item Category Row By Filter` = 24 hits, `Clear Object Row Filter`/`Clear Stream Item
  Category Row Filter` = 20 hits); DB self-clean via a fresh `oracledb` connection -
  `SELECT CODE, NAME FROM OV_STREAM_ITEM_CATEGORY WHERE CODE LIKE 'AUTOTEST%'` -> 0 rows both
  before and after the run.

## 2026-08-25 - alignment fix (registry note, no separate PR body captured for this repo)
- Removed direct `Code Should Be Present In View`/`Field Should Equal In View`/`Code Should Be
  Absent In View` calls from TC02/TC03/TC05 in the `.robot` suite - these violated Bank's
  pure-screen-only verification convention (2026-08-18), the same deviation class as DOA Credit
  Limit (PR #503). Re-verified live 5/5, full-tree dryrun 841/841, DB self-clean 0 residual.
  (Per `docs/ec_screen_registry.md`'s Stream Item Category row.)

## 2026-08-28 - backfill (this task, `docs/lean-deliverable-backfill-workorder.md` Batch 11)
- **Built:** refreshed this screen-local bundle (SOW/README/JOURNAL/evidence/CHECKLIST/KB map),
  which had NOT been touched since the 2026-07-26 generator-scaffolded build and still described
  the pre-PR#473 4-TC/no-filter/Playwright-7-7 shape. The registry and scorecard rows WERE kept
  current at PR #473's merge; this screen-local bundle was the gap. Does not rebuild, modify, or
  re-verify the RF automation itself beyond a fresh dryrun + one live confirmation run, per the
  backfill task's scope.
- **Re-run evidence (2026-08-28):** `robot --dryrun` on this suite - 5/5 pass
  (`evidence/dryrun_output.xml`). Live headless run (`EC_HEADLESS=true robot`) - **5/5 pass on
  first attempt** (`evidence/live_output.xml`/`live_report.html`/`live_log.html`), no retry
  needed. Grid-filter keyword confirmed fired via `output.xml` grep this run: `Find Stream Item
  Category Row By Filter` = 9 hits, `Clear Stream Item Category Row Filter` = 5 hits. `robocop
  check` on the page object + suite - 9 issues, all DOC02 (missing `[Documentation]` on TC02-05
  plus a shared-file DOC02, same baseline-noise class Bank/Storage already carry - no new issue
  class). `py scripts/check_bundle_hygiene.py` -> `RESULT: PASS` (the 2 WARN lines it reports
  belong to an unrelated screen, Contract_Area, not this one).
- **DB self-clean (fresh `oracledb` connection, 2026-08-28):** `SELECT CODE, NAME FROM
  OV_STREAM_ITEM_CATEGORY WHERE CODE LIKE 'AUTOTEST%'` -> empty result set (0 residual), matching
  the same query cited in PR #473's own body.

## Done well
- Full I-U-D DB-verified vs `OV_STREAM_ITEM_CATEGORY` (insert Name, update Name, delete
  End=Start -> absent); fresh-connection self-clean 0 residual `AUTOTEST%` rows, both at PR
  #473's time and at this backfill's re-run.
- Live RF 5/5 pass, both at PR #473's merge and at this backfill's confirmation run (no flake, no
  retry needed - unlike some sibling screens in this batch plan).
- Registry/scorecard MODIFY-not-add convention correctly followed at PR #473 (this screen already
  had a row from the 2026-07-26 build; both rows were replaced cleanly, not left stale alongside
  a new one).

## Done wrong / lessons
- The screen-local bundle under `screens/Configuration/Assets/Stream_Objects/Stream_Item_Category/`
  was NOT refreshed at PR #473's merge (2026-08-23) or at the 2026-08-25 alignment fix - it still
  described the pre-conversion 4-TC/no-filter/Playwright-7-7 shape until this backfill
  (2026-08-28). This is exactly the gap `docs/lean-deliverable-backfill-workorder.md` exists to
  close.
- Disambiguation risk confirmed real, not hypothetical: this screen ("Stream Item Category",
  CD.0016, class `OBJECT`, view `OV_STREAM_ITEM_CATEGORY`) is a DIFFERENT screen from "Stream
  Item Category Split Key" (CD.0042, class `SPLIT_KEY`, shared view `OV_SPLIT_KEY`) - the
  registry itself calls out this exact confusion risk in both screens' rows. This backfill only
  touched this plain screen's files, confirmed via `grep -ril "stream_item_category_page
  .resource"` (excluding any `split_key` hit) before starting.

## Blockers -> resolution
- No blockers. Dryrun and live run both passed first attempt, no retry needed.

## Decisions
- Playwright driver `py/stream_item_category_iud.py` stays untouched and un-rebuilt - permanently
  waived per the 2026-08-27 owner decision (Universal Screen Engine replaces that role going
  forward).
- This backfill only adds documentation/evidence artifacts; it does not re-run the original build
  or modify `stream_item_category_page.resource`, `stream_item_category_iud.robot`, or any
  `testdata/stream_item_category_*.properties` file.

## Evidence
- Dryrun (2026-08-28, this backfill): `evidence/dryrun_output.xml` - 5/5 pass.
- Live headless run (2026-08-28, this backfill): `evidence/live_output.xml` +
  `evidence/live_report.html` + `evidence/live_log.html` - 5/5 pass, first attempt, no retry.
- DB self-clean (fresh `oracledb` connection, 2026-08-28): `SELECT CODE, NAME FROM
  OV_STREAM_ITEM_CATEGORY WHERE CODE LIKE 'AUTOTEST%'` -> empty result set (0 residual).
- Pre-existing (2026-07-26 build, kept as historical evidence, not removed):
  `investigation/recon.py`, `evidence/stream_item_category_0[1-5]_*.png`, `evidence/rf_report.html`.
